# LuxFin Empirical Strategy

## Core Units

- Commune-year: tests fiscal distress prediction and spatial fiscal vulnerability.
- Bank-commune-year: tests whether concentrated public-sector borrower exposure creates a local sovereign-bank nexus.
- Bank-year: tests whether exposure-weighted commune stress maps into bank outcomes.

## Main Hypotheses

H1: Banks more concentrated in stressed commune borrowers reduce local-government credit supply more than less exposed banks.

H2: Commune fiscal deterioration predicts subsequent bank credit tightening after controlling for prior credit conditions.

H3: Forward-looking ML models can predict commune fiscal stress better than a transparent rule-based baseline under temporal validation.

## Baseline Specifications

The core fixed-effects design is:

```text
DeltaCredit_b,i,t = beta * ExposureHHI_b,i,t-1 + theta * FiscalStress_i,t-1
                    + alpha_i + delta_b + gamma_t + controls_i,t-1 + error_b,i,t
```

The minimum viable predictive design is:

```text
FiscalStress_i,t+1 = f(fiscal_i,t, demographic_i,t, spatial_i,t, macro_t)
```

## Identification Risks

- Restricted access to bank-by-commune exposure data.
- Simultaneity between credit supply and fiscal stress.
- Rare-event labels in a fiscally strong country.
- Spatial autocorrelation across neighbouring communes.
- Measurement error in public-sector borrower classification.

## Planned Robustness

- Commune, bank, year, and canton-year fixed effects.
- Lagged exposure variables.
- Matched event-study around stress onset.
- Spatial lag and spatial error specifications.
- Alternative fiscal-stress label thresholds.
- Temporal train/test splits for all predictive models.
