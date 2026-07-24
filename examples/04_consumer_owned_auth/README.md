# 04 — Consumer-owned auth

Put auth in API Gateway, a reverse proxy, or your own middleware. Pass `auth=None` to `mount_mcp` so the library does not double-gate.

```bash
export GATEWAY_KEY=gateway-secret
python examples/04_consumer_owned_auth/main.py
```
