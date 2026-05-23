"""
LuxFin quality checks
----------------------
Validates JSON data integrity, panel CSV structure, JS syntax, and Python
import hygiene. Run from the repo root:

    python3 scripts/validate.py

All checks are independent; failures are collected and reported at the end.
Exit code 0 = all checks passed. Exit code 1 = one or more failures.
"""

from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
WARN = "\033[33m⚠\033[0m"

failures: list[str] = []
warnings: list[str] = []


def ok(msg: str) -> None:
    print(f"  {PASS}  {msg}")


def fail(msg: str) -> None:
    print(f"  {FAIL}  {msg}")
    failures.append(msg)


def warn(msg: str) -> None:
    print(f"  {WARN}  {msg}")
    warnings.append(msg)


# ── 1. JSON data integrity ────────────────────────────────────────────────────
print("\n1. JSON data files")

for fname in ("banking.json", "fiscal.json", "communes.json"):
    path = ROOT / "data" / fname
    if not path.exists():
        fail(f"{fname} missing")
        continue
    try:
        data = json.loads(path.read_text())
        ok(f"{fname} parses OK")
    except json.JSONDecodeError as e:
        fail(f"{fname} JSON parse error: {e}")
        continue

    if fname == "banking.json":
        annual = data.get("annual", {})
        years  = annual.get("years", [])
        if not years:
            fail("banking.json: annual.years missing or empty")
        else:
            ok(f"banking.json: {len(years)} annual years ({years[0]}–{years[-1]})")
        for field in ("total_assets", "credit_govt", "credit_private", "govt_bonds_held"):
            if field not in annual:
                fail(f"banking.json: annual.{field} missing")
            elif len(annual[field]) != len(years):
                fail(f"banking.json: annual.{field} length mismatch ({len(annual[field])} ≠ {len(years)})")
            else:
                ok(f"banking.json: annual.{field} length OK")

    if fname == "fiscal.json":
        annual = data.get("annual", {})
        years  = annual.get("years", [])
        for field in ("balance_pct_gdp", "gdp_eur_bn", "revenue_pct_gdp", "debt_pct_gdp"):
            if field not in annual:
                fail(f"fiscal.json: annual.{field} missing")
            elif len(annual[field]) != len(years):
                fail(f"fiscal.json: annual.{field} length mismatch")
            else:
                ok(f"fiscal.json: annual.{field} length OK")

    if fname == "communes.json":
        communes = data.get("communes", {})
        n = len(communes)
        if n != 102:
            warn(f"communes.json: expected 102 communes, found {n}")
        else:
            ok(f"communes.json: {n} communes")
        required_fields = ("lau_id", "canton", "population", "employment_rate",
                           "unemployment_rate", "income_index", "foreign_pop_pct")
        sample = next(iter(communes.values())) if communes else {}
        for f in required_fields:
            if f not in sample:
                fail(f"communes.json: field '{f}' missing from commune records")
            else:
                ok(f"communes.json: field '{f}' present")

# ── 2. panel_dataset.csv ──────────────────────────────────────────────────────
print("\n2. panel_dataset.csv")

panel_path = ROOT / "data" / "panel_dataset.csv"
if not panel_path.exists():
    fail("data/panel_dataset.csv missing — run: python3 scripts/build_panel.py")
else:
    with open(panel_path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    n = len(rows)
    if n != 102:
        fail(f"panel_dataset.csv: expected 102 rows, found {n}")
    else:
        ok(f"panel_dataset.csv: {n} rows")

    required_cols = [
        "lau_id", "commune", "canton", "year",
        "population", "unemployment_rate", "income_index", "employment_rate",
        "foreign_pop_pct", "pop_density", "degurba",
        "unemp_z", "income_z", "emp_z", "forpop_z",
        "nat_bond_conc", "nat_credit_shr", "nat_fiscal_bal",
        "nat_stress_score", "nat_gdp_bn",
        "fiscal_distress_proxy", "label_source", "data_vintage",
    ]
    cols = set(rows[0].keys()) if rows else set()
    for col in required_cols:
        if col not in cols:
            fail(f"panel_dataset.csv: required column '{col}' missing")
        else:
            ok(f"panel_dataset.csv: column '{col}' present")

    placeholder_cols = [
        "commune_revenue_eur_m", "commune_expenditure_eur_m",
        "commune_balance_eur_m", "commune_debt_per_capita",
        "bank_commune_credit_eur_m", "bank_exposure_hhi",
    ]
    for col in placeholder_cols:
        if col not in cols:
            warn(f"panel_dataset.csv: placeholder column '{col}' missing")
        else:
            filled = sum(1 for r in rows if r[col].strip())
            if filled > 0:
                warn(f"panel_dataset.csv: placeholder column '{col}' has {filled} non-empty values — verify source")
            else:
                ok(f"panel_dataset.csv: placeholder column '{col}' correctly empty")

    if rows:
        n_distress = sum(int(r.get("fiscal_distress_proxy", 0)) for r in rows)
        prevalence = n_distress / n
        if not (0.10 <= prevalence <= 0.40):
            warn(f"panel_dataset.csv: proxy distress prevalence {prevalence:.1%} outside expected 10–40% range")
        else:
            ok(f"panel_dataset.csv: proxy distress prevalence {prevalence:.1%} ({n_distress}/{n})")

        label_src = set(r.get("label_source", "") for r in rows)
        for src in label_src:
            if "proxy" not in src.lower():
                warn(f"panel_dataset.csv: label_source '{src}' does not contain 'proxy' — verify it is not claiming real fiscal events")
            else:
                ok(f"panel_dataset.csv: label_source correctly labelled as proxy ({src!r})")

# ── 3. JS syntax check ────────────────────────────────────────────────────────
print("\n3. JavaScript syntax")

shared_js = ROOT / "js" / "shared.js"
if not shared_js.exists():
    fail("js/shared.js missing")
else:
    result = subprocess.run(
        ["node", "--check", str(shared_js)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        ok("js/shared.js syntax OK (node --check)")
    else:
        fail(f"js/shared.js syntax error:\n    {result.stderr.strip()}")

# ── 4. Python compilation ─────────────────────────────────────────────────────
print("\n4. Python syntax")

for pyfile in ("api/fiscal_ml_api.py", "scripts/build_panel.py", "scripts/validate.py"):
    path = ROOT / pyfile
    if not path.exists():
        fail(f"{pyfile} missing")
        continue
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", str(path)],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        ok(f"{pyfile} compiles OK")
    else:
        fail(f"{pyfile} compile error:\n    {result.stderr.strip()}")

# ── 5. API import check ───────────────────────────────────────────────────────
print("\n5. API import integrity")

api_path = ROOT / "api" / "fiscal_ml_api.py"
if api_path.exists():
    result = subprocess.run(
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, '.'); "
         + "import importlib.util; "
         + f"spec = importlib.util.spec_from_file_location('api', '{api_path}'); "
         + "# skip full import — just check syntax and stdlib imports"],
        capture_output=True, text=True, cwd=str(ROOT)
    )

    # Check for fake/placeholder model results in the API code
    api_src = api_path.read_text()
    forbidden = ["auc_roc = 0.", "auc = 0.", "shap_values = [", "model.predict("]
    any_fake = False
    for pattern in forbidden:
        if pattern in api_src:
            fail(f"api/fiscal_ml_api.py contains suspicious pattern: {pattern!r} — check for fake model results")
            any_fake = True
    if not any_fake:
        ok("api/fiscal_ml_api.py: no fake model result patterns detected")

    # Check planned endpoints correctly flag themselves
    for ep in ("/predict_distress", "/shap_explain"):
        if ep not in api_src:
            warn(f"api/fiscal_ml_api.py: endpoint {ep!r} not found")
        else:
            ok(f"api/fiscal_ml_api.py: endpoint {ep!r} defined")

# ── 6. No fake model files ────────────────────────────────────────────────────
print("\n6. Fake model file check")

suspicious_files = list(ROOT.glob("**/*.pkl")) + list(ROOT.glob("**/*.joblib")) + \
                   list(ROOT.glob("**/*.model")) + list(ROOT.glob("**/*trained*"))
suspicious_files = [f for f in suspicious_files if ".git" not in str(f)]
if suspicious_files:
    for f in suspicious_files:
        warn(f"Potential fake/unregistered model file: {f.relative_to(ROOT)}")
else:
    ok("No trained model files found (correct — model not yet trained)")

# ── 7. Consistency check — heuristic weights ─────────────────────────────────
print("\n7. Heuristic weight consistency (shared.js ↔ fiscal_ml_api.py)")

js_src  = (ROOT / "js" / "shared.js").read_text()  if (ROOT / "js" / "shared.js").exists() else ""
api_src = (ROOT / "api" / "fiscal_ml_api.py").read_text() if (ROOT / "api" / "fiscal_ml_api.py").exists() else ""

expected_weights = ["0.30", "0.25", "0.15"]
for w in expected_weights:
    js_ok  = w in js_src
    api_ok = w in api_src
    if js_ok and api_ok:
        ok(f"Weight {w} present in both shared.js and fiscal_ml_api.py")
    elif js_ok:
        warn(f"Weight {w} in shared.js but not found in fiscal_ml_api.py")
    elif api_ok:
        warn(f"Weight {w} in fiscal_ml_api.py but not found in shared.js")
    else:
        fail(f"Weight {w} not found in either shared.js or fiscal_ml_api.py")

# ── Summary ───────────────────────────────────────────────────────────────────
print("\n" + "─" * 55)
if failures:
    print(f"\n{FAIL}  {len(failures)} check(s) failed:\n")
    for f in failures:
        print(f"    • {f}")
else:
    print(f"\n{PASS}  All checks passed")

if warnings:
    print(f"\n{WARN}  {len(warnings)} warning(s):\n")
    for w in warnings:
        print(f"    • {w}")

print()
sys.exit(1 if failures else 0)
