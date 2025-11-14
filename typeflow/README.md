# Typeflow

**Typeflow** is a **visual, type-safe workflow engine** for Python.  
It turns your **Python functions and classes** into **reusable visual nodes** that can be connected to build **complete systems**.

You **design workflows visually** — Typeflow **generates the orchestrator** and **runs it with full type validation**.

---

## Features

| Feature | Description |
|--------|-------------|
| **Visual DAG editor** | React Flow UI served **locally** |
| **Type-safe nodes** | `@node()` and `@node_class` decorators |
| **Deterministic lifecycle** | `compile → generate → run` |
| **Live execution** | Real-time updates via **Server-Sent Events (SSE)** |
| **Auto orchestrator** | Generates `src/orchestrator.py` |
| **Isolated dependencies** | Project-level `.venv` via **uv** |
| **Python-first** | No external server or cloud required |
| **Fully offline** | Pure local development |

---

## Installation

```bash
pip install typeflowapp
```

---

## Quickstart

### 1. Create a new project

```bash
typeflow setup my_project
cd my_project
source .venv/bin/activate    # macOS/Linux
# or
.\.venv\Scripts\activate     # Windows
```

### 2. Create your first node

```bash
typeflow create-node word_counter
```

Edit `src/nodes/word_counter/main.py`:

```python
from typeflow import node

@node()
def word_counter(text: str) -> int:
    """Count words in a string."""
    return len(text.split())
```

### 3. Create a class node

```bash
typeflow create-class TextFormatter
```

Edit `src/classes/TextFormatter.py`:

```python
from typeflow import node_class

@node_class
class TextFormatter:
    prefix: str = ""
    suffix: str = ""

    def format(self, text: str) -> str:
        """Apply prefix and suffix."""
        return f"{self.prefix}{text}{self.suffix}"
```

### 4. Validate all nodes

```bash
typeflow validate
```

### 5. Open the visual editor

```bash
typeflow start-ui
```

Navigate to: [http://localhost:8000](http://localhost:8000)

### 6. Build your workflow

Drag and connect:

```
Input → TextFormatter.format → word_counter → Output
```

### 7. Compile, generate, and run

```bash
typeflow compile
typeflow generate
typeflow run
```

This builds and executes the orchestrator at `src/orchestrator.py`.

---

## Documentation

Complete documentation, examples, and guides are available at:

[https://typeflow.dev](https://typeflow.dev) *(replace with your hosted MkDocs URL)*

---

## Why Typeflow?

- Brings **structure, clarity, and determinism** to workflow creation  
- Makes **Python functions/classes visually orchestratable**  
- Encourages **modular, strongly typed design**  
- **Future-ready** for **AI-assisted node generation**  
- Ideal for:  
  - Data pipelines  
  - ETL  
  - Automation  
  - ML preprocessing  
  - AI agents  

---

## Contributing

Contributions are **welcome**!  
See [`CONTRIBUTING.md`](./docs/contributing.md) or See Contributing from hosted Documentation for details on:

- Development workflow  
- Testing standards  
- Area ownership  

---

## License

Licensed under the **GNU General Public License**.

---

