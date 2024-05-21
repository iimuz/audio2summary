"""話者分離情報をファイルに保存するモジュール."""

from pathlib import Path

from internal.speaker_segment import SpeakerSegment
from pydantic import RootModel


class SpeakerSegmentFile:
    """話者分離情報をファイルに保存する."""

    class SpeakerSegmentList(RootModel[list[SpeakerSegment]]):
        """話者分離情報のリスト."""

    def __init__(self: "SpeakerSegmentFile", filepath: Path) -> None:
        """初期化処理.

        Parameters
        ----------
        filepath : Path
            保存先のファイルパス

        """
        self._filepath = filepath

    def save(self: "SpeakerSegmentFile", segments: list[SpeakerSegment]) -> None:
        """話者分離情報を保存する."""
        segment_list = self.SpeakerSegmentList.model_validate(segments)
        self._filepath.write_text(segment_list.model_dump_json())

    def get_segment_list(self: "SpeakerSegmentFile") -> list[SpeakerSegment]:
        """話者分離情報を取得する."""
        if not self._filepath.exists():
            return []

        segment_list = self.SpeakerSegmentList.model_validate_json(
            self._filepath.read_text()
        )
        return segment_list.root

    def clean(self: "SpeakerSegmentFile") -> None:
        """保存されている話者分離情報を削除する."""
        if not self._filepath.exists():
            return

        self._filepath.unlink()
