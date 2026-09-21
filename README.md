# CO₂ Storage Heterogeneity Screening — SPE11b (live, reproducible)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/todak2000/co2-heterogeneity-screening/HEAD?labpath=heterogeneity_screening.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/todak2000/co2-heterogeneity-screening/blob/main/heterogeneity_screening.ipynb)

An open-source implementation of three analytical heterogeneity corrections for CO₂
storage screening — **Dykstra–Parsons**, **Shook & Mitchell sweep efficiency**, and the
**Kopp et al. storage-efficiency factor** — applied to the **SPE11b** field-scale
benchmark.

## Run it live (no install)

Click the **Binder** badge above to launch an interactive session in your browser, or
**Open in Colab**. The notebook is fully self-contained: it needs only `numpy` and
`matplotlib`, and either uses the bundled data or downloads it automatically.

Alternatively, clone and run locally:

```bash
git clone https://github.com/todak2000/co2-heterogeneity-screening.git
cd co2-heterogeneity-screening
jupyter notebook heterogeneity_screening.ipynb
```

## What it reproduces

| Result | Value |
|--------|-------|
| Dykstra–Parsons coefficient, derived from SPE11b facies | **V_DP = 0.66** (1σ band 0.50–0.77) |
| SPE11b residual (immobile) trapping at 50 yr | **≈ 0.04–4%** of injected CO₂ |
| Box time-series budget at 50 yr | **≈ 21–32%** of injected CO₂ reported |

Three figures and a full uncertainty quantification (the four-simulator ensemble spread
plus the V_DP/PVI parameter bands) are generated inline.

## Repository contents

- `heterogeneity_screening.ipynb` — the live, executable notebook.
- `manuscript.md` — the companion paper (SPE-formatted).
- `figures/` — the three figures as 300 dpi PNGs.
- `scripts/` — the standalone Python modules (`facies_heterogeneity.py`,
  `benchmark_analysis.py`, `make_figures.py`).
- `data/timeseries/` — SPE11b time series (rice1, ctc-cne1, opm1, sintef1).
- `benchmark_spec/` — the official SPE CSP-11 description and `GROUND_TRUTH.md`.

## Data

SPE11b data © the 11th SPE Comparative Solution Project (Nordbotten, J.M., Fernø, M.A.,
Flemisch, B., Kovscek, A.R., Lie, K.-A. (2024), *SPE Journal*, doi:10.2118/218015-PA),
distributed under the benchmark's open terms: https://spe.org/csp/spe11.
