import os

from fastapi import APIRouter
from fastapi.staticfiles import StaticFiles

router = APIRouter()

ui_path = os.path.join(os.path.dirname(__file__), "../../ui/dist")

if os.path.exists(ui_path):
    router.mount("/", StaticFiles(directory=ui_path, html=True), name="ui")
else:

    @router.get("/")
    async def ui_not_found():
        return {
            "error": "UI not built. Run `npm run build && npm run export` in the ui folder."
        }
