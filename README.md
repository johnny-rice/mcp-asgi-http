# mcp-asgi-http

**ASGI glue for remote MCP** — mount [Streamable HTTP](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports) beside your API, with pluggable auth that works under serverless (`Mangum` + `lifespan="off"`).

```bash
pip install mcp-asgi-http
# JWT backends:
pip install 'mcp-asgi-http[jwt]'
```

```python
from fastapi import FastAPI
from mcp.server import Server
from mcp_asgi_http import ApiKeyAuth, mount_mcp

server = Server("demo")
# ... register tools on server ...

api = FastAPI(redirect_slashes=False)
app = mount_mcp(
    api,
    server,
    auth=ApiKeyAuth(allowed_keys={"dev-secret"}),  # or auth=None for consumer-owned auth
)
```

## What you get

| Piece | Purpose |
|---|---|
| `StatelessMCPASGIApp` | Per-request Streamable HTTP (`stateless=True`, JSON responses) |
| `McpPathMiddleware` / `mount_mcp` | `/mcp` dispatch without Mount slash-redirect loops |
| Pluggable auth | Built-in `api_key` / `jwt` / `dual`, or `auth=None` if you gate upstream |
| `once_ready` | Lazy init when ASGI lifespan is off (Lambda) |
| Enrich + playbook helpers | Deep-link hooks; agent-guide as MCP resource + HTTP twin |

## Auth modes

| Mode | Behavior |
|---|---|
| `auth=None` / `build_auth_backend("none")` | No library gate — **consumer-owned** (API Gateway, your middleware) |
| `ApiKeyAuth` / `"api_key"` | `Authorization: Bearer` or `X-API-Key` |
| `JwtAuth` / `"jwt"` | Bearer JWT via JWKS (`issuer` + `audience`; optional `jwks_url`) |
| `DualAuth` / `"dual"` | API key fast-path, else JWT |

## Not these projects

This library is **not**:

- [FastMCP](https://github.com/jlowin/fastmcp) — use FastMCP (or the official SDK) for tool DX; use this to mount/ops
- [AWS Serverless MCP Server](https://aws.amazon.com/blogs/compute/introducing-aws-serverless-mcp-server-ai-powered-development-for-modern-applications/) — that is an MCP *tool server* for SAM/Lambda guidance
- [invariantlabs-ai/mcp-streamable-http](https://github.com/invariantlabs-ai/mcp-streamable-http) — transport *examples*, not a mount library
- [`mcp-streamablehttp-proxy`](https://pypi.org/project/mcp-streamablehttp-proxy/) / [`-client`](https://pypi.org/project/mcp-streamablehttp-client/) — stdio↔HTTP bridges

Lambda / Function URL is a **supported deploy target**, not the product name.

## Examples

See [`examples/`](examples/):

1. FastAPI minimal  
2. API key auth  
3. Dual JWT + API key  
4. Consumer-owned auth (`auth=None`)  
5. Mangum `lifespan="off"` + `once_ready`  
6. Enrich hooks + agent playbook  

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
```

## License

Apache-2.0
