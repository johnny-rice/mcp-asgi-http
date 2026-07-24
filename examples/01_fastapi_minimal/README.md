# 01 FastAPI minimal

Mount a small MCP server at `/mcp` next to a REST `/health` route. No auth.

```bash
pip install -e '.[dev]'
python examples/01_fastapi_minimal/main.py
# MCP endpoint: http://127.0.0.1:8000/mcp
```
