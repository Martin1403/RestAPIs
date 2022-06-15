import base64
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Optional, Dict, Any
import io

from quart_tts_app.api.lib import TTS
from quart_tts_app.api.lib import InferenceBackend
from quart_tts_app.api.lib.wavfile import write

max_thread_workers: Optional[int] = None
tts_settings: Dict[str, Any] = {"noise_scale": 0.667, "length_scale": 1.0}
vocoder_settings: Dict[str, Any] = {"denoiser_strength": 0.005}

backend = InferenceBackend("pytorch")
executor = ThreadPoolExecutor(max_workers=max_thread_workers)
tts = TTS(voice_or_lang="kathleen-glow_tts",
          vocoder_or_quality="low",  # "high", "medium", "low"
          backend="pytorch",
          tts_settings=tts_settings,
          vocoder_settings=vocoder_settings,
          executor=executor,
          denoiser_strength=vocoder_settings["denoiser_strength"],
          custom_voices_dir="quart_tts_app/voices",
          )


def action_endpoint(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        result = await f(*args, **kwargs)
        text = result.data
        tts_results = tts.text_to_speech(text=text)
        for result_idx, result in enumerate(tts_results):
            with io.BytesIO() as wav_io:
                write(wav_io, result.sample_rate, result.audio)
                wav_data = wav_io.getvalue()
                data = base64.encodebytes(wav_data).decode('ascii')
        return {"data": data, "rate": result.sample_rate}
    return decorated_function
