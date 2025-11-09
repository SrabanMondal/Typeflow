# import importlib.resources as pkg_resources
# from fastapi import APIRouter
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pathlib import Path
# import os
# import typer

# router = APIRouter()
# STATIC_DIR = Path(__file__).parent.parent.parent / "ui" / "build"
# typer.echo("ui: ")
# typer.echo(STATIC_DIR)

# if not STATIC_DIR.exists():
#     typer.echo(f"Warning: Static UI directory not found at {STATIC_DIR}")
#     typer.echo("UI will not be served!")
# try:
#     @router.get("/")
#     async def ui_not_found():
#         return {
#             "error": "path: "+str(STATIC_DIR)
#         }
# except:
#     @router.get("/")
#     async def ui_not_found():
#         return {
#             "error": "path: "+str(STATIC_DIR)
#         }