import json

import typer

from typeflow.utils import (
    create_adjacency_lists,
    ensure_structure,
    save_compiled,
    validate_graph,
    extract_io_nodes,
    save_io_nodes
)


def compile():
    """Compile workflow DAG into adjacency lists and validate edges."""
    dag_path = ensure_structure()

    with open(dag_path, "r") as f:
        workflow_json = json.load(f)

    typer.echo("🧩 Creating adjacency lists...")
    adj_list, rev_adj_list = create_adjacency_lists(workflow_json)
    io_nodes = extract_io_nodes(workflow_json)
    save_io_nodes(io_nodes)
    save_compiled(adj_list, rev_adj_list)

    typer.echo("🔍 Validating graph edges...")
    all_valid = validate_graph(adj_list)

    if all_valid:
        typer.echo("✅ Workflow compiled and validated successfully!")
    else:
        typer.echo("⚠️ Workflow compiled but with some validation errors.")
