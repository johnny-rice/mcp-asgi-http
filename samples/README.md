# Full stack samples

| Sample | Path | Notes |
|---|---|---|
| Ops dual-auth | [`ops-dual-auth/`](ops-dual-auth/) | **Hero** — DualAuth + ops REST twin |
| Clinical intel | [`clinical-intel/`](clinical-intel/) | **Hero** — fixtures, enrich, playbook |
| Catalog | [`catalog/`](catalog/) | Supporting enrich/playbook UI |
| Notes | [`notes/`](notes/) | Supporting API key + `once_ready` UI |

Each includes `Dockerfile`, `fly.toml`, and `render.yaml`. Build from the **repo root**:

```bash
docker build -f samples/ops-dual-auth/Dockerfile -t mcp-asgi-http-ops .
docker build -f samples/clinical-intel/Dockerfile -t mcp-asgi-http-clinical .
docker build -f samples/catalog/Dockerfile -t mcp-asgi-http-catalog .
docker build -f samples/notes/Dockerfile -t mcp-asgi-http-notes .
```

After you deploy, paste live URLs into the sample README and into `docs/samples/*.md`.
