import typing
import numpy as np

import torch

from quart_tts_app.api.lib.glow_tts_lib.checkpoint import load_checkpoint
from quart_tts_app.api.lib.glow_tts_lib.config import TrainingConfig

from quart_tts_app.api.lib.constants import (
    ARRAY_OR_TENSOR,
    InferenceBackend,
    SettingsType,
    TextToSpeechModel,
    TextToSpeechModelConfig,
)


class GlowTextToSpeech(TextToSpeechModel):
    def __init__(self, config: TextToSpeechModelConfig):
        super().__init__(config)
        self.pytorch_model: typing.Optional[typing.Any] = None
        self.use_cuda = config.use_cuda
        pytorch_path = config.model_path / "generator.pth"
        generator_path = pytorch_path
        backend = InferenceBackend.PYTORCH
        config_path = generator_path.parent / "config.json"

        with open(config_path, "r", encoding="utf-8") as config_file:
            self.config = TrainingConfig.load(config_file)

        checkpoint = load_checkpoint(
            pytorch_path, self.config, use_cuda=config.use_cuda
        )

        assert checkpoint.model is not None

        self.pytorch_model = checkpoint.model

        if config.half:
            self.pytorch_model.half()

        self.pytorch_model.decoder.store_inverse()
        self.pytorch_model.eval()

        self.noise_scale = 0.667
        self.length_scale = 1.0

    def phonemes_to_mels(
        self, phoneme_ids: np.ndarray, settings: typing.Optional[SettingsType] = None
    ) -> ARRAY_OR_TENSOR:
        """Convert phoneme ids to mel spectrograms"""
        # Convert to tensors
        noise_scale = self.noise_scale
        length_scale = self.length_scale
        speaker_idx: typing.Optional[int] = None

        if settings:
            noise_scale = float(settings.get("noise_scale", noise_scale))
            length_scale = float(settings.get("length_scale", length_scale))
            speaker_idx = settings.get("speaker_id")

        if self.pytorch_model is not None:
            # Inference with PyTorch
            speaker_id: typing.Optional[torch.Tensor] = None

            if speaker_idx is not None:
                speaker_id = torch.LongTensor([speaker_idx])
                if self.use_cuda:
                    speaker_id = speaker_id.cuda()

            text_tensor = torch.autograd.Variable(
                torch.LongTensor(phoneme_ids).unsqueeze(0)
            )
            text_lengths_tensor: torch.Tensor = torch.LongTensor([text_tensor.shape[1]])

            if self.use_cuda:
                text_tensor = text_tensor.cuda()
                text_lengths_tensor = text_lengths_tensor.cuda()

            # Infer mel spectrograms
            with torch.no_grad():
                (mel, *_), _, _ = self.pytorch_model(
                    text_tensor,
                    text_lengths_tensor,
                    noise_scale=noise_scale,
                    length_scale=length_scale,
                    g=speaker_id,
                )
            return mel.cpu()
