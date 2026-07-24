# Notes demo

Source: [`samples/notes/`](https://github.com/johnny-rice/mcp-asgi-http/tree/main/samples/notes)

Supporting sample (prefer [ops dual-auth](ops-dual-auth.md) as the hosted hero):

- Web UI for notes
- REST under `/api/notes`
- MCP at `/mcp` with API key auth (`MCP_API_KEY`)
- `once_ready` seed data

## Run locally

```bash
pip install -e '.[dev]'
cd samples/notes
MCP_API_KEY=demo-secret SITE_URL=http://127.0.0.1:8080 \
  PYTHONPATH=../../src uvicorn app:app --port 8080
```

## Live instance

Deploy with Docker + Fly or Render (configs in the sample folder). After deploy, record the URL:

| | |
|---|---|
| App | _(set after deploy)_ |
| MCP | `https://<host>/mcp` |
| Auth | `X-API-Key: <MCP_API_KEY>` |
