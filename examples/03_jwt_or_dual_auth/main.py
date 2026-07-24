"""Dual auth: API key fast-path or JWT (JWKS)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from _shared import make_echo_server  # noqa: E402
from mcp_asgi_http import build_auth_backend, mount_mcp  # noqa: E402

api = FastAPI(title="mcp-asgi-http dual auth", redirect_slashes=False)

auth = build_auth_backend(
    "dual",
    api_keys={os.environ.get("MCP_API_KEY", "dev-secret")},
    jwt_issuer=os.environ.get("JWT_ISSUER"),
    jwt_audience=os.environ.get("JWT_AUDIENCE"),
    jwt_jwks_url=os.environ.get("JWT_JWKS_URL"),
)

app = mount_mcp(api, make_echo_server(), auth=auth)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8002)
