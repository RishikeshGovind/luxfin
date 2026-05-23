---
title: LuxFin Fiscal Early-Warning API
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: Heuristic fiscal stress API for Luxembourg communes (PhD research)
---

# LuxFin Fiscal Early-Warning API

FastAPI service for the LuxFin PhD research platform.

**Live heuristic endpoints (operational):**
- `GET /health` — service status, data vintage, panel info
- `GET /stress_score?year=2023` — heuristic composite stress score
- `GET /stress_history` — full 2014–2023 time series
- `GET /panel_summary` — 102-commune prototype panel statistics
- `GET /model_performance` — heuristic benchmark + planned ML metrics
- `GET /feature_importance` — component weights + planned XGBoost groups
- `GET /docs` — interactive Swagger UI

**Planned (WP3 — requires trained XGBoost model):**
- `POST /predict_distress`
- `POST /shap_explain`

Research platform: [rishikeshgovind.github.io/luxfin](https://rishikeshgovind.github.io/luxfin)
