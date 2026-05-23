# LuxFin commune-year panel builder (R version)
# Mirrors scripts/build_panel.py — R is the preferred language for the
# final panel once BCL/STATEC commune fiscal accounts are obtained.
#
# Current state: uses STATEC LUSTAT 2021 snapshot + Eurostat GFS national
# aggregates as a prototype panel with socioeconomic proxy distress labels.
#
# Run from repo root:
#   Rscript scripts/build_lux_panel.R
#
# Required packages: jsonlite, dplyr, readr

suppressPackageStartupMessages({
  library(jsonlite)
  library(dplyr)
  library(readr)
})

ROOT  <- here::here()   # or set manually: ROOT <- "/path/to/luxfin"
DATA  <- file.path(ROOT, "data")

# ── Load source data ──────────────────────────────────────────────────────────
communes_json <- fromJSON(file.path(DATA, "communes.json"))
banking_json  <- fromJSON(file.path(DATA, "banking.json"))
fiscal_json   <- fromJSON(file.path(DATA, "fiscal.json"))

# Flatten communes (list-of-lists → data frame)
communes_list <- communes_json$communes
communes_df   <- bind_rows(lapply(names(communes_list), function(nm) {
  row        <- as.data.frame(communes_list[[nm]], stringsAsFactors = FALSE)
  row$commune <- nm
  row
})) |>
  select(commune, lau_id, canton, everything())

# National annual data frames
banking_df <- as.data.frame(banking_json$annual)
fiscal_df  <- as.data.frame(fiscal_json$annual)

# ── National context at reference year ───────────────────────────────────────
PANEL_YEARS <- 2021L   # expand when additional STATEC years become available

national_ctx <- function(year) {
  b <- banking_df |> filter(years == year)
  f <- fiscal_df  |> filter(years == year)
  bond_conc  <- (b$govt_bonds_held / b$total_assets) * 100
  credit_shr <- (b$credit_govt / (b$credit_govt + b$credit_private)) * 100
  tibble(
    nat_bond_conc    = round(bond_conc, 3),
    nat_credit_shr   = round(credit_shr, 3),
    nat_fiscal_bal   = f$balance_pct_gdp,
    nat_gdp_bn       = f$gdp_eur_bn,
    nat_total_assets = b$total_assets,
    nat_num_banks    = b$num_banks,
    nat_stress_score = {
      comps <- list(
        list(raw = bond_conc,        lo =  3.0, hi = 10.0, inv = FALSE, w = 0.30),
        list(raw = credit_shr,       lo =  6.0, hi = 16.0, inv = FALSE, w = 0.30),
        list(raw = f$balance_pct_gdp,lo = -3.0, hi =  3.0, inv = TRUE,  w = 0.25),
        list(raw = b$total_assets / f$gdp_eur_bn, lo = 8.0, hi = 16.0, inv = FALSE, w = 0.15)
      )
      round(Reduce("+", lapply(comps, function(c) {
        n <- max(0, min(1, (c$raw - c$lo) / (c$hi - c$lo)))
        if (c$inv) n <- 1 - n
        n * c$w
      })), 4)
    }
  )
}

# ── Standardised scores ───────────────────────────────────────────────────────
mu_unemp  <- mean(communes_df$unemployment_rate)
sd_unemp  <- sd(communes_df$unemployment_rate)
mu_income <- mean(communes_df$income_index)
sd_income <- sd(communes_df$income_index)
mu_emp    <- mean(communes_df$employment_rate)
sd_emp    <- sd(communes_df$employment_rate)
mu_forpop <- mean(communes_df$foreign_pop_pct)
sd_forpop <- sd(communes_df$foreign_pop_pct)

# ── Heuristic distress label (proxy) ─────────────────────────────────────────
# Replace with real binary events from BCL commune fiscal accounts when available.
distress_proxy <- function(unemp, income, emp) {
  signals <- 0L
  if (unemp  > mu_unemp  + 0.75 * sd_unemp)  signals <- signals + 1L
  if (income < mu_income - 0.75 * sd_income)  signals <- signals + 1L
  if (emp    < mu_emp    - 0.75 * sd_emp)      signals <- signals + 1L
  as.integer(signals >= 2L)
}

# ── Build panel ───────────────────────────────────────────────────────────────
nat <- national_ctx(PANEL_YEARS)

panel <- communes_df |>
  mutate(
    year        = PANEL_YEARS,
    pop_density = round(population / area_km2, 2),
    unemp_z     = round((unemployment_rate - mu_unemp)  / sd_unemp,  3),
    income_z    = round((income_index      - mu_income) / sd_income, 3),
    emp_z       = round((employment_rate   - mu_emp)    / sd_emp,    3),
    forpop_z    = round((foreign_pop_pct   - mu_forpop) / sd_forpop, 3),
  ) |>
  bind_cols(nat) |>
  mutate(
    # PLACEHOLDER columns — fill when BCL/STATEC supervisory data is obtained
    commune_revenue_eur_m    = NA_real_,
    commune_expenditure_eur_m = NA_real_,
    commune_balance_eur_m    = NA_real_,
    commune_debt_per_capita  = NA_real_,
    bank_commune_credit_eur_m = NA_real_,
    bank_exposure_hhi        = NA_real_,
    fiscal_distress_proxy    = mapply(distress_proxy, unemployment_rate, income_index, employment_rate),
    label_source             = "proxy-socioeconomic-2021",
    data_vintage             = "STATEC-LUSTAT-2021",
  )

# ── Write output ──────────────────────────────────────────────────────────────
output_path <- file.path(DATA, "panel_dataset.csv")
write_csv(panel, output_path)

n_distress <- sum(panel$fiscal_distress_proxy)
cat(sprintf("Written %d rows to %s\n", nrow(panel), output_path))
cat(sprintf("Distress events (proxy): %d / %d (%.1f%%)\n",
            n_distress, nrow(panel), n_distress / nrow(panel) * 100))
cat("\nPLACEHOLDER columns (require BCL/STATEC supervisory data):\n")
cat("  commune_revenue_eur_m, commune_expenditure_eur_m,\n")
cat("  commune_balance_eur_m, commune_debt_per_capita,\n")
cat("  bank_commune_credit_eur_m, bank_exposure_hhi\n")
cat("\nNext: request commune comptes annuels from Ministere de l'Interieur\n")
cat("      and bank-commune credit data via formal BCL/CSSF MOU\n")
