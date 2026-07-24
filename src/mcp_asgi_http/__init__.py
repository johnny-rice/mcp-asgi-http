"""ASGI glue for remote MCP over Streamable HTTP."""

from mcp_asgi_http.auth import (
    ApiKeyAuth,
    AuthBackend,
    AuthContext,
    AuthenticationError,
    DualAuth,
    JwtAuth,
    NoAuth,
    build_auth_backend,
)
from mcp_asgi_http.enrich import (
    ImageAttachment,
    enrich_json_result,
    tool_result_contents,
)
from mcp_asgi_http.http import McpPathMiddleware, StatelessMCPASGIApp
from mcp_asgi_http.mount import mount_mcp
from mcp_asgi_http.playbook import (
    PlaybookSpec,
    playbook_http_route,
    playbook_resource,
    playbook_resource_contents,
)
from mcp_asgi_http.ready import ReadyHook, once_ready

__all__ = [
    "ApiKeyAuth",
    "AuthBackend",
    "AuthContext",
    "AuthenticationError",
    "DualAuth",
    "ImageAttachment",
    "JwtAuth",
    "McpPathMiddleware",
    "NoAuth",
    "PlaybookSpec",
    "ReadyHook",
    "StatelessMCPASGIApp",
    "build_auth_backend",
    "enrich_json_result",
    "mount_mcp",
    "once_ready",
    "playbook_http_route",
    "playbook_resource",
    "playbook_resource_contents",
    "tool_result_contents",
]

__version__ = "0.1.0"
