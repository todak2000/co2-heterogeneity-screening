# Gravity-Dominated CO₂ Storage and the Limits of Agreement in the SPE11b Benchmark

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/todak2000/co2-heterogeneity-screening/HEAD?labpath=heterogeneity_screening.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/todak2000/co2-heterogeneity-screening/blob/main/heterogeneity_screening.ipynb)

A reproducible, evidence-only characterisation of the SPE11b CO₂ storage benchmark: its
dimensionless flow regime, its capillary seal, and how sharply its four participating
simulators agree — and therefore what SPE11b can and cannot be used to validate.

## Run it live (no install)

Click **Binder** or **Open in Colab** above. The notebook needs only `numpy` and `matplotlib`
and uses the bundled data (with an automatic download fallback on Colab).

## Headline results (all verified against the primary sources)

| Result | Value |
|---|---|
| Flow regime | **transitional gravity–viscous**: buoyancy timescale ~43 yr ≈ 50-yr injection |
| Seal | entry pressure **0.19 MPa**, breached by a **~100–200 m** CO₂ column |
| Simulator agreement | **robust** on mobile fraction; **1–2 orders of magnitude spread** on residual & structural trapping |
| Plume fate | centroid rises **+204 m**, migrates **+706 m up-dip** over 1000 yr |

## Repository contents

- `heterogeneity_screening.ipynb` — the live, executable notebook.
- `manuscript.md` — the companion paper (SPE-formatted).
- `figures/` — Figures 1–3 (300 dpi PNG).
- `scripts/` — `spe11b_regime_analysis.py`, `benchmark_analysis.py`, `plume_analysis.py`,
  `make_figures.py`.
- `data/timeseries/` — SPE11b time series (rice1, ctc-cne1, opm1, sintef1).
- `data/spatial_maps_rice1/` — representative rice1 spatial maps.
- `benchmark_spec/GROUND_TRUTH.md` — every verified fact and number with sources.
- `DEPLOY.md` — test → push → deploy guide.

## Data

SPE11b data © the 11th SPE Comparative Solution Project (Nordbotten et al. 2024, *SPE
Journal*, doi:10.2118/218015-PA), https://spe.org/csp/spe11.
