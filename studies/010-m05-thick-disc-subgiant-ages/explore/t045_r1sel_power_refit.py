"""T-045 diagnostic (exploration, post hoc; no label change): refit the R1-SEL power mocks of bin
[-0.7, -0.5) with data-independent starts.

The R-SEL referee found that this bin's power losses come from mocks whose fit finds no valley, and
that BIC sometimes chose K = 1 on two-component mocks of 40,000+ stars, which suggests failed K >= 2
fits (mock fits start only from the data fit and 2 perturbations, README 2.0). This script:

1. rebuilds the bin's data fits, pass table and r pools exactly as run.main_sel does (committed
   PARAMS), and checks the data fits against results/r1_sel.json;
2. regenerates each of the 6 power sets (S15E, S15N, Full x e = r tau, e = r A; 50 mocks each) with
   the SEL-8 stream selaux.mock_rng(seed, 31, k, j), refits it with the original procedure and checks
   d, valley and K against results/r1_sel.json and the R-SEL checkpoints;
3. refits the same catalogue with data-independent starts (m0.mixture_starts, NSTART per K, K = 1-5;
   own stream default_rng([seed, 45, k, j])), records the NLL and convergence of every K under both
   procedures, checks that the best NLL does not increase with K, and recomputes K, valley and d from
   the better of the two fits for each K (the K = 5 mode-matching rule as in run.shape_from_fits).

Power is recounted with the recorded d* of each variant (the null sets are not refitted). Run:
python -m astrolab explore 010 --tag t045-refit --script explore/t045_r1sel_power_refit.py
"""
import json
import time
from pathlib import Path

import numpy as np

import m0
import mocks
import run as R
import selaux
from astrolab import config

BIN = 0
NSTART = 8            # data-independent starts per K (README 2.0's nstart for mixtures)
KMAX_INDEP = 5
SEED_TAG = 45         # own stream for the independent starts (SEL-8 uses 31)
TOL = 0.01            # NLL tolerance (the start-selection tie rule of m0._better)


def shape_given(C, fits, kbest, k5):
    """Valley analysis of run.shape_from_fits with given fits (K -> theta) and K = 5 theta."""
    P = C.P
    p = m0.mix_cells(C.grid, fits[kbest], kbest)
    keep = None
    if kbest == P["kmax"]:
        p5 = m0.mix_cells(C.grid, k5, P["kmax"] + 1)
        pk5 = [C.grid.mid[i] for i in m0.peaks(p5 / C.grid.step, P["prom"])]
        keep = lambda t: any(abs(t - u) <= P["mode_match"] for u in pk5)
    v = m0.valley(C.grid, p, lo=P["valley_lo"], hi=P["valley_hi"], side_mass=P["side_mass"],
                  prom=P["prom"], keep_peaks=keep)
    return {"d": float(v["d"]), "valley": bool(v["valley"]), "k": int(kbest)}


def one_mock(C, D, mech, rng, pools, rng2):
    """run.r1_mock_sel (primary floor, power kind) with the model kept, then the independent refit."""
    P = C.P
    variant = D["variant"]
    s15 = variant != "Full"
    pm = D["power_models"]["primary"]
    lat = lambda k: mocks.latent_power(pm["mu_old"], pm["s_old"], pm["w_old"], pm["young"][1], k, rng,
                                       lo=pm["young"][0], tmax=P["tmax"])
    edges, rpools = pools

    def draw(k):
        tau = lat(k)
        sl = np.zeros(k, np.int64)
        return {"tau": tau, "r": mocks.draw_r_keyed(tau, sl, edges, rpools, rng), "sl": sl}
    cat, par = mocks.catalogue_sel(draw, D["_n"], mech, rng, s15=s15, cut=P["cut"], tmax=P["tmax"])
    coef = None
    if variant == "S15E":
        coef = m0.pass_coefs(R._pass_table(P, par["A"], par["e"] / par["A"], None, 1))
    model = R.onedim(C, cat["A"], cat["e"], s15, sel=R.R1_SEL_MODE[variant], ptab=coef)
    A, w, n = model.cells.A, model.cells.w, model.cells.nstar
    # original procedure (consumes rng exactly as r1_mock_sel)
    t0 = time.perf_counter()
    fits = R.fit_mixtures(C, model, A, w, P["kmax"], starts_from=D["_starts"], rng=rng)
    conv_o = dict(model.converged)
    kbest, bics = R.choose_k(fits, n)
    v, _, k5 = R.shape_from_fits(C, model, fits, kbest, A, w, starts_from=D["_starts"], rng=rng)
    t_o = time.perf_counter() - t0
    nll_o = {K: float(nll) for K, (_, nll) in fits.items()}
    th_o = {K: th for K, (th, _) in fits.items()}
    # data-independent starts, K = 1..5
    t0 = time.perf_counter()
    nll_i, th_i, conv_i = {}, {}, {}
    for K in range(1, KMAX_INDEP + 1):
        r = model.fit_mixture(K, m0.mixture_starts(A, w, K, NSTART, rng2))
        nll_i[K], th_i[K], conv_i[K] = float(r.fun), r.x, bool(r.success)
    t_i = time.perf_counter() - t0
    # better of the two per K (K = 5 from the original only when it was fitted)
    best_th, best_nll, src = {}, {}, {}
    for K in range(1, P["kmax"] + 1):
        if nll_i[K] < nll_o[K] - TOL:
            best_th[K], best_nll[K], src[K] = th_i[K], nll_i[K], "indep"
        else:
            best_th[K], best_nll[K], src[K] = th_o[K], nll_o[K], "orig"
    K5 = P["kmax"] + 1
    th5, nll5 = th_i[K5], nll_i[K5]
    if k5 is not None:
        nll5_o = float(model.mix_negll(k5, K5)[0])
        if not nll_i[K5] < nll5_o - TOL:
            th5, nll5 = k5, nll5_o
    best_nll[K5] = nll5
    kb2, bics2 = R.choose_k({K: (best_th[K], best_nll[K]) for K in range(1, P["kmax"] + 1)}, n)
    v2 = shape_given(C, best_th, kb2, th5)
    v_i = shape_given(C, th_i, R.choose_k({K: (th_i[K], nll_i[K]) for K in range(1, P["kmax"] + 1)}, n)[0], th_i[K5])
    mono = lambda nl: [K for K in range(2, max(nl) + 1) if nl[K] > nl[K - 1] + TOL]
    return {
        "orig": {"d": float(v["d"]), "valley": bool(v["valley"]), "k": int(v["k"]), "nll": nll_o,
                 "converged": {K: bool(c) for K, c in conv_o.items()}, "k5_nll": (float(model.mix_negll(k5, K5)[0]) if k5 is not None else None),
                 "nonmonotone_K": mono(nll_o), "seconds": t_o},
        "indep": {"nll": nll_i, "converged": conv_i, "nonmonotone_K": mono(nll_i), "seconds": t_i,
                  "shape": v_i},
        "best": {"nll": best_nll, "source": src, "nonmonotone_K": mono(best_nll), **v2},
        "gain": {K: nll_o[K] - nll_i[K] for K in range(1, P["kmax"] + 1)},
        "n": int(n),
    }


def main(ctx):
    P = dict(R.PARAMS)
    t_start = time.time()
    C = R.Ctx(P)
    df = R.load(ctx, P)
    F = R.flags(df, P)
    A_all, E_all, feh = df["age"].to_numpy(), df["eage"].to_numpy(), df["feh"].to_numpy()
    with np.errstate(divide="ignore", invalid="ignore"):
        rel_all = E_all / A_all
    F = dict(F, s15=F["s15"] & (A_all > 0))                    # SEL-0, as run.main_sel
    lo, hi = P["r1_bins"][BIN]
    assert [lo, hi] == [-0.7, -0.5]
    mask = F["valid"] & (feh >= lo) & (feh < hi)
    T = R._pass_table(P, A_all[mask], rel_all[mask], None, 1)
    coef = m0.pass_coefs(T)
    pools = R._pools(T, rel_all[mask])
    rec = json.loads((R.HERE / "results" / "r1_sel.json").read_text(encoding="utf-8"))
    sets = selaux.sel_sets(len(P["r1_bins"]), P["mechs"], list(P["sel_floor_sens_bins"]))
    nmock = int(P["sel_n_mock"])
    store = None
    root = config.cache_dir() / "s010_sel_mocks"
    if root.exists():
        cands = [d for d in root.iterdir() if (d / "k004_j00.json").exists()]
        store = cands[0] if len(cands) == 1 else None
    ctx.log(f"T-045: checkpoint folder {store}")
    out = {"bin": [lo, hi], "nstart_indep": NSTART, "kmax_indep": KMAX_INDEP, "tol": TOL, "variants": {}}
    for v in selaux.R1_VARIANTS:
        D = R.r1_data_sel(C, df, F, BIN, v, coef)
        rb = rec["variants"][v]["bins"][BIN]
        rf = rec["data_fits"][f"{v}_{BIN}"]
        data_check = {"d": [D["shape"]["d"], rb["d"]], "k": [D["shape"]["k"], rb["k"]],
                      "fits_max_abs_diff": max(float(np.max(np.abs(np.array(D["fits"][K]) - np.array(rf["fits"][K]))))
                                               for K in rf["fits"]),
                      "power_model_w_old": [D["power_models"]["primary"]["w_old"], rb["power_model"]["w_old"]],
                      "edge": [D["power_models"]["primary"]["young"][1], rb["power_model"]["young"][1]]}
        ctx.log(f"T-045 {v}: data fit check {data_check}")
        dstar = float(rb["d_star"])
        vout = {"data_check": data_check, "d_star": dstar, "mechs": {}}
        for mech in P["mechs"]:
            s = [x for x in sets if x["tag"] == "R1" and x.get("variant") == v and x["bin"] == BIN
                 and x["kind"] == "power" and x["mech"] == mech and x["floor"] == "primary"][0]
            k = s["k"]
            rm = rb["mocks"][f"power_{mech}"]
            assert rm["k"] == k, (v, mech, rm["k"], k)
            rows = []
            for j in range(nmock):
                rng = selaux.mock_rng(P["seed"], P["sel_seed_tag"], k, j)
                rng2 = np.random.default_rng([int(P["seed"]), SEED_TAG, int(k), int(j)])
                r = one_mock(C, D, mech, rng, pools, rng2)
                cp = None
                if store is not None:
                    p = store / f"k{k:03d}_j{j:02d}.json"
                    if p.exists():
                        cp = json.loads(p.read_text(encoding="utf-8"))["result"]
                r["recorded"] = {"d": rm["d"][j], "valley": rm["valley"][j], "k": cp["k"] if cp else None}
                r["reproduced"] = (abs(r["orig"]["d"] - rm["d"][j]) <= 1e-9 and r["orig"]["valley"] == rm["valley"][j]
                                   and (cp is None or r["orig"]["k"] == cp["k"]))
                rows.append(r)
                if j % 10 == 9:
                    ctx.log(f"T-045 {v} {mech}: {j + 1} mocks, {(time.time() - t_start) / 60:.1f} min")
            passes = lambda x: x["valley"] and x["d"] < dstar
            summ = {
                "set_k": k,
                "reproduced": sum(x["reproduced"] for x in rows),
                "power_orig": float(np.mean([passes(x["orig"]) for x in rows])),
                "power_recorded": float(np.mean([rm["valley"][j] and rm["d"][j] < dstar for j in range(nmock)])),
                "power_best": float(np.mean([passes(x["best"]) for x in rows])),
                "power_indep_only": float(np.mean([passes(x["indep"]["shape"]) for x in rows])),
                "no_valley_orig": sum(not x["orig"]["valley"] for x in rows),
                "no_valley_best": sum(not x["best"]["valley"] for x in rows),
                "k_orig": {str(K): sum(x["orig"]["k"] == K for x in rows) for K in range(1, P["kmax"] + 1)},
                "k_best": {str(K): sum(x["best"]["k"] == K for x in rows) for K in range(1, P["kmax"] + 1)},
                "nonmonotone_orig": sum(bool(x["orig"]["nonmonotone_K"]) for x in rows),
                "nonmonotone_indep": sum(bool(x["indep"]["nonmonotone_K"]) for x in rows),
                "nonmonotone_best": sum(bool(x["best"]["nonmonotone_K"]) for x in rows),
                "indep_better_any_K": sum(any(g > 1.0 for g in x["gain"].values()) for x in rows),
                "indep_better_by_K": {str(K): sum(x["gain"][K] > 1.0 for x in rows) for K in range(1, P["kmax"] + 1)},
                "orig_not_converged_by_K": {str(K): sum(not x["orig"]["converged"][K] for x in rows) for K in range(1, P["kmax"] + 1)},
                "indep_not_converged_by_K": {str(K): sum(not x["indep"]["converged"][K] for x in rows) for K in range(1, KMAX_INDEP + 1)},
                "misses_orig_recovered": sum((not passes(x["orig"])) and passes(x["best"]) for x in rows),
                "passes_orig_lost": sum(passes(x["orig"]) and not passes(x["best"]) for x in rows),
                "d_best_quantiles": [float(q) for q in np.percentile([x["best"]["d"] for x in rows], [5, 50, 95])],
                "seconds": {"orig": float(sum(x["orig"]["seconds"] for x in rows)),
                            "indep": float(sum(x["indep"]["seconds"] for x in rows))},
            }
            ctx.log(f"T-045 {v} {mech}: {summ}")
            vout["mechs"][mech] = {"summary": summ, "mocks": [
                {"j": j, "recorded": x["recorded"], "reproduced": x["reproduced"],
                 "orig": {kk: x["orig"][kk] for kk in ("d", "valley", "k", "nll", "converged", "k5_nll", "nonmonotone_K")},
                 "indep": {kk: x["indep"][kk] for kk in ("nll", "converged", "nonmonotone_K", "shape")},
                 "best": {kk: x["best"][kk] for kk in ("d", "valley", "k", "source", "nonmonotone_K")}}
                for j, x in enumerate(rows)]}
        out["variants"][v] = vout
        del D
    out["minutes"] = (time.time() - t_start) / 60
    ctx.save("t045_refit", out)
    return {v: {m: out["variants"][v]["mechs"][m]["summary"]["power_best"] for m in P["mechs"]} for v in out["variants"]}
