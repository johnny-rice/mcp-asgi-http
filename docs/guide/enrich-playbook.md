# Enrich and playbook

## Enrich

Mutate tool JSON before returning it (for example add deep links):

```python
from mcp_asgi_http import tool_result_contents

def add_href(name: str, data: object) -> object:
    if name == "get_item" and isinstance(data, dict):
        data = dict(data)
        data["href"] = f"https://app.example.com/items/{data['id']}"
    return data

contents = tool_result_contents("get_item", {"id": 7}, hooks=[add_href])
```

## Playbook

Ship a markdown agent guide as an MCP resource and as a plain HTTP file:

```python
from mcp_asgi_http import PlaybookSpec, playbook_http_route, playbook_resource

spec = PlaybookSpec(markdown="# Rules\n\n1. Cite ids.\n")
# list_resources / read_resource -> playbook_resource(spec)
api.routes.append(playbook_http_route(spec))  # GET /agent-guide.md
```

See `examples/06_enrich_and_playbook/` and the [Catalog sample](../samples/catalog.md).
