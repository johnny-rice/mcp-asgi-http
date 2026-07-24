"""Pluggable authentication backends for MCP HTTP."""

from mcp_asgi_http.auth.api_key import ApiKeyAuth
from mcp_asgi_http.auth.base import AuthBackend, AuthContext, AuthenticationError
from mcp_asgi_http.auth.dual import DualAuth
from mcp_asgi_http.auth.jwt import JwtAuth
from mcp_asgi_http.auth.none import NoAuth

__all__ = [
    "ApiKeyAuth",
    "AuthBackend",
    "AuthContext",
    "AuthenticationError",
    "DualAuth",
    "JwtAuth",
    "NoAuth",
    "build_auth_backend",
]


def build_auth_backend(
    mode: str,
    *,
    api_keys: set[str] | None = None,
    jwt_issuer: str | None = None,
    jwt_audience: str | None = None,
    jwt_jwks_url: str | None = None,
) -> AuthBackend | None:
    """
    Build a backend from a mode string.

    Modes:
      - ``none`` / ``open``: return ``None`` (caller treats as no gate / consumer-owned)
      - ``api_key``: API key via Bearer or X-API-Key
      - ``jwt``: JWT via JWKS
      - ``dual``: API key fast-path, else JWT
    """
    normalized = (mode or "none").strip().lower()
    keys = api_keys or set()

    if normalized in ("none", "open", "consumer"):
        return None

    api_key_auth = ApiKeyAuth(allowed_keys=keys)
    jwt_auth = JwtAuth(issuer=jwt_issuer, audience=jwt_audience, jwks_url=jwt_jwks_url)

    if normalized == "jwt":
        return jwt_auth
    if normalized == "dual":
        return DualAuth(api_key_auth=api_key_auth, jwt_auth=jwt_auth)
    if normalized == "api_key":
        return api_key_auth
    raise ValueError(f"Unknown auth mode: {mode!r}")
