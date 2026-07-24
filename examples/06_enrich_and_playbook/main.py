"""Enrich tool results + serve an agent playbook as MCP resource and HTTP twin."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import mcp.types as types
from fastapi import FastAPI
from mcp.server import Server

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mcp_asgi_http import (  # noqa: E402
    PlaybookSpec,
    enrich_json_result,
    mount_mcp,
    playbook_http_route,
    playbook_resource,
    playbook_resource_contents,
    tool_result_contents,
)

GUIDE = """# Agent guide

1. Always cite item ids as `name (id)`.
2. Prefer deep links from tool JSON (`href`) when present.
"""

spec = PlaybookSpec(markdown=GUIDE, uri="mcp://docs/agent-guide")

server: Server[Any, Any] = Server("demo-catalog")


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    return [playbook_resource(spec)]


@server.read_resource()
async def read_resource(uri: types.AnyUrl) -> str | bytes:
    if str(uri) == spec.uri:
        return playbook_resource_contents(spec)
    raise ValueError(f"unknown resource: {uri}")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_item",
            description="Fetch a catalog item",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "integer"}},
                "required": ["id"],
            },
        )
    ]


def _add_href(name: str, data: Any) -> Any:
    if name == "get_item" and isinstance(data, dict) and "id" in data:
        data = dict(data)
        data["href"] = f"https://app.example.com/items/{data['id']}"
    return data


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    if name != "get_item":
        raise ValueError(name)
    raw = {"id": int(arguments["id"]), "name": f"Item-{arguments['id']}"}
    # Enrich before returning (or use enrich_json_result alone)
    _ = enrich_json_result(name, raw, hooks=[_add_href])
    return tool_result_contents(name, raw, hooks=[_add_href])  # type: ignore[return-value]


api = FastAPI(title="mcp-asgi-http enrich+playbook", redirect_slashes=False)
api.routes.append(playbook_http_route(spec))
app = mount_mcp(api, server, auth=None)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8006)
