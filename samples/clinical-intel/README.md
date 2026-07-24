# Clinical intel demo

Scientist-facing sample: synthetic CT.gov-shaped fixtures, REST UI, MCP at `/mcp`,
enrich `href` deep links, and an agent playbook (`/agent-guide.md`).

**Fixtures only.** No real trial IDs, company pipelines, or proprietary data.

## Local

From the repo root:

```bash
pip install -e '.[dev]'
cd samples/clinical-intel
MCP_API_KEY=demo-secret SITE_URL=http://127.0.0.1:8081 \
  PYTHONPATH=../../src uvicorn app:app --host 127.0.0.1 --port 8081
```

Open http://127.0.0.1:8081. Point an MCP client at `http://127.0.0.1:8081/mcp`
with `X-API-Key: demo-secret`.

## Docker

From the repo root:

```bash
docker build -f samples/clinical-intel/Dockerfile -t mcp-asgi-http-clinical .
docker run --rm -p 8081:8080 \
  -e MCP_API_KEY=demo-secret \
  -e SITE_URL=http://127.0.0.1:8081 \
  mcp-asgi-http-clinical
```

## Live deploy

- **Fly.io:** `fly launch --config samples/clinical-intel/fly.toml` then
  `fly secrets set MCP_API_KEY=... SITE_URL=https://<app>.fly.dev`
- **Render:** use `samples/clinical-intel/render.yaml`

After deploy:

```
LIVE_URL=
MCP_URL=/mcp
```
