"""Tests for authentication backends."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import jwt
import pytest

from mcp_asgi_http.auth import (
    ApiKeyAuth,
    AuthContext,
    AuthenticationError,
    DualAuth,
    JwtAuth,
    NoAuth,
    build_auth_backend,
)
from mcp_asgi_http.auth.bearer import looks_like_jwt


def test_looks_like_jwt() -> None:
    assert looks_like_jwt("aaa.bbb.ccc")
    assert not looks_like_jwt("dev-local-key")
    assert not looks_like_jwt("a.b")


@pytest.mark.asyncio
async def test_api_key_bearer_ok() -> None:
    auth = ApiKeyAuth(allowed_keys={"secret-key"})
    ctx = await auth.authenticate("Bearer secret-key", None)
    assert ctx.method == "api_key"
    assert ctx.subject.startswith("api-key:")


@pytest.mark.asyncio
async def test_api_key_header_ok() -> None:
    auth = ApiKeyAuth(allowed_keys={"secret-key"})
    ctx = await auth.authenticate(None, "secret-key")
    assert ctx.method == "api_key"


@pytest.mark.asyncio
async def test_api_key_invalid() -> None:
    auth = ApiKeyAuth(allowed_keys={"secret-key"})
    with pytest.raises(AuthenticationError):
        await auth.authenticate("Bearer wrong", None)


@pytest.mark.asyncio
async def test_no_auth() -> None:
    ctx = await NoAuth().authenticate(None, None)
    assert ctx.method == "none"
    assert ctx.subject == "anonymous"


@pytest.mark.asyncio
async def test_jwt_requires_config() -> None:
    auth = JwtAuth(issuer=None, audience=None)
    with pytest.raises(AuthenticationError):
        await auth.authenticate("Bearer a.b.c", None)


@pytest.mark.asyncio
async def test_jwt_validate_payload() -> None:
    auth = JwtAuth(
        issuer="https://auth.example.com/oauth2/default",
        audience="api://demo",
        jwks_url="https://auth.example.com/oauth2/default/v1/keys",
    )
    fake_key = MagicMock()
    fake_key.key = "unused"
    with (
        patch("mcp_asgi_http.auth.jwt._jwks_client") as jwks,
        patch("jwt.decode", return_value={"email": "user@example.com", "sub": "u1"}),
    ):
        jwks.return_value.get_signing_key_from_jwt.return_value = fake_key
        ctx = await auth.authenticate("Bearer aaa.bbb.ccc", None)
    assert ctx.method == "jwt"
    assert ctx.subject == "user@example.com"


@pytest.mark.asyncio
async def test_jwt_invalid_token() -> None:
    auth = JwtAuth(
        issuer="https://auth.example.com/oauth2/default",
        audience="api://demo",
        jwks_url="https://auth.example.com/oauth2/default/v1/keys",
    )
    fake_key = MagicMock()
    fake_key.key = "unused"
    with (
        patch("mcp_asgi_http.auth.jwt._jwks_client") as jwks,
        patch("jwt.decode", side_effect=jwt.InvalidTokenError("bad")),
    ):
        jwks.return_value.get_signing_key_from_jwt.return_value = fake_key
        with pytest.raises(AuthenticationError):
            await auth.authenticate("Bearer aaa.bbb.ccc", None)


@pytest.mark.asyncio
async def test_dual_prefers_api_key() -> None:
    dual = DualAuth(
        api_key_auth=ApiKeyAuth(allowed_keys={"secret-key"}),
        jwt_auth=JwtAuth(
            issuer="https://auth.example.com",
            audience="api://x",
            jwks_url="https://auth.example.com/keys",
        ),
    )
    ctx = await dual.authenticate("Bearer secret-key", None)
    assert ctx.method == "api_key"


@pytest.mark.asyncio
async def test_dual_falls_back_to_jwt() -> None:
    dual = DualAuth(
        api_key_auth=ApiKeyAuth(allowed_keys={"secret-key"}),
        jwt_auth=JwtAuth(
            issuer="https://auth.example.com",
            audience="api://x",
            jwks_url="https://auth.example.com/keys",
        ),
    )
    with patch.object(
        dual.jwt_auth,
        "authenticate",
        return_value=AuthContext(subject="u", method="jwt"),
    ):
        ctx = await dual.authenticate("Bearer aaa.bbb.ccc", None)
    assert ctx.method == "jwt"


def test_build_auth_backend_modes() -> None:
    assert build_auth_backend("none") is None
    assert build_auth_backend("consumer") is None
    assert isinstance(build_auth_backend("api_key", api_keys={"k"}), ApiKeyAuth)
    assert isinstance(
        build_auth_backend(
            "jwt",
            jwt_issuer="https://auth.example.com",
            jwt_audience="api://x",
        ),
        JwtAuth,
    )
    assert isinstance(
        build_auth_backend("dual", api_keys={"k"}, jwt_issuer="https://a", jwt_audience="x"),
        DualAuth,
    )
    with pytest.raises(ValueError):
        build_auth_backend("mystery")
