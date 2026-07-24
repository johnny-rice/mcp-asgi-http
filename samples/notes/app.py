"""Notes demo: REST + MCP + small web UI."""

from __future__ import annotations

import os
import uuid
from pathlib import Path
from typing import Any

import mcp.types as types
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from mcp.server import Server
from pydantic import BaseModel, Field

from mcp_asgi_http import ApiKeyAuth, mount_mcp, once_ready

STATIC = Path(__file__).with_name("static")
API_KEY = os.environ.get("MCP_API_KEY", "demo-secret")
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")

_notes: dict[str, dict[str, str]] = {}
_ready = False


async def warm() -> None:
    global _ready
    if not _notes:
        nid = str(uuid.uuid4())
        _notes[nid] = {"id": nid, "title": "Welcome", "body": "Edit or add notes via REST or MCP."}
    _ready = True


class NoteIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    body: str = Field(default="", max_length=8000)


class NoteOut(BaseModel):
    id: str
    title: str
    body: str
    href: str | None = None


def _href(note_id: str) -> str | None:
    if not SITE_URL:
        return None
    return f"{SITE_URL}/#note-{note_id}"


server = Server("notes-demo")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="list_notes",
            description="List all notes",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_note",
            description="Get a note by id",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
            },
        ),
        types.Tool(
            name="create_note",
            description="Create a note",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["title"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    import json

    if name == "list_notes":
        items = [
            {**n, "href": _href(n["id"])}
            for n in _notes.values()
        ]
        payload = {"items": items}
    elif name == "get_note":
        note = _notes.get(str(arguments.get("id", "")))
        if note is None:
            raise ValueError("note not found")
        payload = {**note, "href": _href(note["id"])}
    elif name == "create_note":
        nid = str(uuid.uuid4())
        note = {
            "id": nid,
            "title": str(arguments.get("title", "")).strip() or "Untitled",
            "body": str(arguments.get("body", "")),
        }
        _notes[nid] = note
        payload = {**note, "href": _href(nid)}
    else:
        raise ValueError(f"unknown tool: {name}")
    return [types.TextContent(type="text", text=json.dumps(payload, indent=2))]


api = FastAPI(title="notes-demo", redirect_slashes=False)


@api.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "ready": _ready, "notes": len(_notes)}


@api.get("/api/notes", response_model=list[NoteOut])
def api_list_notes() -> list[NoteOut]:
    return [
        NoteOut(id=n["id"], title=n["title"], body=n["body"], href=_href(n["id"]))
        for n in _notes.values()
    ]


@api.post("/api/notes", response_model=NoteOut)
def api_create_note(payload: NoteIn) -> NoteOut:
    nid = str(uuid.uuid4())
    note = {"id": nid, "title": payload.title, "body": payload.body}
    _notes[nid] = note
    return NoteOut(id=nid, title=note["title"], body=note["body"], href=_href(nid))


@api.get("/api/notes/{note_id}", response_model=NoteOut)
def api_get_note(note_id: str) -> NoteOut:
    note = _notes.get(note_id)
    if note is None:
        raise HTTPException(status_code=404, detail="not found")
    return NoteOut(id=note["id"], title=note["title"], body=note["body"], href=_href(note_id))


@api.get("/api/config")
def api_config() -> dict[str, str]:
    return {
        "mcp_path": "/mcp",
        "auth": "X-API-Key or Authorization: Bearer",
        "api_key_hint": f"{API_KEY[:4]}…" if len(API_KEY) > 4 else "(set MCP_API_KEY)",
    }


@api.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


api.mount("/static", StaticFiles(directory=STATIC), name="static")

app = mount_mcp(
    api,
    server,
    auth=ApiKeyAuth(allowed_keys={API_KEY}),
    on_ready=once_ready(warm),
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
