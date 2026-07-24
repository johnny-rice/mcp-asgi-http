# 05 — Mangum + lifespan off

Pattern for AWS Lambda Function URL / API Gateway + Mangum when ASGI lifespan is disabled.

```python
handler = Mangum(app, lifespan="off")
# Lazy init via on_ready=once_ready(...)
```

Deploy as you would any Mangum app. Set Function URL auth to NONE if you use the library's API-key gate (or put auth in API Gateway and pass `auth=None`).
