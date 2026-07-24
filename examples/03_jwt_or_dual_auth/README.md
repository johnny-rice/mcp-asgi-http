# 03 — Dual JWT + API key

Accepts a known API key **or** a JWT validated against JWKS.

```bash
export MCP_API_KEY=dev-secret
export JWT_ISSUER=https://auth.example.com/oauth2/default
export JWT_AUDIENCE=api://demo
# Optional; defaults to {issuer}/.well-known/jwks.json
# Okta-style: export JWT_JWKS_URL=$JWT_ISSUER/v1/keys
python examples/03_jwt_or_dual_auth/main.py
```
