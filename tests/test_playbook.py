"""Tests for playbook helpers."""

from __future__ import annotations

from pathlib import Path

from starlette.applications import Starlette
from starlette.testclient import TestClient

from mcp_asgi_http.playbook import (
    PlaybookSpec,
    playbook_http_route,
    playbook_resource,
    playbook_resource_contents,
)


def test_playbook_resource_and_contents(tmp_path: Path) -> None:
    path = tmp_path / "guide.md"
    path.write_text("# Rules\n\n1. Be careful.\n", encoding="utf-8")
    spec = PlaybookSpec.from_path(path, uri="mcp://docs/guide")
    resource = playbook_resource(spec)
    assert str(resource.uri) == "mcp://docs/guide"
    assert "Be careful" in playbook_resource_contents(spec)


def test_playbook_http_twin() -> None:
    spec = PlaybookSpec(markdown="# Hello\n", http_path="/agent-guide.md")
    app = Starlette(routes=[playbook_http_route(spec)])
    client = TestClient(app)
    res = client.get("/agent-guide.md")
    assert res.status_code == 200
    assert res.text.startswith("# Hello")
    assert "markdown" in res.headers["content-type"]
