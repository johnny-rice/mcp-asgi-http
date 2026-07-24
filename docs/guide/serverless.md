# Serverless

When Mangum runs with `lifespan="off"`, FastAPI lifespan never runs. Use `once_ready` for lazy init (DB pool, caches).

```python
from mangum import Mangum
from mcp_asgi_http import ApiKeyAuth, mount_mcp, once_ready

async def warm() -> None:
    # open pool, warm caches, etc.
    ...

app = mount_mcp(
    api,
    server,
    auth=ApiKeyAuth(allowed_keys={"lambda-dev-key"}),
    on_ready=once_ready(warm),
)
handler = Mangum(app, lifespan="off")
```

Also set `redirect_slashes=False` on FastAPI. `mount_mcp` uses path middleware so `/mcp` does not hit Mount slash-redirect loops on Function URL.

See `examples/05_mangum_lambda/` and the [Notes sample](../samples/notes.md) Docker image.
