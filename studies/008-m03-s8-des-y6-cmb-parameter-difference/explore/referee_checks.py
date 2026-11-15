"""Exploration (post hoc, referee items 1, 2, 5; 2026-11-15). Uses the cached chains only.

1. Parametrization dependence of the Gaussian parameter difference (R4 full space): (S8, Omega_m),
   (A_s, Omega_m), the six sampled parameters, the same six with S8 in place of A_s, and the six plus
   sigma_12 (what the full space would have been without the step-A treatment of upper-case
   columns as derived).
2. Chain-row bootstrap of the R2 n_sigma (1-D and 2-D): resample the rows of each chain with
   replacement (keeping their weights), then run the registered estimator with one seed.
3. R5 with the published central values read as modes instead of means.
Run with:
    python -m astrolab explore 008 --tag referee-checks --script explore/referee_checks.py
"""
import numpy as np

import run
import s8diff


def _load(ctx, P, key):
    path = run._fetch(ctx, P, key)
    fmt = s8diff.read_format(path)
    cmap, status = s8diff.column_map(fmt, key, key in P["positional_ok"])
    chain, _ = s8diff.load_chain(path, cmap, 0.0)
    return chain, [h.lower() for h in fmt["header"]]


def main(ctx):
    P = dict(run.PARAMS)
    des, hd = _load(ctx, P, "des_3x2pt")
    cmb, hc = _load(ctx, P, "cmb")

    def cols(c, h, names):
        out = []
        for n in names:
            if n == "s8":
                out.append(c["s8"])
            else:
                out.append(c["data"][:, h.index(n)])
        return np.column_stack(out)

    cp = "cosmological_parameters--"
    six = [cp + x for x in ("a_s_1e9", "h0", "mnu", "n_s", "omega_b", "omega_m")]
    sets = {
        "S8, Omega_m": ["s8", cp + "omega_m"],
        "A_s, Omega_m": [cp + "a_s_1e9", cp + "omega_m"],
        "six sampled (as R4)": six,
        "six with S8 in place of A_s": ["s8"] + six[1:],
        "six plus S8": six + ["s8"],
        "six plus sigma_12": six + [cp + "sigma_12"],
    }
    gauss = {}
    for name, names in sets.items():
        gauss[name] = s8diff.full_space_gaussian(cols(des, hd, names), des["w"], cols(cmb, hc, names), cmb["w"],
                                                 P["max_cond"])
        ctx.log(f"Gaussian {name}: {gauss[name].get('n_sigma')}")

    # chain-row bootstrap of R2
    rng = np.random.default_rng(100)
    boot = {"1d": [], "2d": []}
    for b in range(20):
        ia = rng.integers(0, len(des["w"]), len(des["w"]))
        ib = rng.integers(0, len(cmb["w"]), len(cmb["w"]))
        for d, tag in ((1, "1d"), (2, "2d")):
            va = des["s8"][ia][:, None] if d == 1 else np.column_stack([des["s8"][ia], des["omega_m"][ia]])
            vb = cmb["s8"][ib][:, None] if d == 1 else np.column_stack([cmb["s8"][ib], cmb["omega_m"][ib]])
            r = s8diff.parameter_difference(va, des["w"][ia], vb, cmb["w"][ib], P["n_pairs"], [b])
            boot[tag].append(r["per_seed"][0])
    boot_summary = {t: {"mean": float(np.mean(v)), "sd": float(np.std(v, ddof=1)), "values": v} for t, v in boot.items()}
    ctx.log(f"bootstrap 1d sd {boot_summary['1d']['sd']:.4f}, 2d sd {boot_summary['2d']['sd']:.4f}")

    # R5 with central values read as modes
    r5_mode = {}
    for name, (m, sp, sm, ref) in P["probes"].items():
        mean = m + np.sqrt(2 / np.pi) * (sp - sm)       # a split normal with mode m has this mean
        vals = []
        for seed in P["seeds"]:
            g = np.random.default_rng(seed)
            x = s8diff.split_normal_draws(mean, sp, sm, P["n_probe"], g)
            ib = g.choice(len(cmb["w"]), size=P["n_probe"], replace=True, p=cmb["w"])
            vals.append(s8diff.nsigma_binned((x - cmb["s8"][ib])[:, None])["n_sigma"])
        r5_mode[name] = float(np.mean(vals))
    ctx.save("referee_checks", {"gaussian_by_parametrization": gauss, "bootstrap": boot_summary,
                                "r5_central_value_as_mode": r5_mode})
