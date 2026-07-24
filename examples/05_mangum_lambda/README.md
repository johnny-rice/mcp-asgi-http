# 05 Mangum with lifespan off

For AWS Lambda Function URL / API Gateway + Mangum when ASGI lifespan is disabled.

```python
handler = Mangum(app, lifespan="off")
# Lazy init via on_ready=once_ready(...)
```

Deploy like any Mangum app. Use the library API-key gate, or put auth in API Gateway and pass `auth=None`.
