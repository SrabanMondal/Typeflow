import json
import os
from ast import literal_eval
from pathlib import Path
from pprint import pformat
from typing import Any

import typer
import yaml

IO_FILE = Path(".typeflow/compiled/io.json")

def ensure_structure():
    """Ensure required folders/files exist."""
    cwd = Path.cwd()
    typeflow_dir = cwd / ".typeflow"
    workflow_dir = cwd / "workflow"
    dag_file = workflow_dir / "dag.json"

    if not typeflow_dir.exists():
        typer.echo(
            "⚠️ Missing .typeflow directory. Run from a valid Typeflow project root."
        )
        raise typer.Exit(1)
    if not workflow_dir.exists():
        typer.echo(
            "⚠️ Missing workflow directory. Run from a valid Typeflow project root."
        )
        raise typer.Exit(1)
    if not dag_file.exists():
        typer.echo("⚠️ Missing workflow/dag.json file. Nothing to compile.")
        raise typer.Exit(1)

    return dag_file


def save_compiled(adj_list, rev_adj_list):
    """Save adjacency lists under .typeflow/compiled/."""
    compiled_dir = Path(".typeflow/compiled")
    compiled_dir.mkdir(parents=True, exist_ok=True)

    with open(compiled_dir / "adj_list.json", "w") as f:
        json.dump(adj_list, f, indent=2)
    with open(compiled_dir / "rev_adj_list.json", "w") as f:
        json.dump(rev_adj_list, f, indent=2)

    typer.echo("💾 Saved compiled adjacency lists under .typeflow/compiled/")


def load_compiled_graphs():
    """Load adjacency and reverse adjacency lists from compiled folder."""
    compiled_dir = Path(".typeflow/compiled")
    adj_path = compiled_dir / "adj_list.json"
    rev_path = compiled_dir / "rev_adj_list.json"

    if not adj_path.exists() or not rev_path.exists():
        typer.echo("⚠️ Missing compiled graph files. Run `typeflow compile` first.")
        raise typer.Exit(1)

    with open(adj_path, "r") as f:
        adj_list = json.load(f)
    with open(rev_path, "r") as f:
        rev_adj_list = json.load(f)

    return adj_list, rev_adj_list


def format_input_val(data: dict) -> Any:
    if not isinstance(data, dict):
        raise TypeError("Expected a dict input.")
    if "value" not in data:
        raise KeyError("'val' missing in input.")
    if "valueType" not in data:
        raise KeyError("'valueType' missing in input.")

    raw_val = data["value"]
    vtype = data["valueType"].lower().strip()

    if isinstance(raw_val, str):
        raw_val = raw_val.strip()

    try:
        if vtype in ("str", "string"):
            formatted = f"{pformat(raw_val)}"
            return formatted

        elif vtype in ("int", "integer"):
            return int(raw_val)

        elif vtype in ("float", "number"):
            return float(raw_val)

        elif vtype == "bool":
            if isinstance(raw_val, bool):
                return raw_val
            val_lower = str(raw_val).lower()
            if val_lower in ("true", "1", "yes", "on"):
                return True
            elif val_lower in ("false", "0", "no", "off"):
                return False
            else:
                raise ValueError(f"Invalid boolean value: {raw_val}")

        elif vtype in ("list", "set", "dict", "tuple"):
           
            try:
                parsed = json.loads(raw_val) if isinstance(raw_val, str) else raw_val
            except Exception:
                parsed = literal_eval(raw_val)

            if vtype == "set":
                return set(parsed)
            elif vtype == "tuple":
                return tuple(parsed)
            return parsed

        else:
            return raw_val

    except Exception as e:
        raise ValueError(f"Failed to format value '{raw_val}' as '{vtype}': {e}")

#-------------------------------
def load_const():
    """Load YAML definitions from nodes and classes dirs."""
    CONST_DIR = ".typeflow/consts"
    const_data = {}
    # print(CONST_DIR)

    for fname in os.listdir(CONST_DIR):
        # path = os.path.join(CONST_DIR, fname)
        # print(f"Reading: {path} | Last modified: {os.path.getmtime(path)}")
        # print(fname)
        if fname.endswith(".yaml"):
            path = os.path.join(CONST_DIR, fname)
            with open(path) as f:
                data = yaml.safe_load(f)
                if not data:
                    continue
                const_data[data["name"]] = data
    return const_data
# --------------------------------


def extract_io_nodes(workflow_json: dict):
    """
    Extracts nodes of type X and O from a workflow JSON and returns them as a list.
    """
    io_nodes = [node for node in workflow_json.get("nodes", []) if node.get("type") in ("X", "O")]
    return io_nodes

def save_io_nodes(io_nodes: list, filename = IO_FILE):
    """
    Saves a list of I/O nodes to a JSON file.
    """
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(io_nodes, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Extracted {len(io_nodes)} I/O nodes and saved to {filename}")

def load_io_data():
    """Helper function to load io.json"""
    if not IO_FILE.exists():
        raise FileNotFoundError("io.json not found. Run extract_io_nodes() first.")
    with open(IO_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_io_node(node_id: str, nodes:dict):
    """
    Returns the 'value' of a node with the given ID from io.json.
    """
    for node in nodes:
        if node["id"] == node_id:
            return node["data"]
    raise KeyError(f"Node '{node_id}' not found in io.json.")


def get_node_value_type(node_id: str, nodes:dict):
    """
    Returns the value type of a node (valueType for X nodes, outputType for O nodes).
    """
    for node in nodes:
        if node["id"] == node_id:
            node_type = node.get("type")
            data = node.get("data", {})
            if node_type == "X":
                return data.get("valueType")
            elif node_type == "O":
                return data.get("outputType")
            else:
                raise ValueError(f"Node '{node_id}' is not an X or O type node.")
    raise KeyError(f"Node '{node_id}' not found in io.json.")
