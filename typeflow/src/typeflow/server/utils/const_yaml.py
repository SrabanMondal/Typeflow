from pathlib import Path

import yaml


def save_single_const_yaml(node: dict, output_dir: Path) -> str:
    """
    Saves a single constant ('X' type) node as YAML in the given output directory.
    Returns the path of the saved file.
    """
    d = node.get("data", {})
    if not d.get("name"):
        raise ValueError("Constant node missing 'name' field")

    yaml_obj = {
        "name": f"{d['name']}@{node['id'].split('@')[-1]}",
        "entity": "constant",
        "val": d.get("value", ""),
        "output": d.get("valueType", ""),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{d['name']}.yaml"
    file_path = output_dir / filename

    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_obj, f, sort_keys=False, allow_unicode=True)

    return str(file_path)
