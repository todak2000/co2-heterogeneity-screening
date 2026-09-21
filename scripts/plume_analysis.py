"""
plume_analysis.py
=================
Domain-wide CO2 plume evolution for SPE11b, computed from the spatial maps.

The benchmark's box time series reports CO2 within two LOCAL tracking boxes (A and B);
the domain-wide fate of the plume requires the full spatial maps (Section 2.6.2 / 3.7).
This module computes, from the saturation field, the plume's vertical mass-centroid and
its areal extent over time — the direct spatial signature of buoyancy-driven migration.

Weighting: the plume centroid is weighted by the free-phase CO2 mass in each cell
(saturation x pore volume x CO2 density). Absolute masses are taken from the tmCO2 field.

Run:  python3 plume_analysis.py
"""

import csv, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP_DIR = os.path.join(ROOT, "data", "spatial_maps_rice1")
PHI = 0.20
DX, DZ = 10.0, 10.0

def load_map(path):
    cells = []
    with open(path) as fh:
        for r in csv.reader(fh):
            if not r or r[0].startswith("#"):
                continue
            try:
                # x, z, pressure, saturation, mCO2, mH2O, rhoG, rhoL, tmCO2, temp
                x, z, sat = float(r[0]), float(r[1]), float(r[3])
                rhoG, tmCO2 = float(r[6]), float(r[8])
            except (ValueError, IndexError):
                continue
            cells.append((x, z, sat, rhoG, tmCO2))
    return cells

def plume_metrics(cells, sat_thr=0.01):
    """Return (x_centroid, z_centroid, plume_area_km2, total_mass_kg)."""
    xc = zc = w = 0.0
    area_m2 = 0.0
    total_kg = 0.0
    for x, z, sat, rhoG, tmCO2 in cells:
        total_kg += tmCO2
        if sat > sat_thr:
            m = sat * PHI * DX * DZ * max(rhoG, 640.0)   # free-phase proxy
            xc += x * m
            zc += z * m
            w += m
            area_m2 += DX * DZ
    if w == 0:
        return None
    return xc / w, zc / w, area_m2 / 1e6, total_kg

def plume_series(years=(50, 500, 1000)):
    out = []
    for yr in years:
        p = os.path.join(MAP_DIR, f"spe11b_spatial_map_{yr}y.csv")
        if not os.path.exists(p):
            continue
        m = plume_metrics(load_map(p))
        if m:
            xt, zc, area, mass = m
            out.append((yr, xt, zc, area, mass))
    return out

if __name__ == "__main__":
    rows = plume_series()
    print("rice1 domain-wide plume evolution (from spatial maps):")
    print(f"{'year':>5} {'x-centroid (m)':>15} {'z-centroid (m)':>15} {'area (km2)':>12} {'CO2 mass (Mt)':>14}")
    for yr, xt, zc, area, mass in rows:
        print(f"{yr:>5} {xt:>15.0f} {zc:>15.0f} {area:>12.2f} {mass/1e9:>14.4f}")
    if rows:
        dz = rows[-1][2] - rows[0][2]
        dx = rows[-1][1] - rows[0][1]
        print(f"\nnet rise of plume centroid over {rows[-1][0]-rows[0][0]} yr: dz = +{dz:.0f} m, dx = +{dx:.0f} m")
