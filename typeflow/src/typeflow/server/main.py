from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typeflow.server.routes import api


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
    # app.include_router(ui.router)
    return app


app = create_app()
