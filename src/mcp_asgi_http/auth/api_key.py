"""API key authentication."""

from __future__ import annotations

from mcp_asgi_http.auth.base import AuthContext, AuthenticationError
from mcp_asgi_http.auth.bearer import extract_credential


class ApiKeyAuth:
    def __init__(self, *, allowed_keys: set[str]) -> None:
        self.allowed_keys = allowed_keys

    async def authenticate(
        self, authorization: str | None, api_key_header: str | None
    ) -> AuthContext:
        if not self.allowed_keys:
            raise AuthenticationError("API key auth is enabled but no keys are configured")

        token = extract_credential(authorization, api_key_header)
        if not token:
            raise AuthenticationError(
                "Missing API key; use Authorization: Bearer <key> or X-API-Key"
            )
        if token not in self.allowed_keys:
            raise AuthenticationError("Invalid API key")
        label = token if len(token) <= 12 else f"{token[:8]}…"
        return AuthContext(subject=f"api-key:{label}", method="api_key")

    def matches(self, token: str) -> bool:
        return token in self.allowed_keys
