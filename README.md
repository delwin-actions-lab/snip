# snip

A URL shortener, and the delivery platform around it.

| Path | What |
|---|---|
| `services/api` | FastAPI HTTP API (Python, managed with uv) |
| `services/web` | Static frontend on unprivileged nginx |

## API, locally

```bash
cd services/api
uv sync
uv run pytest
uv run uvicorn snip_api.main:app --reload
```
