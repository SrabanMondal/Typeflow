# ⚡ Quickstart — Build an Image Workflow

Let’s build a **real image processing pipeline** using Typeflow.  
In this tutorial, we’ll build a workflow that:

> loads an image → resizes it → converts to grayscale → adjusts brightness → applies watermark → saves the result

All of this will be designed visually in the Typeflow editor and executed deterministically through Python.

---

## 1️⃣ Create a New Project

```bash
typeflow setup imageflow
cd imageflow
```

This scaffolds your project with a virtual environment and structure like:

```plain
imageflow/
├── .typeflow/
├── src/
│   ├── nodes/
│   ├── classes/
│   └── __init__.py
├── workflow/
│   ├── workflow.yaml
│   └── dag.json
├── pyproject.toml
├── .gitignore
└── README.md
```

Then activate your virtual environment (created automatically by Typeflow):

```bash
source .venv/bin/activate   # or .\.venv\Scripts\activate on Windows
```

## 2️⃣ Add Required Dependency

We’ll need Pillow for image operations.

```bash
typeflow add pillow
```

## 3️⃣ Create Function Nodes

We’ll define five simple nodes for image transformations.  
Each node has its own folder under `src/nodes/` with a `main.py` file.

### 🧩 load_image

```bash
typeflow create-node load_image
```

Then open `src/nodes/load_image/main.py`:

```python
from typeflow import node
from PIL import Image

@node()
def load_image(path: str) -> Image.Image:
    """Load image from a given path."""
    img = Image.open(path).convert("RGBA")
    return img
```

### 🧩 resize_image

```bash
typeflow create-node resize_image
```

Edit `src/nodes/resize_image/main.py`:

```python
from typeflow import node
from PIL import Image
from typing import Tuple

@node()
def resize_image(img: Image.Image, size: Tuple[int, int], keep_aspect: bool = True) -> Image.Image:
    """Resize or thumbnail the image."""
    if keep_aspect:
        img.thumbnail(size)
        return img
    return img.resize(size)
```

### 🧩 grayscale

```bash
typeflow create-node grayscale
```

```python
from typeflow import node
from PIL import Image

@node()
def grayscale(img: Image.Image) -> Image.Image:
    """Convert to grayscale while keeping RGBA mode."""
    return img.convert("L").convert("RGBA")
```

### 🧩 adjust_brightness

```bash
typeflow create-node adjust_brightness
```

```python
from typeflow import node
from PIL import Image, ImageEnhance

@node()
def adjust_brightness(img: Image.Image, factor: float) -> Image.Image:
    """Adjust image brightness."""
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)
```

### 🧩 save_image

```bash
typeflow create-node save_image
```

```python
from typeflow import node
from PIL import Image

@node()
def save_image(img: Image.Image, output_path: str) -> None:
    """Save image to a given path."""
    img.save(output_path)
```

## 4️⃣ Create a Class Node

Let’s define a reusable class that applies watermark text to any image.

```bash
typeflow create-class Watermark
```

Edit `src/classes/Watermark.py`:

```python
from typeflow import node_class
from typing import Tuple
from PIL import Image, ImageDraw, ImageFont

@node_class
class Watermark:
    text: str
    position: Tuple[int, int] = (10, 10)
    opacity: int = 128
    font_size: int = 24

    def apply(self, img: Image.Image) -> Image.Image:
        """Apply watermark text to image."""
        overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(overlay)

        try:
            font = ImageFont.truetype("arial.ttf", self.font_size)
        except Exception:
            font = ImageFont.load_default()

        draw.text(self.position, self.text, fill=(255, 255, 255, self.opacity), font=font)
        return Image.alpha_composite(img, overlay)
```

## 5️⃣ Validate All Nodes

Before using them, validate your definitions:

```bash
typeflow validate node
typeflow validate class
```

Each valid node or class will have a YAML descriptor generated inside `.typeflow/`.

## 6️⃣ Build the Workflow Visually

Launch the editor:

```bash
typeflow start-ui
```

Open `http://localhost:3001`

In the visual editor:

1. Add **Input Node** → **file_path** node (if you want to upload file inside editor) or **string_val** node if you want to write the path of image.  
2. Connect to → **load_image**  
3. Add **Input Node**
    - tuple_val (for size of image for **resize_image**)
    - bool_val  (for keep_aspect input to **resize_image**)
    - float_val (for factor value for **adjust_brightness**)
    - string_val (for text input to **Watermark** class)
    - int_val (for opacity input to **Watermark** class) (*optional*)
    - tuple_val (for position input to **Watermark** class) (*optional*)
    - int_val (for font-size input to **Watermark** class) (*optional*)
4. Then → **resize_image** → **grayscale** → **adjust_brightness**  
5. Then drag **Watermark** on editor
6. Double click on **Watermark** to add method **apply**. It will attach its method node to class.
7. Connect **adjust_brightness** → **Watermark.apply**
8. Finally connect → **save_image**  
9. Add an **string_val** Input node to specify your output file path. You can copy the folder path from ur laptop and paste it with added output image name.

Hit **Export** to save the graph as `workflow/dag.json`.

## 7️⃣ Compile and Run

From terminal:

```bash
typeflow compile
typeflow generate
typeflow run
```

On compile, see type validation in your data flow between the edges, so you can catch any potential errors before running it.
On generate, typeflow will create `src/orchestrator.py` script for transparency.

## Run from Editor

Instead of compiling and using terminal, you can run directly inside the editor — hit **Start**, and Typeflow will do this behind ths scenes.:

- Compile your DAG  
- Generate an orchestrator Python script  
- Run it in an async subprocess via FastAPI  
- Stream live node execution updates over SSE  

## 8️⃣ Result

After execution, you’ll find your processed image in the specified output path —  
resized, brightened, converted to grayscale, and watermarked with your custom text.

### Example generated orchestrator (auto-created by Typeflow)

```python
# Auto-generated workflow script

from src.classes.Watermark import Watermark
from src.nodes.adjust_brightness.main import adjust_brightness
from src.nodes.grayscale.main import grayscale
from src.nodes.load_image.main import load_image
from src.nodes.resize_image.main import resize_image
from src.nodes.save_image.main import save_image

file_input_1 = 'data/X_file_input_1.jpg'
bool_val_2 = True
tuple_val_3 = (400, 400)
float_val_4 = 1.2
string_val_5 = 'Typeflow'
tuple_val_6 = (20, 20)
int_val_7 = 250
int_val_8 = 30
string_val_1 = 'data/outputs/watermark.png'
load_image_out = load_image(path=file_input_1)
watermark_1 = Watermark(text=string_val_5, position=tuple_val_6, opacity=int_val_7, font_size=int_val_8)
resize_image_out = resize_image(img=load_image_out, keep_aspect=bool_val_2, size=tuple_val_3)
grayscale_out = grayscale(img=resize_image_out)
adjust_brightness_out = adjust_brightness(img=grayscale_out, factor=float_val_4)
watermark_1_apply_out = watermark_1.apply(img=adjust_brightness_out)
save_image_out = save_image(img=watermark_1_apply_out, output_path=string_val_1)

# End of generated workflow
```

✅ **Done**  
You’ve successfully created a modular, type-safe workflow using Typeflow — all locally, with zero cloud dependency.

## Output showcase in editor

In Editor, the **Watermark.apply** method outputs **Image**, so you can remove the **save_image** node (for removing just click on node and press DEL/DELETE/BACKSPACE button). And drag a **image_output** node, and connect **Watermark.apply** → **image_output**. And Press on **Start** button to see the image itself on editor. Note: Output nodes only work if you use Editor to run workflow by pressing **Start** button.

### Next steps

- Add more nodes to build complex data/AI pipelines  
- Experiment with class-based logic nodes  
- Or embed Typeflow in your own tools as an orchestrator backend

---
