"""Tiny shared MCP echo server for examples."""

from __future__ import annotations

from typing import Any

import mcp.types as types
from mcp.server import Server


def make_echo_server(name: str = "demo-echo") -> Server[Any, Any]:
    server = Server(name)

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="echo",
                description="Echo a message back",
                inputSchema={
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                    "required": ["message"],
                },
            )
        ]

    @server.call_tool()
    async def call_tool(tool_name: str, arguments: dict[str, Any]) -> list[types.TextContent]:
        if tool_name != "echo":
            raise ValueError(f"unknown tool: {tool_name}")
        return [types.TextContent(type="text", text=str(arguments.get("message", "")))]

    return server
