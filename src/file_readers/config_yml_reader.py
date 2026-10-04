from pathlib import Path
from typing import Any

import yaml


def read_config_yml(config_file_path: str | Path = "config.yml") -> dict[str, Any]:
    """config.ymlを読み込み、辞書形式の設定値として返す。"""
    path = Path(config_file_path)

    # 設定ファイルはアプリ起動時の前提になるため、存在しない場合は明示的に止める。
    if not path.exists():
        raise FileNotFoundError(f"設定ファイルが見つかりません: {path}")

    with path.open("r", encoding="utf-8") as config_file:
        config_data = yaml.safe_load(config_file) or {}

    # ルートがリストや文字列だと後続処理で扱えないため、YAMLの形をここで確認する。
    if not isinstance(config_data, dict):
        raise ValueError(f"設定ファイルのルートはYAMLのマッピング形式にしてください: {path}")

    return config_data
