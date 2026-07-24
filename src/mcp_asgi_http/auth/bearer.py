"""Shared Bearer / API-key header extraction."""

from __future__ import annotations


def extract_bearer(authorization: str | None) -> str | None:
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    return token.strip()


def extract_credential(authorization: str | None, api_key_header: str | None) -> str | None:
    return extract_bearer(authorization) or (api_key_header.strip() if api_key_header else None)


def looks_like_jwt(token: str) -> bool:
    parts = token.split(".")
    return len(parts) == 3 and all(parts)
