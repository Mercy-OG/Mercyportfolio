# AdolescentNCD Watch

A public-health dashboard and adolescent NCD risk screener built for Sub-Saharan Africa.

This repo contains:
- `adolescent-ncd-watch.html` — frontend dashboard and screener UI.
- `backend/app.py` — FastAPI proxy for WHO GHO and World Bank APIs, plus AI proxy support.
- `backend/requirements.txt` — backend dependencies.
- `backend/README.md` — backend-specific setup instructions.

## How it works

The frontend uses the backend to fetch live WHO and World Bank data, avoiding browser CORS restrictions. The backend caches responses in `backend/cache.json` and also proxies `/api/ai` requests to OpenAI or Anthropic when configured.

## Local setup

1. From repo root, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install backend dependencies:

```powershell
pip install -r backend\requirements.txt
```

3. Run the backend:

```powershell
uvicorn backend.app:APP --reload --host 127.0.0.1 --port 8000
```

4. Open the app in your browser:

```text
http://127.0.0.1:8000/adolescent-ncd-watch.html
```

## GitHub Pages + remote backend

If you host `adolescent-ncd-watch.html` on GitHub Pages, the frontend must call a separate deployed backend. Set the backend URL in the HTML constant at the top of `adolescent-ncd-watch.html` (`DEFAULT_BACKEND`) or add `?backend=https://your-backend-url` when testing.

The backend should be deployed to Render, Railway, or another Python host and configured to allow your GitHub Pages origin via `ALLOW_ORIGINS`.

## Environment variables

Set these in a `.env` file or in your deployment environment:

- `ALLOW_ORIGINS` — CORS origins allowed by the backend (default `*`).
- `CACHE_TTL` — seconds to cache WHO and World Bank responses (default `3600`).
- `AI_PROVIDER` — `openai`, `anthropic`, or `auto`.
- `OPENAI_API_KEY` — OpenAI API key for live AI responses.
- `OPENAI_API_BASE` — optional OpenAI base URL.
- `OPENAI_MODEL` — optional OpenAI model, default `gpt-4.1-mini`.
- `ANTHROPIC_API_KEY` — Anthropic API key for live AI responses.
- `ANTHROPIC_API_BASE` — optional Anthropic base URL.
- `ANTHROPIC_MODEL` — optional Anthropic model, default `claude-3.5-sonic`.

## Deployment notes

- For production, deploy the backend to Render, Railway, or Heroku.
- Host the frontend from the same backend origin when possible, or configure `ALLOW_ORIGINS` for your frontend host.
- Use the backend for all live WHO GHO calls to avoid browser CORS blocks.
- Store all API keys in environment variables; do not expose them in frontend code.

## Recommended production architecture

- Backend: `backend/app.py` served with Uvicorn.
- Frontend: `adolescent-ncd-watch.html` served from the same backend or a static host.
- AI: OpenAI/Anthropic proxied through `/api/ai`.
- Caching: `CACHE_TTL` prevents repeated WHO requests.

## Next improvements

- Add a data-refresh cron job to reload WHO/WB data periodically.
- Bake WHO/GBD data into JSON to reduce live dependency on remote APIs.
- Add a GitHub Pages frontend + separate backend origin if needed.
