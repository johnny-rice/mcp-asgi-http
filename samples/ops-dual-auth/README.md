# Ops dual-auth demo

Hero sample: internal-ops REST UI + MCP Streamable HTTP at `/mcp` with **DualAuth**
(API key for agents, JWT when `JWT_*` is configured).

Synthetic fixture data only (services, deploys, freeze windows).

## Local

From the repo root:

```bash
pip install -e '.[dev,jwt]'
cd samples/ops-dual-auth
MCP_API_KEY=demo-secret SITE_URL=http://127.0.0.1:8080 \
  PYTHONPATH=../../src uvicorn app:app --host 127.0.0.1 --port 8080
```

Open http://127.0.0.1:8080. Point an MCP client at `http://127.0.0.1:8080/mcp` with
`X-API-Key: demo-secret`.

Optional human JWT path:

```bash
export JWT_ISSUER=https://example.okta.com/oauth2/default
export JWT_AUDIENCE=api://ops-demo
export JWT_JWKS_URL=https://example.okta.com/oauth2/default/v1/keys
```

## Docker

From the repo root:

```bash
docker build -f samples/ops-dual-auth/Dockerfile -t mcp-asgi-http-ops .
docker run --rm -p 8080:8080 \
  -e MCP_API_KEY=demo-secret \
  -e SITE_URL=http://127.0.0.1:8080 \
  mcp-asgi-http-ops
```

## Live deploy

- **Fly.io:** `fly launch --config samples/ops-dual-auth/fly.toml` then
  `fly secrets set MCP_API_KEY=... SITE_URL=https://<app>.fly.dev`
- **Render:** use `samples/ops-dual-auth/render.yaml`

After deploy, put the public URL here and on the docs samples page:

```
LIVE_URL=
MCP_URL=/mcp
```
