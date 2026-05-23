"""
LuxFin Fiscal Early-Warning API — Hugging Face Spaces deployment
----------------------------------------------------------------
Identical logic to api/fiscal_ml_api.py.
Two differences:
  - ROOT points to /app (Docker workdir), not the repo root
  - CORS allows the GitHub Pages frontend explicitly
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── Data loading ──────────────────────────────────────────────────────────────
ROOT = Path("/app")
_banking  = json.loads((ROOT / "data" / "banking.json").read_text())
_fiscal   = json.loads((ROOT / "data" / "fiscal.json").read_text())
_communes = json.loads((ROOT / "data" / "communes.json").read_text())

BANKING         = _banking["annual"]
FISCAL          = _fiscal["annual"]
AVAILABLE_YEARS = BANKING["years"]

_COMPONENTS = [
    {"id": "bond_concentration", "label": "Bond Concentration",
     "desc": "Govt bond holdings as % of total bank assets",
     "unit": "%", "weight": 0.30, "low": 3.0,  "high": 10.0, "invert": False},
    {"id": "credit_govt_share",  "label": "Public Credit Share",
     "desc": "Credit to general government as % of total credit",
     "unit": "%", "weight": 0.30, "low": 6.0,  "high": 16.0, "invert": False},
    {"id": "fiscal_balance",     "label": "Fiscal Balance",
     "desc": "General government balance (% of GDP). Surplus = low stress",
     "unit": "% GDP", "weight": 0.25, "low": -3.0, "high": 3.0, "invert": True},
    {"id": "sector_size",        "label": "Banking Sector Size",
     "desc": "Total bank assets as multiple of nominal GDP",
     "unit": "x GDP", "weight": 0.15, "low": 8.0,  "high": 16.0, "invert": False},
]


def _stress_level(score: float) -> str:
    if score < 0.25: return "low"
    if score < 0.50: return "moderate"
    if score < 0.75: return "elevated"
    return "high"


def _compute_year(year: int) -> dict:
    idx = BANKING["years"].index(year)
    b, f = BANKING, FISCAL
    bond_conc  = (b["govt_bonds_held"][idx] / b["total_assets"][idx]) * 100
    credit_shr = (b["credit_govt"][idx] / (b["credit_govt"][idx] + b["credit_private"][idx])) * 100
    fiscal_bal = f["balance_pct_gdp"][idx]
    sector_sz  = b["total_assets"][idx] / f["gdp_eur_bn"][idx]
    raws = {
        "bond_concentration": bond_conc,
        "credit_govt_share":  credit_shr,
        "fiscal_balance":     fiscal_bal,
        "sector_size":        sector_sz,
    }
    components = []
    for comp in _COMPONENTS:
        raw  = raws[comp["id"]]
        lo, hi = comp["low"], comp["high"]
        norm = max(0.0, min(1.0, (raw - lo) / (hi - lo)))
        if comp["invert"]:
            norm = 1.0 - norm
        components.append({
            "id":           comp["id"],
            "label":        comp["label"],
            "description":  comp["desc"],
            "unit":         comp["unit"],
            "weight":       comp["weight"],
            "raw_value":    round(raw, 3),
            "normalised":   round(norm, 3),
            "contribution": round(norm * comp["weight"], 4),
        })
    composite = sum(c["contribution"] for c in components)
    return {
        "year":       year,
        "composite":  round(composite, 4),
        "level":      _stress_level(composite),
        "components": components,
        "inputs": {
            "total_assets_bn":    b["total_assets"][idx],
            "credit_govt_bn":     b["credit_govt"][idx],
            "credit_private_bn":  b["credit_private"][idx],
            "govt_bonds_held_bn": b["govt_bonds_held"][idx],
            "gdp_eur_bn":         f["gdp_eur_bn"][idx],
            "fiscal_balance_pct": f["balance_pct_gdp"][idx],
        },
    }


_SCORES = {y: _compute_year(y) for y in AVAILABLE_YEARS}

_PANEL_PATH = ROOT / "data" / "panel_dataset.csv"

def _load_panel() -> list[dict] | None:
    if not _PANEL_PATH.exists():
        return None
    with open(_PANEL_PATH, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))

_PANEL = _load_panel()

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title="LuxFin Fiscal Early-Warning API",
    description=(
        "Heuristic stress index (live) and planned XGBoost commune distress model (WP3). "
        "See /docs for interactive Swagger UI."
    ),
    version="0.2.0-heuristic",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://rishikeshgovind.github.io",
        "http://localhost:8080",
        "http://localhost:3000",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Schemas ───────────────────────────────────────────────────────────────────
class DistressRequest(BaseModel):
    commune_ids: list[str]
    year: Optional[int] = None

class ShapRequest(BaseModel):
    commune_ids: list[str]
    year: Optional[int] = None


# ── Live heuristic endpoints ──────────────────────────────────────────────────

@app.get("/health")
def health():
    latest = AVAILABLE_YEARS[-1]
    s = _SCORES[latest]
    return {
        "status":          "operational",
        "model_layer":     "heuristic-baseline",
        "model_loaded":    True,
        "data_vintage":    _banking["metadata"]["last_updated"],
        "available_years": AVAILABLE_YEARS,
        "latest_year":     latest,
        "latest_stress":   {"composite": s["composite"], "level": s["level"]},
        "panel_dataset":   {"status": "loaded" if _PANEL else "not_built",
                            "rows": len(_PANEL) if _PANEL else 0},
        "ml_layer_status": "planned-WP3",
        "deployment":      "huggingface-spaces",
    }


@app.get("/stress_score")
def stress_score(year: Optional[int] = None):
    y = year or AVAILABLE_YEARS[-1]
    if y not in _SCORES:
        raise HTTPException(
            status_code=404,
            detail=f"Year {y} not in available range {AVAILABLE_YEARS[0]}–{AVAILABLE_YEARS[-1]}."
        )
    return _SCORES[y]


@app.get("/stress_history")
def stress_history():
    series = [
        {"year": y, "composite": s["composite"], "level": s["level"],
         "components": {c["id"]: c["raw_value"] for c in s["components"]}}
        for y, s in _SCORES.items()
    ]
    return {
        "model_layer": "heuristic-baseline",
        "years":       AVAILABLE_YEARS,
        "series":      series,
        "methodology": {
            "type":        "deterministic-composite",
            "components":  [{"id": c["id"], "weight": c["weight"],
                             "low": c["low"], "high": c["high"]} for c in _COMPONENTS],
            "aggregation": "weighted-mean of [0,1]-normalised components",
            "note":        "Descriptive index only. Not a trained predictive model.",
        },
    }


@app.get("/panel_summary")
def panel_summary():
    if _PANEL is None:
        return {"status": "not_built",
                "message": "panel_dataset.csv not found in data/"}
    years      = sorted(set(r["year"] for r in _PANEL))
    cantons    = sorted(set(r["canton"] for r in _PANEL))
    n_distress = sum(int(r["fiscal_distress_proxy"]) for r in _PANEL)
    placeholder_cols = [
        "commune_revenue_eur_m", "commune_expenditure_eur_m",
        "commune_balance_eur_m", "commune_debt_per_capita",
        "bank_commune_credit_eur_m", "bank_exposure_hhi",
    ]
    return {
        "status":   "loaded",
        "rows":     len(_PANEL),
        "communes": len(set(r["commune"] for r in _PANEL)),
        "years":    years,
        "cantons":  cantons,
        "label": {
            "column":     "fiscal_distress_proxy",
            "source":     "proxy-socioeconomic-2021",
            "distress_n": n_distress,
            "prevalence": round(n_distress / len(_PANEL), 4),
            "note":       "Proxy label from socioeconomic z-scores — not fiscal distress events.",
        },
        "communes_at_risk": [
            {"commune": r["commune"], "canton": r["canton"],
             "unemployment_rate": r["unemployment_rate"], "income_index": r["income_index"]}
            for r in _PANEL if int(r["fiscal_distress_proxy"]) == 1
        ],
        "placeholder_features": placeholder_cols,
        "data_vintage": _PANEL[0].get("data_vintage") if _PANEL else None,
    }


@app.get("/model_performance")
def model_performance():
    latest = _SCORES[AVAILABLE_YEARS[-1]]
    return {
        "heuristic_baseline": {
            "type":             "deterministic-composite-index",
            "latest_composite": latest["composite"],
            "latest_level":     latest["level"],
            "note": "Benchmark the XGBoost model must beat. No AUC-ROC (not probabilistic).",
        },
        "ml_model": {
            "status":  "not_trained",
            "target":  "commune-year binary fiscal distress (t+1)",
            "planned_metrics": ["AUC-ROC ≥ 0.75", "PR-AUC", "Brier score", "FAR", "F1"],
            "validation": "rolling-origin temporal CV, no lookahead",
            "blocker":    "Requires fiscal panel with labelled distress events (WP1)",
        },
    }


@app.get("/feature_importance")
def feature_importance():
    latest = _SCORES[AVAILABLE_YEARS[-1]]
    return {
        "heuristic_components": [
            {"id": c["id"], "label": c["label"], "weight": c["weight"],
             "raw_value": next(x["raw_value"] for x in latest["components"] if x["id"] == c["id"]),
             "normalised": next(x["normalised"] for x in latest["components"] if x["id"] == c["id"])}
            for c in _COMPONENTS
        ],
        "planned_feature_groups": [
            {"group": "Fiscal flow",   "status": "planned-WP3"},
            {"group": "Debt stock",    "status": "planned-WP3"},
            {"group": "Demographic",   "status": "planned-WP3"},
            {"group": "Spatial",       "status": "planned-WP3"},
            {"group": "Bank exposure", "status": "requires-BCL-data"},
        ],
    }


# ── Planned WP3 endpoints ─────────────────────────────────────────────────────

@app.post("/predict_distress")
def predict_distress(request: DistressRequest):
    y = request.year or AVAILABLE_YEARS[-1]
    if y not in _SCORES:
        raise HTTPException(status_code=404, detail=f"Year {y} not available.")
    national = _SCORES[y]
    known    = {c: _communes["communes"].get(c) for c in request.commune_ids}
    return {
        "status":          "partial",
        "ml_prediction":   "not_implemented",
        "ml_blocker":      "Trained model required (WP3).",
        "year":            y,
        "commune_ids":     request.commune_ids,
        "unknown_communes": [c for c, v in known.items() if v is None],
        "national_context": {"composite": national["composite"], "level": national["level"],
                             "note": "National heuristic — not commune-specific."},
        "commune_socioeconomic": {
            name: {"canton": info["canton"], "population": info["population"],
                   "unemployment_rate": info["unemployment_rate"],
                   "income_index": info["income_index"]}
            for name, info in known.items() if info
        },
    }


@app.post("/shap_explain")
def shap_explain(request: ShapRequest):
    y = request.year or AVAILABLE_YEARS[-1]
    if y not in _SCORES:
        raise HTTPException(status_code=404, detail=f"Year {y} not available.")
    national = _SCORES[y]
    return {
        "status":         "partial",
        "shap_available": False,
        "shap_blocker":   "SHAP requires a trained XGBoost tree model (WP3).",
        "year":           y,
        "commune_ids":    request.commune_ids,
        "heuristic_decomposition": {
            "note":       "National component breakdown — commune-level SHAP pending.",
            "components": national["components"],
        },
    }
