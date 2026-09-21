"""
spe11b_regime_analysis.py
=========================
Characterisation of the SPE11b CO2 storage benchmark: (1) the dimensionless flow
regime and its governing timescales, and (2) the seal capillary-gravity balance.

This is the analytically-verified core of the paper "Gravity-dominated storage and
the limits of agreement in the SPE11b benchmark". All physics constants trace to the
official SPE CSP-11 description; thermophysical properties are evaluated with the
NIST-consistent Span-Wagner / Fenghour equations of state (via CoolProp 8.0).

No fitting, no hidden constants. MIT licence.
"""

import math

# ---------------------------------------------------------------------------
# Thermophysical properties of CO2 and water at SPE11b conditions
# (30 MPa; geothermal gradient T = 70 - 0.025*z  => 40..70 C across the domain).
# Evaluated with CoolProp 8.0 HEOS (Span & Wagner 1996 for CO2; IAPWS-95 for water;
# Fenghour et al. 1998 viscosity). The benchmark itself references NIST.
# ---------------------------------------------------------------------------
T_C       = 55.0          # mid-depth geothermal temperature
RHO_CO2   = 850.2         # kg/m3   (Span-Wagner @ 30 MPa, 55 C)
RHO_WATER = 998.3         # kg/m3   (pure water @ 30 MPa, 55 C)
DELTA_RHO = RHO_WATER - RHO_CO2          # 148.1 kg/m3
DELTA_RHO_LO, DELTA_RHO_HI = 95.0, 202.5  # at 40 C and 70 C respectively
MU_CO2    = 8.183e-5      # Pa.s     (Fenghour @ 30 MPa, 55 C)
G         = 9.81

# ---------------------------------------------------------------------------
# SPE11b geometry and rock properties (from the SPE CSP-11 description)
# ---------------------------------------------------------------------------
L, H      = 8400.0, 1200.0        # domain width, height (m)
KV_KH     = 0.1                    # vertical/horizontal anisotropy (spec: 10:1)
K_H       = 500.0 * 9.869e-16      # representative reservoir k_h (500 mD), m^2
K_V       = K_H * KV_KH
K_SEAL    = 1e-16                  # facies 1 seal permeability, m^2
PHI_SEAL  = 0.10                   # facies 1 seal porosity

# injection (spec Section 3.5)
Q_MASS_PER_WELL = 0.035            # kg/(s.m)
T_INJ       = 50.0 * (365*86400)   # s
T_MONITOR   = 1000.0 * (365*86400) # s

# ---------------------------------------------------------------------------
# (1) Dimensionless groups
# ---------------------------------------------------------------------------
AR = L / H                                   # aspect ratio
RL = AR * math.sqrt(KV_KH)                   # effective aspect ratio (Lake 1989)

# gravity (buoyant) rise velocity and timescales
u_g      = DELTA_RHO * G * K_V / MU_CO2      # vertical buoyancy Darcy velocity, m/s
t_grav   = H / u_g                            # time to rise the full height, s

# injection Darcy velocity across the domain cross-section (per unit width)
Q_VOL     = Q_MASS_PER_WELL / RHO_CO2        # m3/(s.m)
u_inj     = Q_VOL / H                         # m/s
Ng        = u_g / u_inj                       # gravity number (buoyancy vs injection)

# ---------------------------------------------------------------------------
# (2) Seal capillary-gravity balance (spec Eq. 3.11)
#     p_entry = sqrt(phi / k_x) * 6.12e-3 N/m   (Abdoulghafour 2020)
# ---------------------------------------------------------------------------
P_ENTRY   = math.sqrt(PHI_SEAL / K_SEAL) * 6.12e-3   # Pa
h_break   = P_ENTRY / (DELTA_RHO * G)                 # CO2 column height to breach seal, m
h_break_lo = P_ENTRY / (DELTA_RHO_HI * G)
h_break_hi = P_ENTRY / (DELTA_RHO_LO * G)

# ---------------------------------------------------------------------------
def report():
    out = []
    out.append("=== SPE11b dimensionless regime ===")
    out.append(f"Aspect ratio L/H              = {AR:.2f}")
    out.append(f"Anisotropy k_v/k_h            = {KV_KH:.2f}")
    out.append(f"Effective aspect ratio R_L    = (L/H)sqrt(k_v/k_h) = {RL:.2f}")
    out.append(f"Buoyancy rise velocity u_g    = {u_g:.2e} m/s  (vertical, k_v={KV_KH*K_H/9.869e-16:.0f} mD)")
    out.append(f"Gravity number Ng             = u_g / u_inj = {Ng:.0f}")
    out.append("")
    out.append("=== Governing timescales ===")
    out.append(f"time to rise full 1200 m      = {t_grav/(365*86400):.1f} yr")
    out.append(f"injection duration            = {T_INJ/(365*86400):.1f} yr")
    out.append(f"post-injection monitoring     = {(T_MONITOR-T_INJ)/(365*86400):.1f} yr")
    out.append(f"  ratio t_grav / t_inj        = {t_grav/T_INJ:.2f}")
    out.append("  => viscous and gravity are CO-ACTIVE during injection;")
    out.append("     post-injection buoyancy dominates the long-term fate.")
    out.append("")
    out.append("=== Seal capillary-gravity balance ===")
    out.append(f"seal (facies 1) entry pressure = {P_ENTRY/1e6:.3f} MPa")
    out.append(f"CO2 column to breach seal      = {h_break:.0f} m  (Drho={DELTA_RHO:.0f} kg/m3)")
    out.append(f"  [Drho {DELTA_RHO_LO:.0f}-{DELTA_RHO_HI:.0f} kg/m3 -> breach height {h_break_lo:.0f}-{h_break_hi:.0f} m]")
    return "\n".join(out)

if __name__ == "__main__":
    print(report())
