# LuxFin Data Requirements

This file separates evidence already implemented in the public prototype from datasets required for the full PhD design.

## Public / Implemented

| Dataset | Provider | Current use |
|---|---|---|
| MFI balance sheet indicators | ECB Data Portal, BSI | Banking exposure panel and baseline public-sector exposure context |
| General government fiscal aggregates | Eurostat GFS | Fiscal overview and national stress-index component |
| Commune socio-economic indicators | STATEC LUSTAT snapshot | Commune map and prototype vulnerability context |
| Commune boundaries | Eurostat GISCO LAU 2021 | Map layer and future spatial adjacency construction |

## Data Request / Restricted

| Dataset | Provider | Research role |
|---|---|---|
| Commune financial accounts | STATEC / relevant ministry | Build commune-year fiscal panel and fiscal distress labels |
| Bank-by-commune public-sector credit | BCL supervisory data | Estimate the subnational sovereign-bank nexus directly |
| Bank capital, provisions, and NPL indicators | CSSF / BCL COREP or supervisory extracts | Link commune exposure to bank balance-sheet outcomes |

## Minimum Viable Panel

The minimum viable empirical design requires one row per commune-year with:

- LAU code and commune name
- fiscal revenue, expenditure, balance, and debt where available
- transfer-dependence ratio
- population and demographic indicators
- local labour-market and income proxies
- cantonal identifier and spatial-neighbour identifiers

The full design adds bank identifiers and bank-commune credit exposure.
