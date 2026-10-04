from pathlib import Path


def get_aidlc_state_file_path(
    dashboard_data_directory: str | Path,
    state_file_name: str = "aidlc-state.md",
) -> Path:
    """Dashboard用データディレクトリ配下のaidlc-state.mdパスを返す。"""
    return Path(dashboard_data_directory) / state_file_name


def read_aidlc_state_file(
    dashboard_data_directory: str | Path,
    state_file_name: str = "aidlc-state.md",
) -> str:
    """aidlc-state.mdをUTF-8テキストとして読み込む。"""
    state_file_path = get_aidlc_state_file_path(dashboard_data_directory, state_file_name)

    # ここでは中身を解釈せず、存在確認と読み込みだけを担当する。
    if not state_file_path.is_file():
        raise FileNotFoundError(f"AIDLC状態ファイルが見つかりません: {state_file_path}")

    return state_file_path.read_text(encoding="utf-8")
