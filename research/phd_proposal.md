# Does Concentrated Banking Sector Exposure to Local Government Borrowers Create a Subnational Sovereign-Bank Nexus?
## Evidence from Luxembourg's Commune-Level Credit Market and a Machine Learning Early-Warning Design

**PhD Research Proposal**
**University of Luxembourg · Faculty of Law, Economics and Finance**
**Department of Finance**

Candidate: Rishikesh Govind
Proposed Supervisors: [TBC]
Submission date: 2026

---

## Abstract

This proposal argues that the sovereign-bank nexus literature has a structural blind spot: it treats each country as a single sovereign–bank unit and ignores the within-country heterogeneity in bank exposure to individual sub-sovereign borrowers. Luxembourg offers an unusually tractable setting to test whether this subnational dimension matters. Its banking sector — standing at approximately 12 times GDP, among the highest ratios in the euro area (IMF FSAP 2017; BCL Financial Stability Review) — coexists with 102 administratively distinct communes (LAU 2021 boundary vintage) whose fiscal capacity ranges from prosperous peri-urban centres to transfer-dependent rural municipalities. If banks have concentrated their local-government credit portfolios toward specific communes, a deterioration in those communes' fiscal positions could constrain the credit supply from the most exposed institutions — a subnational sovereign-bank feedback loop invisible in national aggregates.

The proposal organises this argument into three nested hypotheses. H1 asks whether such a nexus exists at the bank-commune level. H2 asks whether commune fiscal deterioration Granger-causes credit supply contraction (rather than the reverse). H3 asks whether a machine-learning early-warning system trained on commune-year fiscal panels can operationalise these signals ahead of time.

The design is deliberately staged around a single binding data constraint: access to BCL supervisory micro-data requires a formal Memorandum of Understanding (MOU). The project identifies which hypotheses are testable now with public data, which require the MOU, and what minimum-viable contribution is publishable in either case. A preliminary proxy-panel logit on 102 communes (AUC-ROC = 0.697 against non-circular structural predictors) demonstrates that the pipeline is functional; it does not constitute a test of any research hypothesis. A fully implemented research platform — including live ECB/Eurostat evidence modules, a 4-component heuristic stress index, and this entire proposal rendered interactively — is available at [rishikeshgovind.github.io/luxfin](https://rishikeshgovind.github.io/luxfin).

---

## 1. Introduction

The 2010–2012 European sovereign debt crisis exposed a feedback mechanism that regulators had underestimated: sovereign stress degraded bank capital (via mark-to-market losses on government bond portfolios and falling collateral values), which in turn raised the expected cost of sovereign bail-outs, amplifying sovereign spreads further. This "diabolic loop" (Brunnermeier et al., 2016; Farhi and Tirole, 2018) became the canonical framing for European financial stability analysis and drove regulatory reforms including the European Banking Union.

Yet the diabolic loop literature has two structural features that limit its scope. First, it operates at the national level: one sovereign, one banking sector, one feedback mechanism. Second, it focuses on tradeable government debt (bond holdings) as the transmission channel. Neither feature captures the *subnational* dimension: banks that extend credit directly to individual local governments, whose fiscal positions are heterogeneous, and whose exposure concentrations may amplify or absorb shocks in ways that aggregate statistics cannot reveal.

Luxembourg presents the conditions under which this gap matters most. Its banking sector is anomalously large (approximately 12 times GDP) but its domestic sovereign is anomalously strong (Maastricht debt approximately 25–26% of GDP, AAA/Aaa rating, persistent fiscal surpluses). The dominant risk channel runs *outward* — Luxembourg MFIs hold substantial euro-area sovereign bond portfolios and face contagion through the European channel. But the banking sector also extends credit to 102 communes whose fiscal positions differ dramatically, and whose dependence on central government transfers, debt-service capacity, and revenue base vary across a wide spectrum.

The research question is therefore: *does concentrated banking sector exposure to local government borrowers in Luxembourg create a subnational sovereign-bank nexus, and can forward-looking ML-based fiscal risk indicators serve as an early-warning system for regional financial stability?*

This proposal argues this question is tractable, original, and policy-relevant. It is tractable because Luxembourg's small scale makes administrative data linkage feasible. It is original because no study has applied the Khwaja-Mian (2008) credit supply identification strategy to public-sector sub-sovereign borrowers. And it is policy-relevant because the ECB's macroprudential framework currently has no mechanism to detect concentrated bank–commune credit risks before they aggregate to a systemic level.

---

## 2. Motivation and Structural Context

### 2.1 Luxembourg's Exceptional Position

Luxembourg's banking sector is structurally unlike that of any typical euro-area economy. With total MFI assets standing at approximately €956 billion against GDP of approximately €70 billion (ECB BSI 2021; Eurostat), the ratio of approximately 12 times GDP places it among the highest in the euro area (IMF FSAP 2017). This scale is explained by Luxembourg's role as a hosting jurisdiction for internationally active financial groups: 126 credit institutions operated as of the most recent available data, many booking cross-border portfolios domestically.

Domestic sovereign risk is minimal by standard measures. General government debt averaged approximately 25–26% of GDP through 2023 (Eurostat gov_10dd_edpt1), the government has maintained persistent fiscal surpluses except for a brief COVID-19 compression, and Luxembourg holds AAA/Aaa ratings from all three major agencies (Luxembourg Ministry of Finance, 2024). The dominant sovereign-bank transmission channel therefore runs through EA sovereign bond contagion, not domestic fiscal stress.

The subnational dimension is analytically separate. Luxembourg's 102 communes (LAU 2021 boundary vintage; reduced to 100 following the 2023 Käerjeng and Reckange/Mess mergers) display heterogeneous fiscal capacity along multiple dimensions. Per-capita income indices range from below 75 to above 130 (LU = 100; STATEC LUSTAT 2021). Population ranges from under 1,000 (Reuland: 872) to over 130,000 (Luxembourg City: 134,881). Unemployment rates vary from below 3.5% to above 6.5%, and foreign population shares — a structural indicator of labour market composition — range from under 25% to over 70%. These differences create differentiated fiscal pressure profiles that are invisible in national aggregates.

### 2.2 The Structural Conditions for a Subnational Nexus

For a subnational nexus to exist and to have financial stability implications, three structural conditions must hold simultaneously. First, banks must have concentrated credit exposures to individual communes rather than diversified across all 102. If exposure is uniform, commune-level fiscal heterogeneity does not map into bank-level heterogeneity. Second, commune-level fiscal stress must be sufficiently severe or correlated across communes that it materially affects bank balance sheets. Third, affected banks must lack the capital buffer or substitution mechanism to absorb the credit loss without contracting other credit. All three conditions are empirically testable — and none has been tested for Luxembourg.

### 2.3 Policy Relevance

The FSB/IMF systemic risk review of June 2023 identified subnational public finance as an understudied transmission channel, particularly in small financial centres where concentrated public-sector lending may escape aggregate indicators. The ECB's macroprudential toolkit — countercyclical capital buffer, systemic risk buffer, SREP — is calibrated on national aggregates. A bank with highly concentrated commune exposure could pass all macro-level screens while carrying a localised vulnerability. This research proposes to measure whether and how much that gap matters for Luxembourg.

---

## 3. Literature Review

The proposal sits at the intersection of three established literatures, each of which leaves a gap that this research is designed to fill.

### 3.1 The Sovereign-Bank Nexus

**Acharya, Drechsler, and Schnabl (2014)** establish the theoretical mechanism of the doom loop: sovereign stress impairs bank capital through marked-to-market losses on government bond holdings; bank distress raises sovereign risk through the expectation of bail-outs. The feedback is mutual and self-reinforcing. Their framework is the foundation of the nexus literature but operates at the national level only — there is a single sovereign and a single banking sector.

**Brunnermeier, Garicano, Lane, Pagano, Reis, Santos, Thesmar, Van Nieuwerburgh, and Vayanos (2016, AEA P&P)** quantify the doom loop across euro-area countries during the 2010–2012 crisis, confirming that banks with high domestic sovereign bond portfolios suffered larger capital losses that fed back into sovereign spreads. The mechanism is empirically documented at national scale; subnational heterogeneity and within-country exposure concentration are not identified.

**Gennaioli, Martin, and Rossi (2014, QJE)** provide cross-country panel evidence that sovereign defaults are more damaging when domestic banks held larger pre-crisis government debt shares. They identify the balance-sheet channel: credit supply contraction after default is proportional to pre-default bank sovereign exposure. The paper establishes the empirical regularity at the national level; the analogous within-country variation across sub-sovereign borrowers and lenders remains unmeasured.

**Farhi and Tirole (2018, AER)** develop the equilibrium model in which banks' sovereign portfolio choices and sovereign default risk are jointly determined. Banks optimally load on domestic government debt to secure implicit bail-out guarantees; sovereigns tolerate this to secure market access. The "deadly embrace" is a self-fulfilling equilibrium. The model has one sovereign and one banking sector; it does not accommodate heterogeneous sub-sovereign borrowers or geographic concentration within a single country's banking system.

### 3.2 Credit Supply Identification

**Khwaja and Mian (2008, AER)** develop the matched bank-borrower identification strategy for separating credit supply shocks from demand. Comparing credit growth to the same borrower across banks with different liquidity shocks isolates the supply component. This is the methodological template for H1 of this proposal — applied, for the first time, to public-sector sub-sovereign borrowers rather than private firms. Commune borrowers may have fewer substitute lenders than firms, which both strengthens the identification and amplifies the economic magnitude.

**Jiménez, Ongena, Peydró, and Saurina (2014, AER)** apply firm × time fixed effects to Spain's credit register (23 million loans) to isolate credit supply from demand in the context of monetary policy transmission. Their identification standard — within-borrower, across-lender variation — is directly adopted by this proposal's H1 design, adapted for public-sector borrowers whose demand is shaped by fiscal rules rather than investment opportunities.

**Peek and Rosengren (2000, AER)** use Japanese bank capital losses as a quasi-experiment to show that bank balance-sheet shocks transmit to real activity through pre-existing lender-borrower relationships. The geographic localisation of the effect demonstrates that borrowers without substitute lenders bear the largest adjustment. The domestic public-sector channel — a home-country bank contracting credit to its local government borrowers — operates with even lower substitution margins and has not been studied with analogous identification.

### 3.3 Subnational Fiscal Dynamics

**Poterba (1994, JPE)** studies how US states adjust to unexpected fiscal shocks, finding that balanced-budget rule stringency and political fragmentation explain adjustment speed and deficit persistence. Fiscal institutions — not just economic fundamentals — determine how subnational governments respond to revenue shortfalls. The banking sector channel — how credit supply conditions shape the adjustment path — is not modelled.

**Rodden (2006, CUP)** documents that fiscal federalism produces soft budget constraints when subnational governments anticipate central-government bail-outs. The expectation of rescue alters borrowing behaviour and reduces fiscal discipline; the effect is priced into sub-sovereign debt terms in Germany, Brazil, and India. The banking sector as transmission mechanism — how lender concentration amplifies fragility or prices soft-budget-constraint risk — is not studied.

**Hendrick (2011)**, **Honadle, Costa, and Cigler (2004)**, and **Kloha, Weissert, and Kleine (2005)** operationalise fiscal stress for municipalities using balance, debt, revenue composition, and expenditure indicators. These frameworks directly inform the commune-level outcome variables and distress labels in this proposal. None of these studies models the banking sector counterpart; fiscal stress is treated as a purely public-finance phenomenon with no credit-market feedback.

### 3.4 Machine Learning for Early Warning

**Beutel, List, and von Schweinitz (2019, Deutsche Bundesbank DP)** compare logit, random forest, and gradient boosting for predicting banking crises at the national level. ML offers modest gains over logit but requires strict temporal validation to avoid look-ahead leakage. Their benchmark methodology — out-of-sample rolling-origin validation, AUC-ROC reporting, false-alarm-rate discipline — is adopted directly by H3 of this proposal. No study has applied temporal ML validation to a subnational commune-year panel as the feature space for a fiscal or banking stability early-warning system.

**Holopainen and Sarlin (2017)** and **Alessi and Detken (2018)** extend the early-warning literature to gradient boosting and deep learning for national banking crisis prediction. The ECB BEAST (Banking Early-Warning Stress Test) model operates similarly. The feature inputs in all cases are macroeconomic aggregates; the subnational commune panel — as both a target and a feature space — has not been used.

### 3.5 Financial Networks and Concentration Risk

**Acemoglu, Ozdaglar, and Tahbaz-Salehi (2015, AER)** show that dense financial networks are robust to small shocks but fragile to large ones, and that concentrated linkages — few heavily-weighted connections — increase system-wide fragility once a shock threshold is crossed. This provides the graph-theoretic foundation for why concentrated borrower networks amplify rather than diversify idiosyncratic risk. The interbank linkage case has been studied extensively; the bank-commune credit network — where banks connect to sub-sovereign borrowers with concentrated weights — represents an analogous but empirically unstudied topology in small financial centres.

### 3.6 Summary of the Gap

The literature has documented the sovereign-bank nexus at the national level, developed gold-standard identification strategies for credit supply, and established ML benchmarks for banking crisis prediction. What has not been done is to bring these three strands together at the subnational level: identifying whether banks' concentrated local-government credit portfolios create a within-country nexus, and whether ML applied to commune-year panels can detect it early. This is the contribution this proposal makes.

---

## 4. Theoretical Framework

### 4.1 The Three-Stage Subnational Nexus Mechanism

The theoretical argument unfolds in three stages, each of which constitutes a testable sub-claim.

**Stage 1 — Exposure Concentration.** Credit to local governments in a small financial centre is unlikely to be uniformly distributed across borrowers. Luxembourg's 126 credit institutions serve 102 communes of vastly different size and fiscal depth. A Herfindahl-Hirschman Index (HHI) of commune credit per bank — constructed as $\text{HHI}_{b,t} = \sum_{i=1}^{102} \left(\frac{C_{b,i,t}}{\sum_j C_{b,j,t}}\right)^2$ — captures the degree to which any given bank's commune lending is concentrated. If this HHI is high for a subset of banks and those banks are concentrated in specific communes, the structural precondition for a nexus is met. Stage 1 is testable with BCL supervisory credit register data.

**Stage 2 — The Capital Channel.** If a concentrated borrower commune enters fiscal stress — operationalised by a deficit-to-revenue ratio exceeding a threshold, a multi-year deficit streak, or a deterioration in transfer-dependence ratios — exposed banks face expected losses that affect their capital positions. The transmission mechanism follows the standard loan-loss logic: $\text{EL}_{b,t} = \text{LGD} \times \text{PD}_{i,t} \times \text{Exposure}_{b,i,t}$. Banks with higher $\text{Exposure}_{b,i,t}$ face proportionally larger capital pressure when commune $i$'s $\text{PD}$ rises. The capital channel determines whether and how quickly the bank contracts other credit in response. Stage 2 requires both BCL credit data and CSSF COREP bank capital data.

**Stage 3 — Real-Economy Feedback.** If the credit contraction in Stage 2 is large enough relative to local credit market depth, or if the affected bank has relationship-specific lending to other local borrowers (small businesses, households), fiscal stress in commune $i$ can generate real activity effects in that commune's economic catchment area. This is the subnational feedback loop: fiscal stress → bank capital impairment → credit contraction → local real activity deterioration → further fiscal stress via the tax base and expenditure demand. Stage 3 requires longitudinal commune-level employment, income, and housing data alongside the bank credit register.

### 4.2 Structural Conditions for Activation

For the three-stage mechanism to produce a measurable nexus, four structural conditions must hold simultaneously: (i) bank exposure to individual communes is concentrated, not diversified; (ii) commune fiscal stress is severe enough and persistent enough to generate material expected losses; (iii) affected banks lack the capital buffer to absorb losses without adjusting their credit book; and (iv) commune borrowers face limited substitution — they cannot costlessly replace a contracting lender with another. None of these conditions is asserted in this proposal; all four are empirically testable.

**Identification assumption.** The key assumption underlying the H1 test is that credit demand from a given commune does not covary with the bank-specific liquidity or capital shock that triggers credit supply contraction. This assumption is satisfied if exposure concentration is predetermined (lagged by at least one year) and if commune-specific credit demand is absorbed by commune × year fixed effects in the fully specified model.

---

## 5. Research Hypotheses

The proposal organises its empirical contribution into three nested hypotheses, each addressing a distinct link in the theoretical chain.

**H1 — Subnational Nexus (Existence Test)**

*Banks with higher concentrated exposure to individual Luxembourg communes are expected to reduce credit supply to those communes differentially when commune fiscal stress rises, controlling for commune credit demand and bank-level characteristics.*

The hypothesis is testable via a bank-commune-year panel regression comparing credit growth to the same commune across banks with different pre-period exposure concentrations (following Khwaja and Mian, 2008). The identification strategy absorbs commune × time fixed effects to isolate supply from demand. This test requires BCL supervisory credit register data (MOU required).

**H2 — Fiscal–Credit Causality (Direction Test)**

*Commune-level fiscal deterioration — measured by balance-to-revenue ratio, deficit persistence, and transfer-dependence — is hypothesised to Granger-cause subsequent changes in bank credit supply to the local public sector at a 1–2 year lag, with the direction running from fiscal to credit rather than the reverse.*

The hypothesis is testable at the aggregate level using ECB BSI public-sector credit series and Eurostat GFS commune fiscal data — no MOU is required for the H2 aggregate test. A bank-by-commune panel VAR test, once BCL data are available, will provide finer-grained identification. H2 tests the causal direction; H1 tests the heterogeneity across exposed and unexposed banks.

**H3 — ML Early Warning (Prediction Test)**

*An XGBoost-based early-warning model trained on the commune-year fiscal panel is proposed to exceed a benchmark of AUC-ROC ≥ 0.75 at a t+1 horizon, with Precision–Recall AUC and calibration metrics reported for macroprudential usefulness.*

H3 is testable once a fiscal panel with credible distress labels is available from STATEC commune financial accounts. The model design follows the Beutel et al. (2019) benchmark methodology: rolling-origin temporal validation, explicit false-alarm-rate reporting, and a transparent logit baseline comparison. The heuristic stress index implemented in `js/shared.js` and `api/fiscal_ml_api.py` serves as the deterministic baseline against which the ML model must demonstrate improvement.

---

## 6. Research Design and Methodology

### 6.1 H1 — Bank-Commune Panel Regression

The baseline specification for H1 is:

$$\Delta \text{Credit}_{b,i,t} = \beta \cdot \text{ExposureHHI}_{b,i,t-1} + \theta \cdot \text{FiscalStress}_{i,t-1} + \alpha_i + \delta_b + \gamma_t + \mathbf{X}'_{b,i,t-1}\lambda + \varepsilon_{b,i,t}$$

where $b$ indexes banks, $i$ communes, $t$ years; $\Delta \text{Credit}$ is the log-change in credit extended by bank $b$ to commune $i$; $\text{ExposureHHI}$ is the bank-level Herfindahl index of commune credit concentration; $\text{FiscalStress}$ is a commune-level indicator of fiscal deterioration; $\alpha_i$, $\delta_b$, $\gamma_t$ are commune, bank, and year fixed effects; and $\mathbf{X}$ is a vector of pre-determined controls. The coefficient of interest is $\beta$: a negative estimate would indicate that more concentrated banks reduce credit more when their key commune borrower deteriorates.

**Robustness:** Commune + bank + year fixed effects as the baseline; canton-year interactions to absorb regional shocks; lagged exposure to address endogeneity; alternative fiscal-stress thresholds; matched event-study around commune stress onset events; spatial lag and spatial error models to account for geographic spillovers.

**Identification limitation.** The critical data requirement is a bank-by-commune credit register from BCL, which has not yet been obtained. Until the MOU is executed, H1 cannot be tested at the bank-commune level. The minimum viable Plan B substitute (described in Section 8) uses the commune-level proxy panel to demonstrate the analytical framework.

### 6.2 H2 — Granger Causality and Panel VAR

The aggregate H2 test uses publicly available data (ECB BSI public-sector credit + Eurostat GFS) in a bivariate panel VAR:

$$\begin{pmatrix} \text{Credit}_{t} \\ \text{FiscalBalance}_{t} \end{pmatrix} = \sum_{k=1}^{K} \mathbf{A}_k \begin{pmatrix} \text{Credit}_{t-k} \\ \text{FiscalBalance}_{t-k} \end{pmatrix} + \mathbf{u}_t$$

Standard Granger causality tests determine whether lagged fiscal balance terms contribute to the credit equation (and vice versa) after controlling for serial dependence. The commune-level version of this test — with bank × commune panel structure — requires BCL data and is designated WP2 in the full design.

### 6.3 H3 — ML Pipeline Architecture

The ML design follows the four-stage model ladder described in `research/ml_pipeline_plan.md`:

1. **Heuristic baseline** — 4-component deterministic stress index (already implemented); serves as the floor the ML model must beat.
2. **Logit benchmark** — cross-sectional and panel logit on fiscal and structural features; provides interpretable odds ratios and establishes the linear separability ceiling. A preliminary version using non-circular structural predictors on the proxy panel (N = 102) has been run and yields AUC-ROC = 0.697; this result is a pipeline feasibility check only, not a test of H3.
3. **Random forest** — captures non-linear interactions between fiscal variables; feature importance via permutation.
4. **XGBoost + SHAP** — gradient boosted trees with SHAP (Shapley Additive Explanations) for per-commune decomposition of predicted distress probability; the primary H3 model.

**Temporal validation protocol.** Rolling-origin cross-validation with expanding training windows and a held-out final period; no future information is permitted in any training feature. AUC-ROC, PR-AUC (appropriate for class-imbalanced labels), Brier score, and false-alarm rate at a policy-relevant threshold are all reported. Calibration curves document whether the model's predicted probabilities are reliable.

**Target variable.** Primary: $\text{FiscalDistress}_{i,t+1} = 1$ if commune $i$ satisfies a fiscal stress criterion in year $t+1$. Candidate criteria: deficit > 15% of revenues; two or more consecutive deficit years; debt-service pressure above an empirically derived threshold. Robustness labels at the 20th and 30th percentile of each criterion are also reported.

---

## 7. Data Sources and Access Requirements

### 7.1 Publicly Available (Implemented)

| Dataset | Provider | Status |
|---|---|---|
| MFI total assets, credit to government, credit to private sector, government bond holdings | ECB Data Portal (BSI) | Live in platform; annual 2014–2023 |
| General government fiscal balance and expenditure | Eurostat GFS (`gov_10q_ggnfa`, `gov_10a_exp`) | Live in platform; annual 2014–2023 |
| Commune socioeconomic indicators | STATEC LUSTAT 2021 | Snapshot in `data/communes.json` (STATEC LUSTAT source; distinct from GISCO GeoJSON `POP_2021`) |
| Commune boundaries | Eurostat GISCO LAU 2021 | In `data/lu_communes.geojson`; 1:1M, EPSG:4326 |

### 7.2 Requiring Formal Data Request (Not Yet Obtained)

| Dataset | Provider | Research role | Blocking for |
|---|---|---|---|
| Commune financial accounts (revenue, expenditure, balance, debt) | STATEC / Ministère de l'Intérieur | True fiscal distress labels; commune-year panel | H1 (outcome variable), H3 (target label) |
| Bank-by-commune public-sector credit register | Banque centrale du Luxembourg (BCL) | Identify nexus exposure; H1 independent variable | H1 (core test) |
| Bank capital, provisions, NPL indicators (COREP) | CSSF / BCL | Link commune exposure to bank-level outcomes | H1 (capital channel, Stage 2) |

Access to BCL and CSSF data requires execution of a formal Memorandum of Understanding. The STATEC commune financial accounts request is an independent process. Both are initiated at the start of WP1; neither has a guaranteed timeline.

### 7.3 Minimum Viable Panel

A commune-year panel row requires: LAU code; commune name; year; fiscal revenue, expenditure, balance, debt (STATEC); transfer-dependence ratio; population; local labour market and income proxies; cantonal identifier; spatial neighbour identifiers. The full design adds bank identifiers and bank-commune credit exposure from BCL. The prototype panel in `data/panel_dataset.csv` contains the structural (non-fiscal) dimension for all 102 communes as of 2021; it uses socioeconomic proxy labels and is useful for pipeline testing only.

---

## 8. Preliminary Evidence

### 8.1 Heuristic Stress Index

A 4-component deterministic stress score has been constructed on publicly available ECB and Eurostat data. The index combines bond concentration (30%), public credit share (30%), fiscal balance (25%), and banking sector size (15%), each normalised to [0, 1] against domain-specific thresholds and aggregated with fixed weights. The score has remained below 0.25 (Low regime) throughout 2014–2023, consistent with Luxembourg's national fiscal resilience. This confirms that national aggregate indicators do not exhibit the stress signal that the subnational hypothesis targets. The index is implemented identically in `js/shared.js` (frontend) and `api/fiscal_ml_api.py` (API). It serves as the deterministic baseline the ML design must exceed. The live API is deployed at `https://aetherno-luxfin-api.hf.space`.

### 8.2 Preliminary Proxy-Panel Logit

To demonstrate pipeline viability, a logistic regression was estimated on the 2021 cross-section (N = 102 communes) using structural predictors that do not enter the proxy label construction (non-circular design). The three label-defining variables — unemployment rate, income index, employment rate — were excluded. The five non-circular predictors are: foreign population share, population density, DEGURBA urbanisation class, total population, and cross-border worker share.

Results (standardised predictors, BFGS optimisation):

| Predictor | Coef. | Std. Error | p-value | Sig. |
|---|---|---|---|---|
| Intercept | −1.473 | 0.281 | < 0.001 | *** |
| Foreign population share (%) | −1.404 | 0.552 | 0.011 | * |
| Population density (per km²) | 1.113 | 0.671 | 0.097 | . |
| DEGURBA (urbanisation class) | −0.913 | 0.615 | 0.137 | |
| Population (total) | −4.860 | 3.692 | 0.188 | |
| Cross-border worker share | 4.223 | 3.253 | 0.194 | |

AUC-ROC = 0.697 · Pseudo R² (McFadden) = 0.092 · AIC = 108.6 · N = 102 · Prevalence = 21.6% (22/102 flagged)

*Note: a convergence warning is produced (BFGS; small N with sparse labels). Point estimates are reported as preliminary indicators; standard errors should be interpreted cautiously.*

**Interpretation.** The negative coefficient on foreign population share is geographically intuitive: communes with high foreign-resident shares tend to be economically active peri-urban areas, while proxy-flagged communes are predominantly rural northern municipalities (Oesling region) with below-average income and above-average unemployment. The positive population density coefficient reflects high per-capita expenditure pressure in smaller, denser communes with limited own-source revenue. When STATEC commune financial accounts replace the proxy label, these structural controls will enter the full commune-year panel regression as baseline covariates.

**This result does not constitute a test of any research hypothesis.** It is a pipeline feasibility demonstration on a proxy outcome. The reproducible script is at `scripts/logit_baseline.py`.

---

## 9. Work Plan

The full design is organised into four work packages spanning 36 months.

| WP | Title | Months | BCL-dependent? |
|---|---|---|---|
| WP1 | Data Architecture & Panel Construction | 0–10 | Partial (MOU submission) |
| WP2 | Empirical Analysis — H1 & H2 | 6–22 | H1 yes; H2 no |
| WP3 | ML Early-Warning Pipeline — H3 | 14–28 | Yes (labelled panel) |
| WP4 | Policy Integration & Dissemination | 26–36 | Partial |

**WP1 (Months 0–10):** Submit STATEC commune financial accounts request; submit BCL/CSSF MOU; construct commune-year panel from STATEC data; validate commune LAU code matching; build spatial adjacency matrix (queen contiguity, R `spdep`); extend prototype panel to multi-year structure. Deliverable: `panel_dataset.csv` with fiscal accounts (extending the prototype).

**WP2 (Months 6–22):** Aggregate H2 VAR test (public data — executable immediately); descriptive statistics and EDA on commune panel; bank-commune panel regression (H1) once BCL data available; Granger causality and panel VAR at commune-bank level (H2); spatial econometrics (spillover tests); robustness: IV design, event study, alternative fixed effects. Deliverables: Working Paper 1 (H1 + H2).

**WP3 (Months 14–28):** Feature engineering on commune-year panel; temporal train/test split and rolling-origin cross-validation; model training: logit → RF → XGBoost; SHAP analysis and per-commune decomposition; API deployment (extending the live LuxFin API); threshold calibration for policy application; false-alarm-rate reporting. Deliverables: Working Paper 2 + deployed ML API.

**WP4 (Months 26–36):** BCL/CSSF policy brief on early-warning design; journal submission (Papers 1 & 2); integration of trained ML model into the LuxFin research platform; PhD thesis compilation and defence. Deliverables: 2 journal papers + BCL policy note + thesis.

---

## 10. Contingency Design

The BCL MOU is the project's binding constraint. Its timeline is institution-dependent and cannot be guaranteed. The table below maps the key activities to their dependency and identifies the Plan B execution path.

| Activity | Months | BCL-dependent? | Plan B if MOU delayed / refused |
|---|---|---|---|
| STATEC commune fiscal accounts request | 0–4 | Partial | Use proxy panel; expand with STATEC open releases |
| BCL/CSSF MOU submission | 0–6 | Core | Begin H2 aggregate VAR immediately |
| Commune panel construction (WP1) | 2–8 | Partial | Prototype N=102 panel sufficient for methods paper |
| Spatial adjacency and spillover analysis | 6–14 | No | Fully executable on public GIS data |
| H2 aggregate test | 6–18 | No | **Publishable independently on public data** |
| H1 bank-commune regression | 8–22 | Core | Replace with proxy-panel logit ladder |
| H3 XGBoost model | 14–28 | Core | Logit benchmark + heuristic index; methods paper |
| Journal submission | 24–36 | Partial | Plan B paper submittable by Month 20 |

### Plan B — Minimum Viable Publishable Paper

If the MOU is refused or delayed beyond 18 months, the following paper remains achievable using public data only:

- **Core contribution:** aggregate nexus evidence (H2 VAR test) + reproducible heuristic stress benchmark
- **H1:** replaced by proxy-panel logit (N=102, AUC=0.697); framed as a pilot cross-section
- **H2:** aggregate VAR/Granger using ECB BSI + Eurostat GFS — testable immediately
- **H3:** logit model ladder + heuristic benchmark; published as a methodology proposal
- **Target journal:** *Public Finance Review* or *Regional Studies* (vs. *Journal of Financial Stability* / *Review of Finance* for the full design)
- **Data requirement:** ECB Data Portal + Eurostat GFS + STATEC open releases (all already available)
- **Estimated submission:** Month 18–22 (unconditional on MOU outcome)

Plan B is not a fallback — it is a parallel track. Beginning the H2 aggregate analysis and the heuristic benchmark paper immediately de-risks the PhD timeline regardless of MOU outcome.

---

## 11. Expected Contributions

**Contribution 1 — Empirical identification of the subnational sovereign-bank nexus.** No study has applied the Khwaja-Mian matched bank-borrower strategy to public-sector sub-sovereign borrowers. If the nexus is confirmed, the finding would demonstrate that aggregate macroprudential indicators miss a systematic localised vulnerability in concentrated banking sectors.

**Contribution 2 — Credit supply identification for public-sector borrowers.** Extending the gold-standard supply identification methodology (Khwaja-Mian; Jiménez et al.) to the public-sector borrower context fills an explicit methodological gap. Commune borrowers face lower lender substitutability than private firms, which both strengthens the identification and raises the policy stakes.

**Contribution 3 — Subnational ML early-warning system.** The H3 design is the first application of temporal ML validation to a commune-year panel as the feature space for a banking stability early-warning indicator. Successful prediction would suggest that the ECB macroprudential toolkit should be extended to incorporate subnational fiscal panel signals.

**Contribution 4 — Reproducible research infrastructure.** The full pipeline — data ingestion from ECB Data Portal and Eurostat, heuristic stress index, commune map, preliminary logit, FastAPI endpoints — is implemented, open, and verifiable at [rishikeshgovind.github.io/luxfin](https://rishikeshgovind.github.io/luxfin). The API (`https://aetherno-luxfin-api.hf.space`) is live. This infrastructure is itself a contribution to reproducible computational social science methodology.

---

## 12. Limitations

**Data constraints.** The core nexus test (H1) and the supervised ML model (H3) require supervisory data not yet obtained. All claims in this proposal about the existence of a nexus are presented as testable hypotheses; none is asserted as a finding.

**Small N.** With 102 communes and a relatively short time series (10 years of public data; potentially more with STATEC accounts), statistical power for the fixed-effects panel regression is limited. Rare fiscal stress events — Luxembourg's structural surpluses mean commune distress is uncommon — will constrain label prevalence for the ML model. The robustness strategy (multiple label thresholds, sensitivity analysis on fixed effects) addresses this partially; it does not eliminate it.

**External validity.** Luxembourg is a structural outlier in the euro area. Results on a 12× GDP banking sector hosting 126 institutions in 102 communes do not straightforwardly generalise to federal countries with thousands of sub-sovereign units and deeper credit markets. The research is designed as a case study that establishes proof-of-concept for the subnational nexus idea; cross-country generalisation would require further work.

**Proxy outcome.** The current prototype panel uses a socioeconomic proxy label (derived from unemployment, income, and employment z-scores) that does not measure fiscal distress. All preliminary analyses using this proxy — including the AUC=0.697 logit result — are pipeline feasibility demonstrations. Substantive inference requires replacement with STATEC commune financial accounts data.

**Identification assumptions.** The H1 credit supply identification requires that exposure concentration is not endogenously determined by anticipated commune fiscal deterioration. Lagging exposure by one year and absorbing commune × year fixed effects partially addresses this; it does not rule out forward-looking bank behaviour.

---

## 13. Ethical Considerations

The research uses aggregate administrative data at the commune level and anonymised bank-level aggregates. No individual-level personal data are involved. BCL/CSSF supervisory data access will be governed by a formal MOU with data security and confidentiality obligations. Results will be aggregated so that no individual bank or commune official is identifiable from published outputs. The research platform [rishikeshgovind.github.io/luxfin](https://rishikeshgovind.github.io/luxfin) displays only aggregate national statistics and commune-level socioeconomic data already published by STATEC/LUSTAT.

---

## 14. References

Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). Systemic risk and stability in financial networks. *American Economic Review*, 105(2), 564–608.

Acharya, V., Drechsler, I., & Schnabl, P. (2014). A pyrrhic victory? Bank bailouts and sovereign credit risk. *Journal of Finance*, 69(6), 2689–2739.

Alessi, L., & Detken, C. (2018). Identifying excessive credit growth and leverage. *Journal of Financial Stability*, 35, 215–225.

Beutel, J., List, S., & von Schweinitz, G. (2019). Does machine learning help us predict banking crises? *Deutsche Bundesbank Discussion Paper*, No. 16/2019.

Blöchliger, H., & King, D. (2006). Fiscal autonomy of sub-central governments. *OECD Working Papers on Fiscal Federalism*, No. 2.

Brunnermeier, M., Garicano, L., Lane, P., Pagano, M., Reis, R., Santos, T., Thesmar, D., Van Nieuwerburgh, S., & Vayanos, D. (2016). The sovereign-bank diabolic loop and ESBies. *American Economic Review: Papers & Proceedings*, 106(5), 508–512.

Farhi, E., & Tirole, J. (2018). Deadly embrace: Sovereign and financial balance sheets doom loops. *American Economic Review*, 108(2), 419–458.

Gennaioli, N., Martin, A., & Rossi, S. (2014). Sovereign default, domestic banks, and financial institutions. *Journal of Finance*, 69(2), 819–866.

Hendrick, R. (2011). Managing the fiscal metropolis: The financial policies, practices, and health of suburban municipalities. *Georgetown University Press*.

Holopainen, M., & Sarlin, P. (2017). Toward robust early-warning models: A horse race, ensembles and model uncertainty. *Quantitative Finance*, 17(12), 1933–1963.

Honadle, B. W., Costa, J. M., & Cigler, B. A. (2004). *Fiscal health for local governments: An introduction to concepts, practical analysis, and strategies*. Elsevier Academic Press.

IMF. (2017). *Luxembourg: Financial System Stability Assessment*. IMF Country Report No. 17/121.

Jiménez, G., Ongena, S., Peydró, J.-L., & Saurina, J. (2014). Hazardous times for monetary policy: What do twenty-three million bank loans say about the effects of monetary policy on credit risk-taking? *Econometrica*, 82(2), 463–505.

Jordà, Ò., Schularick, M., & Taylor, A. M. (2016). The great mortgaging: Housing finance, crises and business cycles. *Economic Policy*, 31(85), 107–152.

Khwaja, A. I., & Mian, A. (2008). Tracing the impact of bank liquidity shocks: Evidence from an emerging market. *American Economic Review*, 98(4), 1413–1442.

Kloha, P., Weissert, C. S., & Kleine, R. (2005). Developing and testing a composite model to predict local fiscal distress. *Public Administration Review*, 65(3), 313–323.

Oates, W. E. (1999). An essay on fiscal federalism. *Journal of Economic Literature*, 37(3), 1120–1149.

Peek, J., & Rosengren, E. (2000). Collateral damage: Effects of the Japanese bank crisis on real activity in the United States. *American Economic Review*, 90(1), 30–45.

Poterba, J. M. (1994). State responses to fiscal crises: The effects of budgetary institutions and politics. *Journal of Political Economy*, 102(4), 799–821.

Rodden, J. A. (2006). *Hamilton's paradox: The promise and peril of fiscal federalism*. Cambridge University Press.

Rodden, J. A., Eskeland, G. S., & Litvack, J. (Eds.). (2003). *Fiscal decentralization and the challenge of hard budget constraints*. MIT Press.

---

*Platform and reproducible code: [rishikeshgovind.github.io/luxfin](https://rishikeshgovind.github.io/luxfin)*
*Live API: [aetherno-luxfin-api.hf.space](https://aetherno-luxfin-api.hf.space)*
*Repository: [github.com/RishikeshGovind/luxfin](https://github.com/RishikeshGovind/luxfin)*
