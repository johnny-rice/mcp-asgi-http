"""Authenticate outside MCP; pass auth=None to the library."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.types import Receive, Scope, Send

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from _shared import make_echo_server  # noqa: E402
from mcp_asgi_http import mount_mcp  # noqa: E402

EXPECTED = os.environ.get("GATEWAY_KEY", "gateway-secret")


class ConsumerAuthMiddleware:
    """Example gateway/auth middleware in front of MCP."""

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http" and scope.get("path", "").startswith("/mcp"):
            headers = {k.decode().lower(): v.decode() for k, v in scope.get("headers", [])}
            if headers.get("x-api-key") != EXPECTED:
                await JSONResponse({"detail": "unauthorized"}, status_code=401)(
                    scope, receive, send
                )
                return
        await self.app(scope, receive, send)


api = FastAPI(title="mcp-asgi-http consumer auth", redirect_slashes=False)
# auth=None: this library does not authenticate; middleware above does.
mounted = mount_mcp(api, make_echo_server(), auth=None)
app = ConsumerAuthMiddleware(mounted)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8003)
