# Clinical intel demo

Source: [`samples/clinical-intel/`](https://github.com/johnny-rice/mcp-asgi-http/tree/main/samples/clinical-intel)

Scientist-facing sample with **synthetic** CT.gov-shaped fixtures only:

- REST search UI for trials, companies, and targets
- MCP tools: `search_trials`, `get_trial`, `list_companies`, `get_company`, `get_target`
- Enrich `href` deep links + agent playbook
- API key auth (`MCP_API_KEY`)

## Run locally

```bash
pip install -e '.[dev]'
cd samples/clinical-intel
MCP_API_KEY=demo-secret SITE_URL=http://127.0.0.1:8081 \
  PYTHONPATH=../../src uvicorn app:app --port 8081
```

## Live instance

Deploy with Docker + Fly or Render (configs in the sample folder). After deploy:

| | |
|---|---|
| App | _(set after deploy)_ |
| MCP | `https://<host>/mcp` |
| Auth | `X-API-Key: <MCP_API_KEY>` |
