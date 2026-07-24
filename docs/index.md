# mcp-asgi-http

Mount an MCP server on an ASGI app over [Streamable HTTP](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports). Optional request auth. Works when ASGI lifespan is off (Mangum on Lambda).

```bash
pip install mcp-asgi-http
```

```python
from fastapi import FastAPI
from mcp_asgi_http import ApiKeyAuth, mount_mcp

api = FastAPI(redirect_slashes=False)
app = mount_mcp(api, server, auth=ApiKeyAuth(allowed_keys={"dev-secret"}))
```

## Where to go

- [Quickstart](guide/quickstart.md)
- [Auth](guide/auth.md)
- [Serverless](guide/serverless.md)
- [Samples](samples/index.md) (including live demos when deployed)
- [Blog](blog/index.md)

## Source

[github.com/johnny-rice/mcp-asgi-http](https://github.com/johnny-rice/mcp-asgi-http)
