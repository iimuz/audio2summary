"""書き起こした文字をテキストで保存するモジュール."""

import os
from pathlib import Path

from internal.speaker_text import SpeakerText


class SpeechTextWriter:
    """書き起こした文字をテキストで保存する."""

    def __init__(self: "SpeechTextWriter", filepath: Path) -> None:
        """初期化処理.

        Parameters
        ----------
        filepath : Path
            保存先のファイルパス

        """
        self._filepath = filepath

    def save(self: "SpeechTextWriter", speaker_text: list[SpeakerText]) -> None:
        """書き起こした文字を保存する.

        Parameters
        ----------
        speaker_text : list[SpeakerText]
            書き起こした文字情報

        """
        if len(speaker_text) < 1:
            self._filepath.write_text("")
            return

        # segmentごとの文字列を生成
        segments = [
            os.linesep.join(
                [
                    f"[{t.start_time:03.1f} --> {t.end_time:03.1f}] {t.speaker_name}",
                    t.text,
                ]
            )
            for t in speaker_text
        ]

        self._filepath.write_text(f"{(os.linesep)*2}".join(segments))

    def clean(self: "SpeechTextWriter") -> None:
        """保存されている書き起こし情報を削除する."""
        if not self._filepath.exists():
            return

        self._filepath.unlink()
