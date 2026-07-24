"""Tests for enrich helpers."""

from __future__ import annotations

from mcp_asgi_http.enrich import ImageAttachment, enrich_json_result, tool_result_contents


def test_enrich_json_result_hooks() -> None:
    def add_link(name: str, data: object) -> object:
        assert isinstance(data, dict)
        data = dict(data)
        data["href"] = f"https://app.example.com/items/{data['id']}"
        return data

    out = enrich_json_result("get_item", {"id": 7, "name": "x"}, hooks=[add_link])
    assert out["href"] == "https://app.example.com/items/7"


def test_enrich_model_dump() -> None:
    class Model:
        def model_dump(self, *, mode: str = "python") -> dict[str, str]:
            return {"hello": "world"}

    assert enrich_json_result("t", Model()) == {"hello": "world"}


def test_tool_result_contents_with_image() -> None:
    contents = tool_result_contents(
        "get_item",
        {"id": 1},
        images=[
            ImageAttachment(
                data_base64="aaa",
                mime_type="image/png",
                title="preview",
            )
        ],
    )
    assert contents[0].type == "text"
    assert '"id": 1' in contents[0].text
    assert contents[1].type == "image"
    assert contents[1].mimeType == "image/png"
