import subprocess
import sys
from pathlib import Path

import typer

root = Path(".")


def run():
    """
    Runs the orchestrator script
    """

    typer.echo("Running project...")
    try:
        subprocess.run(
            [sys.executable, "-m", "src.orchestrator"],
            cwd=root,
            check=True,
        )
    except FileNotFoundError:
        typer.echo(
            "⚠️  Orchestrator script not found! Please run it to get script `typeflow generate`."
        )
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Workflow project failed to run: {e}")
