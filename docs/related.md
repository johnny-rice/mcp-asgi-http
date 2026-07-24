# Related work

| Project | Difference |
|---|---|
| [FastMCP](https://github.com/jlowin/fastmcp) | Tool registration / DX. This package mounts and authenticates HTTP. |
| [AWS Serverless MCP Server](https://aws.amazon.com/blogs/compute/introducing-aws-serverless-mcp-server-ai-powered-development-for-modern-applications/) | MCP tools for SAM/Lambda development, not an ASGI mount library. |
| [invariantlabs-ai/mcp-streamable-http](https://github.com/invariantlabs-ai/mcp-streamable-http) | Transport examples. |
| [`mcp-streamablehttp-proxy`](https://pypi.org/project/mcp-streamablehttp-proxy/) / [`mcp-streamablehttp-client`](https://pypi.org/project/mcp-streamablehttp-client/) | stdio ↔ HTTP bridges. |
| [CodeSignal: mount MCP in FastAPI](https://codesignal.com/learn/courses/advanced-mcp-server-and-agent-integration-in-python/lessons/mounting-an-mcp-server-in-a-fastapi-asgi-application) | Intro to `app.mount` + SSE. This package targets Streamable HTTP, auth, and Mangum. |

Official transport: [Streamable HTTP](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports).
