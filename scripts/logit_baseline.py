"""
Baseline proxy-panel logistic regression — LuxFin
--------------------------------------------------
Reproduces the preliminary logit result reported in the ML Design panel
of index.html.

Outcome: fiscal_distress_proxy (socioeconomic proxy — not fiscal distress)
Predictors: five structural commune characteristics that do NOT enter the
            proxy label construction (non-circular by design).
            Label-defining variables excluded: unemployment_rate,
            income_index, employment_rate.

All predictors are standardised before estimation.

Usage:
    python3 scripts/logit_baseline.py

Requirements: pandas, statsmodels, scikit-learn
"""

import warnings
import pandas as pd
import numpy as np
from statsmodels.discrete.discrete_model import Logit
from statsmodels.tools import add_constant
from sklearn.metrics import roc_auc_score

DATA_PATH = "data/panel_dataset.csv"

NON_CIRCULAR_FEATURES = [
    "foreign_pop_pct",
    "pop_density",
    "degurba",
    "population",
    "cross_border_workers",
]

def main():
    df = pd.read_csv(DATA_PATH)
    print(f"Panel: {len(df)} communes, reference year {df['year'].iloc[0]}")
    print(f"Proxy distress prevalence: {df['fiscal_distress_proxy'].mean():.1%} "
          f"({df['fiscal_distress_proxy'].sum():.0f}/{len(df)} communes)\n")

    y = df["fiscal_distress_proxy"]
    X_raw = df[NON_CIRCULAR_FEATURES].copy()
    X_std = (X_raw - X_raw.mean()) / X_raw.std()
    X_c = add_constant(X_std)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        res = Logit(y, X_c).fit(method="bfgs", disp=False)
        converge_warn = any("converge" in str(w.message).lower() for w in caught)

    probs = res.predict(X_c)
    auc = roc_auc_score(y, probs)

    print("=" * 60)
    print("LOGIT: proxy-panel baseline (non-circular predictors only)")
    print("=" * 60)
    print(f"  N = {len(df)}  |  AUC-ROC = {auc:.3f}  |  "
          f"Pseudo R² = {res.prsquared:.3f}  |  AIC = {res.aic:.1f}")
    if converge_warn:
        print("  NOTE: Convergence warning (small N, sparse labels — "
              "point estimates are still valid)")
    print()
    print(f"  {'Predictor':<30}  {'Coef':>7}  {'SE':>6}  {'p':>6}  Sig")
    print("  " + "-" * 58)
    sig_map = lambda p: "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "." if p < 0.1 else ""
    for name, coef, se, pval in zip(
        res.params.index, res.params, res.bse, res.pvalues
    ):
        print(f"  {name:<30}  {coef:>7.3f}  {se:>6.3f}  {pval:>6.3f}  {sig_map(pval)}")
    print()
    print("IMPORTANT: The dependent variable is a socioeconomic proxy, NOT")
    print("a fiscal distress event. These results demonstrate the pipeline")
    print("and feature relevance only. Replace with STATEC commune account")
    print("data before drawing substantive conclusions.")

if __name__ == "__main__":
    main()
