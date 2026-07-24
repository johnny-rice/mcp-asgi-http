"""Clinical-intel demo: CT.gov-shaped fixtures + enrich/playbook + REST UI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import mcp.types as types
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from mcp.server import Server
from pydantic import BaseModel

from mcp_asgi_http import (
    ApiKeyAuth,
    PlaybookSpec,
    mount_mcp,
    playbook_http_route,
    playbook_resource,
    playbook_resource_contents,
    tool_result_contents,
)

from data import COMPANIES, TARGETS, TRIALS

STATIC = Path(__file__).with_name("static")
SITE_URL = os.environ.get("SITE_URL", "").rstrip("/")
API_KEY = os.environ.get("MCP_API_KEY", "demo-secret")

GUIDE = """# Clinical intel agent guide

Synthetic demo data only. Do not treat NCT IDs or company names as real.

1. Prefer `search_trials` with a short query, then `get_trial`.
2. Cite trials as `Title (NCT id)` and use `href` when linking for a human.
3. Use `get_company` / `get_target` to expand context after a trial hit.
4. Read this guide at session start.
"""

spec = PlaybookSpec(markdown=GUIDE, uri="mcp://docs/agent-guide")

_TRIALS = {t["id"]: t for t in TRIALS}
_COMPANIES = {c["id"]: c for c in COMPANIES}
_TARGETS = {t["id"]: t for t in TARGETS}


def _trial_href(trial_id: str) -> str | None:
    if not SITE_URL:
        return None
    return f"{SITE_URL}/#trial-{trial_id}"


def add_href(name: str, data: Any) -> Any:
    if not SITE_URL:
        return data
    if name == "get_trial" and isinstance(data, dict) and "id" in data:
        data = dict(data)
        data["href"] = _trial_href(str(data["id"]))
    if name in ("search_trials", "list_trials") and isinstance(data, dict):
        data = dict(data)
        items = []
        for item in data.get("items") or []:
            if isinstance(item, dict) and "id" in item:
                item = dict(item)
                item["href"] = _trial_href(str(item["id"]))
            items.append(item)
        data["items"] = items
    if name == "get_company" and isinstance(data, dict) and "id" in data:
        data = dict(data)
        data["href"] = f"{SITE_URL}/#company-{data['id']}"
    if name == "get_target" and isinstance(data, dict) and "id" in data:
        data = dict(data)
        data["href"] = f"{SITE_URL}/#target-{data['id']}"
    return data


def _search_trials(q: str) -> list[dict[str, Any]]:
    needle = q.strip().lower()
    if not needle:
        return list(TRIALS)
    out = []
    for trial in TRIALS:
        blob = " ".join(
            [
                trial["id"],
                trial["title"],
                trial["condition"],
                trial["phase"],
                trial["status"],
                trial["summary"],
            ]
        ).lower()
        if needle in blob:
            out.append(trial)
    return out


server = Server("clinical-intel")


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
            name="search_trials",
            description="Search synthetic trials by free-text query",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_trial",
            description="Get one trial by NCT-style id",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
            },
        ),
        types.Tool(
            name="list_companies",
            description="List synthetic biotech companies in the fixture set",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="get_company",
            description="Get one company and its trials",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
            },
        ),
        types.Tool(
            name="get_target",
            description="Get one target and related trials",
            inputSchema={
                "type": "object",
                "properties": {"id": {"type": "string"}},
                "required": ["id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
    if name == "search_trials":
        raw: Any = {"items": _search_trials(str(arguments.get("query", "")))}
    elif name == "get_trial":
        trial = _TRIALS.get(str(arguments.get("id", "")))
        if trial is None:
            raise ValueError("trial not found")
        raw = trial
    elif name == "list_companies":
        raw = {"items": list(COMPANIES)}
    elif name == "get_company":
        company = _COMPANIES.get(str(arguments.get("id", "")))
        if company is None:
            raise ValueError("company not found")
        trials = [t for t in TRIALS if t["company_id"] == company["id"]]
        raw = {**company, "trials": trials}
    elif name == "get_target":
        target = _TARGETS.get(str(arguments.get("id", "")))
        if target is None:
            raise ValueError("target not found")
        trials = [t for t in TRIALS if target["id"] in t["target_ids"]]
        raw = {**target, "trials": trials}
    else:
        raise ValueError(name)
    return tool_result_contents(name, raw, hooks=[add_href])  # type: ignore[return-value]


api = FastAPI(title="clinical-intel", redirect_slashes=False)
api.routes.append(playbook_http_route(spec))


class TrialOut(BaseModel):
    id: str
    title: str
    phase: str
    status: str
    condition: str
    company_id: str
    target_ids: list[str]
    start_date: str
    summary: str
    href: str | None = None


class CompanyOut(BaseModel):
    id: str
    name: str
    hq: str
    focus: list[str]
    href: str | None = None


class TargetOut(BaseModel):
    id: str
    symbol: str
    name: str
    modality_fit: list[str]
    href: str | None = None


@api.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "trials": len(TRIALS),
        "companies": len(COMPANIES),
        "targets": len(TARGETS),
    }


@api.get("/api/config")
def api_config() -> dict[str, str]:
    return {
        "mcp_path": "/mcp",
        "auth": "X-API-Key or Authorization: Bearer",
        "api_key_hint": f"{API_KEY[:4]}…" if len(API_KEY) > 4 else "(set MCP_API_KEY)",
        "data": "synthetic fixtures only",
    }


@api.get("/api/trials", response_model=list[TrialOut])
def api_trials(q: str | None = Query(default=None)) -> list[TrialOut]:
    items = _search_trials(q or "")
    return [TrialOut(**t, href=_trial_href(t["id"])) for t in items]


@api.get("/api/trials/{trial_id}", response_model=TrialOut)
def api_trial(trial_id: str) -> TrialOut:
    trial = _TRIALS.get(trial_id)
    if trial is None:
        raise HTTPException(status_code=404, detail="not found")
    return TrialOut(**trial, href=_trial_href(trial_id))


@api.get("/api/companies", response_model=list[CompanyOut])
def api_companies() -> list[CompanyOut]:
    return [
        CompanyOut(
            **c,
            href=f"{SITE_URL}/#company-{c['id']}" if SITE_URL else None,
        )
        for c in COMPANIES
    ]


@api.get("/api/targets", response_model=list[TargetOut])
def api_targets() -> list[TargetOut]:
    return [
        TargetOut(
            **t,
            href=f"{SITE_URL}/#target-{t['id']}" if SITE_URL else None,
        )
        for t in TARGETS
    ]


@api.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


api.mount("/static", StaticFiles(directory=STATIC), name="static")

app = mount_mcp(
    api,
    server,
    auth=ApiKeyAuth(allowed_keys={API_KEY}),
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
