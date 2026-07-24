"""Catalog demo: enrich hooks + agent playbook + simple UI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import mcp.types as types
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from mcp.server import Server
from pydantic import BaseModel

from mcp_asgi_http import (
    PlaybookSpec,
    mount_mcp,
    playbook_http_route,
    playbook_resource,
    playbook_resource_contents,
    tool_result_contents,
)

STATIC = Path(__file__).with_name("static")
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")

ITEMS: dict[int, dict[str, Any]] = {
    1: {"id": 1, "name": "Widget", "price_cents": 1200},
    2: {"id": 2, "name": "Gadget", "price_cents": 4500},
    3: {"id": 3, "name": "Doohickey", "price_cents": 900},
}

GUIDE = """# Catalog agent guide

1. Cite items as `Name (id)`.
2. Prefer the `href` field from tool JSON when linking for a human.
3. Read this guide at session start.
"""

spec = PlaybookSpec(markdown=GUIDE, uri="mcp://docs/agent-guide")


def add_href(name: str, data: Any) -> Any:
    if not SITE_URL:
        return data
    if name == "get_item" and isinstance(data, dict) and "id" in data:
        data = dict(data)
        data["href"] = f"{SITE_URL}/#item-{data['id']}"
    if name == "list_items" and isinstance(data, dict):
        data = dict(data)
        items = []
        for item in data.get("items") or []:
            if isinstance(item, dict) and "id" in item:
                item = dict(item)
                item["href"] = f"{SITE_URL}/#item-{item['id']}"
            items.append(item)
        data["items"] = items
    return data


server = Server("catalog-demo")


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
            name="list_items",
            description="List catalog items",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_item",
            description="Get one catalog item",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "integer"}},
                "required": ["id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    if name == "list_items":
        raw = {"items": list(ITEMS.values())}
    elif name == "get_item":
        item = ITEMS.get(int(arguments["id"]))
        if item is None:
            raise ValueError("not found")
        raw = item
    else:
        raise ValueError(name)
    return tool_result_contents(name, raw, hooks=[add_href])  # type: ignore[return-value]


api = FastAPI(title="catalog-demo", redirect_slashes=False)
api.routes.append(playbook_http_route(spec))


class ItemOut(BaseModel):
    id: int
    name: str
    price_cents: int
    href: str | None = None


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@api.get("/api/items", response_model=list[ItemOut])
def api_items() -> list[ItemOut]:
    out = []
    for item in ITEMS.values():
        href = f"{SITE_URL}/#item-{item['id']}" if SITE_URL else None
        out.append(ItemOut(**item, href=href))
    return out


@api.get("/api/items/{item_id}", response_model=ItemOut)
def api_item(item_id: int) -> ItemOut:
    item = ITEMS.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="not found")
    href = f"{SITE_URL}/#item-{item_id}" if SITE_URL else None
    return ItemOut(**item, href=href)


@api.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


api.mount("/static", StaticFiles(directory=STATIC), name="static")

# Open MCP for public demo; put a gateway in front for production.
app = mount_mcp(api, server, auth=None)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
