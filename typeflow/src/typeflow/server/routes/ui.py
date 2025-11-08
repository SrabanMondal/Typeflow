import importlib.resources as pkg_resources
from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import os
import typer
router = APIRouter()
STATIC_DIR = Path(__file__).parent.parent.parent / "ui" / "build"
typer.echo("ui: ")
typer.echo(STATIC_DIR)
from fastapi import exceptions
if not STATIC_DIR.exists():
    typer.echo(f"Warning: Static UI directory not found at {STATIC_DIR}")
    typer.echo("UI will not be served!")
try:
    # ui_path = Path(".")
    # if not ui_path.exists() or not ui_path:
    #     raise FileNotFoundError
    @router.get("/")
    async def ui_not_found():
        return {
            "error": "path: "+str(STATIC_DIR)
        }
    # router.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="ui")
    # ui_p = Path(typeflow.ui.__path__[0])
    # msg = "ui/build not exists"
    # if not ui_p.exists():
    #     msg="ui not exists"
except:
    @router.get("/")
    async def ui_not_found():
        return {
            "error": "path: "+str(STATIC_DIR)
        }