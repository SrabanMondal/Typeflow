# Workflows in Typeflow

A **workflow** in Typeflow represents a **directed acyclic graph (DAG)** connecting nodes, classes, and data sources into a single executable pipeline.  
It defines **how data flows** through your project — from inputs (files, constants, API data) through processing nodes (functions or classes), to final outputs.

---

## Workflow Overview

Each workflow has two main components:

1. **Workflow Metadata** → defined in `workflow.yaml`  
2. **Workflow Graph** → defined in `dag.json` (generated via editor)

Together, these describe both the *structure* and *execution logic* of your Typeflow project.

---

## Workflow Structure

A typical Typeflow project after setup looks like this:

```text
my_app/
│
├── src/
│   ├── nodes/
│   │   ├── load_image/
│   │   │   └── main.py
│   │   ├── resize_image/
│   │   │   └── main.py
│   │   └── ...
│   ├── classes/
│   │   └── Watermark.py
│   └── orchestrator.py          # auto-generated after 'typeflow generate'
│
├── .typeflow/
│   ├── dag.json                 # generated from visual editor
│   ├── compiled/
│   │   ├── adj_list.json
│   │   ├── rev_adj_list.json
│   │   └── io.json
│   └── cache/
│
├── workflow.yaml                # workflow metadata
└── .venv/
```

---

## `workflow.yaml` — The Metadata File

`workflow.yaml` is the **blueprint** of your workflow project.  
It tells Typeflow what nodes and classes exist, and their dependencies.

### Example

```yaml
name: my_app
description: Describe your workflow here
version: 1.0.0
dependencies:
  - pillow
classes:
  - Watermark
nodes:
  - adjust_brightness
  - grayscale
  - load_image
  - resize_image
  - save_image
```

### Key Fields

| Field         | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `name`        | Name of the workflow project                                                |
| `description` | A short description of what your workflow does                              |
| `version`     | Workflow version                                                            |
| `dependencies`| Python packages required (added automatically via `typeflow add`)           |
| `classes`     | List of custom `@node_class` classes                                        |
| `nodes`       | List of function-based nodes (created via `typeflow create-node`)           |

Typeflow uses this file to validate your environment and locate all workflow entities.

---

## `dag.json` — The Graph Definition

This is the **core DAG** representation of your workflow.  
It is generated automatically when you build your workflow visually in the **Typeflow Editor UI**.

Each node in the editor appears here with:
- a unique `id`
- its `type` (F, C, M, or X)
- input/output ports
- coordinates (for layout)
- connection data

### Node Types

| Type | Meaning                                      |
|------|----------------------------------------------|
| `F`  | Function node (created via `@node()`)        |
| `C`  | Class node (declared via `@node_class`)      |
| `M`  | Method node (auto-generated from a class method) |
| `X`  | Constant/Input node (string, int, float, bool, file, tuple, etc.) |
| `O`  | Output nodes (for editor only) |

### Example (excerpt)

```json
{
  "id": "F:load_image@1",
  "type": "F",
  "data": {
    "name": "load_image",
    "inputPorts": ["path"],
    "outputPorts": ["returns"]
  }
}
```

### Connections

```json
{
  "source": "F:resize_image@2",
  "sourceHandle": "returns",
  "target": "F:grayscale@3",
  "targetHandle": "img"
}
```

This means:  
`resize_image(...).returns` → feeds into → `grayscale(img=...)`

---

## From Editor to Execution

When you hit **"Start"** in the Typeflow Editor:

1. The frontend sends `dag.json` to the **FastAPI backend**  
2. The backend validates and compiles it:  
   - Builds adjacency lists (`adj_list.json`, `rev_adj_list.json`)  
   - Extracts all constants and file inputs (`io.json`)  
3. Generates a runnable Python orchestrator at `src/orchestrator.py`  
4. Executes it **asynchronously** via FastAPI subprocess  
5. Streams progress live via **Server-Sent Events (SSE)**

---

## Compilation Process

When you run:

```bash
typeflow compile
```

Here’s what happens step-by-step:

1. Typeflow reads `.typeflow/dag.json`  
2. Builds internal adjacency lists  
3. Validates type links (shows warnings for mismatches)  
4. Saves compiled data into `.typeflow/compiled/`  
5. Prepares everything for orchestration  

### Example Output

```text
Compiling graph...
Extracted 9 I/O nodes and saved to .typeflow\compiled\io.json
Saved compiled adjacency lists under .typeflow/compiled/
Type mismatch: X:tuple_val@6:val (tuple) → C:Watermark@1:position (tuple[int, int])
Workflow compiled but with some validation warnings.
```

---

## Generation & Execution

After a successful compile:

```bash
typeflow generate
```

This command generates:

```text
src/orchestrator.py
```

**Example Output:**

```text
Generating orchestrator script...
Orchestrator generated at: src/orchestrator.py
```

### Inside `orchestrator.py`

```python
from src.classes.Watermark import Watermark
from src.nodes.load_image.main import load_image
from src.nodes.resize_image.main import resize_image
from src.nodes.grayscale.main import grayscale
from src.nodes.adjust_brightness.main import adjust_brightness

file_input_1 = 'data/X_file_input_1.jpg'
load_image_out = load_image(path=file_input_1)
resize_image_out = resize_image(img=load_image_out, size=(400,400))
grayscale_out = grayscale(img=resize_image_out)
adjust_brightness_out = adjust_brightness(img=grayscale_out, factor=1.2)
watermark_1 = Watermark(text="Typeflow", position=(20,20), opacity=128, font_size=24)
watermark_1_apply_out = watermark_1.apply(img=adjust_brightness_out)
```

When you run:

```bash
typeflow run
```

Typeflow executes this orchestrator step-by-step, showing live progress (or streaming via SSE if in editor).

---

## Validation Rules

During `compile`, Typeflow enforces checks for:

- Graph connectivity  
- Node input/output matching  
- Type compatibility  
- Dangling or unused inputs  
- Circular dependencies (**disallowed**)  

Warnings are printed for soft mismatches, but the graph still runs unless a structural error occurs.

---

## Execution via Editor (SSE)

When workflows are executed from the visual editor:

- The backend starts a subprocess for the orchestrator  
- Every node completion emits an event:

```json
{
  "event": "node_complete",
  "node_id": "F:grayscale@3",
  "status": "done"
}
```

- The frontend updates node status **visually in real time**  
- All events delivered as **Server-Sent Events (SSE)** streams

---

## Summary

| Phase             | Command               | Description                                  |
|-------------------|-----------------------|----------------------------------------------|
| Project setup     | `typeflow setup`      | Create workflow base project                 |
| DAG authoring     | — (via Editor)        | Build visual graph                           |
| Compilation       | `typeflow compile`    | Parse & validate graph                       |
| Generation        | `typeflow generate`   | Build executable orchestrator                |
| Execution         | `typeflow run`        | Run workflow or stream via editor            |

---

## Notes

- You can safely **re-compile** and **re-generate** after any node or graph modification  
- All compilation data lives under `.typeflow/compiled/`  
- Workflows are **deterministic** — identical DAGs always produce identical orchestrators  
- The editor is fully decoupled: you can build the same DAG via JSON manually if desired  

---

## Next Steps

- Learn how to create custom nodes  
- Define stateful logic with node classes  
- Manage your project lifecycle using the [CLI guide](./cli.md)  

---
