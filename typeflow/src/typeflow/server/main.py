from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from typeflow.server.routes import api

STATIC_DIR = Path(__file__).parent.parent / "ui" / "build"

OUTPUT_DIR = Path("data/outputs")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)


def create_app():
    app = FastAPI(title="Typeflow UI Backend")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api.router, prefix="/api")
    app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="ui")
    return app


app = create_app()
