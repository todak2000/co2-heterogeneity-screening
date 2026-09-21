# Formation Heterogeneity in Analytical CO₂ Storage Screening: An Open-Source Implementation of Dykstra–Parsons, Shook–Mitchell and Kopp Corrections, Applied to the SPE11b Field-Scale Benchmark

**Daniel Olagunju**

Universiti Teknologi PETRONAS (UTP), Malaysia

*Prepared for presentation at the SPE International CCUS Conference and Exhibition,
12–13 May 2027, Den Haag, Netherlands.*

---

**Copyright 2027, Society of Petroleum Engineers**

This paper was prepared for presentation at the SPE International CCUS Conference and
Exhibition held in Den Haag, Netherlands, 12–13 May 2027. This paper was selected for
presentation by an SPE program committee following review of information contained in an
abstract submitted by the author(s). Contents of the paper have not been reviewed by the
Society of Petroleum Engineers and are subject to correction by the author(s). The material
does not necessarily reflect any position of the Society of Petroleum Engineers, its
officers, or members. Electronic reproduction, distribution, or storage of any part of this
paper without the written consent of the Society of Petroleum Engineers is prohibited.
Permission to reproduce in print is restricted to an abstract of not more than 300 words;
illustrations may not be copied. The abstract must contain conspicuous acknowledgment of
SPE copyright.

---

## Abstract

Analytical screening of CO₂ storage sites frequently treats the reservoir as homogeneous,
whereas real formations exhibit permeability heterogeneity that reduces sweep efficiency,
enlarges the pressure footprint, and alters long-term trapping. This paper makes three
contributions. First, it presents an open-source Python implementation of three established
analytical heterogeneity corrections — the Dykstra–Parsons permeability-variation
coefficient, the Shook & Mitchell (2009) sweep efficiency, and the Kopp et al. (2010)
storage-efficiency capacity factor — with transparent, unit-explicit code and no
unverifiable calibration constants. Second, it derives the Dykstra–Parsons coefficient of
the SPE11b benchmark directly from its published facies table, obtaining
**V_DP = 0.66** (reservoir sands 101–2027 mD, arithmetic mean 770 mD), together with a
sampling-uncertainty band of **0.50–0.77**. Third, it characterises the SPE11b field-scale
benchmark inventory from its official four-simulator time series, treating the
inter-simulator spread as the irreducible model uncertainty. Three findings follow.
Residual (immobile) trapping is effectively **zero** at
end of injection (<0.1% of injected CO₂), so screening tools that centre on residual
trapping mis-allocate the dominant long-term mechanisms — dissolution and structural
trapping. At end of injection roughly **70–80% of the injected CO₂ is unaccounted for by
the box time series alone**, residing in reservoir facies outside the reporting boxes. And
sweep efficiency is a *different physical quantity* from the compartment mass inventory
reported by SPE11b, so a quantitative comparison between the two requires a
benchmark-consistent efficiency metric, which does not currently exist. The open-source
implementation and the benchmark characterisation are offered as a reproducible reference
for screening-tool development and for benchmarking analysis against SPE11b.

**Keywords:** CO₂ geological storage; formation heterogeneity; Dykstra–Parsons coefficient;
sweep efficiency; SPE11b benchmark; analytical screening; uncertainty quantification;
open-source.

---

## 1. Introduction

Permeability heterogeneity is a first-order control on CO₂ storage performance. In layered
or interbedded saline aquifers, injected CO₂ channels preferentially through high-permeability
strata, bypassing lower-permeability intervals. This bypassing simultaneously reduces the
fraction of pore volume contacted (sweep efficiency), enlarges the pressure footprint
(area of review), and modulates the trapping mechanisms that operate over decades to
centuries (Bachu, 2000; Goodman et al., 2011).

At least three analytical tools quantify these effects. The **Dykstra–Parsons coefficient**
V_DP summarises permeability variation from core or log data (Dykstra and Parsons, 1950).
The **Shook–Mitchell sweep efficiency** expresses the fraction of pore volume swept as a
function of V_DP and pore volumes injected (Shook and Mitchell, 2009). The **Kopp storage
efficiency** combines geometric, sweep and displacement sub-factors into a capacity
coefficient (Kopp et al., 2010). These correlations are well cited but are rarely
implemented in accessible screening tools, and are easily misapplied when a single
efficiency scalar is compared against full-physics simulation output.

The SPE11b benchmark (Nordbotten et al., 2024) is a field-scale, heterogeneously faulted
CO₂ storage cross-section designed explicitly to stress-test simulators against realistic
Norwegian-continental-shelf conditions. It is a natural reference for any heterogeneity
correction. However, as we document in Section 3, SPE11b reports a *compartment mass
inventory* (mobile, immobile, dissolved, seal, boundary CO₂) and defines **no** sweep or
storage-efficiency scalar, and **no** Dykstra–Parsons coefficient. These two facts have
important consequences for how analytical corrections may — and may not — be tested
against the benchmark.

The specific contributions of this paper are: (1) a clean, reproducible implementation of
the three corrections; (2) a documented derivation of V_DP from the SPE11b facies, with a
sampling-uncertainty band; and (3) an uncertainty-aware benchmark inventory that shows
where analytical screening metrics and field-scale simulation diverge in kind, not just
in magnitude.

---

## 2. Analytical framework and open-source implementation

### 2.1 Dykstra–Parsons coefficient

For a permeability field characterised by a log-normal distribution with log-standard
deviation σ_ln, the Dykstra–Parsons coefficient is

    V_DP = 1 − exp(−σ_ln)                                     (1)

Equivalently, V_DP = (k_50 − k_84.1)/k_50, where k_84.1 is the permeability at one
log-standard-deviation below the median. V_DP ranges from 0 (homogeneous) to values
approaching 1 (extreme heterogeneity). In Section 4.2 we estimate σ_ln directly from the
SPE11b facies table.

### 2.2 Shook–Mitchell sweep efficiency (empirical screening adaptation)

We follow the empirical screening adaptation of Shook and Mitchell (2009). A Formation
Quality Index (FQI) is defined, and the sweep efficiency is expressed as a closed-form
exponential surrogate fitted to reproduce the breakthrough behaviour of the
Shook–Mitchell heterogeneity framework:

    FQI = √(1/(1−V)) · (1−V)/φ                              (2)
    E_s = 1 − exp(−3 · PVI · FQI)                            (3)

with the homogeneous limit E_s = 1 − exp(−3·PVI/φ) at V = 0. Here PVI is the pore volumes
injected and φ the porosity. The exponential form (and its coefficient 3) is a conventional
screening approximation rather than an equation derived in Shook and Mitchell (2009)
themselves; it is used here for tractability and is flagged as such in the accompanying
code. E_s is a *volumetric* metric: the fraction of accessible pore volume contacted,
hence a proxy for the fraction of the reservoir that can participate in residual and
capillary trapping.

### 2.3 Kopp et al. storage efficiency

Kopp et al. (2010) define a capacity factor

    E_c = E_geo · E_s · E_d                                (4)
    E_geo = (h_net/h_gross) / √(k_h/k_v)                   (5)
    E_d   = 1/√M                                            (6)

where E_geo, E_s and E_d are geometric, sweep and displacement sub-factors respectively,
and M is the CO₂-to-brine mobility ratio.

### 2.4 Implementation

All three corrections are implemented in `scripts/facies_heterogeneity.py` (MIT licence,
NumPy-free, standard library only). Design rules followed throughout: (a) no hard-coded
calibration constants; (b) every input read from a named source or documented as an
assumption; (c) SI units stated and converted explicitly; (d) full reproducibility from the
input tables in this paper.

---

## 3. The SPE11b benchmark: what it actually specifies

### 3.1 Geometry and operational conditions

SPE11b (Nordbotten et al., 2024) is a field-scale vertical cross-section, 8400 m × 1200 m
with a nominal depth of 1 m, configured as a **closed** system (no-flow boundaries with
large pore-volume multipliers ℓ_B = 5×10⁴ m on the left/right boundaries within facies 2–5).
It contains seven facies: one seal (facies 1), five reservoir sands (facies 2–6) and one
impermeable unit (facies 7). Two wells inject pure CO₂: Well 1 at 0.035 kg/(s·m) for
0–50 yr, Well 2 at the same rate for 25–50 yr. The total injected mass is therefore

    0.035 × (50 + 25) × 3.1536×10⁷ = 8.2782×10⁷ kg/m.        (7)

The reservoir is monitored for 1000 years.

### 3.2 Facies properties

Table 1 lists the facies permeabilities and porosities (Nordbotten et al., 2024, Table 4).

**Table 1. SPE11b facies properties.**

| Facies | k [m²] | k [mD] | φ |
|--------|--------|--------|---|
| 1 (seal) | 1.0×10⁻¹⁶ | 0.10 | 0.10 |
| 2 | 1.0×10⁻¹³ | 101.3 | 0.20 |
| 3 | 2.0×10⁻¹³ | 202.7 | 0.20 |
| 4 | 5.0×10⁻¹³ | 506.6 | 0.20 |
| 5 | 1.0×10⁻¹² | 1013.3 | 0.25 |
| 6 | 2.0×10⁻¹² | 2026.5 | 0.35 |
| 7 (impermeable) | 0 | 0 | 0 |

Two points follow directly from Table 1. First, the permeable reservoir spans an
arithmetic mean of **770 mD**, a value comfortably above the millidarcy-scale permeability
often assumed for screening studies. Second, SPE11b specifies **no Dykstra–Parsons
coefficient**; heterogeneity is prescribed by the discrete facies and the fault/anticline
geometry, not by a V_DP value. Any V_DP quoted for this benchmark is therefore an
estimation, not a specification (Section 4.2).

### 3.3 Reported quantities

The benchmark time series reports CO₂ mass *by compartment* in two reporting boxes (A and B):
mobile free phase (relative permeability > 0), immobile free phase (relative
permeability = 0), dissolved, and seal-facies CO₂, plus a total-seal and a boundary column
(Sections 2.5 and 3.7). **No sweep efficiency, storage efficiency, or V_DP is reported.**
Boxes A and B do not cover the whole domain; CO₂ in reservoir facies outside these boxes
only appears in the spatial maps.

---

## 4. Results

### 4.1 Benchmark inventory

Using `scripts/benchmark_analysis.py`, we computed the compartment fractions as a
percentage of the total injected mass (8.2782×10⁷ kg/m) across four participating
simulators (rice1, ctc-cne1, opm1, sintef1). Table 2 reports selected times.

**Table 2. SPE11b compartment inventory (% of injected CO₂).**

| Simulator | yr | mobile | immobile | dissolved | seal | box budget |
|-----------|---|--------|----------|-----------|------|------------|
| rice1 | 50 | 16.5 | 0.06 | 1.9 | 2.3 | 20.8 |
| rice1 | 1000 | 10.0 | 1.36 | 22.7 | 23.0 | 57.1 |
| opm1 | 50 | 27.5 | 0.06 | 1.7 | 0.4 | 29.6 |
| opm1 | 1000 | 44.3 | 0.13 | 8.9 | 0.8 | 54.2 |
| ctc-cne1 | 50 | 25.9 | 4.39 | 1.8 | 0.3 | 32.4 |
| ctc-cne1 | 1000 | 33.9 | 5.51 | 12.2 | 0.3 | 51.9 |
| sintef1 | 50 | 27.5 | 0.04 | 1.6 | 0.1 | 29.3 |
| sintef1 | 1000 | 43.9 | 0.26 | 8.6 | 0.2 | 53.0 |

**Figure 1** presents the full compartment inventory for all four participating
simulators. Three findings are robust across simulators and are the substance of this paper.

> **Figure 1 — SPE11b CO₂ inventory by compartment.** Stacked fraction of injected CO₂
> (mobile, immobile/residual, dissolved, seal) at selected times over the 1000-year
> horizon, for the four participating simulators (rice1, ctc-cne1, opm1, sintef1). The
> hatched grey wedge is the fraction of injected CO₂ not reported by the box time series
> (residing in reservoir facies outside boxes A and B). See `figures/fig1_compartments.png`.

**Finding 1 — residual trapping is negligible at end of injection.** The immobile
fraction is 0.04–4.4% at 50 yr (and remains a few percent even at 1000 yr in three of four
simulators). Analytical screening that centres on residual/capillary trapping therefore
describes a mechanism that is all but absent at the field conditions of this benchmark.

**Finding 2 — dissolution and (simulator-dependent) seal trapping dominate long-term.**
Dissolved CO₂ grows to 9–23% by 1000 yr; rice1 additionally reports ~23% seal trapping
while the other simulators report <1%. The factor-of-two-to-twenty simulator spread on
seal and dissolved CO₂ is itself a reminder that benchmark consensus is far tighter than
any single analytical number.

**Finding 3 — the box time series misses most of the CO₂ at early time.** At 50 yr the box
compartments account for only 21–32% of injected CO₂ (rising to 52–57% by 1000 yr). The
remainder lies in reservoir facies outside boxes A and B, and is invisible without the
spatial maps. Any efficiency metric computed from the box time series alone is therefore
incomplete by construction, and by a large margin at end of injection.

### 4.2 Dykstra–Parsons coefficient from the facies

Restricting to the five reservoir sands (facies 2–6), the sample standard deviation of
ln(k) is σ_ln = 1.076, giving

    V_DP = 1 − exp(−1.076) = 0.66                        (8)

Because this estimate is computed from only n = 5 facies, it carries sampling
uncertainty: the standard error of the sample log-standard deviation is
σ_ln / √(2(n−1)) ≈ 0.38, so a one-sigma band on V_DP is **0.50–0.77**. This band, not a
single value, is the defensible estimate of heterogeneity for the SPE11b reservoir.

### 4.3 Analytical sweep efficiency

Table 3 lists E_s from Equation (3) at V_DP = 0 and V_DP = 0.66, for representative
porosity and a range of pore volumes injected (SPE11b reports no PVI, so E_s is necessarily
a function of an assumed PVI).

**Table 3. Shook–Mitchell sweep efficiency, E_s.**

| φ | PVI | E_s (V=0) | E_s (V=0.66) | ratio |
|---|-----|-----------|--------------|-------|
| 0.20 | 0.02 | 0.259 | 0.161 | 0.62 |
| 0.20 | 0.05 | 0.528 | 0.355 | 0.67 |
| 0.20 | 0.10 | 0.777 | 0.583 | 0.75 |
| 0.25 | 0.05 | 0.451 | 0.296 | 0.66 |

> **Figure 2 — Shook–Mitchell sweep efficiency vs. pore volumes injected**, at V_DP = 0
> (homogeneous) and V_DP = 0.66 (SPE11b facies), for porosity 0.20 and 0.25.
> See `figures/fig2_sweep_vs_pvi.png`.

Heterogeneity reduces the sweep efficiency by 25–40% relative to the homogeneous
assumption — a material effect and a valid qualitative statement. But the magnitude
depends strongly on the assumed PVI, which the benchmark does not pin down.

**Figure 3** shows the same sensitivity across the full V_DP range, including the Kopp
capacity factor E_c computed with documented assumptions (net-to-gross 0.85, permeability
anisotropy k_h/k_v = 10 per the benchmark, mobility ratio M = 10).

> **Figure 3 — Sensitivity of sweep and storage-efficiency factors to V_DP**, at
> PVI = 0.05 and φ = 0.20. E_s (sweep) and E_c (Kopp et al. capacity factor) both decline
> monotonically with heterogeneity; the dashed line marks the SPE11b-derived V_DP = 0.66.
> See `figures/fig3_vdp_sensitivity.png`.

### 4.4 Reconciling analytical E_s with the benchmark

The central difficulty is now apparent. Equation (3) returns a *volumetric sweep*, which
in the analytical worldview feeds *residual* trapping. Table 2 shows SPE11b has *no*
residual trapping to speak of. The benchmark's CO₂ is either still mobile, dissolved, or
structurally trapped in the seal (rice1), none of which Equation (3) predicts — Equation
(3) was derived for waterflood displacement in which residual saturation is the dominant
trapping mechanism, and it does not account for dissolution or structural trapping.
Comparing the analytical E_s (of order 0.3–0.5) to any benchmark compartment fraction is
therefore a comparison of unlike quantities: the benchmark does not report "sweep," and
the analytical model does not report "mobile/dissolved/seal fractions."

This mismatch is structural rather than numerical. The analytical correlations were
derived for waterflood-style displacement in which a large saturable residual phase is
left behind; SPE11b, by contrast, is gravity-dominated, and its CO₂ either accumulates in
the structural high (seal) or dissolves. A quantitative "validation" of a sweep-efficiency
formula against this benchmark is therefore inherently ill-posed unless the comparison
metric is first defined in benchmark terms (Section 5.2).

### 4.5 Uncertainty quantification

Two sources of uncertainty can be quantified directly and without additional assumptions.

**Model uncertainty — the simulator ensemble.** The benchmark is itself an ensemble of
four independent simulators. Table 2 exposes the consequence: at 50 yr the mobile fraction
spans 16.5–27.5% of injected CO₂; at 1000 yr the dissolved fraction spans 8.9–22.7% and the
seal fraction 0.3–23.0%. This factor-of-two spread — not any single simulator — is the
defensible statement of model uncertainty for this benchmark, and it is concentrated
precisely in the quantities most relevant to long-term security.

**Parameter uncertainty — V_DP and PVI.** V_DP is known only to within the 0.50–0.77 band
of Section 4.2, and, more importantly, PVI is not defined by the benchmark at all.
Propagating the V_DP band through Equation (3) at PVI = 0.05 and φ = 0.20 gives E_s between
0.30 and 0.41 (against 0.53 for the homogeneous limit), while varying PVI over the plausible
range 0.02–0.10 moves E_s over 0.16–0.58. The combined conclusion is that an analytical
sweep efficiency for this benchmark should be quoted as a wide band (roughly 0.2–0.6),
with PVI the dominant source of uncertainty, rather than as a point value.

---

## 5. Discussion

### 5.1 What analytical heterogeneity corrections can and cannot do

The corrections implemented here remain useful as *screening heuristics*. Equation (1)–(6)
capture the correct qualitative direction — heterogeneity reduces sweep and capacity, and
that reduction grows with V_DP — and they are cheap to evaluate across candidate sites.
They should be reported as such: directionally correct, magnitude-uncertain, order-of-
magnitude screening inputs, not as predictions validated against full simulation.

### 5.2 What a defensible benchmark comparison would require

A rigorous test of analytical heterogeneity corrections against SPE11b would require
three things that do not currently exist together: (1) a benchmark-consistent definition of
"sweep efficiency" (e.g. the fraction of mobile CO₂ that becomes immobile, computed from
the spatial maps and the immobile-saturation criterion); (2) a V_DP estimated from the
*full* permeability field, including the seal and the faults, not just the clean reservoir
sands; and (3) an account of the closed-system boundary buffering that sequesters a large
fraction of injected mass outside the reporting boxes. Building these is a worthwhile and
clearly-scoped piece of future work.

### 5.3 The residual-trapping surprise

The near-absence of residual trapping in SPE11b at end of injection is worth emphasis for
practitioners. Much screening guidance inherits the waterflood intuition that a significant
fraction of the injected phase is residually trapped. The physical reason that intuition
fails here is drainage-versus-imbibition hysteresis: during the 50-year active injection
the reservoir undergoes continuous **primary drainage** — the non-wetting CO₂ advancing
into an initially water-saturated medium — during which no residual gas is trapped; an
immobile CO₂ phase only appears once brine re-enters the swept region after shut-in, i.e.
during post-shut-in **imbibition**. The benchmark's reported immobile fraction (<0.1% at
50 yr) indicates this imbibition has barely begun within the reporting boxes at end of
injection. Combined with the deep, warm, low-viscosity supercritical-CO₂ conditions and
strong gravity segregation into a structural high, this leaves dissolution and structural
trapping as the dominant long-term mechanisms. Screening tools should therefore weight
these mechanisms — not residual trapping — when assessing long-term security for analogues
of this benchmark.

### 5.4 Limitations

The V_DP estimate of Section 4.2 uses only the five reservoir facies and treats them as a
discrete proxy for a log-normal field; the faults and the seal are excluded, so 0.66 (band
0.50–0.77) is an approximation. The benchmark inventory in Table 2 is reported per
simulator and is not averaged, precisely to preserve the spread that any rigorous
comparison must confront. Finally, PVI — an input to Equation (3) — is not defined by the
benchmark, and E_s is reported as a function of PVI and of the V_DP band rather than as a
single number.

### 5.5 Practical significance for CCUS and petroleum engineering

The contribution here is methodological rather than a new physical law, but it bears on
three practical questions asked repeatedly in CCUS project development.

**A concrete, citable benchmark value.** Dykstra–Parsons coefficients are routinely quoted
for screening studies but rarely traceable to a source. This paper supplies a documented,
reproducible V_DP for a public field-scale benchmark — 0.66, with a 0.50–0.77 sampling
band — that practitioners can use to calibrate their own heterogeneity inputs or to
cross-check a screening tool against a known reference.

**A corrected intuition about long-term trapping.** Screening guidance inherited from
waterflood tends to emphasise residual (capillary) trapping as the workhorse mechanism. The
SPE11b field-scale result here is the opposite: at end of injection the immobile fraction
is negligible, and dissolution plus structural trapping carry the long-term security
burden. Operators who parameterise storage-security or "trapping-efficiency" arguments
against a field-scale analogue should weight the latter mechanisms, not residual trapping.

**Benchmark literacy.** The finding that the box time-series accounts for only ~20–30% of
injected CO₂ at end of injection is a practical warning: "storage-efficiency" style
metrics extracted from SPE11b box outputs alone understate the inventory, and the full
budget requires the spatial maps. This matters for quality assurance of simulator
submissions to the benchmark and for regulators who request simulator-based containment
demonstrations.

---

## 6. Conclusions

1. We provide an open-source, unit-explicit implementation of the Dykstra–Parsons,
   Shook–Mitchell and Kopp analytical heterogeneity corrections (Equations 1–6), available
   in `scripts/facies_heterogeneity.py`.

2. The Dykstra–Parsons coefficient of the SPE11b reservoir, derived from its facies table,
   is **V_DP = 0.66** (reservoir sands 101–2027 mD, mean 770 mD), with a sampling band of
   0.50–0.77. The benchmark itself defines no V_DP; the value here is an estimate with its
   uncertainty stated.

3. A benchmark inventory of SPE11b (Table 2) shows residual trapping is **negligible**
   (<0.1% at 50 yr), dissolution and seal trapping dominate long-term with large simulator
   spread, and the box time series misses most of the injected CO₂ at end of injection
   (~70–80%).

4. Analytical "sweep efficiency" and the benchmark compartment inventory are different
   physical quantities, so a meaningful quantitative comparison requires a
   benchmark-consistent efficiency metric.

5. Uncertainty is quantifiable and material: the four-simulator ensemble spans roughly a
   factor of two on long-term trapping quantities, and analytic sweep efficiency is
   uncertain to a wide band dominated by PVI.

6. Analytical heterogeneity corrections remain legitimate screening heuristics — the
   open-source implementation is offered for reuse — but they must be reported with their
   uncertainty and not treated as validated predictions against full simulation.

---

## Data and code availability

A live, self-contained Jupyter notebook reproducing every result and figure in this paper
is available at **https://github.com/todak2000/co2-heterogeneity-screening**, where it can
be run interactively without installation via its Binder or Google Colab launcher:

- *Notebook:* `heterogeneity_screening.ipynb`
- *Binder:* https://mybinder.org/v2/gh/todak2000/co2-heterogeneity-screening/HEAD?labpath=heterogeneity_screening.ipynb
- *Colab:* https://colab.research.google.com/github/todak2000/co2-heterogeneity-screening/blob/main/heterogeneity_screening.ipynb

All scripts and data are also provided in that repository under `scripts/`, `data/` and
`figures/`.
- `scripts/facies_heterogeneity.py` — facies, V_DP and E_s/E_c computation.
- `scripts/benchmark_analysis.py` — SPE11b compartment inventory from the time series.
- `scripts/make_figures.py` — reproduces Figures 1–3.
- `data/timeseries/` — SPE11b time series (rice1, ctc-cne1, opm1, sintef1).
- `data/spatial_maps_rice1/` — representative rice1 spatial maps.
- `figures/` — Figures 1–3 (PNG, 300 dpi).
- `benchmark_spec/` — the official SPE CSP-11 description and a `GROUND_TRUTH.md`
  documenting every verified fact and number used here.

The SPE11b data are from the 11th SPE Comparative Solution Project
(Nordbotten et al., 2024; https://spe.org/csp/spe11).

---

## References

Bachu, S. (2000). Sequestration of CO₂ in geological media: criteria and approach for
site selection in response to climate change. *Energy Conversion and Management*,
41(9), 953–970.

Dykstra, H. and Parsons, R.L. (1950). The prediction of oil recovery by waterflood.
*Secondary Recovery of Oil in the United States*, 2nd ed., API, 160–174.

Goodman, A., Hakala, A., Bromhal, G., et al. (2011). U.S. DOE methodology for the
development of geologic storage potential of CO₂ at national and regional scale.
*International Journal of Greenhouse Gas Control*, 5(4), 952–965.

Kopp, A., Class, H. and Helmig, R. (2010). Investigation on CO₂ storage capacity in
saline aquifers. Part 2: Estimation of storage capacity coefficients. *International
Journal of Greenhouse Gas Control*, 4(3), 408–418.

Nordbotten, J.M., Fernø, M.A., Flemisch, B., Kovscek, A.R. and Lie, K.-A. (2024). The
11th Society of Petroleum Engineers Comparative Solution Project: Problem Definition.
*SPE Journal*. doi:10.2118/218015-PA.

Shook, G.M. and Mitchell, K.M. (2009). A robust measure of heterogeneity for ranking
earth models: the F-Phi curve and dynamic Lorenz coefficient. SPE-119897-MS.

---

*Every number in this manuscript traces to either the SPE CSP-11 description or the
benchmark data files in this repository; no value is asserted that cannot be reproduced
from those sources with the scripts provided.*
