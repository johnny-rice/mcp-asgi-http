"""Fixture data for the ops dual-auth sample (synthetic only)."""

from __future__ import annotations

SERVICES = [
    {
        "id": "svc-api",
        "name": "Public API",
        "owner": "platform",
        "env": "prod",
        "status": "healthy",
        "version": "1.14.2",
    },
    {
        "id": "svc-worker",
        "name": "Async worker",
        "owner": "platform",
        "env": "prod",
        "status": "degraded",
        "version": "1.14.1",
    },
    {
        "id": "svc-search",
        "name": "Search indexer",
        "owner": "data",
        "env": "prod",
        "status": "healthy",
        "version": "0.9.0",
    },
]

FREEZE_WINDOWS = [
    {
        "id": "fz-q3-close",
        "name": "Q3 close freeze",
        "starts_at": "2026-09-25T00:00:00Z",
        "ends_at": "2026-09-30T23:59:59Z",
        "applies_to": ["svc-api", "svc-worker"],
        "active": True,
    },
    {
        "id": "fz-blackout",
        "name": "Holiday blackout",
        "starts_at": "2026-12-20T00:00:00Z",
        "ends_at": "2026-12-28T23:59:59Z",
        "applies_to": ["svc-api", "svc-worker", "svc-search"],
        "active": False,
    },
]

DEPLOYS = [
    {
        "id": "dep-901",
        "service_id": "svc-api",
        "version": "1.14.2",
        "status": "succeeded",
        "deployed_at": "2026-07-20T15:02:00Z",
        "actor": "ci-bot",
    },
    {
        "id": "dep-900",
        "service_id": "svc-worker",
        "version": "1.14.1",
        "status": "succeeded",
        "deployed_at": "2026-07-19T11:40:00Z",
        "actor": "a.nguyen",
    },
    {
        "id": "dep-899",
        "service_id": "svc-search",
        "version": "0.9.0",
        "status": "succeeded",
        "deployed_at": "2026-07-18T09:10:00Z",
        "actor": "ci-bot",
    },
]
