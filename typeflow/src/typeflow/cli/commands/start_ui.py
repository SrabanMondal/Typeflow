import typer
import uvicorn


def start_ui(port: int = 3001):
    """
    Starts the Typeflow visual editor (UI + API server)
    """
    typer.echo("🚀 Starting Typeflow UI on http://localhost:3000 ...")
    uvicorn.run("typeflow.server.main:app", host="0.0.0.0", port=port, reload=False)
