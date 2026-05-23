"""
LuxFin commune-year panel builder
----------------------------------
Constructs data/panel_dataset.csv from publicly available sources.

Data layers (in order of priority):
  1. STATEC LUSTAT snapshot (communes.json)  — 102 communes, ref year 2021
  2. National fiscal context (fiscal.json)   — Eurostat GFS series, 2014–2023
  3. Derived features                        — computed from layers 1 + 2
  4. Heuristic distress label                — proxy from socioeconomic indicators
                                               (placeholder until BCL fiscal accounts)

Output: data/panel_dataset.csv

When BCL supervisory commune fiscal accounts become available, replace
the heuristic label with real binary distress events and add the
bank-exposure columns marked PLACEHOLDER below.

Run:
    python scripts/build_panel.py
"""

from __future__ import annotations

import csv
import json
import math
import statistics
from pathlib import Path

ROOT   = Path(__file__).parent.parent
DATA   = ROOT / "data"
OUTPUT = DATA / "panel_dataset.csv"

# ── Load source data ──────────────────────────────────────────────────────────
communes_raw = json.loads((DATA / "communes.json").read_text())
banking_raw  = json.loads((DATA / "banking.json").read_text())
fiscal_raw   = json.loads((DATA / "fiscal.json").read_text())

COMMUNES = communes_raw["communes"]
BANKING  = banking_raw["annual"]
FISCAL   = fiscal_raw["annual"]

# Reference year — only 2021 STATEC snapshot is available
# Add additional years here as STATEC releases commune-level time series
PANEL_YEARS = [2021]

# ── National context at year 2021 ─────────────────────────────────────────────
def _national_context(year: int) -> dict:
    idx = BANKING["years"].index(year)
    b, f = BANKING, FISCAL
    bond_conc  = (b["govt_bonds_held"][idx] / b["total_assets"][idx]) * 100
    credit_shr = (b["credit_govt"][idx] / (b["credit_govt"][idx] + b["credit_private"][idx])) * 100
    # Stress score (mirrors shared.js computeStressScores)
    components = [
        {"low": 3.0,  "high": 10.0, "invert": False, "raw": bond_conc},
        {"low": 6.0,  "high": 16.0, "invert": False, "raw": credit_shr},
        {"low": -3.0, "high": 3.0,  "invert": True,  "raw": f["balance_pct_gdp"][idx]},
        {"low": 8.0,  "high": 16.0, "invert": False, "raw": b["total_assets"][idx] / f["gdp_eur_bn"][idx]},
    ]
    weights = [0.30, 0.30, 0.25, 0.15]
    score = 0.0
    for comp, w in zip(components, weights):
        lo, hi = comp["low"], comp["high"]
        n = max(0.0, min(1.0, (comp["raw"] - lo) / (hi - lo)))
        if comp["invert"]:
            n = 1.0 - n
        score += n * w
    return {
        "nat_bond_conc":    round(bond_conc, 3),
        "nat_credit_shr":   round(credit_shr, 3),
        "nat_fiscal_bal":   f["balance_pct_gdp"][idx],
        "nat_gdp_bn":       f["gdp_eur_bn"][idx],
        "nat_stress_score": round(score, 4),
        "nat_total_assets": b["total_assets"][idx],
        "nat_num_banks":    b["num_banks"][idx],
    }

# ── Distributional stats for z-score normalisation ───────────────────────────
def _dist_stats(values: list[float]) -> tuple[float, float]:
    mu  = statistics.mean(values)
    sd  = statistics.stdev(values) if len(values) > 1 else 1.0
    return mu, sd

all_unemp  = [c["unemployment_rate"] for c in COMMUNES.values()]
all_income = [c["income_index"]      for c in COMMUNES.values()]
all_emp    = [c["employment_rate"]   for c in COMMUNES.values()]
all_forpop = [c["foreign_pop_pct"]   for c in COMMUNES.values()]

mu_unemp,  sd_unemp  = _dist_stats(all_unemp)
mu_income, sd_income = _dist_stats(all_income)
mu_emp,    sd_emp    = _dist_stats(all_emp)
mu_forpop, sd_forpop = _dist_stats(all_forpop)

# ── Heuristic distress label (proxy) ─────────────────────────────────────────
# A commune is flagged as "at-risk" if it sits in the vulnerable tail on
# ≥ 2 of 3 socioeconomic dimensions. This is a prototype label; it will be
# replaced by binary fiscal distress events from BCL/STATEC commune accounts.
#
# Thresholds (1 SD from mean, directionally appropriate):
#   unemployment_rate > mu + 0.75*sd  →  stress signal
#   income_index      < mu - 0.75*sd  →  stress signal
#   employment_rate   < mu - 0.75*sd  →  stress signal
def _distress_label(row: dict) -> int:
    signals = 0
    if row["unemployment_rate"] > mu_unemp  + 0.75 * sd_unemp:  signals += 1
    if row["income_index"]      < mu_income - 0.75 * sd_income:  signals += 1
    if row["employment_rate"]   < mu_emp    - 0.75 * sd_emp:     signals += 1
    return 1 if signals >= 2 else 0

# ── Build rows ────────────────────────────────────────────────────────────────
COLUMNS = [
    # Identifiers
    "lau_id", "commune", "canton", "year",
    # STATEC LUSTAT socioeconomic (ref 2021)
    "population", "area_km2", "pop_density",
    "employment_rate", "unemployment_rate",
    "income_index", "foreign_pop_pct",
    "cross_border_workers", "degurba",
    # Standardised socioeconomic scores
    "unemp_z", "income_z", "emp_z", "forpop_z",
    # National fiscal context (from Eurostat / ECB)
    "nat_bond_conc", "nat_credit_shr", "nat_fiscal_bal",
    "nat_gdp_bn", "nat_stress_score",
    "nat_total_assets", "nat_num_banks",
    # PLACEHOLDER — requires BCL/CSSF supervisory data
    "commune_revenue_eur_m",   # commune total revenue (EUR million)
    "commune_expenditure_eur_m",
    "commune_balance_eur_m",
    "commune_debt_per_capita",
    "bank_commune_credit_eur_m",  # bank lending to commune public sector
    "bank_exposure_hhi",          # Herfindahl index of bank concentration
    # Label
    "fiscal_distress_proxy",
    "label_source",
    "data_vintage",
]

rows = []
for year in PANEL_YEARS:
    nat = _national_context(year)
    for name, info in COMMUNES.items():
        pop = info["population"]
        area = info.get("area_km2", None)
        pop_density = round(pop / area, 2) if area else None

        unemp_z  = round((info["unemployment_rate"] - mu_unemp)  / sd_unemp,  3)
        income_z = round((info["income_index"]      - mu_income) / sd_income, 3)
        emp_z    = round((info["employment_rate"]   - mu_emp)    / sd_emp,    3)
        forpop_z = round((info["foreign_pop_pct"]   - mu_forpop) / sd_forpop, 3)

        label = _distress_label(info)

        rows.append({
            "lau_id":    info["lau_id"],
            "commune":   name,
            "canton":    info["canton"],
            "year":      year,
            "population":          pop,
            "area_km2":            area,
            "pop_density":         pop_density,
            "employment_rate":     info["employment_rate"],
            "unemployment_rate":   info["unemployment_rate"],
            "income_index":        info["income_index"],
            "foreign_pop_pct":     info["foreign_pop_pct"],
            "cross_border_workers": info.get("cross_border_workers"),
            "degurba":             info["degurba"],
            "unemp_z":   unemp_z,
            "income_z":  income_z,
            "emp_z":     emp_z,
            "forpop_z":  forpop_z,
            **nat,
            # Placeholders
            "commune_revenue_eur_m":      "",
            "commune_expenditure_eur_m":  "",
            "commune_balance_eur_m":      "",
            "commune_debt_per_capita":    "",
            "bank_commune_credit_eur_m":  "",
            "bank_exposure_hhi":          "",
            "fiscal_distress_proxy":      label,
            "label_source":               "proxy-socioeconomic-2021",
            "data_vintage":               "STATEC-LUSTAT-2021",
        })

# ── Write CSV ─────────────────────────────────────────────────────────────────
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT, "w", newline="", encoding="utf-8") as fh:
    writer = csv.DictWriter(fh, fieldnames=COLUMNS)
    writer.writeheader()
    writer.writerows(rows)

n_distress = sum(r["fiscal_distress_proxy"] for r in rows)
print(f"Written {len(rows)} rows to {OUTPUT}")
print(f"Distress events (proxy label=1): {n_distress} / {len(rows)} communes")
print(f"Prevalence: {n_distress/len(rows)*100:.1f}%")
print()
print("Columns with placeholders (require BCL/STATEC supervisory data):")
placeholders = [
    "commune_revenue_eur_m", "commune_expenditure_eur_m",
    "commune_balance_eur_m", "commune_debt_per_capita",
    "bank_commune_credit_eur_m", "bank_exposure_hhi",
]
for col in placeholders:
    print(f"  {col}")
print()
print("Next steps:")
print("  1. Apply for commune financial accounts from Ministere de l'Interieur")
print("  2. Request BCL/CSSF bank-by-commune credit data via formal MOU")
print("  3. Add additional STATEC LUSTAT years when released (2022, 2023)")
print("  4. Replace proxy label with binary fiscal distress events")
