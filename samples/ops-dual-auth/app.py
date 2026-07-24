"""Ops dual-auth demo: REST UI + MCP with DualAuth (API key and/or JWT)."""

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
    build_auth_backend,
    mount_mcp,
    playbook_http_route,
    playbook_resource,
    playbook_resource_contents,
    tool_result_contents,
)

from data import DEPLOYS, FREEZE_WINDOWS, SERVICES

STATIC = Path(__file__).with_name("static")
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")
API_KEY = os.environ.get("MCP_API_KEY", "demo-secret")

GUIDE = """# Ops agent guide

1. Prefer `list_services` then `get_service` before advising a deploy.
2. Always call `check_freeze` for the target service before recommending a change window.
3. Cite services as `Name (id)` and use the `href` field when linking for a human.
4. Read this guide at session start.
"""

spec = PlaybookSpec(markdown=GUIDE, uri="mcp://docs/agent-guide")

_BY_ID = {s["id"]: s for s in SERVICES}


def add_href(name: str, data: Any) -> Any:
    if not SITE_URL:
        return data
    if name == "get_service" and isinstance(data, dict) and "id" in data:
        data = dict(data)
        data["href"] = f"{SITE_URL}/#service-{data['id']}"
    if name == "list_services" and isinstance(data, dict):
        data = dict(data)
        items = []
        for item in data.get("items") or []:
            if isinstance(item, dict) and "id" in item:
                item = dict(item)
                item["href"] = f"{SITE_URL}/#service-{item['id']}"
            items.append(item)
        data["items"] = items
    if name == "list_deploys" and isinstance(data, dict):
        data = dict(data)
        items = []
        for item in data.get("items") or []:
            if isinstance(item, dict) and item.get("service_id"):
                item = dict(item)
                item["href"] = f"{SITE_URL}/#service-{item['service_id']}"
            items.append(item)
        data["items"] = items
    return data


def _freeze_for(service_id: str) -> dict[str, Any]:
    active = [
        fz
        for fz in FREEZE_WINDOWS
        if fz.get("active") and service_id in (fz.get("applies_to") or [])
    ]
    return {
        "service_id": service_id,
        "blocked": bool(active),
        "active_windows": active,
        "message": (
            "Deploy blocked by an active freeze window"
            if active
            else "No active freeze window for this service"
        ),
    }


server = Server("ops-dual-auth")


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
            name="list_services",
            description="List platform services and health status",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_service",
            description="Get one service by id",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
            },
        ),
        types.Tool(
            name="list_deploys",
            description="List recent deploys (optionally filter by service_id)",
            inputSchema={
                "type": "object",
                "properties": {"service_id": {"type": "string"}},
            },
        ),
        types.Tool(
            name="check_freeze",
            description="Check whether an active freeze window blocks deploys for a service",
            inputSchema={
                "type": "object",
                "properties": {"service_id": {"type": "string"}},
                "required": ["service_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    if name == "list_services":
        raw: Any = {"items": list(SERVICES)}
    elif name == "get_service":
        svc = _BY_ID.get(str(arguments.get("id", "")))
        if svc is None:
            raise ValueError("service not found")
        raw = svc
    elif name == "list_deploys":
        sid = arguments.get("service_id")
        items = DEPLOYS
        if sid:
            items = [d for d in DEPLOYS if d["service_id"] == sid]
        raw = {"items": items}
    elif name == "check_freeze":
        sid = str(arguments.get("service_id", ""))
        if sid not in _BY_ID:
            raise ValueError("service not found")
        raw = _freeze_for(sid)
    else:
        raise ValueError(name)
    return tool_result_contents(name, raw, hooks=[add_href])  # type: ignore[return-value]


api = FastAPI(title="ops-dual-auth", redirect_slashes=False)
api.routes.append(playbook_http_route(spec))


class ServiceOut(BaseModel):
    id: str
    name: str
    owner: str
    env: str
    status: str
    version: str
    href: str | None = None


class DeployOut(BaseModel):
    id: str
    service_id: str
    version: str
    status: str
    deployed_at: str
    actor: str
    href: str | None = None


class FreezeOut(BaseModel):
    id: str
    name: str
    starts_at: str
    ends_at: str
    applies_to: list[str]
    active: bool


def _svc_href(service_id: str) -> str | None:
    if not SITE_URL:
        return None
    return f"{SITE_URL}/#service-{service_id}"


@api.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "services": len(SERVICES),
        "auth": "dual",
    }


@api.get("/api/config")
def api_config() -> dict[str, object]:
    jwt_ready = all(
        os.environ.get(k)
        for k in ("JWT_ISSUER", "JWT_AUDIENCE", "JWT_JWKS_URL")
    )
    return {
        "mcp_path": "/mcp",
        "auth": "dual",
        "api_key_header": "X-API-Key or Authorization: Bearer <api-key>",
        "jwt": "Authorization: Bearer <jwt> when JWT_* env is set",
        "jwt_configured": jwt_ready,
        "api_key_hint": f"{API_KEY[:4]}…" if len(API_KEY) > 4 else "(set MCP_API_KEY)",
    }


@api.get("/api/services", response_model=list[ServiceOut])
def api_services() -> list[ServiceOut]:
    return [ServiceOut(**s, href=_svc_href(s["id"])) for s in SERVICES]


@api.get("/api/services/{service_id}", response_model=ServiceOut)
def api_service(service_id: str) -> ServiceOut:
    svc = _BY_ID.get(service_id)
    if svc is None:
        raise HTTPException(status_code=404, detail="not found")
    return ServiceOut(**svc, href=_svc_href(service_id))


@api.get("/api/deploys", response_model=list[DeployOut])
def api_deploys(service_id: str | None = None) -> list[DeployOut]:
    items = DEPLOYS
    if service_id:
        items = [d for d in DEPLOYS if d["service_id"] == service_id]
    return [
        DeployOut(**d, href=_svc_href(d["service_id"])) for d in items
    ]


@api.get("/api/freeze-windows", response_model=list[FreezeOut])
def api_freezes() -> list[FreezeOut]:
    return [FreezeOut(**fz) for fz in FREEZE_WINDOWS]


@api.get("/api/services/{service_id}/freeze")
def api_service_freeze(service_id: str) -> dict[str, Any]:
    if service_id not in _BY_ID:
        raise HTTPException(status_code=404, detail="not found")
    return _freeze_for(service_id)


@api.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


api.mount("/static", StaticFiles(directory=STATIC), name="static")

auth = build_auth_backend(
    "dual",
    api_keys={API_KEY},
    jwt_issuer=os.environ.get("JWT_ISSUER"),
    jwt_audience=os.environ.get("JWT_AUDIENCE"),
    jwt_jwks_url=os.environ.get("JWT_JWKS_URL"),
)

app = mount_mcp(api, server, auth=auth)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
