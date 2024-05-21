"""指定したファイルをmp4に変換するモジュール."""

import logging
import subprocess
from pathlib import Path

_logger = logging.getLogger(__name__)


class ConvertToMp4File:
    """指定したファイルをmp4に変換する."""

    def __init__(self: "ConvertToMp4File", output_dir: Path) -> None:
        """初期化処理.

        Parameters
        ----------
        output_dir : Path
            変換後のファイルを保存するディレクトリ.

        """
        self._output_dir = output_dir

    def convert(self: "ConvertToMp4File", filepath: Path) -> Path:
        """指定したファイルをmp4に変換する.

        Parameters
        ----------
        filepath : Path
            変換対象のファイルパス.

        """
        if not filepath.is_file():
            message = f"file not found: {filepath!s}"
            raise FileNotFoundError(message)
        if any(char in str(filepath) for char in ["'", '"', "&", "|", ";"]):
            message = f"invalid character in filepath: {filepath!s}"
            raise ValueError(message)

        output_filepath = self._output_dir / f"{filepath.stem}.mp4"
        command_args = [
            "ffmpeg",
            "-y",  # 既存ファイルが存在する場合などで入力が必要となる部分を全てYesとする
            "-i",
            f"{filepath.resolve()!s}",
            str(output_filepath.resolve()),
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

            message = "error converting to mp4 file."
            raise ValueError(message)

        _logger.info("stdout: %s", result)
        _logger.warning("stderr: %s", result)

        return output_filepath
