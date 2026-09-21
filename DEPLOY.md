# Test → Push → Deploy guide (co2-heterogeneity-screening)

A complete recipe for (1) testing the notebook and scripts locally, (2) creating the
GitHub repo, (3) pushing, and (4) going live on Binder / Google Colab.

> **Current state (21 Sep 2026):** the repo already exists at
> `https://github.com/todak2000/co2-heterogeneity-screening` (public, branch `main`).
> If you only want to *re-verify*, skip to **§1**. If you want to recreate it from
> scratch under a different name/account, follow **§2** onward and read the gotchas in §5.

---

## 0. Files involved

| File | Purpose |
|------|---------|
| `heterogeneity_screening.ipynb` | the live notebook (bundled data + GitHub-raw fallback) |
| `requirements.txt` | `numpy`, `matplotlib` (everything Binder/Colab needs to install) |
| `data/timeseries/*.csv` | 4 SPE11b simulator time series |
| `data/spatial_maps_rice1/*.csv` | representative rice1 spatial maps |
| `scripts/*.py` | `spe11b_regime_analysis`, `benchmark_analysis`, `plume_analysis`, `make_figures` |
| `manuscript.md`, `figures/` | the paper and its figures |
| `benchmark_spec/GROUND_TRUTH.md` | every verified fact and number |

---

## 1. Test locally BEFORE pushing

### 1.1 Create a virtualenv

The system Python here is Homebrew-managed (PEP 668: "externally-managed"), so install
inside a venv:

```bash
cd heterogeneity_screening
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install numpy matplotlib jupyter nbformat nbconvert ipykernel
```

### 1.2 Run the standalone scripts and check the numbers

```bash
python scripts/spe11b_regime_analysis.py   # dimensionless regime + seal balance
python scripts/benchmark_analysis.py       # inventory + inter-simulator agreement
python scripts/plume_analysis.py           # plume centroid rise / migration
python scripts/make_figures.py             # writes figures/ (needs matplotlib)
```

Confirm these **exact** values appear (they are the paper's ground truth):

- `t_grav = 43.4 yr`, `R_L = 2.21`, gravity number `26`, `seal entry = 0.194 MPa`, `breach ~133 m`
- agreement: mobile spread `0.40` (robust) vs seal spread `~115x` (fragile) at 1000 yr
- plume: net rise `+204 m`, net up-dip migration `+706 m`
- figures: `fig1_agreement.png`, `fig2_plume.png`, `fig3_regime.png`

### 1.3 Execute the notebook headlessly (the real test)

```bash
python -m nbconvert --to notebook --execute --inplace heterogeneity_screening.ipynb
```

Then confirm **zero errors**:

```bash
python - <<'PY'
import nbformat
nb = nbformat.read("heterogeneity_screening.ipynb", as_version=4)
errs = [c for c in nb.cells if c.cell_type == "code"
        for o in c.get("outputs", []) if o.get("output_type") == "error"]
print("errors:", len(errs))
PY
```

Expected: `errors: 0`. The same check re-runs every figure and number inline.

### 1.4 (Optional) interactive check

```bash
jupyter notebook heterogeneity_screening.ipynb
```

Open it in the browser, run **Cell → Run All**, confirm figures render and no cell errors.

### 1.5 Test the Colab data fallback (only if you changed the repo name/account)

The notebook has a hard-coded fallback that downloads the time-series from GitHub raw if
`data/timeseries` is missing:

```python
REPO = "todak2000/co2-heterogeneity-screening"
GITHUB_RAW = f"https://raw.githubusercontent.com/{REPO}/main/data/timeseries/"
```

If your final repo is named differently, update this string in the notebook's first code
cell **and** the badges in `README.md` (see §5).

---

## 2. Create the repository (from scratch)

### Option A — GitHub CLI `gh` (recommended; already authenticated here)

```bash
cd heterogeneity_screening
git init -b main
git add -A
git commit -m "CO2 storage heterogeneity screening: analytical corrections + SPE11b characterization"

gh repo create co2-heterogeneity-screening \
  --public --source=. --remote=origin --push
```

### Option B — plain git (if you created the repo in the browser first)

```bash
cd heterogeneity_screening
git init -b main
git add -A
git commit -m "CO2 storage heterogeneity screening: analytical corrections + SPE11b characterization"
git remote add origin https://github.com/<you>/co2-heterogeneity-screening.git
git push -u origin main
```

Check:

```bash
git status            # should be clean
gh repo view --json name,url,visibility
```

---

## 3. Push updates later

```bash
git add -A
git commit -m "describe the change"
git push origin main
```

---

## 4. Go live

### 4.1 Binder (full Jupyter in browser, no install)

Requirements are already satisfied: `requirements.txt` lists exactly `numpy` and
`matplotlib`, and the repo is public. The launcher URL pattern is:

```
https://mybinder.org/v2/gh/<user>/<repo>/HEAD?labpath=heterogeneity_screening.ipynb
```

i.e. for this repo:

```
https://mybinder.org/v2/gh/todak2000/co2-heterogeneity-screening/HEAD?labpath=heterogeneity_screening.ipynb
```

- First click builds a Docker image: **1–3 minutes**, then cached.
- Rebuild is automatic whenever you push a change.

### 4.2 Google Colab (instant)

```
https://colab.research.google.com/github/<user>/<repo>/blob/main/heterogeneity_screening.ipynb
```

Colab has no local data, so it exercises the automatic GitHub-raw download fallback in the
first code cell (~6 MB). This is why the `REPO` string in the notebook must match the real
repo (see §5).

### 4.3 Badges

Put these in `README.md` (already present) so anyone on GitHub can one-click:

```markdown
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/<user>/<repo>/HEAD?labpath=heterogeneity_screening.ipynb)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/<user>/<repo>/blob/main/heterogeneity_screening.ipynb)
```

---

## 5. Gotchas

1. **Repo name/account must match the notebook.** The hard-coded `REPO` fallback and the
   badges use `todak2000/co2-heterogeneity-screening`. Rename → update the notebook's
   first code cell + `README.md` badges together, then re-run §1.3.
2. **Binder needs a *public* repo.** Private repos will not build.
3. **Binder first-click latency.** It's a free service; a cold build can take a few
   minutes. Colab is the faster demo path.
4. **Keep the repo clean.** `.gitignore` already excludes `__pycache__/`, `*.pyc`,
   `.ipynb_checkpoints/`, `.DS_Store`. Don't commit `.venv/` — add it if you create one:
   `echo ".venv/" >> .gitignore`.
5. **Re-execute after any code edit.** Any change to `scripts/` or the notebook's own code
   should be followed by §1.3 before you push, so the committed notebook always contains
   fresh, error-free outputs.
