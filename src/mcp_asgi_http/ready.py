"""Readiness hooks for lifespan-off / serverless environments."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import TypeAlias

ReadyHook: TypeAlias = Callable[[], Awaitable[None]]


def once_ready(hook: ReadyHook) -> ReadyHook:
    """Wrap an async hook so it runs at most once (safe under concurrent requests)."""
    lock = asyncio.Lock()
    done = False

    async def _wrapped() -> None:
        nonlocal done
        if done:
            return
        async with lock:
            if done:
                return
            await hook()
            done = True

    return _wrapped
