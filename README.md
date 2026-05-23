# LuxFin

**Interactive PhD research platform for Luxembourg subnational sovereign-bank nexus analysis**

A research prototype supporting the PhD proposal:
> *Does concentrated banking sector exposure to local government borrowers create a subnational sovereign-bank nexus, and can forward-looking ML-based fiscal risk indicators serve as an early warning system for regional financial stability?*

Live dashboard → **[rishikeshgovind.github.io/luxfin](https://rishikeshgovind.github.io/luxfin)**

---

## Overview

LuxFin is an interactive proposal and research prototype. It combines a narrative PhD dossier with implemented evidence modules and a scaffold for the eventual R/Python research pipeline.

| Panel | Content |
|---|---|
| **Overview** | Research question, hypotheses, motivation, literature gap, and readiness status |
| **Nexus** | Conceptual framework for domestic local-government and euro-area sovereign channels |
| **Evidence** | MFI balance sheet, public finance, and baseline heuristic stress index |
| **ML Design** | Planned early-warning target, feature groups, model ladder, validation, and API contract |
| **Empirical** | Units of analysis, variables, fixed effects, identification risks, and robustness strategy |
| **Map** | LAU 2021 choropleth of socio-economic indicators across all 102 communes |
| **Architecture** | Data access matrix, research stack, work packages, and scaffolded artifacts |

---

## Current Status

| Layer | Status | Notes |
|---|---|---|
| Frontend proposal platform | Implemented | Static HTML/CSS/JS on GitHub Pages |
| Public data evidence modules | Implemented | ECB Data Portal, Eurostat, STATEC/LUSTAT snapshots |
| Baseline stress index | Implemented | Descriptive heuristic benchmark, not predictive ML |
| Commune-year panel builder | Scaffolded | See `scripts/build_lux_panel.R` |
| ML API | Scaffolded | See `api/fiscal_ml_api.py`; endpoints return explicit not-implemented statuses |
| Full bank-commune nexus test | Requires access | Needs BCL/CSSF supervisory data or formal MOU |

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
| Commune indicators | STATEC LUSTAT | Reference year 2021 |

Static data snapshots are stored in `data/`. The Banking Exposure and Public Finance panels include live refresh buttons that pull the latest values from the ECB Data Portal API and Eurostat REST API.

---

## Stress Index — Methodology & Limitations

The composite stress score is a **deterministic descriptive index**, not a predictive or machine-learning model. Four components are normalised to [0, 1] against domain-specific thresholds and aggregated with fixed weights:

| Component | Weight | Low threshold | High threshold |
|---|---|---|---|
| Bond concentration (govt bonds / total assets) | 30% | 3% | 10% |
| Public credit share (credit to govt / total credit) | 30% | 6% | 16% |
| Fiscal balance (% of GDP, inverted) | 25% | −3% | +3% |
| Banking sector size (total assets / GDP) | 15% | 8× | 16× |

**This baseline heuristic serves as a proposal-stage benchmark.** Converting it to the forward-looking early-warning system described in the research design requires: labelled stress events, a forecasting model, out-of-sample validation, calibration analysis, lead-time tests, and false-alarm rate reporting.

---

## Running Locally

No build step required. Serve the root directory over HTTP (required for the GeoJSON fetch and API calls):

```bash
# Python
python3 -m http.server 8080

# Node
npx serve .
```

Then open `http://localhost:8080`.

---

## Repository Structure

```
luxfin/
├── index.html              # Interactive PhD proposal platform
├── style.css               # Styles
├── js/
│   └── shared.js           # Shared constants, formatters, API fetchers, stress score logic
├── research/
│   ├── data_requirements.md # Public vs restricted datasets and minimum viable panel
│   ├── empirical_strategy.md# Fixed-effects, event-study, and ML design notes
│   └── ml_pipeline_plan.md  # Target, feature groups, model ladder, validation plan
├── scripts/
│   └── build_lux_panel.R    # Scaffold for future commune-year panel construction
├── api/
│   └── fiscal_ml_api.py     # Scaffold for future FastAPI + XGBoost + SHAP service
└── data/
    ├── banking.json         # ECB BSI MFI statistics (2014–2023, EUR bn)
    ├── fiscal.json          # Eurostat GFS general government (2014–2023)
    ├── communes.json        # STATEC LUSTAT commune indicators (2021)
    └── lu_communes.geojson  # Eurostat GISCO LAU 2021 commune boundaries (LU)
```

---

## Research Context

Luxembourg presents a structurally atypical case: despite hosting a banking sector of ~12× GDP, domestic sovereign risk is minimal (Maastricht debt ~25% GDP, AAA/Aaa, persistent fiscal surpluses). The dominant transmission channel is therefore *outward* — Luxembourg MFIs hold significant EA sovereign bonds and are exposed to contagion through the European sovereign risk channel.

The core hypothesis targets the *subnational* dimension: whether individual banks' concentrated lending to specific communes or cantons creates localised feedback loops not visible in national aggregates, and whether fiscal indicators at commune level can serve as leading signals of that stress.

---

## Acknowledgements

Data: [ECB Data Portal](https://data-api.ecb.europa.eu) · [Eurostat](https://ec.europa.eu/eurostat) · [STATEC](https://statistiques.public.lu) · [Banque centrale du Luxembourg](https://www.bcl.lu)
