# Notes demo

Full stack sample: web UI + REST + MCP Streamable HTTP at `/mcp`.

## Local

From the repo root:

```bash
pip install -e '.[dev]'
cd samples/notes
MCP_API_KEY=demo-secret SITE_URL=http://127.0.0.1:8080 \
  PYTHONPATH=../../src uvicorn app:app --host 127.0.0.1 --port 8080
```

Open http://127.0.0.1:8080. Point an MCP client at `http://127.0.0.1:8080/mcp` with header `X-API-Key: demo-secret`.

## Docker

From the repo root:

```bash
docker build -f samples/notes/Dockerfile -t mcp-asgi-http-notes .
docker run --rm -p 8080:8080 \
  -e MCP_API_KEY=demo-secret \
  -e SITE_URL=http://127.0.0.1:8080 \
  mcp-asgi-http-notes
```

## Live deploy

- **Fly.io:** `fly launch --config samples/notes/fly.toml` then `fly secrets set MCP_API_KEY=... SITE_URL=https://<app>.fly.dev`
- **Render:** use `samples/notes/render.yaml` (set `SITE_URL` to the Render URL after first deploy)

After deploy, put the public URL here and on the docs samples page:

```
LIVE_URL=
MCP_URL=/mcp
```
