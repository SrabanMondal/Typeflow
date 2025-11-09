from pathlib import Path

import yaml


def yaml_to_class_json(yaml_path: Path) -> dict:
    """
    Convert a class node YAML manifest into simplified JSON format for UI.
    """
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    name = data.get("name")
    description = data.get("description", "")
    entity_symbol = "C"

    fields = list(data.get("fields", {}).keys()) if data.get("fields") else []

    methods_data = data.get("methods", {})
    methods = []

    for method_name, m in methods_data.items():
        input_ports = list(m.get("input", {}).keys()) if m.get("input") else []
        output_ports = []

        returns = m.get("returns")
        if returns and returns != "NoneType":
            output_ports.append("returns")

        methods.append(
            {
                "entity": "C",
                "name": method_name,
                "description": m.get("description", ""),
                "inputPorts": input_ports,
                "outputPorts": output_ports,
                "is_static": m.get("is_static", False),
            }
        )

    class_json = {
        "entity": entity_symbol,
        "name": name,
        "description": description,
        "inputPorts": fields,
        "outputPorts": fields,
        "methods": methods,
    }

    return class_json


def load_all_class_manifests(class_dir: Path) -> list:
    """
    Parse all class YAML files under given directory.
    Returns a list of simplified JSON dicts.
    """
    class_jsons = []
    for yaml_file in class_dir.glob("*.yaml"):
        try:
            class_jsons.append(yaml_to_class_json(yaml_file))
        except Exception as e:
            print(f"⚠️ Error parsing {yaml_file.name}: {e}")
    return class_jsons
