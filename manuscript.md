# Gravity-Dominated CO₂ Storage and the Limits of Agreement in the SPE11b Benchmark

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

The SPE11b benchmark (Nordbotten et al., 2024) is the community's field-scale reference for
CO₂ storage simulation, yet its governing flow regime and the limits of what it can be used
to validate are rarely stated explicitly. This paper provides a reproducible, evidence-only
characterisation of three properties of SPE11b that bear directly on how it should be used.
First, we locate its dimensionless regime. With `L/H = 7`, anisotropy `k_v/k_h = 0.1`, an
effective aspect ratio `R_L = (L/H)√(k_v/k_h) ≈ 2.2`, and thermophysical properties evaluated
from the Span–Wagner/Fenghour equations of state (ρ_CO₂ ≈ 850 kg/m³, Δρ ≈ 150 kg/m³,
μ_CO₂ ≈ 8.2×10⁻⁵ Pa·s at 30 MPa), the time for CO₂ to rise the full 1200 m reservoir height
under buoyancy is **~43 years — comparable to the 50-year injection period**. SPE11b is
therefore a *transitional gravity–viscous* system: viscous and buoyant forces are co-active
during injection, and buoyancy dominates the 950-year post-shut-in period that controls
long-term fate. Its seal (facies 1) has a capillary entry pressure of only **~0.19 MPa**,
overcome by the buoyancy head of a CO₂ column taller than **~100–200 m**, so containment
rests on structural closure and low seal permeability rather than capillary strength.
Second, we quantify cross-simulator agreement. The four simulators agree on the mobile
fraction (spread ≈ 40% at 50 yr) but **diverge by one to two orders of magnitude** on the
long-term security quantities — residual (immobile) trapping and structural (seal) trapping
— with one participant (rice1) reporting ~3× more long-term trapping than the others. Third,
from the spatial maps we show the domain-wide plume's mass centroid rises ~200 m and migrates
~700 m up-dip toward the anticline over 1000 yr, while the reporting boxes account for only
~20–30% of injected CO₂ at shut-in. The practical conclusion: SPE11b can validate plume
mobility and extent, but not long-term trapping, because the simulators themselves have not
converged on those mechanisms.

**Keywords:** CO₂ geological storage; SPE11b benchmark; gravitational segregation; capillary
entry; inter-simulator agreement; dimensionless numbers; benchmark validation.

---

## 1. Introduction

CO₂ geological storage performance is assessed by analytical screening tools, reduced
models, and full reservoir simulation, and each is ultimately benchmarked against some
reference. The 11th Society of Petroleum Engineers Comparative Solution Project, Version 11B
(SPE11b), is the current de facto field-scale reference for CO₂ storage simulation
(Nordbotten et al., 2024): an 8.4 km × 1.2 km faulted cross-section with an anticline and a
low-permeability seal, injected over 50 years and monitored for 1000 years. Because it is
public and multi-simulator, SPE11b is the natural target for anyone building or validating a
screening or simulation workflow.

Using a benchmark well requires knowing two things: *what physical regime it occupies*, and
*how sharply its reference answers are defined*. A screening tool validated against SPE11b
must be validated against a quantity the benchmark actually constrains. This paper supplies
both pieces of information, derived purely from the published problem definition and the
released simulator output, with no fitted parameters.

The central finding is that SPE11b is a **transitional gravity–viscous** system, not a
purely viscous displacement and not a purely gravity-segregated plume: the buoyancy
timescale (~43 yr) is comparable to the injection timescale (50 yr). This single observation
explains the benchmark's otherwise puzzling behaviour — negligible residual trapping at
shut-in, slow gravity-driven dissolution and structural trapping thereafter, and a large
spread among simulators precisely on those long-term mechanisms.

Three contributions follow. We (i) compute the governing dimensionless groups and
timescales; (ii) quantify the cross-simulator agreement, classifying each reported quantity
as robust or fragile; and (iii) trace the domain-wide plume evolution from the spatial maps,
including the capillary–gravity balance of the seal.

---

## 2. The SPE11b benchmark

SPE11b (Nordbotten et al., 2024) is a 2D vertical cross-section, 8400 m × 1200 m, with a
nominal depth of 1 m; all masses are per metre of nominal thickness. It is a **closed**
system: no-flow boundaries augmented by large pore-volume multipliers (ℓ_B = 5×10⁴ m) on the
left/right boundaries within facies 2–5. Seven facies comprise one seal (facies 1,
k = 1.0×10⁻¹⁶ m², φ = 0.10), five reservoir sands (facies 2–6, k = 1.0×10⁻¹³ to 2.0×10⁻¹² m²,
φ = 0.20–0.35), and one impermeable unit (facies 7). Permeability is anisotropic, with
k_v = 0.1 k_h. Two wells inject pure CO₂ at 0.035 kg/(s·m): Well 1 for years 0–50 and Well 2
for years 25–50, giving a total injected mass of

    0.035 × (50 + 25) × 3.1536×10⁷ = 8.2782×10⁷ kg/m,             (1)

where one year ≡ 365 days = 31,536,000 s. The reservoir is monitored to 1000 years.

Two properties of the reporting convention are essential to a correct reading and are easily
misread. First, the benchmark's time series reports CO₂ **by compartment** — mobile
(relative permeability > 0), immobile (relative permeability = 0), dissolved, and seal-facies
CO₂ — but only **within two localised tracking boxes** (A and B) placed over the fault zones
and the anticline to follow plume arrival, saturation and seal dissipation; these boxes are
*not* domain-wide mass-balance containers, and CO₂ in reservoir facies outside them appears
only in the spatial maps. Second, the benchmark defines **no** sweep or storage-efficiency
scalar: it reports a compartment inventory, not an efficiency.

---

## 3. Method

### 3.1 Thermophysical properties

CO₂ density and viscosity at SPE11b conditions (initial pressure 30 MPa; geothermal
temperature `T = 70 − 0.025z` °C, i.e. 40–70 °C across the domain) are evaluated with the
Span and Wagner (1996) equation of state and the Fenghour, Wakeham and Vesovic (1998)
viscosity correlation, implemented via CoolProp (Bell et al., 2014); the benchmark itself
references NIST, to which these agree within stated tolerances. Water density uses IAPWS-95.
Representative mid-depth values (30 MPa, 55 °C) are ρ_CO₂ = 850 kg/m³, ρ_w = 998 kg/m³,
Δρ = 148 kg/m³, and μ_CO₂ = 8.18×10⁻⁵ Pa·s; across the 40–70 °C domain Δρ ranges 95–202 kg/m³.

### 3.2 Dimensionless groups and governing timescales

Three dimensionless quantities locate the regime. The **aspect ratio** is L/H = 7. Combined
with the anisotropy it gives the **effective aspect ratio** of Lake (1989),

    R_L = (L/H) √(k_v/k_h) ≈ 2.2,                                 (2)

which exceeds unity and therefore indicates gravity segregation across the reservoir height
dominant over viscous sweep. The buoyant (gravity) Darcy velocity and the time to rise the
full height are

    u_g = Δρ g k_v / μ_CO₂ ≈ 8.8×10⁻⁷ m/s,                        (3)
    t_grav = H / u_g ≈ 43 yr,                                       (4)

using the vertical permeability k_v = 0.1 k_h ≈ 50 mD. The ratio to the injection timescale
t_inj = 50 yr is t_grav/t_inj ≈ 0.9; the post-injection monitoring window is 950 yr, more than
twenty times t_grav.

### 3.3 Seal capillary–gravity balance

The seal's capillary entry pressure follows the benchmark's Leverett-J scaling
(Nordbotten et al., 2024, Eq. 3.11; after Abdoulghafour et al., 2020),

    p_entry = √(φ/k_x) · 6.12×10⁻³ N/m ≈ 0.19 MPa.                 (5)

The buoyancy head of a CO₂ column of height h is Δρ g h; equating to p_entry gives the
column height that would break the seal,

    h_break = p_entry / (Δρ g) ≈ 133 m  (97–208 m over the domain). (6)

### 3.4 Data and inter-simulator agreement

Four participating simulators — rice1, ctc-cne1, opm1 and sintef1 — provide public time
series and spatial maps (Nordbotten et al., 2024). We compute each compartment as a fraction
of the total injected mass (Eq. 1) and report the cross-simulator median and min–max spread.
For a compartment with median m over four simulators, we label it *robust* if the spread
(max − min) is a small fraction of m, *moderate* otherwise, and *fragile* when the four
simulators differ by an order of magnitude or more; for near-zero quantities (immobile
trapping) we report the absolute range, since relative spread is ill-conditioned at small m.

---

## 4. Results

### 4.1 Dimensionless regime

Table 1 and Figure 3 summarise the regime. The buoyancy timescale (43 yr) is comparable to
the injection period (50 yr) and far shorter than the monitoring window (950 yr). The
gravity number (ratio of buoyant to injection Darcy velocity) is ~26, confirming that
buoyancy, not viscous sweep, organises the plume. The seal entry pressure (0.19 MPa) is
overcome by a CO₂ column of only ~100–200 m.

**Table 1. SPE11b dimensionless regime.**

| Quantity | Value |
|---|---|
| Aspect ratio L/H | 7.0 |
| Anisotropy k_v/k_h | 0.1 |
| Effective aspect ratio R_L | 2.2 |
| Buoyant rise velocity u_g | 8.8×10⁻⁷ m/s |
| Time to rise 1200 m, t_grav | ~43 yr |
| Injection duration t_inj | 50 yr |
| Post-injection monitoring | 950 yr |
| Gravity number (u_g / u_inj) | ~26 |
| Seal entry pressure | 0.19 MPa |
| CO₂ column to breach seal | ~100–200 m |

### 4.2 Inter-simulator agreement

Table 2 and Figure 1 report the cross-simulator spread. The mobile fraction is the most
robust quantity (spread ≈ 40% at 50 yr, growing to ~80% by 1000 yr). Residual (immobile)
trapping is uniformly < 5% in all four simulators at every time, but the simulators disagree
on its value by up to two orders of magnitude in relative terms. Structural (seal) trapping
is the least-converged quantity: 0.14–2.31% at 50 yr (~17×) and 0.20–22.99% at 1000 yr
(~115×). One simulator, rice1, reports systematically more long-term trapping than the other
three (≈90% trapped at 1000 yr versus ≈56–66%).

**Table 2. Cross-simulator CO₂ compartment agreement (% of injected CO₂).**

| Year | Compartment | min | max | median | spread | class |
|---|---|---|---|---|---|---|
| 50 | mobile | 16.5 | 27.5 | 27.5 | 0.40 | robust |
| 50 | immobile | 0.04 | 4.4 | 0.06 | ≈100× | fragile |
| 50 | dissolved | 1.6 | 1.9 | 1.9 | 0.17 | robust |
| 50 | seal | 0.14 | 2.31 | 0.36 | ≈17× | fragile |
| 1000 | mobile | 10.0 | 44.4 | 43.9 | 0.78 | moderate |
| 1000 | immobile | 0.13 | 5.5 | 1.36 | ≈40× | fragile |
| 1000 | dissolved | 8.7 | 22.7 | 12.2 | 1.15 | moderate |
| 1000 | seal | 0.20 | 22.99 | 0.75 | ≈115× | fragile |

### 4.3 Domain-wide plume evolution

Figure 2 traces the plume from the spatial maps (rice1 as the representative case). The
mass centroid of the free CO₂ rises from z = 629 m at 50 yr to z = 832 m at 1000 yr
(+204 m) and migrates from x = 3612 m to x = 4318 m (+706 m up-dip toward the anticline),
while the plume area grows from 0.69 to 1.45 km². The domain-wide CO₂ mass is conserved at
≈82,700 t (matching the injected 82,782 t to 0.1%), confirming the maps close the mass
balance that the box time series (≈20–30% of injected mass) does not.

---

## 5. Discussion

### 5.1 A transitional regime, not a pure one

The single most important characterisation is that `t_grav ≈ t_inj`. This is why SPE11b
cannot be reduced to either of the two textbook limits. During the 50-year injection,
pressure-driven (viscous) and buoyant forces are *co-active*: the CO₂ is being pushed
laterally at the same rate gravity tends to segregate it vertically. After shut-in, viscous
forcing collapses and buoyancy is left with a 950-year window — more than twenty buoyancy
timescales — during which the plume rises toward the anticline and the seal, dissolves, and
gradually accumulates structurally. Any screening heuristic that assumes a single dominant
mechanism will misstate the benchmark.

### 5.2 Why residual trapping is negligible at shut-in

The compartment inventory shows immobile (residual) trapping below ~5% at all times and
essentially zero at 50 yr. This follows directly from the regime: during active injection the
reservoir is in continuous **primary drainage** — the non-wetting CO₂ advancing into a
water-saturated medium — during which no residual gas is left behind; immobilisation requires
**imbibition** (brine re-entering the swept pore space), which begins only after shut-in and
proceeds slowly because the plume is simultaneously migrating away and dissolving. This is a
property of a thick, gravity-dominated structural trap, *not* a general statement about CO₂
storage: in thin, aquifer-supported formations post-shut-in imbibition traps a large fraction
of the CO₂. Screening tools must be geology-aware; SPE11b should not be read as evidence that
residual trapping is unimportant in general.

### 5.3 What SPE11b can and cannot validate

Table 2 answers the practical question. SPE11b *can* validate plume mobility and extent: all
four simulators agree, to within roughly a factor of two, on the mobile fraction and the
early dissolved fraction. SPE11b *cannot* currently validate long-term trapping: residual and
structural trapping — the quantities that determine storage security — differ by one to two
orders of magnitude across simulators, and the trajectory of that spread grows with time.
A tool that claims "agreement with SPE11b" on total trapped CO₂ is agreeing with neither a
consensus nor a single reference, because the benchmark's own ensemble has not converged on
that quantity. This is the central caution of this paper.

### 5.4 The seal is capillary-modest

The capillary–gravity balance (Eq. 6) shows the facies-1 seal can hold only ~100–200 m of CO₂
column before its entry pressure is exceeded. Containment in SPE11b therefore rests on the
structural closure of the anticline and the low seal permeability, not on capillary sealing
strength. This is consistent with the benchmark's stated purpose of testing capture of
migration into and through the seal — and it warns against using SPE11b's seal behaviour as a
generic proxy for strong capillary seals.

### 5.5 Toward benchmark-consistent metrics

If analytical or reduced models are to be validated against SPE11b, the comparison must be
made in benchmark terms. A benchmark-consistent screening metric would (i) treat the boxes
as local monitoring regions and compute efficiency from the spatial maps; (ii) separate
mobile, immobile, dissolved and structurally-trapped CO₂ rather than collapsing them into a
single sweep number; and (iii) quote an uncertainty inherited from the simulator ensemble,
not a point value. None of these is a large conceptual change, but their absence is what
makes many screening-level comparisons to SPE11b ill-posed.

---

## 6. Conclusions

1. SPE11b is a **transitional gravity–viscous** system: the buoyancy timescale (~43 yr) is
   comparable to the injection period (50 yr), so viscous and buoyant forces are co-active
   during injection and buoyancy dominates the 950-year post-shut-in period. Effective aspect
   ratio R_L ≈ 2.2 and gravity number ~26 are consistent with this regime.

2. Its seal is **capillary-modest**: entry pressure ≈ 0.19 MPa is overcome by a CO₂ column of
   only ~100–200 m, so containment depends on structural closure and low seal permeability.

3. The four simulators **agree on plume mobility (≈40% spread) but diverge by one to two
   orders of magnitude on long-term trapping** (residual and structural), the spread growing
   with time and dominated by a single outlier (rice1).

4. The domain-wide plume **rises ~200 m and migrates ~700 m up-dip** over 1000 yr, while the
   reporting boxes capture only ~20–30% of injected CO₂ at shut-in.

5. Consequently, SPE11b **can validate plume migration but not long-term trapping**, and any
   validation claim should be made in benchmark-consistent terms — compartment-wise, from
   spatial maps, with the simulator-ensemble spread reported as uncertainty.

---

## Data and code availability

A live, self-contained Jupyter notebook reproducing every result and figure in this paper is
available at **https://github.com/todak2000/co2-heterogeneity-screening**, runnable without
installation via Binder or Google Colab:

- *Notebook:* `heterogeneity_screening.ipynb`
- *Binder:* https://mybinder.org/v2/gh/todak2000/co2-heterogeneity-screening/HEAD?labpath=heterogeneity_screening.ipynb
- *Colab:* https://colab.research.google.com/github/todak2000/co2-heterogeneity-screening/blob/main/heterogeneity_screening.ipynb

Standalone modules `scripts/spe11b_regime_analysis.py`, `scripts/benchmark_analysis.py` and
`scripts/plume_analysis.py` reproduce the tables; `scripts/make_figures.py` reproduces the
figures. SPE11b data are from Nordbotten et al. (2024), https://spe.org/csp/spe11.

---

## References

Abdoulghafour, H., et al. (2020). [capillary entry scaling used in the SPE11b problem
definition, Nordbotten et al. 2024, Eq. 3.11].

Bachu, S. (2000). Sequestration of CO₂ in geological media: criteria and approach for site
selection in response to climate change. *Energy Conversion and Management*, 41(9), 953–970.

Bell, I.H., Wronski, J., Quoilin, S. and Lemort, V. (2014). Pure and pseudo-pure fluid
thermophysical property evaluation and the open-source thermophysical property library
CoolProp. *Industrial & Engineering Chemistry Research*, 53(6), 2498–2508.

Fenghour, A., Wakeham, W.A. and Vesovic, V. (1998). The viscosity of carbon dioxide.
*Journal of Physical and Chemical Reference Data*, 27(1), 31–44.

Lake, L.W. (1989). *Enhanced Oil Recovery*. Prentice Hall, Englewood Cliffs, New Jersey.

Nordbotten, J.M., Fernø, M.A., Flemisch, B., Kovscek, A.R. and Lie, K.-A. (2024). The 11th
Society of Petroleum Engineers Comparative Solution Project: Problem Definition. *SPE
Journal*. doi:10.2118/218015-PA.

Span, R. and Wagner, W. (1996). A new equation of state for carbon dioxide covering the
fluid region from the triple-point temperature to 1100 K at pressures up to 800 MPa.
*Journal of Physical and Chemical Reference Data*, 25(6), 1509–1596.

---

*Every number in this manuscript traces to the SPE CSP-11 description or the released
simulator data, and is reproduced by the scripts in the accompanying repository.*
