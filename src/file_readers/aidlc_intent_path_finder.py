from pathlib import Path


def build_aidlc_intent_directory(
    aidlc_root_directory: str | Path,
    space_name: str,
    intent_name: str,
) -> Path:
    """aidlc/spaces/<space>/intents/<intent> のパスを組み立てる。"""
    return (
        Path(aidlc_root_directory)
        / "spaces"
        / space_name
        / "intents"
        / intent_name
    )


def find_aidlc_intent_directory(
    aidlc_root_directory: str | Path,
    space_name: str = "default",
    intent_name: str | None = None,
) -> Path:
    """対象となるAIDLC intentディレクトリを探す。"""
    intents_directory = Path(aidlc_root_directory) / "spaces" / space_name / "intents"

    # intent名が指定されている場合は、そのディレクトリだけを確認する。
    if not intents_directory.is_dir():
        raise FileNotFoundError(f"AIDLC intentsディレクトリが見つかりません: {intents_directory}")

    if intent_name:
        intent_directory = intents_directory / intent_name
        if not intent_directory.is_dir():
            raise FileNotFoundError(f"AIDLC intentディレクトリが見つかりません: {intent_directory}")
        return intent_directory

    intent_directories = sorted(path for path in intents_directory.iterdir() if path.is_dir())

    if not intent_directories:
        raise FileNotFoundError(f"AIDLC intentディレクトリが1件も見つかりません: {intents_directory}")

    # intent名が未指定で複数存在する場合、どれを読むべきか判断できないためエラーにする。
    if len(intent_directories) > 1:
        names = ", ".join(path.name for path in intent_directories)
        raise ValueError(
            "AIDLC intentディレクトリが複数見つかりました。"
            f"intent_nameを明示してください。見つかったintent: {names}"
        )

    return intent_directories[0]
