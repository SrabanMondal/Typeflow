import json
import os
from ast import literal_eval
from pathlib import Path
from pprint import pformat
from typing import Any

import typer
import yaml


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


def format_yaml_val(data: dict) -> Any:
    """
    Takes a dict containing 'val' and 'valueType',
    and returns a properly typed Python value.

    Supports:
      - str, int, float, bool, list, dict, set, number (float alias)

    Examples:
      {"val": "true", "valueType": "bool"}  -> True
      {"val": "123", "valueType": "int"}    -> 123
      {"val": "[1,2]", "valueType": "list"} -> [1, 2]
      {"val": "hello", "valueType": "str"}  -> "hello"
    """

    if not isinstance(data, dict):
        raise TypeError("Expected a dict input.")
    if "val" not in data:
        raise KeyError("'val' missing in input.")
    if "output" not in data:
        raise KeyError("'valueType' missing in input.")

    raw_val = data["val"]
    vtype = data["output"].lower().strip()

    if isinstance(raw_val, str):
        raw_val = raw_val.strip()

    try:
        if vtype in ("str", "string"):
            formatted = f"{pformat(data['val'])}"
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

        elif vtype in ("list", "set", "dict"):
            # try parsing JSON or Python literal
            try:
                parsed = json.loads(raw_val) if isinstance(raw_val, str) else raw_val
            except Exception:
                parsed = literal_eval(raw_val)

            if vtype == "set":
                return set(parsed)
            return parsed

        else:
            # fallback — keep as string
            return raw_val

    except Exception as e:
        raise ValueError(f"Failed to format value '{raw_val}' as '{vtype}': {e}")


def load_const():
    """Load YAML definitions from nodes and classes dirs."""
    CONST_DIR = ".typeflow/consts"
    const_data = {}
    print(CONST_DIR)

    for fname in os.listdir(CONST_DIR):
        print(fname)
        if fname.endswith(".yaml"):
            path = os.path.join(CONST_DIR, fname)
            with open(path) as f:
                data = yaml.safe_load(f)
                if not data:
                    continue
                const_data[data["name"]] = data
    return const_data
