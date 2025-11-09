from pathlib import Path

import typer

from typeflow.core import generate_script, write_script_to_file
from typeflow.utils import load_compiled_graphs


def generate():
    """Generate orchestrator script based on compiled graphs."""
    #typer.echo("🔧 Loading compiled adjacency data...")
    adj_list, rev_adj_list = load_compiled_graphs()

    typer.echo("🧠 Generating orchestrator script...")
    script = generate_script(adj_list, rev_adj_list)

    output_path = Path.cwd() / "src" / "orchestrator.py"
    write_script_to_file(script, output_path)

    typer.echo(f"✅ Orchestrator generated at: {output_path}")
