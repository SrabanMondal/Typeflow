from pathlib import Path

import yaml


def yaml_to_node_json(yaml_path: Path) -> dict:
    """
    Convert a single node manifest YAML file into simplified JSON format for UI.
    """
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f)

    # Basic fields
    name = data.get("name")
    description = data.get("description", "")

    # Normalize entity: F for function, C for class, etc.
    entity_symbol = "F"

    # Extract inputs
    inputs = list(data.get("inputs", {}).keys()) if data.get("inputs") else []

    # Extract outputs
    returns = data.get("returns")
    output_ports = []
    if returns and returns != "NoneType":
        output_ports.append("returns")

    # Construct final JSON-compatible dict
    node_json = {
        "entity": entity_symbol,
        "name": name,
        "description": description,
        "inputPorts": inputs,
        "outputPorts": output_ports,
    }

    return node_json


def load_all_node_manifests(nodes_dir: Path) -> list:
    """
    Parse all node YAML files under given directory.
    Returns a list of simplified JSON dicts.
    """
    node_jsons = []
    for yaml_file in nodes_dir.glob("*.yaml"):
        try:
            node_jsons.append(yaml_to_node_json(yaml_file))
        except Exception as e:
            print(f"⚠️ Error parsing {yaml_file.name}: {e}")
    return node_jsons
