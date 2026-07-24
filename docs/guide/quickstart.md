# Quickstart

Register tools on an official MCP `Server`, then mount it on FastAPI (or any ASGI app).

```python
from typing import Any

import mcp.types as types
from fastapi import FastAPI
from mcp.server import Server
from mcp_asgi_http import mount_mcp

server = Server("demo")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="echo",
            description="Echo a message",
            inputSchema={
                "type": "object",
                "properties": {"message": {"type": "string"}},
                "required": ["message"],
            },
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=str(arguments.get("message", "")))]


api = FastAPI(redirect_slashes=False)


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app = mount_mcp(api, server, auth=None)
```

Run with uvicorn:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

MCP endpoint: `http://127.0.0.1:8000/mcp`

Prefer `mount_mcp` over Starlette `Mount` under Mangum / Function URL. See [Serverless](serverless.md).
