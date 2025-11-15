# Class Node Guide

Class nodes are one of the most powerful parts of **Typeflow**.  
Unlike typical workflow systems that only pass plain data, Typeflow lets you work with **actual Python objects** — **instantiated, passed around, accessed, and used visually**.

A class node represents a **real object instance** inside the workflow graph.  
You can:

- Instantiate objects  
- Receive objects returned by other nodes  
- Access object fields  
- Call object methods  
- Pass objects to functions or other class nodes  

This makes Typeflow a true **visual object-oriented programming system**.

---

## 1. Creating a Class Node

Every class node lives under:

```plain
src/classes/<ClassName>.py
```

Created using:

```bash
typeflow create-class MyClass
```

A class node uses the **`@node_class` decorator**.

### Example

```python
from typeflow import node_class

@node_class
class BlurFilter:
    radius: float = 2.5

    def apply(self, img):
        """Apply blur using configured radius."""
        # implementation
        ...
```

**Note**: When you want different objects, then just drag another class node. Each class node in editor is a unique object instance. If you want to have different object, just drag more class nodes.

---

## 2. How Class Nodes Actually Work

Understanding this unlocks the real power of Typeflow.

### 2.1 Class Node = Instance of a Class

When you **drag a class node into the editor**, you're not placing a class definition.  
You’re placing an **object instance**.

- **Left-side ports** = constructor inputs  
  These populate class fields — essentially calling:

  ```python
  obj = BlurFilter(radius=2.5)
  ```

- **Right-side ports** = field outputs  
  You can pass these fields to other nodes:

  ```plain
  obj.radius → next_node.input
  ```

---

### 3. Passing Objects (Self Ports)

Every class node has **two special ports** for passing entire objects:

#### **self input port**

Use this when a function returns an object of the same class.

```plain
(SomeFunction returns UserProfile)
        ↓
UserProfile class node (self port)
```

**Meaning**:  
"Use the returned object instance for this class node."  
Conceptually like **assignment** or a **copy constructor** in OOP.

#### **self output port**

Use this to pass the **entire object instance** to another node:

```plain
UserProfile.self → ValidateUser(input=obj)
```

---

### 4. Calling Methods (Subnodes)

When you **double-click** a class node, a **mini method-toolbar** appears (not in the sidebar).  
Clicking a method creates an **M-node (method node)**, visually connected to the class:

```plain
[Class Node] --self--> [Method Node]
```

Method nodes work **exactly like function nodes**:

- Take inputs  
- Take `self`  
- Output return value  

The backend treats method nodes as **class-method calls**:

```python
obj.method(...)
```

---

## 5. Full Example — Easy to Understand

Let’s build a simple `Counter` class.

```python
from typeflow import node_class

@node_class
class Counter:
    start: int = 0

    def increment(self, step: int = 1) -> int:
        """Return start + step."""
        return self.start + step

    def double(self) -> int:
        """Return start * 2."""
        return self.start * 2
```

### In the Editor

#### Step 1: Instantiate it

```plain
[start] → (Counter)
```

This constructs:

```python
counter_obj = Counter(start=value)
```

#### Step 2: Use method nodes

```plain
Counter.start → other_node
Counter.double → other_node
Counter.increment → other_node
```

Each is:

```python
counter_obj.double()
counter_obj.increment(step)
```

#### Step 3: Use objects returned by functions

If a function returns a new `Counter` object, connect it to `.self`:

```plain
build_counter() → Counter.self
```

**Meaning**:

```python
counter_obj = build_counter()
```

---

## 6. Advanced Example – Object Flow

```python
from typeflow import node_class

@node_class
class TextBox:
    text: str
    width: int
    height: int

    def summary(self) -> str:
        return f"{self.text} ({self.width}x{self.height})"
```

Create two `TextBox` nodes:

```plain
[text] → TB1 ← [width] [height]
```

Call method:

```plain
TB1.self → TB1.summary → Output
```

Receive object from somewhere else:

```plain
GenerateSizes() → TB2.self
[text] → TB2
```

This uses the **returned object** for all methods and field access.

---

## 7. Important Rules & Notes

| Rule | Requirement |
|------|-------------|
| **Do NOT define `__init__`** | Typeflow generates it automatically from typed fields |
| **Dunder methods are ignored** | `__repr__`, `__str__`, `__hash__`, etc. — don’t appear as nodes or fields |
| **Type hints are required** | Both fields and methods must be typed |
| **Complex logic allowed** | Everything inside methods is just Python |
| **One class = one file** | Avoid splitting unless necessary |

---

## 8. Supported Use Cases

Class nodes let you model:

- Processing pipelines with **internal state**  
- **Configurable reusable logic**  
- **Multi-method tools** (like a mini SDK)  
- **Agent states** (memory, persona, goals)  
- **Structured AI prompts**  
- **Runtime objects** like Images, Models, DB clients  
- **ANY Python class** with pure logic  

> **Typeflow class nodes make workflows feel like visual OOP.**

---

## 9. Validation

Validate class definition:

```bash
typeflow validate class MyClass
```

This ensures:

- Fields are typed  
- Methods are typed  
- Docstrings exist  
- Class can be instantiated  

---

## 10. Developer Notes

| Concept | Meaning |
|--------|--------|
| **Fields** | Inputs & outputs (constructor & getters) |
| **Methods** | Extra nodes in canvas |
| **self input** | Use an existing instance |
| **self output** | Pass object to another node |
| **Instance flow** | Full object can travel through workflow |

---

## 11. Summary

**Class nodes** allow you to define **rich, stateful, object-oriented logic** in Typeflow.  
You can:

- Instantiate classes  
- Call methods  
- Pass objects around  
- Build entire systems **visually**

This is **one of the most unique features of Typeflow** — not found in **n8n, Node-RED, Airflow, LangChain**, or any standard workflow tool.

---

## Next Steps

Once you understand class nodes, combine them with **function nodes** to build **powerful visual pipelines**.

See **[editor.md](./editor.md)** to learn how to connect class nodes inside the editor.

---
