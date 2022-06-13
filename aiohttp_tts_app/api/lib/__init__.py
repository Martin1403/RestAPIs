import json
import typing
from concurrent.futures import Executor, Future
from pathlib import Path
import gruut
import numpy as np
import onnxruntime
import phonemes2ids
from aiohttp_tts_app.api.lib.glow_tts import GlowTextToSpeech

from aiohttp_tts_app.api.lib.audio import AudioSettings
from aiohttp_tts_app.api.lib.constants import (
    InferenceBackend,
    TextToSpeechModel,
    TextToSpeechModelConfig,
    TextToSpeechResult,
    TextToSpeechType,
    VocoderModel,
    VocoderModelConfig,
    VocoderQuality,
    VocoderType,
)
from aiohttp_tts_app.api.lib.utils import (
    VOCODER_QUALITY,
    get_voices_dirs,
    resolve_voice_name,
    split_voice_name,
    valid_voice_dir,
)


_DIR = Path(__file__).parent

__version__ = (_DIR / "VERSION").read_text().strip()

_DEFAULT_AUDIO_SETTINGS = AudioSettings()


class TTS:
    def __init__(self, voice_or_lang="en-us", vocoder_or_quality=VocoderQuality.HIGH, backend=None, tts_settings=None,
                 vocoder_settings=None, executor=None, denoiser_strength=0.0, custom_voices_dir=None):
        self.voice_or_lang = voice_or_lang
        self.resolved_name = resolve_voice_name(self.voice_or_lang)
        self.vocoder_or_quality = vocoder_or_quality
        self.backend = backend
        self.tts_settings = tts_settings
        self.vocoder_settings = vocoder_settings
        self.executor = executor
        self.denoiser_strength = denoiser_strength
        self.custom_voices_dir = custom_voices_dir
        self.ssml = False,
        self.use_cuda = False,
        self.half = False

        self.tts_model = get_tts_model(self.resolved_name, backend=self.backend, use_cuda=False,
                                       half=False, custom_voices_dir=self.custom_voices_dir)

        self.vocoder_model = get_vocoder_model(self.vocoder_or_quality, backend=self.backend,
                                               use_cuda=False, half=False, denoiser_strength=self.denoiser_strength,
                                               custom_voices_dir=self.custom_voices_dir,)

    def text_to_speech(self, text: str) -> typing.Iterable[TextToSpeechResult]:

        voice_lang, _voice_name, _voice_model_type = split_voice_name(self.resolved_name)
        voice_lang = gruut.resolve_lang(voice_lang)
        futures: typing.Dict[Future, TextToSpeechResult] = {}

        for c, sentence in enumerate(gruut.sentences(text, lang=voice_lang, ssml=False, explicit_lang=False), 1):

            phoneme_to_id = getattr(self.tts_model, "phoneme_to_id", {})
            audio_settings = getattr(self.tts_model, "audio_settings", None)

            if audio_settings is None:
                audio_settings = _DEFAULT_AUDIO_SETTINGS

            sent_phonemes = [w.phonemes for w in sentence if w.phonemes]
            sent_phoneme_ids = phonemes2ids.phonemes2ids(
                sent_phonemes,
                phoneme_to_id,
                pad="_",
                blank="#",
                separate={"ˈ", "ˌ", "²"},
                simple_punctuation=True,
            )

            # Add pauses from SSML <break> tags
            pause_before_ms = sentence.pause_before_ms
            if sentence.words:
                # Add pause from first word
                pause_before_ms += sentence.words[0].pause_before_ms

            pause_after_ms = sentence.pause_after_ms
            if sentence.words:
                # Add pause from last word
                pause_after_ms += sentence.words[-1].pause_after_ms

            # Convert phonemes to audio
            future = self.executor.submit(
                _sentence_task,
                sentence.text,
                np.array(sent_phoneme_ids, dtype=np.int64),
                audio_settings,
                self.tts_model,
                self.tts_settings,
                self.vocoder_model,
                self.vocoder_settings,
                pause_before_ms=pause_before_ms,
                pause_after_ms=pause_after_ms,
            )

            marks_before = []
            if sentence.marks_before:
                marks_before.extend(sentence.marks_before)

            marks_after = []
            if sentence.marks_after:
                marks_after.extend(sentence.marks_after)

            for word_idx, word in enumerate(sentence):
                if word.marks_before:
                    if word_idx == 0:
                        marks_before.extend(word.marks_before)
                    else:
                        marks_after.extend(word.marks_before)

                if word.marks_after:
                    marks_after.extend(word.marks_after)

            futures[future] = TextToSpeechResult(
                text=sentence.text_with_ws,
                audio=None,
                sample_rate=audio_settings.sample_rate,
                marks_before=marks_before,
                marks_after=marks_after,
            )

        for future, result in futures.items():
            result.audio = future.result()

            yield result


_PHONEME_TO_ID: typing.Dict[str, typing.Dict[str, int]] = {}

_LANG_STRESS = {
    "en": True,
    "en-us": True,
    "fr": True,
    "fr-fr": True,
    "es": True,
    "es-es": True,
    "it": True,
    "it-it": True,
    "nl": True,
    "sw": True,
}


def _sentence_task(
    text: str,
    phoneme_ids,
    audio_settings,
    tts_model,
    tts_settings,
    vocoder_model,
    vocoder_settings,
    pause_before_ms: int = 0,
    pause_after_ms: int = 0,
):

    mels = tts_model.phonemes_to_mels(phoneme_ids, settings=tts_settings)

    if audio_settings.signal_norm:
        mels = audio_settings.denormalize(mels)

    if audio_settings.convert_db_to_amp:
        mels = audio_settings.db_to_amp(mels)

    if audio_settings.do_dynamic_range_compression:
        mels = audio_settings.dynamic_range_compression(mels)

    audio = vocoder_model.mels_to_audio(mels, settings=vocoder_settings)

    before_samples = max(0, (pause_before_ms * audio_settings.sample_rate) // 1000)
    after_samples = max(0, (pause_after_ms * audio_settings.sample_rate) // 1000)
    if (before_samples > 0) or (after_samples > 0):
        audio = np.pad(
            audio, pad_width=(before_samples, after_samples), constant_values=0
        )

    return audio


_TTS_MODEL_CACHE: typing.Dict[str, TextToSpeechModel] = {}


def get_tts_model(
    name: str = "",
    lang: str = "en-us",
    backend: typing.Optional[InferenceBackend] = None,
    use_cuda: bool = False,
    half: bool = True,
    custom_voices_dir: typing.Optional[typing.Union[str, Path]] = None,
) -> typing.Optional[TextToSpeechModel]:
    resolved_name = resolve_voice_name(name or gruut.resolve_lang(lang))

    model_dir: typing.Optional[Path] = None

    voice_lang, voice_name, voice_model_type = split_voice_name(resolved_name)
    voice_dir_name = f"{voice_name}-{voice_model_type}"

    voices_dirs = get_voices_dirs(custom_voices_dir)

    for voices_dir in voices_dirs:
        maybe_model_dir = voices_dir / voice_lang / voice_dir_name
        if valid_voice_dir(maybe_model_dir):
            model_dir = maybe_model_dir
            break

    with open(model_dir / "phonemes.txt", "r", encoding="utf-8") as phonemes_file:
        phoneme_to_id = phonemes2ids.load_phoneme_ids(phonemes_file)

    config_path = model_dir / "config.json"
    with open(config_path, "r", encoding="utf-8") as config_file:
        config = json.load(config_file)
        audio_settings = AudioSettings(**config["audio"])

    model = load_tts_model(
        voice_model_type, model_dir, backend=backend, use_cuda=use_cuda, half=half
    )
    setattr(model, "phoneme_to_id", phoneme_to_id)
    setattr(model, "audio_settings", audio_settings)
    return model


def load_tts_model(
    model_type: typing.Union[str, TextToSpeechType],
    model_path: typing.Union[str, Path],
    backend: typing.Optional[InferenceBackend] = None,
    no_optimizations: bool = False,
    use_cuda: bool = False,
    half: bool = False,
) -> TextToSpeechModel:

    sess_options = onnxruntime.SessionOptions()
    if no_optimizations:
        sess_options.graph_optimization_level = (
            onnxruntime.GraphOptimizationLevel.ORT_DISABLE_ALL
        )

    config = TextToSpeechModelConfig(
        model_path=Path(model_path),
        session_options=sess_options,
        use_cuda=use_cuda,
        half=half,
        backend=backend,
    )

    if model_type == TextToSpeechType.GLOW_TTS:

        return GlowTextToSpeech(config)


_VOCODER_MODEL_CACHE: typing.Dict[str, VocoderModel] = {}


def get_vocoder_model(
    name_or_quality: typing.Union[str, VocoderQuality] = VocoderQuality.HIGH,
    backend: typing.Optional[InferenceBackend] = None,
    use_cuda: bool = False,
    half: bool = False,
    denoiser_strength: float = 0.0,
    custom_voices_dir: typing.Optional[typing.Union[str, Path]] = None,
) -> typing.Optional[VocoderModel]:
    # Try to load model from cache first
    maybe_model = _VOCODER_MODEL_CACHE.get(name_or_quality)

    if maybe_model is None:
        model_dir: typing.Optional[Path] = None
        model_type, model_name = VOCODER_QUALITY.get(
            name_or_quality, name_or_quality
        ).split("/", maxsplit=1)

        voices_dirs = get_voices_dirs(custom_voices_dir)

        for voices_dir in voices_dirs:
            maybe_model_dir = voices_dir / model_type / model_name

            if valid_voice_dir(maybe_model_dir):
                model_dir = maybe_model_dir
                break

        model = load_vocoder_model(
            VocoderType.HIFI_GAN,
            model_dir,
            backend=backend,
            use_cuda=use_cuda,
            half=half,
            denoiser_strength=denoiser_strength,
        )

        _VOCODER_MODEL_CACHE[name_or_quality] = model

        return model

    return maybe_model


def load_vocoder_model(
    model_type: typing.Union[str, VocoderType],
    model_path: typing.Union[str, Path],
    backend: typing.Optional[InferenceBackend] = None,
    no_optimizations: bool = False,
    use_cuda: bool = False,
    half: bool = False,
    denoiser_strength: float = 0.0,
    executor: typing.Optional[Executor] = None,
) -> VocoderModel:

    """Load the appropriate vocoder model"""
    sess_options = onnxruntime.SessionOptions()
    if no_optimizations:
        sess_options.graph_optimization_level = (
            onnxruntime.GraphOptimizationLevel.ORT_DISABLE_ALL
        )

    config = VocoderModelConfig(
        model_path=Path(model_path),
        session_options=sess_options,
        use_cuda=use_cuda,
        half=half,
        denoiser_strength=denoiser_strength,
        backend=backend,
    )

    if model_type == VocoderType.GRIFFIN_LIM:
        from aiohttp_tts_app.api.lib.griffin_lim import GriffinLimVocoder

        return GriffinLimVocoder(config)

    if model_type == VocoderType.HIFI_GAN:
        from aiohttp_tts_app.api.lib.hifi_gan import HiFiGanVocoder

        return HiFiGanVocoder(config, executor=executor)
