"""
make_figures.py
===============
Publication figures for "Gravity-dominated storage and the limits of agreement in
the SPE11b benchmark". Regenerates Figures 1-3 from the data in this repo.

Figure 1 - cross-simulator CO2 compartment agreement (t=50 and t=1000 yr)
Figure 2 - domain-wide plume centroid trajectory and areal growth (rice1)
Figure 3 - governing timescales and the seal capillary-gravity balance

Run:  python3 make_figures.py   (needs numpy, matplotlib)
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SDIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SDIR)
FIGS = os.path.join(ROOT, "figures")
os.makedirs(FIGS, exist_ok=True)

from benchmark_analysis import load_sims, inventory, TOTAL_INJECTED
from plume_analysis import plume_series
from spe11b_regime_analysis import (T_INJ, T_MONITOR, t_grav, P_ENTRY,
                                    DELTA_RHO, G, AR, RL)

plt.rcParams.update({"font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9.5,
                     "legend.fontsize": 7.5, "xtick.labelsize": 7.5,
                     "ytick.labelsize": 7.5, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 300,
                     "savefig.dpi": 300, "savefig.bbox": "tight"})

SIMS = ["rice1", "ctc-cne1", "opm1", "sintef1"]
SCOL = {"rice1": "#c0392b", "ctc-cne1": "#2b6cb0", "opm1": "#2f855a", "sintef1": "#805ad5"}

def fig1_agreement():
    sims = load_sims()
    inv = inventory(sims)
    comps = [("mobile", "Mobile"), ("immobile", "Immobile (residual)"),
             ("dissolved", "Dissolved"), ("seal", "Seal (structural)")]
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.6), sharey=True)
    for ax, yr in zip(axes, (50, 1000)):
        x = np.arange(len(comps))
        w = 0.2
        for i, s in enumerate(SIMS):
            vals = [inv[yr][k][s] for k, _ in comps]
            ax.bar(x + (i - 1.5) * w, vals, w, color=SCOL[s], label=s)
        ax.set_xticks(x); ax.set_xticklabels([c[1] for c in comps], rotation=15, ha="right")
        ax.set_title(f"t = {yr} yr")
        ax.set_ylabel("Fraction of injected CO\u2082 (%)")
    axes[0].legend(frameon=False, ncol=1, loc="upper right", fontsize=6.5)
    fig.suptitle("SPE11b: do the four simulators agree? (per compartment)", y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig1_agreement.png")); plt.close(fig)

def fig2_plume():
    rows = plume_series()
    yr = [r[0] for r in rows]; xc = [r[1] for r in rows]
    zc = [r[2] for r in rows]; area = [r[3] for r in rows]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.0, 3.6))
    ax1.plot(xc, zc, "o-", color="#2b6cb0", lw=2)
    for xt, zt, t in zip(xc, zc, yr):
        ax1.annotate(f"{t} yr", (xt, zt), textcoords="offset points", xytext=(6, -8), fontsize=7)
    ax1.set_xlabel("x-centroid of plume (m)"); ax1.set_ylabel("z-centroid (m)")
    ax1.set_title("Plume centroid migrates up-dip (rice1)")
    ax1.invert_yaxis()
    ax2.plot(yr, area, "s-", color="#2f855a", lw=2)
    ax2.set_xlabel("Year"); ax2.set_ylabel("Plume area (km\u00b2)")
    ax2.set_title("Plume areal growth")
    fig.suptitle("Domain-wide CO\u2082 plume evolution (from spatial maps)", y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig2_plume.png")); plt.close(fig)

def fig3_regime():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.0, 3.6))
    # (a) governing timescales
    labels = ["buoyant rise\nof full 1200 m", "injection\nduration", "post-injection\nmonitoring"]
    vals = [t_grav / (365*86400), T_INJ / (365*86400), (T_MONITOR - T_INJ) / (365*86400)]
    cols = ["#c0392b", "#2b6cb0", "#95a5a6"]
    ax1.barh(labels, vals, color=cols)
    ax1.set_xscale("log"); ax1.set_xlim(1, 3000)
    ax1.set_xlabel("Timescale (yr, log)")
    for i, v in enumerate(vals):
        ax1.text(v * 1.3, i, f"{v:.0f} yr", va="center", fontsize=8)
    ax1.set_title("Gravity and injection are co-active")
    # (b) seal capillary-gravity balance
    h = np.linspace(0, 250, 100)
    buoy = DELTA_RHO * G * h / 1e6
    ax2.plot(h, buoy, color="#c0392b", lw=2, label="buoyancy head")
    ax2.axhline(P_ENTRY / 1e6, color="#2b6cb0", ls="--", lw=2, label="seal entry pressure")
    hb = P_ENTRY / (DELTA_RHO * G)
    ax2.axvline(hb, color="0.6", ls=":", lw=1)
    ax2.text(hb + 5, 0.35, f"breach\n\u2248{hb:.0f} m", fontsize=7)
    ax2.set_xlabel("CO\u2082 column height (m)")
    ax2.set_ylabel("Pressure (MPa)")
    ax2.set_xlim(0, 250); ax2.set_ylim(0, 0.45)
    ax2.legend(frameon=False, fontsize=7.5)
    ax2.set_title("Seal holds \u2248200 m, not the full 1200 m")
    fig.suptitle("SPE11b dimensionless regime", y=1.02)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGS, "fig3_regime.png")); plt.close(fig)

if __name__ == "__main__":
    fig1_agreement(); fig2_plume(); fig3_regime()
    print("figures written to", FIGS)
