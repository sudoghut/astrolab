"""M9 NANOGrav 15-yr GWB: power-law amplitude and spectral index from the KDE free spectrum.

Pre-registration: README sections 1-4. Run with:
    python -m astrolab run 005-m09-nanograv-gwb-power-law
Explore with:
    python -m astrolab explore 005-m09-nanograv-gwb-power-law --tag <topic> --set KEY=VALUE

R1  log10 A at gamma = 13/3 vs L8's interval (Hellinger < 0.15 against a two-piece half-normal).
R2  free (log10 A, gamma): HPD level q at gamma = 13/3 (descriptive category).
R2b L37 Table A1 overlap summary (Lean NUM binding: n_models_overlap_ci90 >= 1).
R3  v1.1.0 vs v2.0.0 (descriptive).
R4  turnover vs gamma = 13/3 power law, ln Bayes factor (descriptive).
"""
import numpy as np

import gwb
from table_a1 import TABLE_A1

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    "versions": ["v2.0.0", "v1.1.0"],
    "urls": {
        "v2.0.0": "https://zenodo.org/records/21844115/files/ceffyl_data.zip?download=1",
        "v1.1.0": "https://zenodo.org/records/10344086/files/NANOGrav15yr_KDE-FreeSpectra_v1.1.0.zip?download=1",
    },
    "dir_key": "30f_fs{hd}",
    "n_freq_file": 30,
    "n_freq": 14,
    "t_yr": 16.03,
    "freq_tol": 0.01,
    "grid_rtol": 1e-6,
    "below_grid": "clip",
    "gamma_fixed": 13.0 / 3.0,
    "r1_range": [-18.0, -14.0], "r1_step": 0.001,
    "r2_range_a": [-18.0, -11.0], "r2_range_g": [0.0, 7.0], "r2_step": 0.005,
    "r4_range_fb": [-9.0, -7.5], "r4_range_k": [0.0, 7.0], "r4_steps": [0.01, 0.025, 0.1],
    "chunk": 64,
    "edge_frac": 0.01, "edge_max": 0.01,
    # pre-registered reference values and thresholds (README section 2)
    "l8_A_13_3": [2.4e-15, 1.8e-15, 3.1e-15],      # median, 5%, 95%
    "h_max": 0.15,
    "q_cat": [0.95, 0.997],
    # zip safety (README section 4 step 1)
    "max_member_bytes": 50 * 2 ** 20, "max_total_bytes": 150 * 2 ** 20, "max_members": 10000,
}


def _round(a, sig=5):
    a = np.asarray(a, dtype=float)
    return [float(f"{v:.{sig}g}") for v in a.ravel()]


def _load(ctx, P, version, path=None):
    if path is None:
        path = ctx.http(P["urls"][version], label=f"NANOGrav 15yr KDE free spectra {version}")
    prod = gwb.load_product(path, P["dir_key"], max_member_bytes=P["max_member_bytes"],
                            max_total_bytes=P["max_total_bytes"], max_members=P["max_members"])
    return gwb.check_product(prod, n_freq_file=P["n_freq_file"], t_yr=P["t_yr"],
                             freq_tol=P["freq_tol"], grid_rtol=P["grid_rtol"])


def _guard(fn, *a, **kw):
    try:
        return fn(*a, **kw)
    except gwb.NotEvaluable as e:
        return {"verdict": "not evaluable", "reason": str(e)}


def _r1(prod, P):
    lo, hi = P["r1_range"]
    return gwb.r1(prod, n_freq=P["n_freq"], gamma=P["gamma_fixed"], lo=lo, hi=hi, step=P["r1_step"],
                  below_grid=P["below_grid"], l8_a=P["l8_A_13_3"], edge_frac=P["edge_frac"],
                  edge_max=P["edge_max"], h_max=P["h_max"])


def _r2(prod, P):
    out = gwb.r2(prod, n_freq=P["n_freq"], lo_a=P["r2_range_a"][0], hi_a=P["r2_range_a"][1],
                 lo_g=P["r2_range_g"][0], hi_g=P["r2_range_g"][1], step=P["r2_step"],
                 below_grid=P["below_grid"], gamma_line=P["gamma_fixed"], edge_frac=P["edge_frac"],
                 edge_max=P["edge_max"], chunk=P["chunk"])
    out["category"] = gwb.category(out["q_hpd_13_3"], *P["q_cat"])
    return out


def _public(d):
    return {k: v for k, v in d.items() if not k.startswith("_")}


def main(ctx):
    P = dict(PARAMS)
    summary = {"params": P}
    prods = {}
    for v in P["versions"]:
        path = ctx.http(P["urls"][v], label=f"NANOGrav 15yr KDE free spectra {v}")
        try:
            prods[v] = _load(ctx, P, v, path)
        except gwb.NotEvaluable as e:
            prods[v] = None
            summary[f"load_{v}"] = {"verdict": "not evaluable", "reason": str(e)}
            ctx.log(f"{v}: not evaluable: {e}")
            ctx.log(f"{v}: archive members: {gwb.list_members(path)}")
        else:
            p = prods[v]
            summary[f"load_{v}"] = {"dir": p["dir"], "n_grid": int(p["grid"].size),
                                    "grid_lo": float(p["grid"][0]), "grid_hi": float(p["grid"][-1]),
                                    "db": p["db"], "T_yr": p["T"] / gwb.YEAR_S,
                                    "f1_nHz": float(p["freqs"][0] * 1e9)}
            ctx.log(f"{v}: {p['dir']}, grid {p['grid'][0]:.2f}..{p['grid'][-1]:.2f} ({p['grid'].size}), "
                    f"T = {p['T'] / gwb.YEAR_S:.2f} yr")

    primary = P["versions"][0]
    pv = prods.get(primary)
    res = {}
    for v, prod in prods.items():
        if prod is None:
            res[v] = {"r1": {"verdict": "not evaluable", "reason": "data product not evaluable"},
                      "r2": {"verdict": "not evaluable", "reason": "data product not evaluable"}}
            continue
        res[v] = {"r1": _guard(_r1, prod, P), "r2": _guard(_r2, prod, P)}
        r1v, r2v = res[v]["r1"], res[v]["r2"]
        ctx.log(f"{v} R1: {r1v.get('median_A', float('nan')):.3e} "
                f"[{r1v.get('q05_A', float('nan')):.3e}, {r1v.get('q95_A', float('nan')):.3e}], "
                f"H = {r1v.get('hellinger', float('nan')):.3f} -> {r1v.get('verdict')}")
        ctx.log(f"{v} R2: q = {r2v.get('q_hpd_13_3', float('nan')):.4f}, gamma = "
                f"{r2v.get('gamma_median', float('nan')):.2f} [{r2v.get('gamma_q05', float('nan')):.2f}, "
                f"{r2v.get('gamma_q95', float('nan')):.2f}]")

    # R1, R2 (primary)
    r1 = res.get(primary, {}).get("r1", {"verdict": "not evaluable", "reason": "no data"})
    r2 = res.get(primary, {}).get("r2", {"verdict": "not evaluable", "reason": "no data"})
    ctx.save("r1", {"version": primary, **_public(r1)})
    ctx.save("r2", {"version": primary, **_public(r2)})

    # R2b
    if "median_A" in r1:
        r2b = gwb.r2b(r1["q05_A"], r1["median_A"], r1["q95_A"], TABLE_A1)
        r2b["A_q05"], r2b["A_median"], r2b["A_q95"] = r1["q05_A"], r1["median_A"], r1["q95_A"]
    else:
        r2b = {"verdict": "not evaluable", "reason": "R1 not evaluable"}
    ctx.save("r2b", r2b)

    # R3 (descriptive)
    r3 = {"primary": primary, "versions": {}}
    for v in P["versions"][1:]:
        a, b = res.get(v, {}), res.get(primary, {})
        out = {"r1": _public(a.get("r1", {})), "r2": _public(a.get("r2", {}))}
        if "median_A" in a.get("r1", {}) and "median_A" in b.get("r1", {}):
            out["delta_median_A"] = a["r1"]["median_A"] - b["r1"]["median_A"]
            out["delta_q05_A"] = a["r1"]["q05_A"] - b["r1"]["q05_A"]
            out["delta_q95_A"] = a["r1"]["q95_A"] - b["r1"]["q95_A"]
            x = b["r1"]["_x"]
            out["hellinger_v1_v2"] = gwb.hellinger(x, a["r1"]["_p"], b["r1"]["_p"])
        if "q_hpd_13_3" in a.get("r2", {}) and "q_hpd_13_3" in b.get("r2", {}):
            out["delta_q"] = a["r2"]["q_hpd_13_3"] - b["r2"]["q_hpd_13_3"]
        r3["versions"][v] = out
    ctx.save("r3", r3)

    # R4 (descriptive)
    if pv is not None:
        r4 = _guard(gwb.r4, pv, n_freq=P["n_freq"], gamma=P["gamma_fixed"], lo_a=P["r2_range_a"][0],
                    hi_a=P["r2_range_a"][1], lo_fb=P["r4_range_fb"][0], hi_fb=P["r4_range_fb"][1],
                    lo_k=P["r4_range_k"][0], hi_k=P["r4_range_k"][1], steps=tuple(P["r4_steps"]),
                    below_grid=P["below_grid"], edge_frac=P["edge_frac"], edge_max=P["edge_max"],
                    chunk=max(1, P["chunk"] // 8))
    else:
        r4 = {"verdict": "not evaluable", "reason": "primary data product not evaluable"}
    ctx.save("r4", {"version": primary, **r4})
    ctx.log(f"R4: ln BF = {r4.get('ln_bf_turnover_vs_pl', float('nan')):.3f}")

    # curves for the web page (downsampled, rounded; small)
    curves = {}
    if "_x" in r1:
        k = max(1, r1["_x"].size // 400)
        curves["r1"] = {"log10A": _round(r1["_x"][::k], 6), "post": _round(r1["_p"][::k]),
                        "ref": _round(r1["_ref"][::k])}
    if "_xa" in r2:
        ka = max(1, r2["_xa"].size // 140)
        curves["r2"] = {"axes": ["gamma", "log10A"],
                        "log10A": _round(r2["_xa"][::ka], 5), "gamma": _round(r2["_xg"][::ka], 5),
                        "post": [_round(row, 3) for row in r2["_p"][::ka, ::ka]]}
    ctx.save("curves", curves)

    summary.update({
        "r1": {k: r1.get(k) for k in ("median_A", "q05_A", "q95_A", "hellinger", "verdict", "reason")
               if k in r1},
        "r2": {k: r2.get(k) for k in ("q_hpd_13_3", "category", "gamma_median", "A_median", "reason")
               if k in r2},
        "r2b": {k: r2b.get(k) for k in ("n_models_overlap_ci90", "n_models_contain_median", "reason")
                if k in r2b},
        "r4": {k: r4.get(k) for k in ("ln_bf_turnover_vs_pl", "reason") if k in r4},
    })
    ctx.save("summary", summary)
    return summary
