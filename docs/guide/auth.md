# Auth

| Mode | Behavior |
|---|---|
| `auth=None` | No auth in this library. Use API Gateway or your middleware. |
| `ApiKeyAuth` | `Authorization: Bearer` or `X-API-Key` |
| `JwtAuth` | Bearer JWT via JWKS |
| `DualAuth` | API key first, then JWT |

## API key

```python
from mcp_asgi_http import ApiKeyAuth, mount_mcp

app = mount_mcp(
    api,
    server,
    auth=ApiKeyAuth(allowed_keys={"dev-secret"}),
)
```

## Dual JWT + API key

```python
from mcp_asgi_http import build_auth_backend, mount_mcp

auth = build_auth_backend(
    "dual",
    api_keys={"dev-secret"},
    jwt_issuer="https://auth.example.com/oauth2/default",
    jwt_audience="api://demo",
    jwt_jwks_url="https://auth.example.com/oauth2/default/v1/keys",  # optional
)
app = mount_mcp(api, server, auth=auth)
```

If `jwt_jwks_url` is omitted, the default is `{issuer}/.well-known/jwks.json`.

## Auth outside this library

Authenticate in a gateway or middleware, then pass `auth=None`:

```python
app = mount_mcp(api, server, auth=None)
```

See `examples/04_consumer_owned_auth/` in the repo.
