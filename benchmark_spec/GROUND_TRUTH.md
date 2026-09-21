# Verified ground truth — SPE11b benchmark

All facts below were extracted **directly** from the official SPE CSP-11 description
(`spe_csp11_description.txt`) and the benchmark data files in `data/`. Nothing is an
estimate. Thermophysical values are from the NIST-consistent Span–Wagner/Fenghour equations
of state (via CoolProp 8.0), the same thermodynamic basis the benchmark references.

---

## 1. What SPE11b is

- Version 11B of the 11th SPE Comparative Solution Project (Nordbotten et al. 2024,
  doi:10.2118/218015-PA).
- A **2D vertical cross-section**, 8400 m (x) × 1200 m (z), nominal depth **1 m** (all
  masses per metre of nominal thickness).
- A **closed system**: no-flow boundaries with pore-volume multipliers ℓ_B = 5×10⁴ m on the
  left/right boundaries within facies 2–5.
- Seven facies: one seal (facies 1), five reservoir sands (facies 2–6), one impermeable
  (facies 7). Anisotropy k_v/k_h = 0.1.
- Reporting boxes A and B are **localised tracking regions** (fault zones / anticline), not
  domain-wide mass-balance containers.

## 2. Facies (spec Table 4)

| Facies | k [m²] | k [mD] | φ |
|--------|--------|--------|---|
| 1 (seal) | 1.0×10⁻¹⁶ | 0.10 | 0.10 |
| 2 | 1.0×10⁻¹³ | 101.3 | 0.20 |
| 3 | 2.0×10⁻¹³ | 202.7 | 0.20 |
| 4 | 5.0×10⁻¹³ | 506.6 | 0.20 |
| 5 | 1.0×10⁻¹² | 1013.3 | 0.25 |
| 6 | 2.0×10⁻¹² | 2026.5 | 0.35 |
| 7 | 0 | 0 | 0 |

## 3. Injection (spec Section 3.5)

- Well 1 @ 0.035 kg/(s·m), 0–50 yr; Well 2 @ 0.035 kg/(s·m), 25–50 yr.
- One year ≡ 365 days = 31,536,000 s (spec). Monitor to 1000 yr.
- **Total injected = 8.2782×10⁷ kg/m = 82,782 t/m.**

## 4. Thermophysical properties (30 MPa; geothermal T = 70 − 0.025z °C)

| Quantity | value | note |
|---|---|---|
| ρ_CO₂ (55 °C) | 850 kg/m³ | Span–Wagner; 788–910 over 40–70 °C |
| ρ_water | 998 kg/m³ | IAPWS-95 (pure water, no salt) |
| Δρ | 148 kg/m³ | 95–202 across domain |
| μ_CO₂ (55 °C) | 8.18×10⁻⁵ Pa·s | Fenghour |

## 5. Dimensionless regime (computed)

- Aspect ratio L/H = 7.0
- Effective aspect ratio R_L = (L/H)√(k_v/k_h) = 2.21
- Buoyant rise velocity u_g = Δρ g k_v / μ_CO₂ ≈ 8.8×10⁻⁷ m/s (k_v = 0.1·k_h ≈ 50 mD)
- **Time to rise 1200 m, t_grav ≈ 43 yr** ≈ injection period (50 yr) ⇒ *transitional*
  gravity–viscous regime
- Gravity number (u_g / u_inj) ≈ 26
- Seal entry pressure p_entry = √(φ/k_x)·6.12×10⁻³ = **0.194 MPa**
- **CO₂ column to breach seal ≈ 133 m** (97–208 m over the Δρ range)

## 6. Verified benchmark numbers (4 simulators, % of injected CO₂)

| Year | Compartment | min | max | median |
|---|---|---|---|---|
| 50 | mobile | 16.5 | 27.5 | 27.5 |
| 50 | immobile | 0.04 | 4.4 | 0.06 |
| 50 | seal | 0.14 | 2.31 | 0.36 |
| 1000 | mobile | 10.0 | 44.4 | 43.9 |
| 1000 | dissolved | 8.7 | 22.7 | 12.2 |
| 1000 | seal | 0.20 | 22.99 | 0.75 |

`seal` = `sealTot` (benchmark total CO₂ in the seal facies, Proxy P5), not the per-box
sealA/sealB columns.

## 7. Plume evolution (rice1 spatial maps)

- Mass centroid z: 629 m (50 yr) → 832 m (1000 yr), **+204 m rise**.
- Mass centroid x: 3612 m → 4318 m, **+706 m up-dip**.
- Plume area: 0.69 → 1.45 km². Domain-wide CO₂ mass ≈ 82,700 t (conserved; matches injection
  to 0.1%), versus ≈20–30% captured by the boxes at shut-in.

---
*Prepared 21 Sep 2026. Source: `benchmark_spec/spe_csp11_description.txt`,
`data/timeseries/*_time_series.csv`, `data/spatial_maps_rice1/*`.*
