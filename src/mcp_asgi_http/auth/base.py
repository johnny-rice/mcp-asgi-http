"""Authentication backend protocol."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class AuthenticationError(Exception):
    """Raised when credentials are missing or invalid."""


@dataclass(frozen=True)
class AuthContext:
    subject: str
    method: str


class AuthBackend(Protocol):
    async def authenticate(
        self, authorization: str | None, api_key_header: str | None
    ) -> AuthContext:
        """Validate credentials from Authorization and/or X-API-Key headers."""
        ...
