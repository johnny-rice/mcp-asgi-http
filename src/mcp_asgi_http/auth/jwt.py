"""JWT authentication via JWKS (OIDC-compatible)."""

from __future__ import annotations

import logging
from functools import lru_cache

from mcp_asgi_http.auth.base import AuthContext, AuthenticationError
from mcp_asgi_http.auth.bearer import extract_credential, looks_like_jwt

logger = logging.getLogger(__name__)


@lru_cache(maxsize=8)
def _jwks_client(jwks_url: str):
    try:
        from jwt import PyJWKClient
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "JWT auth requires PyJWT; install with: pip install 'mcp-asgi-http[jwt]'"
        ) from exc
    return PyJWKClient(jwks_url, cache_keys=True)


class JwtAuth:
    """Validate bearer JWTs against a JWKS endpoint (issuer + audience)."""

    def __init__(
        self,
        *,
        issuer: str | None,
        audience: str | None,
        jwks_url: str | None = None,
    ) -> None:
        self.issuer = (issuer or "").rstrip("/") or None
        self.audience = audience or None
        if jwks_url:
            self.jwks_url = jwks_url
        elif self.issuer:
            # Common OIDC default; pass jwks_url explicitly for Okta (/v1/keys) etc.
            self.jwks_url = f"{self.issuer}/.well-known/jwks.json"
        else:
            self.jwks_url = None

    def configured(self) -> bool:
        return bool(self.issuer and self.audience and self.jwks_url)

    async def authenticate(
        self, authorization: str | None, api_key_header: str | None
    ) -> AuthContext:
        if not self.configured():
            raise AuthenticationError(
                "JWT auth requires issuer, audience, and a JWKS URL (or issuer-derived default)"
            )
        token = extract_credential(authorization, api_key_header)
        if not token:
            raise AuthenticationError("Missing Authorization bearer token")
        if not looks_like_jwt(token):
            raise AuthenticationError("Bearer token is not a JWT")
        return self._validate(token)

    def _validate(self, token: str) -> AuthContext:
        import jwt

        assert self.issuer and self.audience and self.jwks_url
        try:
            signing_key = _jwks_client(self.jwks_url).get_signing_key_from_jwt(token)
            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=self.audience,
                issuer=self.issuer,
                options={"require": ["exp", "iss", "aud"]},
            )
        except jwt.PyJWTError as exc:
            logger.info("JWT validation failed: %s", exc)
            raise AuthenticationError(f"Invalid JWT: {exc}") from exc

        subject = (
            payload.get("email")
            or payload.get("preferred_username")
            or payload.get("sub")
            or "jwt-user"
        )
        return AuthContext(subject=str(subject), method="jwt")
