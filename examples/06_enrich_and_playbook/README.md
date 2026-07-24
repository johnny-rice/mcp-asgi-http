# 06 — Enrich + playbook

- Tool results get an `href` deep link via enrich hooks
- Agent guide is an MCP resource (`mcp://docs/agent-guide`) and `GET /agent-guide.md`

```bash
python examples/06_enrich_and_playbook/main.py
curl -sS http://127.0.0.1:8006/agent-guide.md
```
