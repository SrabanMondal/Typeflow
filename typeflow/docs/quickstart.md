# Quickstart Guide

Welcome to **Typeflow** — a **visual workflow engine** for Python that lets you **design, connect, and execute** logic nodes in an **explainable visual environment**.

This quickstart walks you through building your **first simple data-processing workflow** — **end-to-end**.

---

## 1. Installation

Install Typeflow globally:

```bash
pip install typeflowapp
```

---

## 2. Setup a New Project

Create a new **isolated Typeflow project**:

```bash
typeflow setup my_project
```

This will:

- Create a new folder: `my_project/`  
- Initialize a local `.venv` using **uv**  
- Install Typeflow inside that **isolated environment**

Then, **activate** your environment:

```bash
cd my_project
. .venv/bin/activate        # macOS / Linux
# or
.\.venv\Scripts\activate    # Windows PowerShell
```

> You’re now ready to create your first workflow.

---

## 3. Add a Dependency *(Optional)*

If your nodes need external packages, add them using:

```bash
typeflow add requests
```

This ensures dependencies are added **directly into your project’s isolated environment**.

---

## 4. Create a Node

Let’s create a simple **text utility node** that counts words in a string.

```bash
typeflow create-node word_counter
```

This creates:

```text
src/nodes/word_counter/main.py
```

Now **edit the file**:

```python
from typeflow import node

@node()
def word_counter(text: str) -> int:
    """Count the number of words in a given text."""
    return len(text.split())
```

> **Tip**: Always use **type hints** and a **docstring** — they appear in the **visual editor** and improve **validation**.

---

## 5. Create a Class Node

Class nodes are **stateful** — ideal for **reusable logic** or **configuration**.

```bash
typeflow create-class TextFormatter
```

Then open:

```plain
src/classes/TextFormatter.py
```

Replace its content with:

```python
from typeflow import node_class

@node_class
class TextFormatter:
    prefix: str = ""
    suffix: str = ""

    def format(self, text: str) -> str:
        """Add prefix and suffix to a given text."""
        return f"{self.prefix} {text} {self.suffix}"
```

---

## 6. Validate Nodes & Classes

Before using them, **validate**:

```bash
typeflow validate node
typeflow validate class
```

You should see:

```text
All nodes and classes validated successfully.
```

This ensures everything is correctly registered in `.typeflow/`.

---

## 7. Open the Visual Editor

Launch the editor:

```bash
typeflow start-ui
```

Typeflow starts a **FastAPI server** that serves the **Next.js React Flow UI** at:

**`http://localhost:3001`**

<!-- Placeholder Image -->
![Typeflow Editor Home](../assets/emptyEditor.png)  
*Caption: The visual workflow editor with node sidebar and canvas.*

Now you can:

- Drag your `word_counter` and `TextFormatter` nodes from the **sidebar**  
- Connect them **visually**  
- Add an **Input Node** and an **Output Node**  
- Use sidebar tabs: **Input / Function / Class / Output**

**Note**: Double-click on TextFormatter node to see list of methods and click it to add method node in editor. Double click again to hide the list.

<!-- Placeholder Image -->
![Connected Workflow Example](../assets/dag.png)  
*Caption: “Input string val → TextFormatter.format → WordCounter → Output text output” workflow.*

Once you have built a similar DAG. Now you can input something in string_val. Then click on **Export** button.

---

## 8. Compile and Generate

Once your **DAG (graph)** is exported. You can stop the fastapi server or use another terminal to compile and generate its **runnable orchestrator script**:

```bash
typeflow compile
typeflow generate
```

You’ll see:

```text
Validating DAG...

Generating orchestrator script...
Orchestrator generated at: src/orchestrator.py
```

---

## 9. Run the Workflow

You can run it in **two ways**:

### A. From the Editor

Click the **Start button** on the top bar.  
This triggers **live execution** with **real-time SSE updates**.

As the nodes run, you’ll see progress **streaming in the editor console**.

<!-- Placeholder Image -->
![Live Execution Preview](../assets/executed.png)  
*Caption: Live workflow execution updates via SSE inside the editor.*

**Note**: When you run from editor, you don't need to run compile and generate commands at terminal. **Start** button will take the dag, compile, generate and run for you. You can just watch your workflow being compiled. And iterate over it, change inputs and see live run.

### A. From Terminal

```bash
typeflow run
```

Runs the orchestrator (`python -m src.orchestrator`).

**Note**: If you want to run from terminal, and want to see the output in terminal like you saw in editor. You need to replace the Output node of editor with your custom node that takes the integer return of `word_counter` and prints in console/terminal. Then go back in editor, refresh it, to see that node added in Functions Sidebar tab, drag it and connect: `word_count:returns`->`console:input`. (*Assuming your custom node name is console that takes input arg and prints in terminal*)

---

## 10. Output

Your **Output Node** displays results **directly inside the editor**.

Connect your nodes like this:

```text
Input Text → TextFormatter.format → WordCounter → Output
```

Run it with:

```text
Input: "Typeflow makes visual programming fun"
```

**Output:**

```text
Word Count: 5
```

---

## You’ve Built Your First Workflow

You just:

1. Created a Typeflow project  
2. Added **custom nodes**  
3. Validated and **visualized** them  
4. Compiled a **DAG**  
5. Executed it **live** with **SSE-powered updates**

---

## Next Steps

- Check out **[examples.md](./examples.md)** for a more advanced **image-processing pipeline**  
- Explore **Node Definition Guide** and **Class Node Guide**  

---
