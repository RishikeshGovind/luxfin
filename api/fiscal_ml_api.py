"""
LuxFin fiscal ML API scaffold.

Planned service:
- FastAPI
- XGBoost fiscal distress model
- SHAP explanations
- temporal validation metrics

This is a non-training scaffold until data/panel_dataset.csv exists.
"""

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="LuxFin Fiscal Early-Warning API",
    description="Planned API for Luxembourg commune fiscal distress prediction.",
    version="0.1.0-scaffold",
)


class PredictionRequest(BaseModel):
    commune_ids: list[str]
    year: int | None = None


@app.get("/health")
def health():
    return {
        "status": "scaffold",
        "model_loaded": False,
        "message": "Panel dataset and trained model are not yet available.",
    }


@app.post("/predict_distress")
def predict_distress(request: PredictionRequest):
    return {
        "status": "not_implemented",
        "commune_ids": request.commune_ids,
        "message": "Train the Luxembourg fiscal distress model before using this endpoint.",
    }


@app.post("/shap_explain")
def shap_explain(request: PredictionRequest):
    return {
        "status": "not_implemented",
        "commune_ids": request.commune_ids,
        "message": "SHAP explanations require a trained tree model.",
    }


@app.get("/model_performance")
def model_performance():
    return {
        "status": "not_available",
        "metrics": {},
        "message": "No validation metrics exist until model training is complete.",
    }


@app.get("/feature_importance")
def feature_importance():
    return {
        "status": "not_available",
        "features": [],
        "message": "Feature importance requires a trained model.",
    }
