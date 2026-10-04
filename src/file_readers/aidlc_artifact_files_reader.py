from pathlib import Path


SUPPORTED_ARTIFACT_EXTENSIONS = (
    ".md",
    ".csv",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".png",
    ".jpg",
    ".jpeg",
)


def list_aidlc_artifact_files(
    artifacts_data_directory: str | Path,
    supported_extensions: tuple[str, ...] = SUPPORTED_ARTIFACT_EXTENSIONS,
    recursive: bool = True,
) -> list[Path]:
    """Artifacts画面で扱う対象拡張子の成果物ファイルを一覧する。"""
    base_directory = Path(artifacts_data_directory)

    if not base_directory.is_dir():
        raise FileNotFoundError(f"成果物用データディレクトリが見つかりません: {base_directory}")

    # 拡張子の大文字小文字差分を吸収して、対応ファイルだけを抽出する。
    normalized_extensions = {extension.lower() for extension in supported_extensions}
    glob_pattern = "**/*" if recursive else "*"

    return sorted(
        path
        for path in base_directory.glob(glob_pattern)
        if path.is_file() and path.suffix.lower() in normalized_extensions
    )


def read_aidlc_artifact_text(artifact_file_path: str | Path) -> str:
    """テキスト系の成果物ファイルをUTF-8テキストとして読み込む。"""
    path = Path(artifact_file_path)

    if not path.is_file():
        raise FileNotFoundError(f"AIDLC成果物ファイル（Markdownもしくはテキストファイル）が見つかりません: {path}")

    return path.read_text(encoding="utf-8")


def read_aidlc_artifact_bytes(artifact_file_path: str | Path) -> bytes:
    """画像などの成果物ファイルをバイト列として読み込む。"""
    path = Path(artifact_file_path)

    if not path.is_file():
        raise FileNotFoundError(f"AIDLC成果物ファイル（画像ファイル）が見つかりません: {path}")

    return path.read_bytes()
