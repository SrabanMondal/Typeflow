# Node Definition Guide

Nodes are the **building blocks** of Typeflow workflows.  
Each node represents a **single logical step** that transforms inputs into outputs — from simple data operations to complex modular processes.

---

## Node Basics

Every node lives under:

```plain
src/nodes/<node_name>/main.py
```

Each node is a **function decorated with `@node()`**.

### Example — Simple Node

```python
from typeflow import node

@node()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers and return the sum."""
    return a + b
```

When validated, this node automatically:

- Registers itself as a Typeflow node  
- Becomes available in the **visual editor**  
- Is validated by the compiler  
- Is included in **DAGs and orchestrator generation**

---

## Node Lifecycle

```bash
# 1. Create node scaffold
typeflow create-node add_numbers

# 2. Edit the function
# → src/nodes/add_numbers/main.py

# 3. Validate node
typeflow validate node add_numbers

# 4. Use inside editor or compile DAG
```

---

## Decorator: `@node()`

The `@node()` decorator handles:

| Responsibility               | Description |
|-----------------------------|-----------|
| **Function registration**    | Adds node to Typeflow registry |
| **Type extraction**          | Parses input/output types for validation |
| **Metadata generation**      | Saves node info to `.typeflow/` |
| **Editor exposure**          | Makes node visible in UI |

Each `@node()`-decorated function becomes part of the **workflow ecosystem**.

---

## Node Function Rules

| Rule                                 | Description |
|--------------------------------------|-------------|
| **Type hints are mandatory**         | Every argument and return must have a type annotation |
| **Docstring is required**            | Displayed in the editor tooltip |
| **Function name = Node name**        | Use `lowercase_with_underscores` |
| **Return exactly one output**        | Multi-output nodes coming in future versions |
| **Keep functions pure**              | Avoid global state or external mutations |
| **Use standard types**               | `int`, `float`, `str`, `bool`, `tuple`, `list`, `dict`, `Callable`, `Any`, `Class` supported |

**Note**: If you want to reuse function in multiple places, then don't use the same node, drag more nodes of same function into editor, and use them to different areas. Each function nodes even if same produces different(unique) outputs, so you can run the function with different inputs multiple times and get different output. So each node take **single input per input port**.

---

## Example: Image Resize Node

```python
from typeflow import node
from PIL import Image
from typing import Tuple

@node()
def resize_image(
    img: Image.Image,
    size: Tuple[int, int],
    keep_aspect: bool = True
) -> Image.Image:
    """Resize or thumbnail an image."""
    if keep_aspect:
        img.thumbnail(size)
        return img
    return img.resize(size)
```

**Validation:**

```bash
typeflow validate node resize_image
```

**Output:**

```text
Node validated successfully
```

---

## Brain Complex Node Example — Modular Logic

Let’s create a node that **cleans text** by removing stopwords, lowercasing, and optionally applying stemming.

### Step 1: Create Node

```bash
typeflow create-node text_cleaner
```

Generates:

```text
src/nodes/text_cleaner/
   └── main.py
```

### Step 2: Add `utils/` Folder

```text
src/nodes/text_cleaner/
   ├── main.py
   └── utils/
       ├── __init__.py
       ├── normalize.py
       └── stemmer.py
```

### Step 3: Implement Utilities

**`utils/normalize.py`**

```python
import re
from typing import List

def normalize_text(text: str) -> str:
    """Lowercase and remove non-alphanumeric characters."""
    return re.sub(r"[^a-z0-9\s]", "", text.lower())
```

**`utils/stemmer.py`**

```python
from typing import List
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def apply_stemming(words: List[str]) -> List[str]:
    """Apply stemming to a list of words."""
    return [stemmer.stem(w) for w in words]
```

### Step 4: Connect in `main.py`

```python
from typeflow import node
from typing import List
from .utils.normalize import normalize_text
from .utils.stemmer import apply_stemming

STOPWORDS = {"the", "is", "and", "to", "of"}

@node()
def text_cleaner(text: str, apply_stem: bool = False) -> List[str]:
    """Clean raw text by removing stopwords and applying stemming."""
    normalized = normalize_text(text)
    words = [w for w in normalized.split() if w not in STOPWORDS]
    return apply_stemming(words) if apply_stem else words
```

---

## Puzzle Typeflow Type System Notes

- Always annotate **every input and output**  
- Supported types:  
  - `int`, `float`, `str`, `bool`  
  - `tuple`, `list`, `dict`  
  - `Callable`, `Any`  
- Advanced types (`TypedDict`, `TypedTuple`) can be used for **IDE clarity**  
  - But **not yet registered** in Typeflow’s internal type registry  

---

## Gear Validation & Registration

```bash
typeflow validate node text_cleaner
```

The node now appears in the **Typeflow Editor sidebar** and is ready for workflow design.

---

## Light Bulb Best Practices

| Do | Avoid |
|------|----------|
| Write **short, self-contained nodes** | Overly complex logic in one node |
| Use `utils/` for **reusable logic** | Duplicated code across nodes |
| Use **descriptive docstrings & names** | Vague or cryptic naming |
| Keep nodes **deterministic** | Side effects or I/O inside nodes |
| **Test nodes independently** | Rely only on DAG testing |

---

## Rocket Summary

| Command                          | Description |
|----------------------------------|-------------|
| `typeflow create-node <name>`    | Create new node scaffold |
| `typeflow validate node <name>`  | Validate node’s types and metadata |
| `typeflow compile`               | Build workflow DAG |
| `typeflow generate`              | Create orchestrator script |
| `typeflow run`                   | Execute compiled workflow |

---

## Next Steps

You can now create **Class Nodes** to group related functions and maintain state across multiple nodes.

See **[class.md](./classes.md)** for the next section of the developer guide.

---
