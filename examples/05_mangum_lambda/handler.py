"""Mangum handler with lifespan off + once_ready lazy init."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import FastAPI
from mangum import Mangum

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from _shared import make_echo_server  # noqa: E402
from mcp_asgi_http import ApiKeyAuth, mount_mcp, once_ready  # noqa: E402

_ready = False


async def warm() -> None:
    """Example lazy init when lifespan is off (e.g. open a DB pool)."""
    global _ready
    _ready = True


api = FastAPI(title="mcp-asgi-http mangum", redirect_slashes=False)


@api.get("/live")
def live() -> dict[str, object]:
    return {"live": True, "ready": _ready}


app = mount_mcp(
    api,
    make_echo_server("lambda-echo"),
    auth=ApiKeyAuth(allowed_keys={"lambda-dev-key"}),
    on_ready=once_ready(warm),
)

# Lifespan off: FastAPI lifespan never runs; use on_ready instead.
handler = Mangum(app, lifespan="off")
