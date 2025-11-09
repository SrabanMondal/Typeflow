import typer
import subprocess
import sys
from pathlib import Path
from .utils import check_decorator, update_workflow_yaml


def validate_class(class_name: str = typer.Argument(None)):
    cwd = Path.cwd()

    if not (cwd / ".typeflow").exists():
        typer.echo("Error: Cannot detect .typeflow folder. Run from project root.")
        raise typer.Exit(code=1)

    classes_dir = cwd / "src" / "classes"

    if class_name is None:
        typer.echo("No class specified — validating all classes...")
        for file in classes_dir.glob("*.py"):
            if file.name != "__init__.py":
                validate_class(file.stem)
        return

    class_file = classes_dir / f"{class_name}.py"

    if not class_file.exists():
        typer.echo(f"Error: Class '{class_name}' does not exist.")
        raise typer.Exit(code=1)

    module_path = f"src.classes.{class_name}"

    try:
        subprocess.run([sys.executable, "-m", module_path], cwd=cwd, check=True)
    except subprocess.CalledProcessError as e:
        typer.echo(f"Runtime Error in class '{class_name}': {e}")
        raise typer.Exit(code=1)

    if not check_decorator(class_file, "node_class"):
        typer.echo(f"Error: Class '{class_name}' does not have @node_class decorator.")
        raise typer.Exit(code=1)

    update_workflow_yaml(class_name, "classes")
    typer.echo(f"Class '{class_name}' validated and added to workflow.yaml")
