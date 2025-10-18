# later needed

poetry add --group dev pytest-asyncio pytest-httpx mkdocs mkdocs-material pre-commit

## Commands

ruff check src/
mypy src/
black src/
isort src/
pytest -v
poetry build
pip install dist/typeflow-0.1.0-py3-none-any.whl
