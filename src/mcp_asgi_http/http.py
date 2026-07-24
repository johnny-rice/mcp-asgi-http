"""Stateless Streamable HTTP ASGI app for MCP (serverless-friendly)."""

from __future__ import annotations

import logging
from typing import Any

import anyio
from mcp.server.lowlevel.server import Server as MCPServer
from mcp.server.streamable_http import StreamableHTTPServerTransport
from starlette.responses import JSONResponse
from starlette.types import Receive, Scope, Send

from mcp_asgi_http.auth.base import AuthBackend, AuthenticationError
from mcp_asgi_http.ready import ReadyHook

logger = logging.getLogger(__name__)


class McpPathMiddleware:
    """Dispatch ``/mcp`` without Starlette Mount trailing-slash redirects.

    Useful under Mangum / Function URL where slash redirects can 404 or loop.
    """

    def __init__(self, app: Any, mcp_app: Any, *, prefix: str = "/mcp") -> None:
        self.app = app
        self.mcp_app = mcp_app
        self.prefix = prefix.rstrip("/") or "/mcp"

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            path = scope.get("path", "")
            if path == self.prefix or path.startswith(f"{self.prefix}/"):
                await self.mcp_app(scope, receive, send)
                return
        await self.app(scope, receive, send)


class StatelessMCPASGIApp:
    """
    Per-request MCP Streamable HTTP handler.

    Uses JSON responses and no cross-request session state so it works under
    Mangum with lifespan off (e.g. AWS Lambda Function URL).

    Pass ``auth=None`` when the consumer already authenticated upstream
    (API Gateway authorizer, FastAPI middleware, etc.).
    """

    def __init__(
        self,
        mcp_server: MCPServer[Any, Any],
        *,
        auth: AuthBackend | None = None,
        on_ready: ReadyHook | None = None,
    ) -> None:
        self.mcp_server = mcp_server
        self.auth = auth
        self.on_ready = on_ready

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            raise RuntimeError("MCP HTTP transport only supports HTTP")

        headers = {
            k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope.get("headers", [])
        }
        authorization = headers.get("authorization")
        api_key_header = headers.get("x-api-key")

        if self.auth is not None:
            try:
                await self.auth.authenticate(authorization, api_key_header)
            except AuthenticationError as exc:
                response = JSONResponse(
                    {"detail": str(exc)},
                    status_code=401,
                    headers={"WWW-Authenticate": "Bearer"},
                )
                await response(scope, receive, send)
                return

        if self.on_ready is not None:
            await self.on_ready()

        transport = StreamableHTTPServerTransport(
            mcp_session_id=None,
            is_json_response_enabled=True,
            event_store=None,
        )

        async with anyio.create_task_group() as tg:

            async def run_server(
                *, task_status: anyio.abc.TaskStatus[None] = anyio.TASK_STATUS_IGNORED
            ) -> None:
                async with transport.connect() as streams:
                    read_stream, write_stream = streams
                    task_status.started()
                    try:
                        await self.mcp_server.run(
                            read_stream,
                            write_stream,
                            self.mcp_server.create_initialization_options(),
                            stateless=True,
                        )
                    except Exception:  # noqa: BLE001
                        logger.exception("Stateless MCP session crashed")

            await tg.start(run_server)
            await transport.handle_request(scope, receive, send)
            await transport.terminate()
