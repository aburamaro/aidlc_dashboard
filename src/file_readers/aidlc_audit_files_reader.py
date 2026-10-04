from pathlib import Path


def list_aidlc_audit_files(audit_log_directory: str | Path) -> list[Path]:
    """auditディレクトリ配下のファイルを更新日時の新しい順で一覧する。"""
    audit_directory = Path(audit_log_directory)

    if not audit_directory.is_dir():
        raise FileNotFoundError(f"AIDLC auditディレクトリが見つかりません: {audit_directory}")

    # Dashboardの「最近の更新」に使いやすいよう、新しいファイルを先頭に並べる。
    return sorted(
        (path for path in audit_directory.rglob("*") if path.is_file()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def read_aidlc_audit_file(audit_file_path: str | Path) -> str:
    """auditファイルを1件読み込む。"""
    path = Path(audit_file_path)

    if not path.is_file():
        raise FileNotFoundError(f"AIDLC auditファイルが見つかりません: {path}")

    return path.read_text(encoding="utf-8")


def read_aidlc_audit_files(audit_log_directory: str | Path) -> dict[Path, str]:
    """auditディレクトリ配下の全ファイルを読み込む。"""
    return {
        audit_file_path: read_aidlc_audit_file(audit_file_path)
        for audit_file_path in list_aidlc_audit_files(audit_log_directory)
    }
