from fastapi import APIRouter, HTTPException

from typeflow.server.core.loader import load_dag, load_nodes_classes
from typeflow.server.core.saver import create_const_yamls

router = APIRouter()

# @router.get("/manifest")
# def get_manifest():
#     return load_manifest()


@router.get("/dag")
def get_dag():
    try:
        return load_dag()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
def save_workflow_api(data: dict):
    try:
        saved_files = create_const_yamls(data)
        return {"status": "saved", "const_files": saved_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nodes")
def get_nodes():
    try:
        return load_nodes_classes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
