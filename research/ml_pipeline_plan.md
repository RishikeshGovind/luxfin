# LuxFin ML Pipeline Plan

The ML layer is planned as a forward-looking early-warning system, not as a contemporaneous dashboard score.

## Target

Primary target:

```text
FiscalStress_i,t+1 = 1 if commune i enters fiscal stress next year
```

Candidate stress labels:

- deficit greater than 15% of revenues
- deficit streak of at least two consecutive years
- debt-service pressure above an empirically chosen threshold
- robustness labels based on percentile cutoffs

## Feature Groups

- Fiscal balance and revenue structure
- Expenditure pressure and debt-service burden
- Local labour-market and demographic stress
- Spatial lags from neighbouring communes
- Bank exposure concentration, once BCL data are available

## Model Ladder

1. Rule-based baseline score
2. Logit / probit benchmark
3. Random forest
4. XGBoost with SHAP explanations

## Validation

- Rolling-origin validation
- Held-out final years
- AUC-ROC, PR-AUC, Brier score
- false-alarm rate at policy thresholds
- lead-time analysis
- calibration curves

## API Contract

Planned endpoints:

- `GET /health`
- `POST /predict_distress`
- `POST /shap_explain`
- `GET /model_performance`
- `GET /feature_importance`
