from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from typeflow.server.routes import api
from fastapi.staticfiles import StaticFiles
import asyncio, subprocess, sys, os, json

STATIC_DIR = Path(__file__).parent.parent / "ui" / "build"

OUTPUT_DIR = Path("data/outputs")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)


def create_app():
    app = FastAPI(title="Typeflow UI Backend")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # ya ["*"] for all
        allow_credentials=True,
        allow_methods=["*"],  # GET, POST, PUT, DELETE etc
        allow_headers=["*"],  # Authorization, Content-Type etc
    )
    app.include_router(api.router, prefix="/api")
    app.mount("/outputs", StaticFiles(directory="data/outputs"), name="outputs")
    app.mount(
        "/",
        StaticFiles(directory=STATIC_DIR, html=True),
        name="ui"
    )
    return app

app = create_app()

