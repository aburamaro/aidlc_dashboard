from pathlib import Path


def read_aidlc_version_file(aidlc_release_version_file: str | Path) -> str:
    """AIDLCリリースバージョン定義ファイルをUTF-8テキストとして読み込む。"""
    path = Path(aidlc_release_version_file)

    # バージョン文字列の抽出はextractor側で行い、ここではファイル読み込みだけを担当する。
    if not path.is_file():
        raise FileNotFoundError(f"AIDLCリリースバージョン定義ファイルが見つかりません: {path}")

    return path.read_text(encoding="utf-8")
