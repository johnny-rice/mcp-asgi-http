---
draft: false
date: 2026-07-23
categories:
  - mcp
  - asgi
---

# Why mcp-asgi-http exists

The official MCP Python SDK and FastMCP can expose Streamable HTTP. Tutorials show `app.mount("/mcp", ...)`. That is enough for local demos.

Problems show up when you put the same pattern on Mangum with `lifespan="off"`, share auth with a REST API, or hit Function URL slash redirects. This package is the small set of helpers we kept rewriting for that case:

1. Stateless Streamable HTTP ASGI app (JSON responses, no session store)
2. Path middleware instead of `Mount` for `/mcp`
3. Optional API key / JWT / dual auth, or `auth=None` if the gateway already authenticated
4. `once_ready` for lazy init when lifespan never runs

It is not a tool framework. Register tools with the official SDK (or FastMCP). Use this to mount and protect `/mcp` next to your existing API.

<!-- more -->

## What this is not

- Not [AWS Serverless MCP Server](https://aws.amazon.com/blogs/compute/introducing-aws-serverless-mcp-server-ai-powered-development-for-modern-applications/) (that product is guidance tools for SAM/Lambda).
- Not an SSE mount tutorial. Prefer Streamable HTTP for new remote servers.
- Not a stdio proxy. See `mcp-streamablehttp-proxy` if you need that bridge.

## Try it

```bash
pip install mcp-asgi-http
```

Or run a [fullstack sample](../../samples/index.md) and point Cursor / Claude at the public `/mcp` URL.
