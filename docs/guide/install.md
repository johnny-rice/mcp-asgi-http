# Install

```bash
pip install mcp-asgi-http
```

JWT backends need the extra:

```bash
pip install 'mcp-asgi-http[jwt]'
```

Requires Python 3.10+.

From a clone:

```bash
pip install -e '.[dev]'
pytest -q
```
