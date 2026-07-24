"""Tests for ReadyHook helpers."""

from __future__ import annotations

import asyncio

import pytest

from mcp_asgi_http.ready import once_ready


@pytest.mark.asyncio
async def test_once_ready_runs_once() -> None:
    calls = 0

    async def hook() -> None:
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.01)

    wrapped = once_ready(hook)
    await asyncio.gather(wrapped(), wrapped(), wrapped())
    assert calls == 1
