"""Dual authentication: API key (fast path) or JWT."""

from __future__ import annotations

from mcp_asgi_http.auth.api_key import ApiKeyAuth
from mcp_asgi_http.auth.base import AuthContext, AuthenticationError
from mcp_asgi_http.auth.bearer import extract_credential, looks_like_jwt
from mcp_asgi_http.auth.jwt import JwtAuth


class DualAuth:
    """Accept a known API key or a valid JWT on the same endpoints."""

    def __init__(self, *, api_key_auth: ApiKeyAuth, jwt_auth: JwtAuth) -> None:
        self.api_key_auth = api_key_auth
        self.jwt_auth = jwt_auth

    async def authenticate(
        self, authorization: str | None, api_key_header: str | None
    ) -> AuthContext:
        token = extract_credential(authorization, api_key_header)
        if not token:
            raise AuthenticationError(
                "Missing credentials; use Authorization: Bearer <api-key|jwt> or X-API-Key"
            )

        if self.api_key_auth.allowed_keys and self.api_key_auth.matches(token):
            return await self.api_key_auth.authenticate(authorization, api_key_header)

        if looks_like_jwt(token) and self.jwt_auth.configured():
            return await self.jwt_auth.authenticate(authorization, api_key_header)

        if looks_like_jwt(token) and not self.jwt_auth.configured():
            raise AuthenticationError(
                "JWT presented but JWT auth is not configured (set issuer, audience, jwks_url)"
            )

        if self.api_key_auth.allowed_keys:
            raise AuthenticationError("Invalid API key")

        raise AuthenticationError(
            "Dual auth requires API keys and/or JWT issuer + audience (+ JWKS)"
        )
