"""音声データをテキスト化するモジュール."""

import logging
import os
import re
import subprocess
from pathlib import Path

from internal.speaker_segment import SpeakerSegment
from internal.speaker_text import SpeakerText
from pydub import AudioSegment

_logger = logging.getLogger(__name__)


class SpeechToText:
    """音声データをテキスト化する."""

    def __init__(
        self: "SpeechToText", wav_dirpath: Path, whisper_cpp_path: Path, model_name: str
    ) -> None:
        """初期化処理.

        Parameters
        ----------
        wav_dirpath : Path
            wavファイルのディレクトリパス

        whisper_cpp_path : Path
            whisper.cppのパス

        model_name : string
            モデル名

        """
        self._wav_dirpath = wav_dirpath
        self._whisper_cpp_path = whisper_cpp_path.resolve()

        self._re_query = re.compile(
            r"(\[\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}])\s+(.+)"
        )
        self._whisper_cpp_venv = self._whisper_cpp_path / ".venv/bin"
        self._whisper_command = [
            str(whisper_cpp_path / "main"),
            "-m",
            str(whisper_cpp_path / f"models/ggml-{model_name}.bin"),
            "-l",
            "ja",
        ]

    def to_text(
        self: "SpeechToText", sound: AudioSegment, segments: list[SpeakerSegment]
    ) -> list[SpeakerText]:
        """指定したwavファイルをテキスト化する."""
        speaker_text_list: list[SpeakerText] = []
        for segment in segments:
            start_time = int(segment.start_time * 1000)  # s -> ms
            end_time = int(segment.end_time * 1000)  # s -> ms
            sound_segment = sound[start_time:end_time]
            if type(sound_segment) is not AudioSegment:
                st = segment.start_time
                et = segment.end_time
                message = (
                    f"sound segment is not AudioSegment. [{st:03.1f}s - {et:03.1f}s]"
                )
                raise ValueError(message)
            try:
                text = self._sound_segment_to_text(sound_segment)
            except Exception:
                _logger.exception(
                    (
                        "Unhandled exception in speech to text. continue... "
                        "[%03.1f s - %03.1f s] %s"
                    ),
                    segment.start_time,
                    segment.end_time,
                    segment.speaker_name,
                )
                continue
            speaker_text = SpeakerText(
                start_time=segment.start_time,
                end_time=segment.end_time,
                speaker_name=segment.speaker_name,
                text=text,
            )
            speaker_text_list.append(speaker_text)
            _logger.debug(
                "[%03.1f s - %03.1f s] %s : %s",
                segment.start_time,
                segment.end_time,
                segment.speaker_name,
                text,
            )

        return speaker_text_list

    def _sound_segment_to_text(self: "SpeechToText", sound: AudioSegment) -> str:
        """1つ分のオーディオデータをテキスト化する."""
        wav_filepath = self._wav_dirpath / "cut_export.wav"
        sound.export(wav_filepath, format="wav")

        old_path = os.environ["PATH"]
        os.environ["PATH"] = (
            f"{self._whisper_cpp_path}/.venv/bin:{os.environ.get('PATH')}"
        )
        command_args = [
            *self._whisper_command,
            "-f",
            str(wav_filepath),
        ]
        proc = subprocess.Popen(
            command_args,  # noqa: S603
            encoding="utf-8",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            result, error = proc.communicate(timeout=1800)
        except Exception:
            proc.kill()
            raise
        if proc.returncode != 0:
            _logger.error("command failed with exit status %d", proc.returncode)
            _logger.error(error)

            message = "speech to text error."
            raise ValueError(message)
        os.environ["PATH"] = old_path
        wav_filepath.unlink()

        result_lines = result.splitlines()
        match_list: list[str] = []
        num_split = 2  # regexで分割した場合に2個に分割されることを期待している
        for line in result_lines:
            line_str = self._re_query.search(line)
            if line_str is None:
                continue
            if len(line_str.groups()) != num_split:
                _logger.warning("skip match string: num=%d", len(line_str.groups()))
                continue
            match_list.append(line_str.group(2))

        return " ".join(match_list)
