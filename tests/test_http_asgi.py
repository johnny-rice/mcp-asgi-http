"""Integration tests for StatelessMCPASGIApp over Streamable HTTP."""

from __future__ import annotations

from typing import Any

import pytest
from httpx import ASGITransport, AsyncClient
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from mcp_asgi_http import ApiKeyAuth, mount_mcp, once_ready
from mcp_asgi_http.http import StatelessMCPASGIApp


def _initialize_body() -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "0.0.1"},
        },
    }


@pytest.mark.asyncio
async def test_tools_list_without_auth(echo_server: Any) -> None:
    mcp_asgi = StatelessMCPASGIApp(echo_server, auth=None)
    transport = ASGITransport(app=mcp_asgi)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post(
            "/mcp",
            json=_initialize_body(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )
    assert res.status_code == 200
    data = res.json()
    # JSON response may be a single object or wrapped depending on SDK version
    if isinstance(data, dict) and "result" in data:
        assert "serverInfo" in data["result"] or "protocolVersion" in data["result"]
    else:
        assert data is not None


@pytest.mark.asyncio
async def test_auth_rejects_missing_key(echo_server: Any) -> None:
    mcp_asgi = StatelessMCPASGIApp(
        echo_server,
        auth=ApiKeyAuth(allowed_keys={"secret"}),
    )
    transport = ASGITransport(app=mcp_asgi)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post(
            "/mcp",
            json=_initialize_body(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )
    assert res.status_code == 401
    assert "detail" in res.json()


@pytest.mark.asyncio
async def test_auth_accepts_api_key(echo_server: Any) -> None:
    mcp_asgi = StatelessMCPASGIApp(
        echo_server,
        auth=ApiKeyAuth(allowed_keys={"secret"}),
    )
    transport = ASGITransport(app=mcp_asgi)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post(
            "/mcp",
            json=_initialize_body(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "X-API-Key": "secret",
            },
        )
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_on_ready_invoked(echo_server: Any) -> None:
    calls = 0

    async def ready() -> None:
        nonlocal calls
        calls += 1

    mcp_asgi = StatelessMCPASGIApp(echo_server, auth=None, on_ready=once_ready(ready))
    transport = ASGITransport(app=mcp_asgi)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        for _ in range(2):
            await client.post(
                "/mcp",
                json=_initialize_body(),
                headers={
                    "Accept": "application/json, text/event-stream",
                    "Content-Type": "application/json",
                },
            )
    assert calls == 1


@pytest.mark.asyncio
async def test_mount_mcp_and_rest(echo_server: Any) -> None:
    async def health(_: Request) -> JSONResponse:
        return JSONResponse({"status": "ok"})

    app = Starlette(routes=[Route("/health", endpoint=health)])
    wrapped = mount_mcp(app, echo_server, auth=None)
    transport = ASGITransport(app=wrapped)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        health_res = await client.get("/health")
        assert health_res.status_code == 200
        assert health_res.json() == {"status": "ok"}

        mcp_res = await client.post(
            "/mcp",
            json=_initialize_body(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )
        assert mcp_res.status_code == 200


@pytest.mark.asyncio
async def test_consumer_owned_auth_pattern(echo_server: Any) -> None:
    """Outer middleware authenticates; MCP uses auth=None."""

    class Gate:
        def __init__(self, app: Any) -> None:
            self.app = app

        async def __call__(self, scope: Any, receive: Any, send: Any) -> None:
            if scope["type"] == "http":
                headers = {
                    k.decode().lower(): v.decode() for k, v in scope.get("headers", [])
                }
                if headers.get("x-api-key") != "gateway-secret":
                    from starlette.responses import JSONResponse

                    await JSONResponse({"detail": "forbidden"}, status_code=403)(
                        scope, receive, send
                    )
                    return
            await self.app(scope, receive, send)

    inner = StatelessMCPASGIApp(echo_server, auth=None)
    app = Gate(inner)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        denied = await client.post(
            "/mcp",
            json=_initialize_body(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
            },
        )
        assert denied.status_code == 403

        ok = await client.post(
            "/mcp",
            json=_initialize_body(),
            headers={
                "Accept": "application/json, text/event-stream",
                "Content-Type": "application/json",
                "X-API-Key": "gateway-secret",
            },
        )
        assert ok.status_code == 200
