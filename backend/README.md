AdolescentNCD Watch — Backend Proxy

This lightweight FastAPI proxy provides CORS-friendly endpoints for the frontend to fetch WHO GHO and World Bank data, with simple file-based caching.

Quick start (Windows / PowerShell):

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the app locally:

```powershell
uvicorn backend.app:APP --reload --host 127.0.0.1 --port 8000
```

4. Browse the frontend at: http://127.0.0.1:8000/adolescent-ncd-watch.html

Environment variables:
- `ALLOW_ORIGINS` — comma-separated origins allowed by CORS; default is `*`.
- `CACHE_TTL` — seconds to keep WHO / WB responses cached; default is `3600`.
- `AI_PROVIDER` — `openai`, `anthropic`, or `auto` (default).
- `OPENAI_API_KEY` — OpenAI key for live AI responses.
- `OPENAI_API_BASE` — optional custom OpenAI base URL.
- `OPENAI_MODEL` — optional OpenAI model, default `gpt-4.1-mini`.
- `ANTHROPIC_API_KEY` — Anthropic key for live AI responses.
- `ANTHROPIC_API_BASE` — optional Anthropic base URL.
- `ANTHROPIC_MODEL` — optional Anthropic model, default `claude-3.5-sonic`.

If you set `AI_PROVIDER=auto`, the backend uses OpenAI first if `OPENAI_API_KEY` exists, otherwise Anthropic if `ANTHROPIC_API_KEY` exists.

Endpoints:
- `GET /api/who/multi?indicator=...&countries=NGA,KEN&sex=BTSX` — proxied WHO multi-country OData
- `GET /api/who/{indicator}?country=NGA&sex=BTSX` — single-country
- `GET /api/wb/{indicator}?country=SSF` — World Bank proxy
- `POST /api/ai` — AI proxy endpoint; returns structured JSON when keys are configured

Notes:
- The backend serves the frontend and API from the same origin locally.
- For GitHub Pages, deploy the backend separately and set `ALLOW_ORIGINS` to your GitHub Pages origin.
- Cache TTL defaults to 3600s; set `CACHE_TTL` environment var to change.
- For production, deploy to Render/Railway and secure AI proxy keys using environment variables.
