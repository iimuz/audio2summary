"""話者ごとのテキストをファイル保存するモジュール."""

from pathlib import Path

from internal.speaker_text import SpeakerText
from pydantic import RootModel


class SpeechTextFile:
    """話者ごとのテキストをファイル保存する."""

    class SpeechTextList(RootModel[list[SpeakerText]]):
        """話者ごとのテキストのリスト."""

    def __init__(self: "SpeechTextFile", filepath: Path) -> None:
        """初期化処理.

        Parameters
        ----------
        filepath : Path
            保存先のファイルパス

        """
        self._filepath = filepath

    def save(self: "SpeechTextFile", segments: list[SpeakerText]) -> None:
        """話者ごとのテキストを保存する."""
        segment_list = self.SpeechTextList.model_validate(segments)
        self._filepath.write_text(segment_list.model_dump_json())

    def get_segment_list(self: "SpeechTextFile") -> list[SpeakerText]:
        """話者ごとのテキストを取得する."""
        if not self._filepath.exists():
            return []

        segment_list = self.SpeechTextList.model_validate_json(
            self._filepath.read_text()
        )
        return segment_list.root

    def clean(self: "SpeechTextFile") -> None:
        """保存されている話者ごとのテキストを削除する."""
        if not self._filepath.exists():
            return

        self._filepath.unlink()
