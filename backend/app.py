from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import time
import json
import os
import re
from typing import Optional

APP = FastAPI(title="AdolescentNCD Watch API Proxy")

allowed_origins = [o.strip() for o in os.environ.get("ALLOW_ORIGINS", "*").split(",") if o.strip()]
if allowed_origins == ["*"]:
    allow_origins = ["*"]
else:
    allow_origins = allowed_origins

APP.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CACHE_FILE = os.path.join(os.path.dirname(__file__), 'cache.json')
CACHE_TTL = int(os.environ.get('CACHE_TTL', '3600'))  # seconds

AI_PROVIDER = os.environ.get('AI_PROVIDER', 'auto').strip().lower()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
OPENAI_API_BASE = os.environ.get('OPENAI_API_BASE', 'https://api.openai.com/v1').rstrip('/')
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4.1-mini')
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
ANTHROPIC_API_BASE = os.environ.get('ANTHROPIC_API_BASE', 'https://api.anthropic.com/v1').rstrip('/')
ANTHROPIC_MODEL = os.environ.get('ANTHROPIC_MODEL', 'claude-3.5-sonic')

WHO_BASE = 'https://ghoapi.azureedge.net/api'
WB_BASE = 'https://api.worldbank.org/v2'


def load_cache():
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_cache(c):
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(c, f)
    except Exception:
        pass


def cached_get(key: str, fetch_fn):
    cache = load_cache()
    entry = cache.get(key)
    now = int(time.time())
    if entry and now - entry.get('ts', 0) < CACHE_TTL:
        return entry.get('data')
    data = fetch_fn()
    cache[key] = {'ts': now, 'data': data}
    save_cache(cache)
    return data


def extract_json(text: str):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if not match:
            raise
        return json.loads(match.group(0))


def get_openai_response(prompt: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError('OpenAI API key is not configured')

    url = f"{OPENAI_API_BASE}/chat/completions"
    payload = {
        'model': OPENAI_MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.2,
        'max_tokens': 400,
    }
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    response = requests.post(url, json=payload, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content']


def get_anthropic_response(prompt: str) -> str:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError('Anthropic API key is not configured')

    url = f"{ANTHROPIC_API_BASE}/chat/completions"
    payload = {
        'model': ANTHROPIC_MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.2,
        'max_tokens_to_sample': 400,
    }
    headers = {
        'x-api-key': ANTHROPIC_API_KEY,
        'Content-Type': 'application/json',
    }
    response = requests.post(url, json=payload, headers=headers, timeout=20)
    response.raise_for_status()
    data = response.json()
    return data['choices'][0]['message']['content']


def get_ai_response(prompt: str) -> str:
    provider = AI_PROVIDER
    if provider == 'auto':
        if OPENAI_API_KEY:
            provider = 'openai'
        elif ANTHROPIC_API_KEY:
            provider = 'anthropic'
        else:
            provider = 'none'

    if provider == 'openai':
        return get_openai_response(prompt)
    if provider == 'anthropic':
        return get_anthropic_response(prompt)
    raise RuntimeError('No AI provider configured. Set OPENAI_API_KEY or ANTHROPIC_API_KEY.')


@APP.get('/api/who/multi')
def who_multi(indicator: str = Query(..., description='WHO indicator code'), countries: str = Query(..., description='Comma-separated ISO3 list'), sex: Optional[str] = Query('BTSX')):
    if not countries.strip():
        raise HTTPException(status_code=400, detail='No countries')

    iso_list = "'" + "','".join([c.strip().upper() for c in countries.split(',') if c.strip()]) + "'"
    filter_q = f"SpatialDimType eq 'COUNTRY' and SpatialDim in ({iso_list})"
    if sex and sex != 'ALL':
        filter_q += f" and Dim1 eq '{sex}'"
    url = f"{WHO_BASE}/{indicator}?$filter={filter_q}&$orderby=TimeDim desc&$top=200"

    def fetch():
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        return r.json()

    key = f"who_multi:{indicator}:{countries}:{sex}"
    return cached_get(key, fetch)


@APP.get('/api/who/{indicator}')
def who_indicator(indicator: str, country: str = Query(...), sex: Optional[str] = Query('BTSX')):
    filter_q = f"SpatialDimType eq 'COUNTRY' and SpatialDim eq '{country.upper()}'"
    if sex and sex != 'ALL':
        filter_q += f" and Dim1 eq '{sex}'"
    url = f"{WHO_BASE}/{indicator}?$filter={filter_q}&$orderby=TimeDim desc&$top=20"

    def fetch():
        r = requests.get(url, timeout=12)
        r.raise_for_status()
        return r.json()

    key = f"who:{indicator}:{country}:{sex}"
    return cached_get(key, fetch)


@APP.get('/api/wb/{indicator}')
def wb_indicator(indicator: str, country: str = Query('SSF')):
    url = f"{WB_BASE}/country/{country}/indicator/{indicator}?format=json&mrv=5&per_page=5"

    def fetch():
        r = requests.get(url, timeout=12)
        r.raise_for_status()
        return r.json()

    key = f"wb:{indicator}:{country}"
    return cached_get(key, fetch)


class AIPayload(BaseModel):
    prompt: str


FALLBACK_RESPONSE = {
    'riskLevel': 'Moderate',
    'riskFactors': ['High sedentary time', 'Dietary quality concerns'],
    'protectiveFactors': ['Young age'],
    'summary': 'Your responses show some lifestyle areas to improve; increasing activity and diet quality reduces long-term risk.',
    'actions': ['Aim for 60 min of moderate activity daily', 'Add one fruit or vegetable to each meal', 'Obtain an annual blood pressure check at a clinic'],
}


@APP.post('/api/ai')
def ai_proxy(payload: AIPayload):
    try:
        content = get_ai_response(payload.prompt)
        parsed = extract_json(content)
        if not isinstance(parsed, dict):
            raise ValueError('AI response was not a JSON object')
        return parsed
    except Exception as exc:
        print('AI proxy error:', exc)
        return FALLBACK_RESPONSE


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
APP.mount('/', StaticFiles(directory=ROOT_DIR, html=True), name='static')
