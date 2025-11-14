# Typeflow CLI

Typeflow ships with a powerful CLI that manages your entire workflow lifecycle —  
from setup and dependency management to validation, compilation, generation, and execution. (*deplpyment coming soon*)

The CLI is installed automatically when you install the package:

```bash
pip install typeflowapp
```

---

## Overview

The `typeflow` CLI is designed to make workflow projects **self-contained and reproducible**.  
It can:

- Create isolated environments automatically using `uv`.
- Install and manage workflow dependencies  
- Validate your DAG structure  
- Graph Compiler compiles your DAG json into a python script.
- Run workflows locally or via the visual editor  

---

## Command Summary

| Command                        | Description                                                                         |
|--------------------------------|-------------------------------------------------------------------------------------|
| `typeflow setup`               | Initializes a new Typeflow project with virtual environment and `uv` integration    |
| `typeflow add <package>`       | Adds a dependency to the workflow using `uv`                                        |
| `typeflow install`             | Installs dependencies and sets up venv for existing workflows                       |
| `typeflow validate`            | Validates the `workflow.yaml` and DAG structure                                     |
| `typeflow compile`             | Compiles DAG (from `.typeflow/dag.json`) to internal adjacency data                 |
| `typeflow generate`            | Generates executable orchestrator script at `src/orchestrator.py`                   |
| `typeflow run`                 | Runs the compiled workflow synchronously                                            |
| `typeflow create-node <name>`  | Creates a node folder with `name` under src/nodes with main.py where you define your function |
| `typeflow create-class <name>` | Creates a class file with `name` under src/classes where you define your class |

---

## Commands in Detail

### `typeflow setup`

Creates a new Typeflow project in the current directory.

**What it does:**

- Initializes a `.typeflow/` folder  
- Creates a `uv` project  
- Installs and pins dependencies  
- Creates a local virtual environment under the project root  

```bash
typeflow setup
```

**Example output:**

```text
Creating isolated Typeflow project...
Virtual environment created under .venv
Added 'typeflow' to project dependencies
Next: cd into project root and activate your venv
```

---

### `typeflow add <package>`

Adds an external dependency to your workflow.

```bash
typeflow add pillow
```

Under the hood, this uses `uv` to install and record the dependency in your project’s metadata.

---

### `typeflow install`

Used when you’ve cloned an existing Typeflow project (with `.typeflow` and `workflow.yaml` present).

```bash
typeflow install
```

It will:
- Ensure `.venv` exists (create if missing)  
- Install all listed dependencies  
- Verify environment setup  
- Guide you to activate venv and proceed  

**Example output:**

```text
Checking environment...
Virtual environment found
Installing dependencies...
All dependencies installed
Next: run 'typeflow validate' and 'typeflow compile'
```

---

### `typeflow validate`

Scans the project structure, ensuring that:
- `workflow.yaml` exists  
- All declared nodes and classes are discoverable  
- DAG consistency can be checked  

```bash
typeflow validate
```

**Example output:**

```text
Validating workflow...
workflow.yaml found
All nodes and classes resolved
```

---

### `typeflow compile`

This is where your graph starts taking shape.  
`compile` parses the `dag.json` file (usually generated from the visual editor) and extracts valid nodes, connections, and data types.

```bash
typeflow compile
```

**Example output:**

```text
Compiling graph...
Extracted 9 I/O nodes and saved to .typeflow\compiled\io.json
Saved compiled adjacency lists under .typeflow/compiled/
Validating graph edges...
Edge valid: F:load_image@1:returns → F:resize_image@2:img
Edge valid: X:file_input@1:val → F:load_image@1:path
Type mismatch: X:tuple_val@3:val (tuple) → F:resize_image@2:size (tuple[int, int])
Edge valid: C:Watermark@1:apply@2:returns → F:save_image@1:img
Workflow compiled but with some validation warnings. You can still run it.
```

---

### `typeflow generate`

Reads the compiled adjacency data and creates an executable orchestrator script.

```bash
typeflow generate
```

**Example output:**

```text
Generating orchestrator script...
Orchestrator generated at: src/orchestrator.py
```

This file contains the exact sequence of node calls derived from your DAG.  
It is ready to be executed manually or via `typeflow run`.

---

### `typeflow run`

Executes your compiled workflow.

```bash
typeflow run
```

If the workflow is launched from the Editor, this command is executed **asynchronously via FastAPI**, with real-time SSE updates streamed to the frontend.

---

## Workflow Lifecycle Example

Here’s the complete flow for a sample project:

```bash
# 1. Setup new project
typeflow setup

# 2. Validate structure
typeflow validate

# 3. Compile graph (from dag.json)
typeflow compile

# 4. Generate orchestrator
typeflow generate

# 5. Run the workflow
typeflow run
```

**Expected file structure after generation:**

```text
my_app/
│
├── .typeflow/
├── src/
│   └──nodes/
│   └──classes/
│   └── orchestrator.py
├── workflow/
│     └── workflow.yaml
│     └──dag.json
├── data/
├── .gitignore
├── README.md
├── pyproject.toml
├── uv.lock
└── .venv/
```

---

## Tips & Notes

- You can re-run `typeflow compile` anytime after modifying your DAG in the editor.  
- Future versions will support **async nodes** and **looping workflows**.  
- Use `typeflow add <package>` instead of manually editing dependencies.  
- The CLI aims to make your workflow **reproducible, portable, isolated, and explainable**.  

---

## Developer Notes

Internally, `typeflow compile` and `typeflow generate` rely on:

- `.typeflow/dag.json` for node topology  
- `workflow.yaml` for metadata  
- Dynamic writing of the orchestrator using **topological order** of connected nodes  

The resulting `src/orchestrator.py` serves as a **fully generated runnable graph script**.
You can manually write the script from your project root by using `python -m src.orchestrator`

---
