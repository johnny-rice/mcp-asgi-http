# Catalog demo

Source: [`samples/catalog/`](https://github.com/johnny-rice/mcp-asgi-http/tree/main/samples/catalog)

Supporting enrich/playbook sample (prefer [clinical intel](clinical-intel.md) for a knowledge-style hero):

- Catalog UI
- Open MCP (`auth=None` for the public demo)
- Enrich hooks add `href` when `SITE_URL` is set
- Agent guide: MCP resource + `GET /agent-guide.md`

## Run locally

```bash
pip install -e '.[dev]'
cd samples/catalog
SITE_URL=http://127.0.0.1:8081 PYTHONPATH=../../src \
  uvicorn app:app --port 8081
```

## Live instance

| | |
|---|---|
| App | _(set after deploy)_ |
| MCP | `https://<host>/mcp` |
| Guide | `https://<host>/agent-guide.md` |
