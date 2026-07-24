"""Anonymous auth (no credential checks)."""

from __future__ import annotations

from mcp_asgi_http.auth.base import AuthContext


class NoAuth:
    """Accept every request as anonymous. Prefer api_key/jwt/dual in production."""

    async def authenticate(
        self, authorization: str | None, api_key_header: str | None
    ) -> AuthContext:
        return AuthContext(subject="anonymous", method="none")
