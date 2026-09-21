"""
make_figures.py
==============
Generate the publication figures for the honest heterogeneity-screening paper.
Reads data directly from ../data and ../scripts; no hard-coded results.

Outputs (into ../figures):
  fig1_compartments.png   - SPE11b compartment inventory over 1000 yr (4 simulators)
  fig2_sweep_vs_pvi.png   - Shook-Mitchell E_s vs PVI, V=0 vs V=0.66
  fig3_vdp_sensitivity.png - E_s and E_c vs V_DP

Run:  python3 make_figures.py
"""

import os, csv, glob, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys_path = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(sys_path)
FIGS = os.path.join(ROOT, "figures")
os.makedirs(FIGS, exist_ok=True)

from facies_heterogeneity import (shook_mitchell_E_s, kopp_E_c,
                                  dykstra_parsons_from_lognormal, MD,
                                  FACIES, k_md)

plt.rcParams.update({
    "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9.5,
    "legend.fontsize": 7.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.dpi": 300, "savefig.dpi": 300, "savefig.bbox": "tight",
})

TOTAL_INJECTED = 0.035 * (50 * 365 * 86400) + 0.035 * (25 * 365 * 86400)
TIMES = [50, 100, 200, 500, 1000]
T_TARGET = {50: 1.5768e9, 100: 3.1536e9, 200: 6.3072e9,
            500: 1.5768e10, 1000: 3.1536e10}

# ---------------------------------------------------------------------------
# load benchmark compartments
# ---------------------------------------------------------------------------
def load_rows(path):
    out = []
    with open(path) as fh:
        for r in csv.reader(fh):
            if not r or r[0].startswith("#"):
                continue
            try:
                out.append([float(x) for x in r])
            except (ValueError, IndexError):
                continue
    return out

def at_year(rows, t):
    return min(rows, key=lambda r: abs(r[0] - t))

def compartments(row):
    return dict(
        mobile=row[3] + row[7],
        immobile=row[4] + row[8],
        dissolved=row[5] + row[9],
        seal=row[12],          # sealTot (all seal facies), benchmark-defined
        boundary=row[13],
    )

def sim_data():
    sims = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "data", "timeseries", "*.csv"))):
        name = os.path.basename(path).replace("_time_series.csv", "")
        rows = load_rows(path)
        sims[name] = {yr: compartments(at_year(rows, T_TARGET[yr]))
                      for yr in TIMES}
    return sims

# ---------------------------------------------------------------------------
# Figure 1: compartment inventory
# ---------------------------------------------------------------------------
def fig1():
    sims = sim_data()
    order = sorted(sims.keys())
    fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.2), sharey=True)
    cats = ["mobile", "immobile", "dissolved", "seal"]
    labels = ["Mobile", "Immobile (residual)", "Dissolved", "Seal"]
    colors = ["#2b6cb0", "#9b2c2c", "#2f855a", "#805ad5"]
    bottom = np.zeros(len(TIMES))
    total = np.full(len(TIMES), 100.0)
    for ax, name in zip(axes.ravel(), order):
        c = sims[name]
        vals = {k: np.array([c[yr][k] / TOTAL_INJECTED * 100 for yr in TIMES])
                for k in cats}
        bottom = np.zeros(len(TIMES))
        for k, lab, col in zip(cats, labels, colors):
            ax.fill_between(TIMES, bottom, bottom + vals[k],
                            label=lab, color=col, alpha=0.85)
            bottom = bottom + vals[k]
        # unreported wedge
        ax.fill_between(TIMES, bottom, total, label="Outside boxes A/B",
                        color="0.82", alpha=0.9, hatch="///")
        ax.set_title(name)
        ax.set_xlim(50, 1000); ax.set_xscale("log")
        ax.set_xticks(TIMES); ax.set_xticklabels([str(t) for t in TIMES])
        ax.set_ylim(0, 100)
    for ax in axes[:, 0]:
        ax.set_ylabel("Fraction of injected CO$_2$ (%)")
    for ax in axes[1, :]:
        ax.set_xlabel("Time after injection start (yr)")
    handles, labels_ = axes.ravel()[0].get_legend_handles_labels()
    fig.legend(handles, labels_, loc="lower center", ncol=5, frameon=False,
               bbox_to_anchor=(0.5, -0.02))
    fig.suptitle("SPE11b CO$_2$ inventory by compartment", y=1.02, fontsize=10)
    fig.savefig(os.path.join(FIGS, "fig1_compartments.png"))
    plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 2: E_s vs PVI
# ---------------------------------------------------------------------------
def fig2():
    pvi = np.linspace(0.005, 0.15, 200)
    V = dykstra_parsons_from_lognormal([k_md(f[1]) for f in FACIES if f[3] == "reservoir"])[0]
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    for phi, ls, col in [(0.20, "-", "#2b6cb0"), (0.25, "--", "#2f855a")]:
        ax.plot(pvi, [shook_mitchell_E_s(0.0, p, phi) for p in pvi],
                ls=ls, color=col, lw=2,
                label=f"homogeneous, $\\phi$={phi:.2f}")
        ax.plot(pvi, [shook_mitchell_E_s(V, p, phi) for p in pvi],
                ls=ls, color=col, lw=2, alpha=0.45,
                label=f"V$_\\mathrm{{DP}}$={V:.2f}, $\\phi$={phi:.2f}")
    ax.set_xlabel("Pore volumes injected (PVI)")
    ax.set_ylabel("Sweep efficiency $E_s$")
    ax.set_xlim(0, 0.15); ax.set_ylim(0, 1)
    ax.legend(frameon=False)
    ax.set_title("Shook–Mitchell sweep efficiency")
    fig.savefig(os.path.join(FIGS, "fig2_sweep_vs_pvi.png"))
    plt.close(fig)

# ---------------------------------------------------------------------------
# Figure 3: V_DP sensitivity
# ---------------------------------------------------------------------------
def fig3():
    Vgrid = np.linspace(0.0, 0.85, 200)
    pvi, phi = 0.05, 0.20
    NTG, kh_kv, M = 0.85, 10.0, 10.0   # documented assumptions
    es = [shook_mitchell_E_s(v, pvi, phi) for v in Vgrid]
    ec = [kopp_E_c(v, pvi, phi, NTG, kh_kv, M) for v in Vgrid]
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    ax.plot(Vgrid, es, lw=2, color="#2b6cb0", label="$E_s$ (sweep)")
    ax.plot(Vgrid, ec, lw=2, color="#9b2c2c", label="$E_c$ (Kopp)")
    ax.axvline(0.66, ls=":", color="0.4", lw=1)
    ax.text(0.67, 0.55, "SPE11b\n$V_{DP}{=}0.66$", fontsize=7)
    ax.set_xlabel("Dykstra–Parsons coefficient $V_{DP}$")
    ax.set_ylabel("Efficiency factor")
    ax.set_xlim(0, 0.85); ax.set_ylim(0, 0.6)
    ax.legend(frameon=False)
    ax.set_title("Heterogeneity reduces sweep and capacity "
                 "(PVI = 0.05, $\\phi$ = 0.20)")
    fig.savefig(os.path.join(FIGS, "fig3_vdp_sensitivity.png"))
    plt.close(fig)

if __name__ == "__main__":
    fig1(); fig2(); fig3()
    print("wrote to", FIGS)
    for f in sorted(os.listdir(FIGS)):
        print("  ", f)
