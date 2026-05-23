# LuxFin

**Interactive PhD research platform — subnational sovereign-bank nexus analysis · Luxembourg**

A research prototype supporting the PhD proposal:
> *Does concentrated banking sector exposure to local government borrowers create a subnational sovereign-bank nexus, and can forward-looking ML-based fiscal risk indicators serve as an early warning system for regional financial stability?*

Live platform → **[rishikeshgovind.github.io/luxfin](https://rishikeshgovind.github.io/luxfin)**

---

## Overview

LuxFin combines a narrative PhD dossier with implemented evidence modules, a live heuristic API, and a prototype research pipeline. The goal is to demonstrate the full system design before supervisory data access is obtained.

| Panel | Content |
|---|---|
| **Overview** | Research question, H1/H2/H3 hypotheses, motivation, literature gap, readiness status |
| **Nexus** | Conceptual framework — domestic local-government and euro-area sovereign channels |
| **Evidence** | ECB MFI balance sheet, Eurostat public finance, baseline heuristic stress index |
| **ML Design** | Three-layer distinction: heuristic baseline (live), prototype panel, planned XGBoost/SHAP |
| **Empirical** | Variables, fixed effects, identification risks, robustness strategy |
| **Map** | LAU 2021 choropleth — 102 Luxembourg communes, STATEC LUSTAT socioeconomic indicators |
| **Architecture** | Data access matrix, API readiness table, work packages, repository artifact status |

---

## Current Status

| Layer | Status | Notes |
|---|---|---|
| Frontend proposal platform | **Implemented** | Static HTML/CSS/JS on GitHub Pages |
| Public data evidence modules | **Implemented** | ECB Data Portal, Eurostat, STATEC/LUSTAT snapshots |
| Baseline heuristic stress index | **Implemented** | Deterministic 4-component index; serves as ML benchmark |
| FastAPI heuristic endpoints | **Live** | `/health`, `/stress_score`, `/stress_history`, `/panel_summary`, `/model_performance`, `/feature_importance` |
| Prototype commune panel | **Built** | 102 communes × 2021 snapshot; proxy distress labels from socioeconomic indicators |
| Panel builder script | **Implemented** | `python3 scripts/build_panel.py` (canonical); R mirror at `scripts/build_lux_panel.R` |
| Baseline proxy-panel logit | **Implemented** | `python3 scripts/logit_baseline.py` — N=102, non-circular predictors, AUC-ROC=0.697 (proxy outcome only) |
| Validation script | **Implemented** | `python3 scripts/validate.py` |
| Commune financial accounts panel | **Data request** | STATEC micro-data request required for true fiscal labels |
| Supervised ML model (XGBoost/SHAP) | **Planned WP3** | Requires fiscal panel with labelled distress events |
| API ML endpoints | **Planned WP3** | `/predict_distress`, `/shap_explain` return informative WP3 blockers |
| Bank-commune nexus test | **Requires access** | BCL/CSSF supervisory data via formal MOU |

> **Proxy label note:** `data/panel_dataset.csv` uses unemployment/income/employment z-scores as a proxy for fiscal distress. This is useful for testing pipeline mechanics only — it is not a measure of fiscal distress and should not be treated as one.

---

## Running Locally

No build step required for the frontend. Serve the root directory over HTTP:

```bash
# Python
python3 -m http.server 8080

# Node
npx serve .
```

Then open `http://localhost:8080`.

### Running the API

**Live deployment (Hugging Face Spaces):**
```
https://aetherno-luxfin-api.hf.space/health
https://aetherno-luxfin-api.hf.space/docs
```
Free-tier CPU Space — first request after inactivity takes ~30s to wake.

**Run locally:**
```bash
pip install -r api/requirements.txt
uvicorn api.fiscal_ml_api:app --reload
# Interactive docs at http://localhost:8000/docs
```

### Reproducing the panel

```bash
python3 scripts/build_panel.py
# Writes data/panel_dataset.csv (102 rows)
# Reports proxy distress prevalence
```

### Running quality checks

```bash
python3 scripts/validate.py
# Checks JSON integrity, panel row count, required columns,
# proxy label prevalence, JS syntax, and Python import hygiene
```

---

## Data Sources

| Series | Provider | Identifier |
|---|---|---|
| MFI total assets | ECB Data Portal (BSI) | `BSI/A.LU.N.A.T.A.1.U2.2240.Z01.E` |
| Credit to general government | ECB Data Portal (BSI) | `BSI/A.LU.N.A.A20.A.1.U2.2240.Z01.E` |
| Credit to private sector | ECB Data Portal (BSI) | `BSI/A.LU.N.A.A30.A.1.U2.2240.Z01.E` |
| Government bond holdings | ECB Data Portal (BSI) | `BSI/A.LU.N.A.A51.A.1.U2.2240.Z01.E` |
| General government fiscal balance | Eurostat GFS | `gov_10q_ggnfa` · S13 · B.9 · PC_GDP |
| Government expenditure by COFOG | Eurostat | `gov_10a_exp` |
| Commune boundaries | Eurostat GISCO | LAU 2021, 1:1M, EPSG:4326 |
| Commune socioeconomic indicators | STATEC LUSTAT | Reference year 2021 |

Static snapshots are in `data/`. The Banking Exposure and Public Finance panels include live refresh buttons that pull from the ECB Data Portal API and Eurostat REST API.

**Data provenance notes:**
- `data/communes.json` population figures are drawn from **STATEC LUSTAT 2021 commune-level tables**, not from the GeoJSON `POP_2021` field (Eurostat GISCO estimate). The two sources use different reference dates and methodology; discrepancies are expected and both are citable.
- The 102-commune structure reflects the **LAU 2021 boundary vintage**. Luxembourg reduced to 100 municipalities after the 2023 Käerjeng and Reckange/Mess mergers. All analysis is explicitly bounded to the 2021 vintage.
- Luxembourg's banking sector size (~12× GDP) is described as "among the highest in the euro area" following IMF FSAP (2017) and BCL Financial Stability Review characterisations. The superlative "largest" is intentionally avoided pending a systematic cross-country comparison.

**Not yet obtained (require formal request):**
- Commune financial accounts (STATEC micro-data) — for true fiscal distress labels
- Bank-by-commune credit register (BCL supervisory) — for the core nexus test
- Bank capital and COREP data (CSSF/BCL) — for bank-level outcomes

---

## Stress Index — Methodology & Limitations

The composite stress score is a **deterministic descriptive index**, not a predictive or machine-learning model. Four components are normalised to [0, 1] against domain-specific thresholds and aggregated with fixed weights:

| Component | Weight | Low threshold | High threshold |
|---|---|---|---|
| Bond concentration (govt bonds / total assets) | 30% | 3% | 10% |
| Public credit share (credit to govt / total credit) | 30% | 6% | 16% |
| Fiscal balance (% of GDP, inverted) | 25% | −3% | +3% |
| Banking sector size (total assets / GDP) | 15% | 8× | 16× |

**This baseline heuristic serves as a proposal-stage benchmark.** Converting it to the forward-looking early-warning system described in H3 requires: labelled stress events, a forecasting model, out-of-sample validation, calibration analysis, lead-time tests, and false-alarm rate reporting.

The same logic is implemented in both `js/shared.js` (frontend) and `api/fiscal_ml_api.py` (API). Results are identical.

---

## Repository Structure

```
luxfin/
├── index.html                    # Interactive PhD proposal platform (7 panels)
├── style.css                     # Academic design system
├── js/
│   └── shared.js                 # Shared constants, formatters, ECB/Eurostat fetchers,
│                                 # stress score logic (canonical heuristic implementation)
├── api/
│   ├── fiscal_ml_api.py          # FastAPI service — heuristic layer live,
│   │                             # XGBoost/SHAP layer planned (WP3)
│   └── requirements.txt          # fastapi, uvicorn, pydantic
├── scripts/
│   ├── build_panel.py            # Canonical Python panel builder → data/panel_dataset.csv
│   ├── logit_baseline.py         # Reproducible proxy-panel logit (non-circular predictors)
│   ├── build_lux_panel.R         # R mirror (comparison output, not used by API)
│   └── validate.py               # Quality checks: JSON, CSV, JS syntax, Python imports
├── research/
│   ├── data_requirements.md      # Public vs restricted datasets, minimum viable panel
│   ├── empirical_strategy.md     # Fixed-effects, IV, and ML design notes
│   └── ml_pipeline_plan.md       # Target, feature groups, model ladder, validation plan
└── data/
    ├── banking.json              # ECB BSI MFI statistics (2014–2023, EUR bn)
    ├── fiscal.json               # Eurostat GFS general government (2014–2023)
    ├── communes.json             # STATEC LUSTAT commune indicators (2021, 102 communes)
    ├── panel_dataset.csv         # Prototype commune panel — proxy labels only
    └── lu_communes.geojson       # Eurostat GISCO LAU 2021 commune boundaries
```

**Deployment note:** `luxfin-api/` is a separate Hugging Face Spaces deployment repository (Docker SDK, port 7860) and is not tracked by this repo's git history. `api/fiscal_ml_api.py` is the **canonical** service implementation; the Hugging Face copy is a deployment mirror. Any divergence between the two is intentional for platform compatibility and is documented in `luxfin-api/README.md`.

---

## Research Context

Luxembourg presents a structurally atypical case: despite hosting a banking sector of ~12× GDP, domestic sovereign risk is minimal (Maastricht debt ~25% GDP, AAA/Aaa, persistent fiscal surpluses). The dominant transmission channel is therefore *outward* — Luxembourg MFIs hold significant EA sovereign bonds and are exposed to contagion through the European sovereign risk channel.

The core hypothesis targets the *subnational* dimension: whether individual banks' concentrated lending to specific communes creates localised feedback loops not visible in national aggregates, and whether fiscal indicators at commune level can serve as leading signals of that stress.

**What is and is not claimed:**
- The heuristic stress index **is** a transparent, reproducible descriptive benchmark.
- The prototype panel **is** a pipeline-feasibility demonstration using public socioeconomic data.
- The proxy distress label **is not** a measure of true fiscal distress.
- A preliminary proxy-panel **logit** has been run (N=102, AUC-ROC=0.697) using non-circular structural predictors; reproducible via `python3 scripts/logit_baseline.py`. The dependent variable is a socioeconomic proxy — not a fiscal distress event.
- No XGBoost/SHAP model has been trained; no ML predictions or SHAP values exist yet.
- The core nexus test (H1) requires BCL supervisory data not yet obtained.

---

## Acknowledgements

Data: [ECB Data Portal](https://data-api.ecb.europa.eu) · [Eurostat](https://ec.europa.eu/eurostat) · [STATEC](https://statistiques.public.lu) · [Banque centrale du Luxembourg](https://www.bcl.lu)
