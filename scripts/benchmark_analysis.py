"""
benchmark_analysis.py
=====================
SPE11b benchmark CO2 inventory and INTER-SIMULATOR AGREEMENT.

Reads the four official simulator time series and computes:
  (1) the compartment inventory (mobile / immobile / dissolved / seal) as a fraction
      of injected CO2, and
  (2) the cross-simulator agreement (median, min-max spread, and a robust/fragile
      classification) for each compartment over the 1000-year horizon.

Column layout (SPE CSP-11 description, Section 2.6.1 / 3.7):
    t, p1, p2, mobA, immA, dissA, sealA, mobB, immB, dissB, sealB, mC, sealTot, boundary

Note: `sealTot` is the benchmark-defined total CO2 in the seal facies (Proxy P5); it is
used here (not the per-box sealA/sealB, which are anomalously large in rice1).

Run:  python3 benchmark_analysis.py
"""

import csv, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOTAL_INJECTED = 0.035 * (50*365*86400) + 0.035 * (25*365*86400)   # kg/m (spec Section 3.5)
TIMES = [50, 100, 200, 500, 1000]
T_TARGET = {50:1.5768e9, 100:3.1536e9, 200:6.3072e9, 500:1.5768e10, 1000:3.1536e10}

def load(path):
    rows = []
    with open(path) as fh:
        for r in csv.reader(fh):
            if not r or r[0].startswith("#"):
                continue
            try:
                rows.append([float(x) for x in r])
            except (ValueError, IndexError):
                continue
    return rows

def at_year(rows, t):
    return min(rows, key=lambda r: abs(r[0] - t))

def compartments(row):
    return dict(mobile=row[3] + row[7],
                immobile=row[4] + row[8],
                dissolved=row[5] + row[9],
                seal=row[12])

def load_sims():
    sims = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "data", "timeseries", "*_time_series.csv"))):
        name = os.path.basename(p).replace("_time_series.csv", "")
        sims[name] = load(p)
    return sims

def inventory(sims):
    """Return {year: {compartment: {name: pct}}} as fractions of injected CO2."""
    out = {}
    for yr in TIMES:
        out[yr] = {k: {} for k in ("mobile", "immobile", "dissolved", "seal")}
        for name, rows in sims.items():
            c = compartments(at_year(rows, T_TARGET[yr]))
            for k in out[yr]:
                out[yr][k][name] = c[k] / TOTAL_INJECTED * 100
    return out

def agreement(sims):
    """Cross-simulator agreement: median and min-max spread per compartment per time."""
    inv = inventory(sims)
    print(f"{'time':>5} {'compartment':<11} {'min':>7} {'max':>7} {'median':>7} {'spread':>7}  class")
    print("-" * 70)
    for yr in TIMES:
        for key, label in (("mobile","mobile"), ("immobile","immobile"),
                           ("dissolved","dissolved"), ("seal","seal (structural)")):
            vals = list(inv[yr][key].values())
            lo, hi = min(vals), max(vals)
            med = sorted(vals)[len(vals)//2]
            spread = (hi - lo) / med if med > 1e-9 else float("nan")
            if key == "immobile":
                # absolute spread is what matters for near-zero quantities
                cls = "fragile"
            else:
                cls = "robust" if spread < 0.5 else ("moderate" if spread < 1.5 else "fragile")
            print(f"{yr:>5} {label:<11} {lo:7.2f} {hi:7.2f} {med:7.2f} {spread:7.2f}  {cls}")
        print("-" * 70)
    return inventory(sims)

if __name__ == "__main__":
    sims = load_sims()
    print(f"Total injected CO2 = {TOTAL_INJECTED:.4e} kg/m = {TOTAL_INJECTED/1e3:.0f} t/m\n")
    inv = agreement(sims)
