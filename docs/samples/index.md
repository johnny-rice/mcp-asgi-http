# Samples

Runnable apps under [`samples/`](https://github.com/johnny-rice/mcp-asgi-http/tree/main/samples) in the repo. Each has a Dockerfile so you can publish a live instance.

| Sample | What it shows | Live |
|---|---|---|
| [Notes](notes.md) | FastAPI + MCP + small web UI, API key auth | See sample README for URL after deploy |
| [Catalog](catalog.md) | Enrich hooks, agent playbook, public guide page | See sample README for URL after deploy |

Short snippets without a UI live under [`examples/`](https://github.com/johnny-rice/mcp-asgi-http/tree/main/examples).

## Deploy a live demo

Each sample includes:

- `Dockerfile`
- `render.yaml` (Render)
- `fly.toml` (Fly.io)

Pick one host, set `MCP_API_KEY` (and any other env vars), deploy, then paste the public `/mcp` URL into your MCP client.
