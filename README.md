# mcp-asgi-http

Mount an MCP server on an ASGI app over [Streamable HTTP](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports). Includes optional request auth and helpers that work when ASGI lifespan is off (for example Mangum on Lambda).

**Docs and blog:** [johnny-rice.github.io/mcp-asgi-http](https://johnny-rice.github.io/mcp-asgi-http/)

```bash
pip install mcp-asgi-http
pip install 'mcp-asgi-http[jwt]'   # if you use JwtAuth / dual JWT
```

```python
from fastapi import FastAPI
from mcp.server import Server
from mcp_asgi_http import ApiKeyAuth, mount_mcp

server = Server("demo")
# register tools on server

api = FastAPI(redirect_slashes=False)
app = mount_mcp(
    api,
    server,
    auth=ApiKeyAuth(allowed_keys={"dev-secret"}),
    # auth=None if you authenticate in API Gateway or your own middleware
)
```

## Components

| Piece | Role |
|---|---|
| `StatelessMCPASGIApp` | Per-request Streamable HTTP (`stateless=True`, JSON responses) |
| `McpPathMiddleware` / `mount_mcp` | Route `/mcp` without Starlette Mount slash-redirect issues |
| Auth backends | `api_key`, `jwt`, `dual`, or `auth=None` |
| `once_ready` | Run lazy init once when lifespan is off |
| Enrich / playbook helpers | Optional deep-link hooks; markdown guide as MCP resource + HTTP route |

## Auth

| Mode | Behavior |
|---|---|
| `auth=None` / `build_auth_backend("none")` | No auth in this library (use your gateway or middleware) |
| `ApiKeyAuth` / `"api_key"` | `Authorization: Bearer` or `X-API-Key` |
| `JwtAuth` / `"jwt"` | Bearer JWT via JWKS (`issuer`, `audience`, optional `jwks_url`) |
| `DualAuth` / `"dual"` | API key first, then JWT |

## Related projects

These are different tools:

| Project | Difference |
|---|---|
| [FastMCP](https://github.com/jlowin/fastmcp) | Tool registration / DX. This package is for mounting and HTTP auth. |
| [AWS Serverless MCP Server](https://aws.amazon.com/blogs/compute/introducing-aws-serverless-mcp-server-ai-powered-development-for-modern-applications/) | MCP tools for SAM/Lambda development, not an ASGI mount library. |
| [invariantlabs-ai/mcp-streamable-http](https://github.com/invariantlabs-ai/mcp-streamable-http) | Transport examples. |
| [`mcp-streamablehttp-proxy`](https://pypi.org/project/mcp-streamablehttp-proxy/) / [`mcp-streamablehttp-client`](https://pypi.org/project/mcp-streamablehttp-client/) | stdio ↔ HTTP bridges. |

## Examples and samples

Short snippets: [`examples/`](examples/)

Full stack apps (Docker / Fly / Render): [`samples/`](samples/)

1. [`samples/ops-dual-auth`](samples/ops-dual-auth) - DualAuth + ops REST twin (hero)
2. [`samples/clinical-intel`](samples/clinical-intel) - fixtures + enrich + playbook (hero)
3. [`samples/catalog`](samples/catalog) - supporting enrich/playbook UI
4. [`samples/notes`](samples/notes) - supporting API-key + `once_ready` UI

## Development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
mkdocs serve   # local docs site
```

## License

Apache-2.0
