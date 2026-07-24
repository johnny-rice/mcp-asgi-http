# 04 Auth outside this library

Authenticate in API Gateway, a reverse proxy, or your own middleware. Pass `auth=None` to `mount_mcp`.

```bash
export GATEWAY_KEY=gateway-secret
python examples/04_consumer_owned_auth/main.py
```
