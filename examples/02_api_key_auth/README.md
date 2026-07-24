# 02 — API key auth

Send `Authorization: Bearer <key>` or `X-API-Key: <key>`.

```bash
export MCP_API_KEY=dev-secret
python examples/02_api_key_auth/main.py
curl -sS -H "X-API-Key: $MCP_API_KEY" -H "Accept: application/json, text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl","version":"0"}}}' \
  http://127.0.0.1:8001/mcp
```
