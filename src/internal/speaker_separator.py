"""音声から話者分離を行うクラスを提供するモジュール."""

from collections.abc import Generator
from pathlib import Path

import torch
from internal.speaker_segment import SpeakerSegment
from pyannote.audio import Pipeline


class SpeakerSeparator:
    """音声から話者分離を行う."""

    def __init__(self: "SpeakerSeparator", config_path: Path, device_name: str) -> None:
        """初期化処理.

        Parameters
        ----------
        config_path : Path
            モデル設定ファイルのパス

        device_name : str
            デバイス名

        """
        self._config_path = config_path
        self._device_name = device_name

    def diarization(
        self: "SpeakerSeparator", wav_filepath: Path
    ) -> Generator[SpeakerSegment, None, None]:
        """音声から話者分離を行う.

        Parameters
        ----------
        wav_filepath : Path
            音声ファイルのパス

        """
        pipeline = Pipeline.from_pretrained(self._config_path)
        pipeline.to(torch.device(self._device_name))
        diarization = pipeline(wav_filepath)

        for segment, _, speaker in diarization.itertracks(yield_label=True):
            speaker_segment = SpeakerSegment(
                start_time=segment.start, end_time=segment.end, speaker_name=speaker
            )
            yield speaker_segment
