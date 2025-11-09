import ast
from pathlib import Path

import typer
import yaml

from . import validate_node, validate_class, validate_workflow

app = typer.Typer(help="Validate nodes or classes")



# ---------------- NODE SUBCOMMAND ----------------

app.command("node")(validate_node.validate_node)
app.command("class")(validate_class.validate_class)
app.command("workflow")(validate_workflow.validate_workflow)