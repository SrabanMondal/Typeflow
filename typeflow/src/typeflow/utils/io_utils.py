from pprint import pformat
import json
from pathlib import Path
import os
import yaml
import typer


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


def format_yaml_val(data: dict) -> str:
    """
    Takes a YAML-loaded dict and returns a formatted Python assignment string.
    
    Example:
        {'val': 'Hello'}  ->  "data = 'Hello'"
        {'val': [1, 2, 3]}  ->  "data = [1, 2, 3]"
    """
    if not isinstance(data, dict):
        raise TypeError("Expected a dictionary (YAML-loaded data).")

    if "val" not in data:
        raise KeyError("'val' key not found in the input data.")

    formatted = f"{pformat(data['val'])}"
    return formatted

def load_const():
    """Load YAML definitions from nodes and classes dirs."""
    CONST_DIR = ".typeflow/consts"
    const_data={}
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