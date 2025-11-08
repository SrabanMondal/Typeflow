# 🌀 TypeFlow

# tasks
## backend
- type fix for input/output nodes
- event check on sse event jsons print
## frontend
- ui for events
- input file/img upload - passing path string
- X to I type symbol for input
- output img receive check
## next
- dependency management
- async

**Composable, Type-Safe, Reproducible Python Workflows.**

TypeFlow is a modular low-code framework for building, managing, and executing Python workflows through a visual editor and CLI.  
It brings together **declarative workflow definitions**, **auto-managed environments**, and **typed DAG compilation** — ensuring your pipelines are both **reproducible** and **type-safe**.

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 🧩 **Node-based architecture** | Each function or class is a modular, reusable node. |
| 🧠 **Auto type inference** | Input/output ports inferred from Python type hints. |
| 📦 **Dependency management via `uv`** | Reproducible Python environments with lockfiles. |
| 🔄 **Workflow manifest** | Declarative YAML-based metadata tracking all nodes & dependencies. |
| 🔍 **Type-safe DAG compiler** | Validates compatible input/output types before execution. |
| 🖥️ **Integrated UI + CLI** | Visual editor for designing workflows, powered by a FastAPI backend. |
| 💾 **Hidden `.typeflow` build system** | Stores node manifests, compiled scripts, cache, etc. |
| 🌐 **Public & private nodes** | Supports reusable and shareable nodes. |
| ⚙️ **Reproducibility-first** | Workflows can be cloned, locked, and replayed anywhere. |

---

## 🧭 Quick Start

### 0. Install TypeFlow
```bash
pip install typeflow
```

### 1️⃣ Initialize a new workflow
```bash
typeflow init workflow
```

This creates:

```
workflow/
├── workflow.yaml
├── dag.json
├── uv.lock
└── .typeflow/
```

### 2️⃣ Create a new node
```bash
typeflow create node text_clean
```

Generates:

```
nodes/
└── text_clean/
    ├── main.py
    └── test_text_clean.py
```

Edit `main.py` and use the `@node` decorator:

```python
from typeflow import node

@node
def text_clean(text: str) -> str:
    return text.strip().lower()
```

### 3️⃣ Validate & Track the Node
```bash
typeflow validate node text_clean
```

This:
- Extracts type hints
- Generates node manifest YAML
- Updates `workflow.yaml`

### 4️⃣ Build the Workflow
```bash
typeflow compile
```

Compiles the DAG from `dag.json` (created via UI).  
Ensures all types match.  
Generates a reproducible workflow script in `.typeflow/build/`.

> Use the visual editor to create `dag.json` — see next step.

### 5️⃣ Start the UI
```bash
typeflow start ui
```

Launches FastAPI server at [`http://localhost:3000`](http://localhost:3000)

Serves:
- Visual editor (Next.js static export)
- API endpoints:
  - `/api` → Fetch all nodes (`yaml` → `json`)
  - `/api/dag` → Load `dag.json`
  - `/api/save` → Save modified DAG from UI

---

## 🧩 Workflow Manifest Example (`workflow.yaml`)

```yaml
name: sample-workflow
python: "3.11"
dependencies:
  - pandas
  - requests
nodes:
  - text_clean
  - console
```

---

## 🧠 Design Philosophy

> **“Every workflow should be human-readable, type-safe, and reproducible — without writing boilerplate orchestration code.”**

TypeFlow bridges **traditional scripting** and **visual workflow authoring**, making it easy to:

- Convert any Python function or class into a typed node  
- Visually connect nodes into DAGs  
- Compile and run with **guaranteed reproducibility**

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a feature branch
3. Submit a Pull Request

We especially love:
- New node templates
- DAG validators
- UI improvements
- Performance optimizations

---

## 🧾 License

**MIT License** © 2025 TypeFlow

---

**TypeFlow** — *Where code meets clarity, and pipelines never break.*