"""Tests for McpPathMiddleware."""

from __future__ import annotations

from typing import Any

import pytest
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.testclient import TestClient

from mcp_asgi_http.http import McpPathMiddleware


async def _api_home(request: Request) -> JSONResponse:
    return JSONResponse({"ok": True})


async def _mcp_stub(scope: dict[str, Any], receive: Any, send: Any) -> None:
    response = PlainTextResponse("mcp-hit")
    await response(scope, receive, send)


@pytest.fixture
def client() -> TestClient:
    app = Starlette(routes=[Route("/", endpoint=_api_home)])
    wrapped = McpPathMiddleware(app, _mcp_stub, prefix="/mcp")
    return TestClient(wrapped)


def test_api_path_falls_through(client: TestClient) -> None:
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"ok": True}


def test_mcp_prefix_dispatched(client: TestClient) -> None:
    res = client.get("/mcp")
    assert res.status_code == 200
    assert res.text == "mcp-hit"


def test_mcp_subpath_dispatched(client: TestClient) -> None:
    res = client.post("/mcp/anything")
    assert res.status_code == 200
    assert res.text == "mcp-hit"
