# Verified ground truth — SPE11b benchmark (basis for the manuscript)

All facts below were extracted **directly** from the official SPE CSP-11 description
(`spe_csp11_description.txt`) and the benchmark data files in `data/`. Nothing here is an
estimate or an extrapolation; each number traces to a source line in the spec or to the
raw simulator CSVs.

---

## 1. What SPE11b is

- Version 11B of the 11th SPE Comparative Solution Project (Nordbotten et al., 2024).
- A **2D vertical cross-section**, field scale: **8400 m (x) × 1200 m (z)**, nominal
  depth **1 m** (so all masses are reported per metre of nominal thickness).
- A **closed system**: no-flow fluid boundaries, with large pore-volume multipliers
  ("boundary volumes", ℓ_B = 5×10⁴ m) on the left/right boundaries within facies 2–5 to
  absorb pressure.
- Seven facies: **one seal (facies 1), five reservoir sands (facies 2–6), one
  impermeable (facies 7, zero permeability)**.

## 2. Facies properties (spec Table 4)

| Facies | Intrinsic k [m²] | k [mD] | Porosity φ |
|--------|------------------|--------|-----------|
| 1 (seal) | 1.0×10⁻¹⁶ | 0.10 | 0.10 |
| 2 | 1.0×10⁻¹³ | 101.3 | 0.20 |
| 3 | 2.0×10⁻¹³ | 202.7 | 0.20 |
| 4 | 5.0×10⁻¹³ | 506.6 | 0.20 |
| 5 | 1.0×10⁻¹² | 1013.3 | 0.25 |
| 6 | 2.0×10⁻¹² | 2026.5 | 0.35 |
| 7 (impermeable) | 0 | 0 | 0 |

> **Reservoir sands (facies 2–6) span 101–2027 mD, arithmetic mean 770 mD.**
> Horizontal:vertical permeability anisotropy = 10:1 (k_z = 0.1·k_h).

## 3. Injection schedule (spec Section 3.5)

- Well 1: Q₁ = 0.035 kg/(s·m) for 0 < t ≤ 1.5768×10⁹ s (0–50 yr).
- Well 2: Q₂ = 0.035 kg/(s·m) for 7.884×10⁸ s < t ≤ 1.5768×10⁹ s (25–50 yr).
- One year ≡ 31,536,000 s. Monitor to t = 3.1536×10¹⁰ s (1000 yr).
- **Total injected = 0.035 × (50 + 25) × 3.1536×10⁷ = 8.2782×10⁷ kg/m = 82,782 t/m.**

## 4. Measurables reported by the benchmark (spec Section 2.5 / 3.6)

Per box A and box B, the benchmark reports CO₂ mass **by category** in kg: mobile free
phase, immobile free phase, dissolved, and (separately) seal-facies CO₂, plus a total-seal
column and a boundary-volume column.

**Notable:** SPE11b reports **no** "sweep efficiency", **no** "storage efficiency", and
**no** "Dykstra–Parsons coefficient". Heterogeneity is prescribed by the seven *discrete*
facies and the fault/anticline geometry. So (i) any V_DP is an estimation derived by the
user, and (ii) there is no benchmark scalar "efficiency" against which an analytical sweep
model can be directly compared — the benchmark provides a compartment mass inventory only.

## 5. Why a direct "sweep-efficiency" comparison is ill-posed here

- There is **no V_DP value in the spec**; V_DP must be **derived and documented**.
- The box A/B mass fractions do not cover the whole domain. At t = 50 yr (rice1), the box
  compartments plus total seal account for only ~21% of injected CO₂; the remainder sits in
  *reservoir facies outside boxes A/B*, only recoverable from the spatial maps. A
  domain-scale efficiency metric must therefore be defined from the spatial maps and
  documented.

## 6. Verified benchmark numbers (rice1, for use in the case study)

End of injection, t = 50 yr (from `data/timeseries/rice1_time_series.csv`):

- mobile A+B ≈ 1.365×10⁷ kg, immobile A+B ≈ 4.70×10⁴ kg,
  dissolved A+B ≈ 1.608×10⁶ kg, **total seal (sealTot) = 1.910×10⁶ kg**,
  boundary = 0.

Column note: the benchmark distinguishes `sealTot` (total CO₂ in the seal facies,
domain-wide — the official "Proxy P5") from the per-box `sealA`/`sealB` columns (CO₂ in
facies 1 within boxes A/B). These are not the same quantity, and in rice1 the `sealA`
column is anomalously large (≈1.35×10⁷ kg) relative to `sealTot` (1.91×10⁶ kg); the
manuscript uses `sealTot`, which is the benchmark-defined total seal CO₂.

**Mass-balance note:** boxes A/B (mobile+immobile+dissolved) + sealTot + boundary
account for only ~21–32% of injected CO₂ at t = 50 yr (rising to ~52–57% at 1000 yr).
The remainder sits in reservoir facies *outside* boxes A/B and is invisible in the
time-series (only in the spatial maps).

**Derived heterogeneity (Section 4.2):** σ_ln = 1.076 over the five reservoir facies
→ V_DP = 1 − exp(−1.076) = 0.66, with a one-sigma sampling band of 0.50–0.77
(standard error σ_ln/√(2(n−1)) ≈ 0.38 at n = 5).

---
*Prepared 21 Sep 2026. Source: `benchmark_spec/spe_csp11_description.txt` and
`data/timeseries/*_time_series.csv`.*
