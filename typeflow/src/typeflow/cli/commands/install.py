import subprocess
import yaml
from pathlib import Path
import sys, os
import typer

def run_cmd(cmd: list[str]):
    """Run a subprocess and stream output live."""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        typer.echo(f"❌ Command failed: {' '.join(cmd)}", file=sys.stderr)

def install():
    root = Path(".")
    typeflow_dir = root / ".typeflow"
    workflow_file = root / "workflow" / "workflow.yaml"

    if not typeflow_dir.exists():
        typer.echo("⚠️  .typeflow folder not found in root.")
        return
    if not workflow_file.exists():
        typer.echo("⚠️  workflow/workflow.yaml file not found.")
        return

    with open(workflow_file, "r") as f:
        config = yaml.safe_load(f)

    name = config.get("name", "Unnamed Workflow")
    typer.echo(f"🚀 Installing workflow: {name}")
        # Initialize uv project
    typer.echo("Initializing uv project...")
    try:
        subprocess.run(
            ["uv", "init"],
            cwd=root,
            check=True,
        )
        typer.echo("✅ uv project initialized successfully!")
    except FileNotFoundError:
        typer.echo("⚠️  'uv' not found! Please install it with `pip install uv`.")
        raise typer.Exit(code=1)
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ uv init failed: {e}")
        raise typer.Exit(code=1)

    # Install typeflow inside project venv
    typer.echo("Installing typeflow inside project .venv...")
    try:
        subprocess.run(
            ["uv", "add", "pip"],
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["pip", "install", "typeflow"],
            cwd=root,
            check=True,
        )
        typer.echo("✅ typeflow installed in project .venv!")
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Failed to install typeflow in project .venv: {e}")

    deps = config.get("dependencies", [])
    # nodes = config.get("nodes", [])
    # classes = config.get("classes", [])

    if deps:
        typer.echo("\n📦 Installing dependencies via uv...")
        for dep in deps:
            typer.echo(f"   → {dep}")
            run_cmd(["uv", "add", dep])
    else:
        typer.echo("\n📦 No dependencies listed.")

    # if nodes:
    #     typer.echo("\n🧩 Validating nodes...")
    #     for node in nodes:
    #         typer.echo(f"   → {node}")
    #         run_cmd(["typeflow", "validate", "node", node])
    # else:
    #         typer.echo("\n🧩 No nodes found in workflow.yaml.")

    # if classes:
    #     print("\n🏗️  Validating classes...")
    #     for cls in classes:
    #         print(f"   → {cls}")
    #         run_cmd(["typeflow", "validate", "class", cls])
    # else:
    #     print("\n🏗️  No classes found in workflow.yaml.")

    typer.echo("\n✅ Installation successful!")
    typer.echo(f"👉 To activate the project environment, run:")
    if sys.platform.startswith("win"):
        typer.echo(f"    .venv\\Scripts\\Activate.ps1  # PowerShell")
    else:
        typer.echo(f"    source .venv/bin/activate  # Linux/macOS")
    typer.echo("After activation, you can run \n1.typeflow validate workflow\n2. typeflow compile\n3. typeflow generate\n4. typeflow run.")

