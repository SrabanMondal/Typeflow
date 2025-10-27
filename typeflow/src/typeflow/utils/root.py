from pathlib import Path


def get_project_root() -> str:
    """Find the project root by looking for .typeflow folder in current,
    parent, or parent-parent directory."""
    current_dir = Path.cwd()
    for directory in [current_dir, current_dir.parent, current_dir.parent.parent]:
        typeflow_dir = directory / ".typeflow"
        if typeflow_dir.exists() and typeflow_dir.is_dir():
            return str(directory)
    raise FileNotFoundError(
        "Could not find .typeflow folder in current directory, parent, or parent-parent directory."
        "Please run from a directory containing .typeflow."
    )
