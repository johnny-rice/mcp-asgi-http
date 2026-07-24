# Ops dual-auth demo

Source: [`samples/ops-dual-auth/`](https://github.com/johnny-rice/mcp-asgi-http/tree/main/samples/ops-dual-auth)

Hero sample for platform engineers:

- REST UI for services, deploys, and freeze windows
- MCP at `/mcp` with **DualAuth** (API key fast-path; JWT when `JWT_*` is set)
- Enrich `href` deep links into the UI
- Agent playbook at `/agent-guide.md` and as an MCP resource

## Run locally

```bash
pip install -e '.[dev,jwt]'
cd samples/ops-dual-auth
MCP_API_KEY=demo-secret SITE_URL=http://127.0.0.1:8080 \
  PYTHONPATH=../../src uvicorn app:app --port 8080
```

## Live instance

Deploy with Docker + Fly or Render (configs in the sample folder). After deploy:

| | |
|---|---|
| App | _(set after deploy)_ |
| MCP | `https://<host>/mcp` |
| Auth | `X-API-Key: <MCP_API_KEY>` (and Bearer JWT when configured) |
