"""Shared fixtures for mcp-asgi-http tests."""

from __future__ import annotations

from typing import Any

import mcp.types as types
import pytest
from mcp.server import Server


@pytest.fixture
def echo_server() -> Server[Any, Any]:
    """Minimal MCP server with one echo tool."""
    server = Server("test-echo")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="echo",
                description="Echo a message",
                inputSchema={
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                    "required": ["message"],
                },
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
        if name != "echo":
            raise ValueError(f"unknown tool: {name}")
        return [types.TextContent(type="text", text=str(arguments.get("message", "")))]

    return server
