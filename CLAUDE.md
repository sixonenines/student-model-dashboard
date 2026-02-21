# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run

### v2 (Microservice Architecture — recommended)

```bash
cd v2 && docker compose up --build
# Frontend: http://localhost:3000
# Python backend health: http://localhost:3000/api/python/health
# R backend health: http://localhost:3000/api/r/health
```

For local frontend development (requires backends running):
```bash
cd v2/frontend && npm install && npm run dev
```

### v1 (Legacy Streamlit — preserved in root)

```bash
docker build . -t studentmodeldash
docker run -it -p 8501:8501 studentmodeldash
```

## Architecture

### v2 — Microservice Architecture (`v2/`)

Three services orchestrated via Docker Compose:

1. **Python Backend** (FastAPI, port 8000) — `v2/python-backend/`
   - `app/main.py` — FastAPI app with CORS
   - `app/routers/training.py` — `POST /api/validate`, `POST /api/train`
   - `app/services/model_trainer.py` — sklearn LogisticRegression, 10-fold CV, 80/20 split metrics
   - `app/services/feature_engineering.py` — data cleaning and column renaming
   - `app/services/data_validator.py` — validates 7 required columns + dtypes
   - `app/schemas/responses.py` — Pydantic models for all responses

2. **R Backend** (Plumber, port 8001) — `v2/r-backend/`
   - `plumber.R` — Plumber API: `GET /api/health`, `POST /api/train`
   - `train_model.R` — unified `train_model(filepath, model_type)` function (replaces 3 separate scripts)
   - Trains one model per request; frontend parallelizes

3. **Frontend** (React + Vite + TypeScript + Tailwind, port 3000) — `v2/frontend/`
   - `src/App.tsx` — main layout
   - `src/hooks/useTraining.ts` — manages training state, concurrent API calls
   - `src/api/pythonApi.ts` / `rApi.ts` — API clients
   - `src/lib/zipBuilder.ts` — client-side ZIP generation with JSZip
   - `nginx.conf` — serves SPA, proxies `/api/python/` → python-backend, `/api/r/` → r-backend

### API Contracts

**Python `POST /api/train`** — multipart form (file + model_types JSON string), returns all models:
```json
{ "models": { "AFM": { "stats": {...}, "coefficients": [...], "predictions": [...] } } }
```

**R `POST /api/train`** — multipart form (file + model_type string), returns one model:
```json
{ "stats": {...}, "coefficients": [...], "predictions": [...] }
```

### v1 — Streamlit Monolith (root)

- **`app.py`** — Main Streamlit entry point
- **`PythonModelScripts.py`** — Python model training
- **`AFM_Script.R` / `PFM_Script.R` / `IFM_Script.R`** — R model scripts

### Required Input Columns
`AnonStudentId`, `First Attempt`, `Corrects`, `Incorrects`, `Opportunity`, `Hints`, `KC (Default)`

### Three Model Types
- **AFM** (Additive Factors Model)
- **PFM** (Performance Factors Model)
- **IFM** (Individualized Factors Model)

## Conventions

- Python outputs prefixed with `Py_`, R outputs with `R_`
- v2 services are stateless (no file persistence between requests)
- ZIP generation is client-side in v2 (JSZip)
- Frontend proxies: `/api/python/*` → python-backend:8000, `/api/r/*` → r-backend:8001
