# Pila API

The Pila API is a standalone Node.js and Express service. During the frontend-reproduction phase it exposes only operational endpoints and has no database dependency.

## Development

From the repository root:

```bash
pnpm dev:api
```

The API listens on port `4000` by default.

## Health check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "service": "pila-api",
  "timestamp": "2026-11-16T00:00:00.000Z"
}
```
