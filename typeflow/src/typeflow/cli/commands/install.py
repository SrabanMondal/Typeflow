import subprocess
import sys
from pathlib import Path

import typer
import yaml


def run_cmd(cmd: list[str], cwd: Path = Path(".")):
    """Run a subprocess command and stream output live."""
    try:
        subprocess.run(cmd, cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"❌ Command failed: {' '.join(cmd)}", file=sys.stderr)
        raise typer.Exit(code=e.returncode)


def install(
    active: bool = typer.Option(
        False, "--active", "-a", help="Use existing virtual environment and sync deps"
    ),
    deps: bool = typer.Option(
        False, "--deps", "-d", help="Initialize uv project and add deps manually"
    ),
):
    root = Path(".")
    typeflow_dir = root / ".typeflow"
    workflow_file = root / "workflow" / "workflow.yaml"

    if not typeflow_dir.exists():
        typer.echo("⚠️  .typeflow folder not found in root.")
        raise typer.Exit(1)
    if not workflow_file.exists():
        typer.echo("⚠️  workflow/workflow.yaml not found.")
        raise typer.Exit(1)

    with open(workflow_file, "r") as f:
        config = yaml.safe_load(f)

    name = config.get("name", "Unnamed Workflow")
    declared_py = config.get("python")
    deps_list = config.get("dependencies", [])

    typer.echo(f"🚀 Installing workflow: {name}\n")

    # ----------------------------
    # 🔍 Python version check
    # ----------------------------
    current_py = f"{sys.version_info.major}.{sys.version_info.minor}"
    if declared_py:
        if declared_py != current_py:
            typer.echo(
                f"⚠️  Python version mismatch:\n"
                f"   → Workflow expects: {declared_py}\n"
                f"   → Current interpreter: {current_py}\n"
                "   This may cause dependency or runtime issues.\n"
            )
        else:
            typer.echo(f"🐍 Python version OK ({current_py})\n")
    else:
        typer.echo(
            f"ℹ️  No Python version specified in workflow.yaml (current: {current_py})\n"
        )

    # ----------------------------
    # Case 1: Default (no flags)
    # ----------------------------
    if not active and not deps:
        typer.echo("🧱 Setting up new uv project...")
        run_cmd(["uv", "init"], cwd=root)
        typer.echo("✅ uv project initialized successfully!\n")

        typer.echo("📦 Installing typeflow inside project .venv...")
        try:
            run_cmd(["uv", "add", "pip"], cwd=root)
            run_cmd(["pip", "install", "typeflow"], cwd=root)
            typer.echo("✅ typeflow installed in project .venv!\n")
        except subprocess.CalledProcessError as e:
            typer.echo(f"❌ Failed to install typeflow: {e}")
            raise typer.Exit(code=1)

        typer.echo("🔄 Syncing environment with uv.lock ...")
        run_cmd(["uv", "sync"], cwd=root)
        typer.echo("✅ Environment fully set up!\n")

    # ----------------------------
    # Case 2: Active flag
    # ----------------------------
    elif active:
        typer.echo("⚙️ Using active environment, syncing dependencies...")
        run_cmd(["uv", "sync"], cwd=root)
        typer.echo("✅ Synced successfully using uv.lock!\n")

    # ----------------------------
    # Case 3: Deps flag
    # ----------------------------
    elif deps:
        typer.echo("🧱 Initializing new uv project...")
        run_cmd(["uv", "init"], cwd=root)
        typer.echo("✅ uv project initialized successfully!\n")

        if deps_list:
            typer.echo("📦 Installing dependencies manually:")
            for dep in deps_list:
                typer.echo(f"   → {dep}")
                run_cmd(["uv", "add", dep], cwd=root)
            typer.echo("✅ Dependencies installed via uv add!\n")
        else:
            typer.echo("📦 No dependencies listed in workflow.yaml\n")

    # ----------------------------
    # Post-install instructions
    # ----------------------------
    typer.echo("✅ Installation complete!")
    typer.echo("👉 To activate your environment:")
    if sys.platform.startswith("win"):
        typer.echo("   .venv\\Scripts\\Activate.ps1  # PowerShell")
    else:
        typer.echo("   source .venv/bin/activate     # macOS/Linux")

    typer.echo("\nThen run:")
    typer.echo("  1. typeflow validate workflow")
    typer.echo("  2. typeflow compile")
    typer.echo("  3. typeflow generate")
    typer.echo("  4. typeflow run")

    # Optional summary line
    mode = (
        "Fresh setup (init + sync)"
        if not active and not deps
        else "Active environment sync" if active else "Manual deps install"
    )
    typer.echo(f"\n🧩 Mode: {mode}")
