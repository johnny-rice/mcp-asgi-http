# Samples

Runnable apps under [`samples/`](https://github.com/johnny-rice/mcp-asgi-http/tree/main/samples) in the repo. Each has a Dockerfile so you can publish a live instance.

| Sample | What it shows | Role |
|---|---|---|
| [Ops dual-auth](ops-dual-auth.md) | DualAuth (API key + optional JWT), ops REST twin, freeze checks | **Hero** |
| [Clinical intel](clinical-intel.md) | Scientist knowledge UI, enrich hrefs, agent playbook (fixtures only) | **Hero** |
| [Catalog](catalog.md) | Enrich hooks + playbook on a small read model | Supporting |
| [Notes](notes.md) | Minimal UI + API key + `once_ready` | Supporting |

Short snippets without a UI live under [`examples/`](https://github.com/johnny-rice/mcp-asgi-http/tree/main/examples).

## Deploy a live demo

Each sample includes:

- `Dockerfile`
- `render.yaml` (Render)
- `fly.toml` (Fly.io)

Pick one host, set `MCP_API_KEY` (and any other env vars), deploy, then paste the public `/mcp` URL into your MCP client.
