# Class Node Guide

Class nodes encapsulate **stateful or reusable logic**.  
They are perfect for tasks that need **persistent attributes** or **configuration** across multiple steps in a workflow.

---

## Structure

Each class node lives under:

```
src/classes/<ClassName>.py
```

A class node is defined using the **`@node_class` decorator**.

---

## Simple Class Example

```python
from typeflow import node_class
from PIL import Image, ImageFilter

@node_class
class BlurFilter:
    radius: float = 2.5

    def apply(self, img: Image.Image) -> Image.Image:
        """Apply a Gaussian blur."""
        return img.filter(ImageFilter.GaussianBlur(self.radius))
```

### Notes:

- `@node_class` **automatically creates `__init__`** to populate class fields  
- **Do not define `__init__` manually** — only use typed fields  
- Methods like `.apply()` become **nodes in the editor**  
- Dunder methods (`__str__`, `__repr__`, etc.) are **ignored** by compiler and editor  

---

## Class Lifecycle

```bash
# 1. Create class scaffold
typeflow create-class BlurFilter

# 2. Edit the file
# → src/classes/BlurFilter.py

# 3. Validate class
typeflow validate class BlurFilter

# 4. Use inside editor or DAG
```

---

## Complex Class Example — Single File

```python
from typeflow import node_class
from typing import List
import math

@node_class
class StatsProcessor:
    data: List[float]

    def mean(self) -> float:
        """Return the arithmetic mean."""
        return sum(self.data) / len(self.data) if self.data else 0.0

    def variance(self) -> float:
        """Return the variance."""
        m = self.mean()
        return sum((x - m) ** 2 for x in self.data) / len(self.data) if self.data else 0.0

    def stddev(self) -> float:
        """Return the standard deviation."""
        return math.sqrt(self.variance())
```

### Developer Notes

- **Fields** → become inputs when instantiating the class node  
- **Methods** → treated as **function nodes** in the editor  
- Always use **type hints and docstrings** → enables metadata & validation  
- Keep logic **deterministic**; avoid I/O or global state  
- Complex helper logic can be written **in-file** as private/static functions  

---

## Type and Validation Notes

| Requirement                  | Details |
|-----------------------------|--------|
| **Fields**                  | Must be type-annotated class attributes |
| **Methods**                 | Must annotate all inputs and outputs |
| **Supported types**         | `int`, `float`, `str`, `bool`, `list`, `tuple`, `dict`, `Callable`, `Any` |
| **Advanced types**          | `TypedDict`, `TypedTuple` allowed but **limited validation** |

**Validate your class:**

```bash
typeflow validate class StatsProcessor
```

---

## Best Practices

| Do | Avoid |
|------|----------|
| Keep class nodes **focused** — one responsibility | Overloading with unrelated logic |
| Use **methods** for complex logic | Heavy work in field defaults |
| **Dunder & private attrs** (`_var`) ignored in DAG | Using them for workflow logic |
| Write **docstrings for every method** | Missing tooltips in editor |
| Use **single file** for moderate complexity | Premature `utils/` folders |

---

## Rocket Summary

| Command                            | Description |
|------------------------------------|-------------|
| `typeflow create-class <name>`     | Scaffold a new class node |
| `typeflow validate class <name>`   | Validate fields and methods |
| `typeflow compile`                 | Build workflow DAG |
| `typeflow generate`                | Create orchestrator script |
| `typeflow run`                     | Execute compiled workflow |

---

## Next Steps

After class nodes are ready, combine them with function nodes in the editor to orchestrate workflows.

See **[editor.md](./editor.md)** for instructions on connecting nodes and building DAGs visually.

---
