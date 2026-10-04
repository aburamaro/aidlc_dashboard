from pathlib import Path


DEFAULT_PHASE_DIRECTORY_NAMES = (
    "ideation",
    "inception",
    "construction",
    "operation",
    "verification",
)


def list_aidlc_phase_directories(
    workflow_data_directory: str | Path,
    phase_directory_names: tuple[str, ...] = DEFAULT_PHASE_DIRECTORY_NAMES,
) -> dict[str, Path]:
    """Workflow用データディレクトリ配下に存在するPhaseディレクトリを一覧する。"""
    base_directory = Path(workflow_data_directory)

    if not base_directory.is_dir():
        raise FileNotFoundError(f"Workflow用データディレクトリが見つかりません: {base_directory}")

    phase_directories: dict[str, Path] = {}
    for phase_name in phase_directory_names:
        phase_directory = base_directory / phase_name
        # AIDLCの構成差分を許容するため、存在するPhaseだけを返す。
        if phase_directory.is_dir():
            phase_directories[phase_name] = phase_directory

    return phase_directories


def list_aidlc_phase_files(
    workflow_data_directory: str | Path,
    phase_directory_names: tuple[str, ...] = DEFAULT_PHASE_DIRECTORY_NAMES,
    recursive: bool = True,
) -> dict[str, list[Path]]:
    """各Phaseディレクトリ配下のファイルを一覧する。"""
    phase_directories = list_aidlc_phase_directories(
        workflow_data_directory,
        phase_directory_names,
    )
    # Phase配下にサブディレクトリがある可能性を考慮し、初期値では再帰的に探索する。
    glob_pattern = "**/*" if recursive else "*"

    phase_files: dict[str, list[Path]] = {}
    for phase_name, phase_directory in phase_directories.items():
        phase_files[phase_name] = sorted(
            path for path in phase_directory.glob(glob_pattern) if path.is_file()
        )

    return phase_files
