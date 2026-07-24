# Catalog demo

Web UI + open MCP (`auth=None`) + enrich hooks + `/agent-guide.md` playbook.

## Local

```bash
pip install -e '.[dev]'
cd samples/catalog
SITE_URL=http://127.0.0.1:8081 PYTHONPATH=../../src \
  uvicorn app:app --host 127.0.0.1 --port 8081
```

- UI: http://127.0.0.1:8081
- MCP: http://127.0.0.1:8081/mcp
- Guide: http://127.0.0.1:8081/agent-guide.md

## Docker

```bash
docker build -f samples/catalog/Dockerfile -t mcp-asgi-http-catalog .
docker run --rm -p 8081:8080 -e SITE_URL=http://127.0.0.1:8081 mcp-asgi-http-catalog
```

## Live deploy

Same pattern as the notes sample (`fly.toml`, `render.yaml`). Set `SITE_URL` to the public origin so `href` fields resolve.

```
LIVE_URL=
```
