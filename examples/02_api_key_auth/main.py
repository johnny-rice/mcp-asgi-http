"""API-key gated MCP at /mcp."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from _shared import make_echo_server  # noqa: E402
from mcp_asgi_http import ApiKeyAuth, mount_mcp  # noqa: E402

KEY = os.environ.get("MCP_API_KEY", "dev-secret")

api = FastAPI(title="mcp-asgi-http api-key", redirect_slashes=False)
app = mount_mcp(
    api,
    make_echo_server(),
    auth=ApiKeyAuth(allowed_keys={KEY}),
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)
