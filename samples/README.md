# Full stack samples

| Sample | Path | Notes |
|---|---|---|
| Notes | [`notes/`](notes/) | UI + REST + MCP with API key |
| Catalog | [`catalog/`](catalog/) | UI + open MCP + enrich + playbook |

Each includes `Dockerfile`, `fly.toml`, and `render.yaml`. Build from the **repo root**:

```bash
docker build -f samples/notes/Dockerfile -t mcp-asgi-http-notes .
docker build -f samples/catalog/Dockerfile -t mcp-asgi-http-catalog .
```

After you deploy, paste live URLs into the sample README and into `docs/samples/*.md`.
