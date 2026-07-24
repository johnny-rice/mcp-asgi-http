"""Agent playbook helpers: MCP resource + optional HTTP twin."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import mcp.types as types
from starlette.responses import PlainTextResponse
from starlette.routing import Route


@dataclass(frozen=True)
class PlaybookSpec:
    """Markdown playbook exposed as an MCP resource (and optionally over HTTP)."""

    markdown: str
    uri: str = "mcp://docs/agent-guide"
    name: str = "Agent guide"
    description: str = "Hard rules for agents using this MCP server"
    http_path: str = "/agent-guide.md"
    mime_type: str = "text/markdown"

    @classmethod
    def from_path(cls, path: str | Path, **kwargs: object) -> PlaybookSpec:
        text = Path(path).read_text(encoding="utf-8")
        return cls(markdown=text, **kwargs)  # type: ignore[arg-type]


def playbook_resource(spec: PlaybookSpec) -> types.Resource:
    return types.Resource(
        uri=spec.uri,  # type: ignore[arg-type]
        name=spec.name,
        description=spec.description,
        mimeType=spec.mime_type,
    )


def playbook_resource_contents(spec: PlaybookSpec) -> str:
    return spec.markdown


def playbook_http_route(spec: PlaybookSpec) -> Route:
    """Starlette/FastAPI-compatible route returning the playbook markdown."""

    async def _handler(_request: object) -> PlainTextResponse:
        return PlainTextResponse(spec.markdown, media_type=spec.mime_type)

    return Route(spec.http_path, endpoint=_handler, methods=["GET"])
