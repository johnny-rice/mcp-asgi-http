"""Minimal FastAPI + remote MCP at /mcp (no auth)."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from _shared import make_echo_server  # noqa: E402
from mcp_asgi_http import mount_mcp  # noqa: E402

api = FastAPI(title="mcp-asgi-http minimal", redirect_slashes=False)


@api.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app = mount_mcp(api, make_echo_server(), auth=None)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
