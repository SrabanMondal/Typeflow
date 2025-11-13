import asyncio
import json
import os
import re
import shutil
import sys
import uuid
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from typeflow.core import generate_script, write_script_to_file
from typeflow.server.core.loader import load_dag, load_nodes_classes
from typeflow.server.core.saver import save_workflow
from typeflow.utils import (  # validate_graph,
    create_adjacency_lists,
    extract_io_nodes,
)

UPLOAD_DIR = Path("data/inputs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
router = APIRouter()

# @router.get("/manifest")
# def get_manifest():
#     return load_manifest()


sessions: dict[str, asyncio.Queue] = {}


async def run_script(session_id: str, script_path: Path):
    proc = await asyncio.create_subprocess_exec(
        sys.executable,
        "-m",
        "src.orchestrator_live",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    queue = sessions[session_id]

    async def read_stdout():
        if not proc.stdout:
            return
        async for line in proc.stdout:
            # print("logs: ",line)
            text = line.decode().strip()
            if not text:
                continue
            try:
                event = json.loads(text)
                if isinstance(event, dict) and "event" in event:
                    await queue.put(event)
                else:
                    await queue.put({"event": "log", "data": text})
            except json.JSONDecodeError:
                await queue.put({"event": "log", "data": text})

    async def read_stderr():
        if not proc.stderr:
            return
        async for line in proc.stderr:
            # print("logs: ",line)
            text = line.decode().strip()
            if not text:
                continue
            await queue.put({"event": "error_log", "data": text})

    # Run both concurrently
    stdout_task = asyncio.create_task(read_stdout())
    stderr_task = asyncio.create_task(read_stderr())

    await asyncio.wait([stdout_task, stderr_task])

    return_code = await proc.wait()

    if return_code != 0:
        await queue.put({"event": "workflow_error", "data": f"Exit code {return_code}"})
    else:
        await queue.put({"event": "workflow_complete", "data": None})
    try:
        if os.path.exists(script_path):
            os.remove(script_path)
            print(f"✅ Deleted script: {script_path}")
        else:
            print(f"⚠️ Script not found: {script_path}")
    except Exception as e:
        print(f"⚠️ Error deleting script: {e}")


@router.post("/start")
async def start_script(data: dict, background_tasks: BackgroundTasks):
    try:
        session_id = str(uuid.uuid4())
        sessions[session_id] = asyncio.Queue()
        adj_list, rev_adj_list = create_adjacency_lists(data)
        io_nodes = extract_io_nodes(data)
        script = generate_script(adj_list, rev_adj_list, True, io_nodes)
        output_path = Path.cwd() / "src" / "orchestrator_live.py"
        write_script_to_file(script, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    background_tasks.add_task(run_script, session_id, output_path)
    return {"session_id": session_id, "message": "Script execution started"}


@router.get("/dag")
def get_dag():
    try:
        return load_dag()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/save")
def save_workflow_api(data: dict):
    try:
        save_workflow(data)
        # saved_files = create_const_yamls(data)
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/nodes")
def get_nodes():
    try:
        return load_nodes_classes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload_file")
async def upload_file(file: UploadFile = File(...), nodeId: str = Form(...)):
    if file.filename:
        ext = Path(file.filename).suffix
        safe_node_id = re.sub(r"[^\w\d_-]", "_", nodeId)
        save_path = UPLOAD_DIR / f"{safe_node_id}{ext}"
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_path_str = str(save_path).replace("\\", "/")
        return {"filePath": file_path_str}
    raise HTTPException(status_code=400, detail="")


# ----------- SSE Event Stream -----------
# async def event_generator():
#     while True:
#         msg = await event_queue.get()
#         print("msg: ",msg)
#         yield f"data: {json.dumps(msg)}\n\n"
#         await asyncio.sleep(1)


@router.get("/stream")
async def stream(session_id: str):
    queue = sessions.get(session_id)
    if not queue:
        return StreamingResponse(
            iter([b"data: session not found\n\n"]), media_type="text/event-stream"
        )

    async def event_generator():
        try:
            while True:
                msg = await queue.get()
                # print("msg:", msg)
                yield f"data: {json.dumps(msg)}\n\n"
                await asyncio.sleep(0.2)
                if msg.get("event") in {"workflow_complete", "workflow_error"}:
                    break
        finally:
            sessions.pop(session_id, None)
            print(f"🧹 Cleaned up session {session_id}")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
