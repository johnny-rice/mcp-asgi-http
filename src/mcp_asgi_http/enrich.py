"""Generic MCP tool-result enrichment helpers."""

from __future__ import annotations

import copy
import json
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

import mcp.types as types

EnrichHook = Callable[[str, Any], Any]


def _as_jsonable(result: Any) -> Any:
    if hasattr(result, "model_dump"):
        return result.model_dump(mode="json")
    return copy.deepcopy(result)


def enrich_json_result(
    name: str,
    result: Any,
    *,
    hooks: Sequence[EnrichHook] | None = None,
) -> Any:
    """Convert a tool result to a JSON-serializable value and run optional hooks."""
    data = _as_jsonable(result)
    for hook in hooks or ():
        data = hook(name, data)
    return data


@dataclass(frozen=True)
class ImageAttachment:
    data_base64: str
    mime_type: str
    title: str | None = None


def tool_result_contents(
    name: str,
    result: Any,
    *,
    hooks: Sequence[EnrichHook] | None = None,
    images: Sequence[ImageAttachment] | None = None,
    indent: int = 2,
) -> list[types.TextContent | types.ImageContent]:
    """Build MCP content blocks: JSON text plus optional images."""
    payload = enrich_json_result(name, result, hooks=hooks)
    contents: list[types.TextContent | types.ImageContent] = [
        types.TextContent(type="text", text=json.dumps(payload, indent=indent, default=str))
    ]
    for image in images or ():
        meta = {"title": image.title} if image.title else None
        contents.append(
            types.ImageContent(
                type="image",
                data=image.data_base64,
                mimeType=image.mime_type,
                annotations=types.Annotations(audience=["user"], priority=0.8),
                _meta=meta,
            )
        )
    return contents
