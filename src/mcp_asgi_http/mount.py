"""Convenience helpers to mount MCP on an ASGI app."""

from __future__ import annotations

from typing import Any

from mcp.server.lowlevel.server import Server as MCPServer

from mcp_asgi_http.auth.base import AuthBackend
from mcp_asgi_http.http import McpPathMiddleware, StatelessMCPASGIApp
from mcp_asgi_http.ready import ReadyHook


def mount_mcp(
    app: Any,
    mcp_server: MCPServer[Any, Any],
    *,
    prefix: str = "/mcp",
    auth: AuthBackend | None = None,
    on_ready: ReadyHook | None = None,
) -> McpPathMiddleware:
    """
    Wrap ``app`` so ``prefix`` is handled by a stateless Streamable HTTP MCP ASGI app.

    Returns the outer ASGI app (path middleware wrapping the original app).
    Use this instead of Starlette ``Mount`` under Mangum / Function URL.
    """
    mcp_asgi = StatelessMCPASGIApp(mcp_server, auth=auth, on_ready=on_ready)
    return McpPathMiddleware(app, mcp_asgi, prefix=prefix)
