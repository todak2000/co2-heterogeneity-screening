"""
benchmark_analysis.py
=====================
Reproducible extraction of the SPE11b benchmark CO2 inventory from the official
time-series files.

Column layout (source: SPE CSP-11 description, Section 2.6.1 / 3.7):
    [0] t [s], [1] p1 [Pa], [2] p2 [Pa],
    [3] mobA, [4] immA, [5] dissA, [6] sealA   (box A, kg),
    [7] mobB, [8] immB, [9] dissB, [10] sealB  (box B, kg),
    [11] mC [m^2], [12] sealTot [kg], [13] boundary [kg]

Definitions (spec Section 2.5):
    mob  = mobile free-phase CO2 (k_rn > 0)
    imm  = immobile free-phase CO2 (k_rn = 0)   -> residual/capillary trapping
    diss = CO2 dissolved in water
    seal = CO2 in the seal facies (facies 1), any form

We report, at selected times, the compartment fractions as a % of the TOTAL
injected CO2 (8.2782e7 kg/m, computed from the injection schedule). This is the
unambiguous, benchmark-defined inventory.

Run:  python3 benchmark_analysis.py
"""

import csv, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOTAL_INJECTED = 0.035 * (50 * 365 * 86400) + 0.035 * (25 * 365 * 86400)  # kg/m

TIMES = [(50, 1.5768e9), (100, 3.1536e9), (200, 6.3072e9),
         (500, 1.5768e10), (1000, 3.1536e10)]

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

def at_year(rows, t_target):
    best, bd = None, 1e18
    for r in rows:
        d = abs(r[0] - t_target)
        if d < bd:
            bd, best = d, r
    return best

def compartments(row):
    mobA, immA, dissA = row[3], row[4], row[5]
    mobB, immB, dissB = row[7], row[8], row[9]
    sealTot, boundary = row[12], row[13]
    return dict(
        mobile=mobA + mobB, immobile=immA + immB, dissolved=dissA + dissB,
        seal_total=sealTot, boundary=boundary,
    )

def main():
    sims = sorted(glob.glob(os.path.join(ROOT, "data", "timeseries", "*_time_series.csv")))
    results = {}
    for path in sims:
        name = os.path.basename(path).replace("_time_series.csv", "")
        rows = load(path)
        results[name] = {}
        for yr, ts in TIMES:
            r = at_year(rows, ts)
            if r is None:
                continue
            c = compartments(r)
            results[name][yr] = c

    print(f"Total injected CO2 = {TOTAL_INJECTED:.4e} kg/m")
    print(f"                   = {TOTAL_INJECTED/1e3:.1f} t/m")
    print()
    for name in results:
        print(f"--- {name} ---")
        print(f"{'yr':>5} {'mobile%':>9} {'immob%':>9} {'diss%':>9} "
              f"{'seal%':>9} {'bound%':>9} {'boxes budget%':>14}")
        for yr in [50, 100, 200, 500, 1000]:
            c = results[name].get(yr)
            if not c:
                continue
            mobile = c["mobile"] / TOTAL_INJECTED * 100
            immob = c["immobile"] / TOTAL_INJECTED * 100
            diss = c["dissolved"] / TOTAL_INJECTED * 100
            seal = c["seal_total"] / TOTAL_INJECTED * 100
            bound = c["boundary"] / TOTAL_INJECTED * 100
            # fraction recovered by the box time-series alone:
            # boxes A/B (mobile+immobile+dissolved) + total seal + boundary.
            reported = (c["mobile"] + c["immobile"] + c["dissolved"]
                        + c["seal_total"] + c["boundary"])
            budget = reported / TOTAL_INJECTED * 100
            print(f"{yr:>5} {mobile:>9.1f} {immob:>9.2f} {diss:>9.1f} "
                  f"{seal:>9.1f} {bound:>9.2f} {budget:>13.1f}")
        print()

if __name__ == "__main__":
    main()
