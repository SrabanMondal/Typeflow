import json
from pathlib import Path

from typeflow.server.utils.const_yaml import save_single_const_yaml

WORKFLOW_DIR = Path("workflow")


def save_workflow(data: dict):
    f = WORKFLOW_DIR / "dag.json"
    f.write_text(json.dumps(data, indent=2))


def create_const_yamls(workflow_data: dict) -> list[str]:
    """
    Iterates through the workflow data, finds all 'X' type nodes,
    and calls `save_single_const_yaml` for each of them.
    Returns a list of saved YAML file paths.
    """
    saved_files = []
    const_dir = Path(".typeflow/consts")
    const_dir.mkdir(parents=True, exist_ok=True)

    for node in workflow_data.get("nodes", []):
        if node.get("type") == "X":
            try:
                path = save_single_const_yaml(node, const_dir)
                saved_files.append(path)
            except Exception as e:
                print(f"⚠️ Failed to save const for node {node.get('id')}: {e}")

    return saved_files
