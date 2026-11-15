"""M3 S8 tension: DES Y6 3x2pt against the CMB, parameter difference (README sections 1-4).

Pre-registration: README sections 1-4 (frozen 2026-11-15). Run with:
    python -m astrolab run 008-m03-s8-des-y6-cmb-parameter-difference
Step A only (formats and column maps, no statistics; written under explore/):
    python -m astrolab explore 008 --tag step-a --set step_a_only=true

R1  S8 means and 68% intervals of the CMB, DES 3x2pt and DES xi+- chains against D26.
R2  DES 3x2pt - CMB parameter difference, 1-D (S8) and 2-D (S8, Omega_m), D26 eqs. 17-19.
R3  DES xi+- - CMB parameter difference (descriptive).
R4  sensitivity: projection shift, MAP shift, algorithms, threshold, full-space Gaussian.
R5  published S8 summaries of other probes against the CMB chain (descriptive).
"""
import re

import numpy as np

import s8diff

BASE = "https://desdr-server.ncsa.illinois.edu/despublic/y6a2_files/y6_key/chains_release/"

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    "step_a_only": False,
    "chains": {
        "des_3x2pt": "32pt_wolensbin2_lin_lcdm_DV0723_R0723.txt",
        "cmb": "fiducial_cmb_tp_external_R1006.txt",
        "des_xipm": "12pt_wolensbin2_lin_lcdm_DV0723_R0723.txt",
        "des_xipm_nla": "shear_nla_wolensbin2_lcdm_DV0723_R0723.txt",
    },
    "positional_ok": ["des_3x2pt", "des_xipm", "des_xipm_nla"],
    # one-off cap for the 32pt chain only: user consent in chat, 2026-11-15 (log.md, README section 3)
    "max_bytes_32pt": 150 * 1024 ** 2,
    "mcmc_burn": 0.30,
    "ess_flag": 2000,
    # R1 (published D26 means and 68% intervals)
    "published": {"cmb": [0.836, 0.012, 0.013], "des_3x2pt": [0.789, 0.012, 0.012],
                  "des_xipm": [0.783, 0.019, 0.015], "des_xipm_nla": [0.783, 0.019, 0.015]},
    "tol_mean": 0.002, "tol_end": 0.003, "mass": 0.68, "n_grid": 2000,
    # R2
    "published_nsigma": {"1d": 2.6, "2d": 2.2},
    "tol_nsigma": 0.15, "s_max": 0.03, "n_pairs": 4_000_000, "seeds": [0, 1, 2, 3, 4],
    "bw_variants": [0.5, 2.0], "bw_flag": 0.1, "support_frac_max": 0.01, "conv_spacing": 1e-4,
    # R4
    "proj_shift": 0.17 * 0.012, "map_shift": 0.793 - 0.789, "max_cond": 1e8,
    "corr_max": 0.999, "constrained_ratio": 0.25,
    # R5: name -> [mean, sigma_plus, sigma_minus, reference]
    "probes": {
        "KiDS-Legacy": [0.813, 0.018, 0.018, "arXiv:2503.19441 Table 4 (mean)"],
        "HSC Y3 (Zhang+ 2025)": [0.780, 0.029, 0.030, "arXiv:2507.01386"],
        "ACT DR6 + Planck lensing + BAO": [0.831, 0.023, 0.023, "arXiv:2304.05203"],
        "eROSITA eRASS1": [0.86, 0.01, 0.01, "arXiv:2402.08458 eq. 83"],
        "DES Y3 3x2pt": [0.776, 0.017, 0.017, "arXiv:2105.13549"],
        "KiDS-1000 3x2pt": [0.766, 0.020, 0.014, "arXiv:2007.15632"],
        "KiDS-1000 cosmic shear": [0.759, 0.024, 0.021, "arXiv:2007.15633"],
        "HSC Y3 shear (Li+ 2023)": [0.769, 0.031, 0.034, "arXiv:2304.00702"],
        "HSC Y3 shear (Dalal+ 2023)": [0.776, 0.032, 0.033, "arXiv:2304.00701"],
        "HSC Y3 3x2pt (Sugiyama+ 2023)": [0.775, 0.043, 0.038, "arXiv:2304.00705"],
    },
    "n_probe": 1_000_000,
}

DERIVED = {"sigma_8", "sigma8", "s_8", "s8", "omega_lambda", "omega_nu", "omega_c", "omch2", "ommh2",
           "h0", "theta_star", "100theta_star"}


AMPLITUDE = {"a_s", "as", "log1e10as", "ln10^{10}a_s", "loga", "ln10_10_as", "log10as", "ln_as1e10",
             "logas", "ln10as", "ln_1e10_as", "logA_s".lower()}


def _parse_priors(lines):
    """CosmoSIS ini files echoed as '##' lines.

    values.ini: '## [section]' then '## name = lo start hi' (uniform range);
    priors.ini (between START_OF_PRIORS_INI and END_OF_PRIORS_INI): '## name = gaussian mu sigma'.
    Returns {section--name: {"range": (lo, hi)} or {"gaussian_sigma": s}}; inline ';' or '#' comments
    are stripped before matching.
    """
    out, section, block = {}, "", ""
    for line in lines:
        s = line.lstrip("#").strip()
        up = s.upper()
        if up.startswith("START_OF_"):
            block = up[len("START_OF_"):]
            continue
        if up.startswith("END_OF_"):
            block = ""
            continue
        s = re.split(r"[;#]", s)[0].strip()
        m = re.match(r"\[(.+)\]$", s)
        if m:
            section = m.group(1).strip().lower()
            continue
        if not section:
            continue
        m = re.match(r"([\w\-]+)\s*=\s*(.+)$", s)
        if not m:
            continue
        name, rhs = f"{section}--{m.group(1).lower()}", m.group(2).split()
        if block.startswith("PRIORS") and rhs and rhs[0].lower() in ("gaussian", "gauss", "normal") and len(rhs) >= 3:
            out.setdefault(name, {})["gaussian_sigma"] = float(rhs[2])
        elif block.startswith("PRIORS") and rhs and rhs[0].lower() == "uniform" and len(rhs) >= 3:
            out.setdefault(name, {})["uniform"] = (float(rhs[1]), float(rhs[2]))
        elif block.startswith("VALUES") and len(rhs) == 3:
            try:
                lo, _, hi = (float(x) for x in rhs)
            except ValueError:
                continue
            out.setdefault(name, {})["range"] = (lo, hi)
    for v in out.values():           # a priors.ini uniform prior narrows the values.ini range
        if "uniform" in v and "range" in v:
            v["range"] = (max(v["range"][0], v["uniform"][0]), min(v["range"][1], v["uniform"][1]))
    return out


def _support_names(names):
    """README 2.2: Omega_m and the amplitude parameter only."""
    keep = []
    for n in names:
        short = n.split("--")[-1].lower()
        if short in ("omega_m", "omegam") or short in AMPLITUDE:
            keep.append(n)
    return sorted(keep)


def _fetch(ctx, P, key):
    name = P["chains"][key]
    kw = {"max_bytes": P["max_bytes_32pt"]} if name == P["chains"]["des_3x2pt"] else {}
    return ctx.http(BASE + name, label=f"DES Y6 chain {name}", **kw)


def main(ctx):
    P = dict(PARAMS)
    paths, formats, maps, status = {}, {}, {}, {}
    for key in ("des_3x2pt", "cmb", "des_xipm"):
        paths[key] = _fetch(ctx, P, key)
        formats[key] = s8diff.read_format(paths[key])
        maps[key], status[key] = s8diff.column_map(formats[key], key, key in P["positional_ok"])
        ctx.log(f"step A {key}: {formats[key]['ncols']} cols, {formats[key]['nrows']} rows, "
                f"header {'yes' if formats[key]['header'] else 'no'}, sampler {formats[key]['sampler']}; {status[key]}")
    def _status(k):
        return status[k] if not formats[k]["ragged_rows"] else f"{status[k]}, but {formats[k]['ragged_rows']} ragged rows: not loaded"

    formats_out = {k: {**{kk: vv for kk, vv in f.items() if kk != "prior_lines"}, "column_map": maps[k],
                       "status": _status(k)} for k, f in formats.items()}
    ctx.save("formats", formats_out)
    if P["step_a_only"]:
        return {"step": "A"}

    chains, info = {}, {}

    def load(key):
        if maps[key] is None or formats[key]["ragged_rows"]:
            return None
        burn, why = s8diff.burn_in_fraction(formats[key]["sampler"], P["mcmc_burn"])
        c, inf = s8diff.load_chain(paths[key], maps[key], burn)
        inf.update({"burn_in": burn, "burn_reason": why, "ess_flag": inf["ess"] < P["ess_flag"]})
        chains[key], info[key] = c, inf
        return c

    for key in ("des_3x2pt", "cmb", "des_xipm"):
        load(key)

    # ---------------------------------------------------------------- R1 ----
    def r1_one(key, pub):
        c = chains.get(key)
        if c is None:
            return {"status": f"not evaluable ({status.get(key)}; ragged rows {formats[key]['ragged_rows']})"}
        iv = s8diff.interval_around_mean(c["s8"], c["w"], P["mass"], P["n_grid"])
        mean_ok = abs(iv["mean"] - pub[0]) <= P["tol_mean"]
        end_ok = (abs(iv["hi"] - (pub[0] + pub[1])) <= P["tol_end"]
                  and abs(iv["lo"] - (pub[0] - pub[2])) <= P["tol_end"])
        return {**iv, "published": pub, "mean_ok": mean_ok, "ends_ok": end_ok,
                "verdict": "reproduced" if (mean_ok and end_ok) else "not reproduced",
                "omega_m_mean": s8diff.wmean(c["omega_m"], c["w"]), "chain": info[key]}

    r1 = {k: r1_one(k, P["published"][k]) for k in ("cmb", "des_3x2pt", "des_xipm")}
    xi_key = "des_xipm"
    if not r1["des_xipm"].get("mean_ok"):
        paths["des_xipm_nla"] = _fetch(ctx, P, "des_xipm_nla")
        formats["des_xipm_nla"] = s8diff.read_format(paths["des_xipm_nla"])
        maps["des_xipm_nla"], status["des_xipm_nla"] = s8diff.column_map(
            formats["des_xipm_nla"], "des_xipm_nla", "des_xipm_nla" in P["positional_ok"])
        formats_out["des_xipm_nla"] = {**{kk: vv for kk, vv in formats["des_xipm_nla"].items() if kk != "prior_lines"},
                                       "column_map": maps["des_xipm_nla"], "status": _status("des_xipm_nla")}
        ctx.save("formats", formats_out)
        load("des_xipm_nla")
        r1["des_xipm_nla"] = r1_one("des_xipm_nla", P["published"]["des_xipm_nla"])
        xi_key = "des_xipm_nla" if r1["des_xipm_nla"].get("mean_ok") else None
    r1["r3_chain"] = xi_key
    for k, v in r1.items():
        if isinstance(v, dict) and "mean" in v:
            ctx.log(f"R1 {k}: mean {v['mean']:.4f} [{v['lo']:.4f}, {v['hi']:.4f}] -> {v['verdict']}")
    ctx.save("r1", r1)

    # ---------------------------------------------------------------- R2 ----
    gate = r1["cmb"].get("mean_ok") and r1["des_3x2pt"].get("mean_ok")
    des, cmb = chains.get("des_3x2pt"), chains.get("cmb")

    def vec(c, d, shift=0.0):
        s8 = c["s8"] + shift
        return s8[:, None] if d == 1 else np.column_stack([s8, c["omega_m"]])

    # prior support from '##' lines: Omega_m and the amplitude parameter only (README 2.2)
    priors = {k: _parse_priors(formats[k]["prior_lines"]) for k in ("des_3x2pt", "cmb")}
    ranges = {k: {n: v["range"] for n, v in priors[k].items() if "range" in v} for k in priors}
    support = {"status": "not performed (no prior ranges in either header)"}
    names = _support_names(set(ranges["des_3x2pt"]) | set(ranges["cmb"]))
    if names and des is not None and cmb is not None:
        support = {"status": "performed", "parameters": {}, "rule": "weight of each chain outside the other "
                   "chain's prior range, where that range is given"}
        bad = False
        for name in names:
            fr = {}
            for a, b in (("des_3x2pt", "cmb"), ("cmb", "des_3x2pt")):
                hdr = formats[a]["header"]
                low = [h.lower() for h in hdr] if hdr else []
                if name not in ranges[b] or name not in low:
                    fr[f"{a}_outside_{b}"] = None
                    continue
                x = chains[a]["data"][:, low.index(name)]
                lo, hi = ranges[b][name]
                fr[f"{a}_outside_{b}"] = float(np.sum(chains[a]["w"][(x < lo) | (x > hi)]))
            support["parameters"][name] = fr
            bad = bad or any(v is not None and v > P["support_frac_max"] for v in fr.values())
        support["fails"] = bad
        support["other_shared_ranges"] = sorted((set(ranges["des_3x2pt"]) & set(ranges["cmb"])) - set(names))
    amp = [n for n in names if n.split("--")[-1] in AMPLITUDE]
    support["amplitude_name"] = amp if amp else "none found"

    r2 = {"gate_r1_means": bool(gate), "support": support}
    if des is not None and cmb is not None:
        for d, tag in ((1, "1d"), (2, "2d")):
            base = s8diff.parameter_difference(vec(des, d), des["w"], vec(cmb, d), cmb["w"], P["n_pairs"], P["seeds"])
            variants_full = {f"bw_x{bw}": s8diff.parameter_difference(vec(des, d), des["w"], vec(cmb, d), cmb["w"],
                                                                      P["n_pairs"], P["seeds"], bw_factor=bw)
                             for bw in P["bw_variants"]}
            variants = {k: v["n_sigma"] for k, v in variants_full.items()}
            pub = P["published_nsigma"][tag]
            ok = abs(base["n_sigma"] - pub) <= P["tol_nsigma"] + 2 * base["s"]
            if not gate:
                verdict = "not evaluable (R1 gate)"
            elif base["s"] > P["s_max"]:
                verdict = "not evaluable (s > s_max)"
            elif support.get("fails"):
                verdict = "not evaluable (prior support); descriptive"
            else:
                verdict = "reproduced" if ok else "not reproduced"
            flag = any(abs(v - base["n_sigma"]) > P["bw_flag"] for v in variants.values())
            r2[tag] = {**base, "published": pub, "bandwidth_variants": variants,
                       "bandwidth_variant_diagnostics": {k: v["diagnostics"] for k, v in variants_full.items()},
                       "cell_flag_any": base["cell_flag"] or any(v["cell_flag"] for v in variants_full.values()),
                       "bandwidth_dependent": flag, "within_tolerance": bool(ok), "verdict": verdict}
            ctx.log(f"R2 {tag}: n_sigma {base['n_sigma']:.3f} (s {base['s']:.4f}) vs {pub} -> {verdict}")
        r2["1d"]["convolution_check"] = s8diff.convolution_check(des["s8"], des["w"], cmb["s8"], cmb["w"], P["conv_spacing"])
        r2["1d"]["convolution_check"]["note"] = "cross-check only; not used for the bandwidth flag"
        ms = {k: (s8diff.wmean(c["s8"], c["w"]), s8diff.wstd(c["s8"], c["w"])) for k, c in (("des", des), ("cmb", cmb))}
        r2["gaussian_means"] = s8diff.gaussian_estimate(ms["des"][0], ms["des"][1], ms["cmb"][0], ms["cmb"][1])
        r2["gaussian_modes"] = s8diff.gaussian_estimate(r1["des_3x2pt"]["kde_mode"], ms["des"][1],
                                                        r1["cmb"]["kde_mode"], ms["cmb"][1])
        # sensitivity: truncation to the overlap of the sampled Omega_m ranges
        lo = max(des["omega_m"].min(), cmb["omega_m"].min()); hi = min(des["omega_m"].max(), cmb["omega_m"].max())
        sel_d = (des["omega_m"] >= lo) & (des["omega_m"] <= hi); sel_c = (cmb["omega_m"] >= lo) & (cmb["omega_m"] <= hi)
        trunc = {"omega_m_range": [float(lo), float(hi)], "dropped_des": float(np.sum(des["w"][~sel_d])),
                 "dropped_cmb": float(np.sum(cmb["w"][~sel_c]))}
        for d, tag in ((1, "1d"), (2, "2d")):
            trunc[tag] = s8diff.parameter_difference(vec(des, d)[sel_d], des["w"][sel_d], vec(cmb, d)[sel_c],
                                                     cmb["w"][sel_c], P["n_pairs"], P["seeds"][:1])["n_sigma"]
        r2["truncated_sensitivity"] = trunc
    ctx.save("r2", r2)

    # ---------------------------------------------------------------- R3 ----
    r3 = {"chain": xi_key}
    if xi_key and cmb is not None:
        xi = chains[xi_key]
        for d, tag in ((1, "1d"), (2, "2d")):
            r3[tag] = s8diff.parameter_difference(vec(xi, d), xi["w"], vec(cmb, d), cmb["w"], P["n_pairs"], P["seeds"])
        ctx.log(f"R3 ({xi_key}): 1d {r3['1d']['n_sigma']:.3f}, 2d {r3['2d']['n_sigma']:.3f}")
    ctx.save("r3", r3)

    # ---------------------------------------------------------------- R4 ----
    r4 = {}
    if des is not None and cmb is not None:
        for name, sh in (("projection_shift", P["proj_shift"]), ("map_shift", P["map_shift"])):
            r4[name] = {"shift": sh, **s8diff.parameter_difference(vec(des, 1, sh), des["w"], vec(cmb, 1), cmb["w"],
                                                                   P["n_pairs"], P["seeds"])}
        rng = np.random.default_rng(P["seeds"][0])
        dp = s8diff.draw_pairs(vec(des, 1), des["w"], vec(cmb, 1), cmb["w"], P["n_pairs"], rng)
        r4["algorithms_1d"] = {"iso_density": r2["1d"]["n_sigma"], "equal_tail": s8diff.equal_tail(dp),
                               "gaussian": r2["gaussian_means"]}
        r4["threshold"] = {tag: {"n_sigma": r2[tag]["n_sigma"], "below_3": r2[tag]["n_sigma"] < 3}
                           for tag in ("1d", "2d")}
        # full space (Gaussian) over shared sampled parameters
        hd, hc = formats["des_3x2pt"]["header"], formats["cmb"]["header"]
        fs = {"status": "no headers"}
        if hd and hc:
            low_d, low_c = [h.lower() for h in hd], [h.lower() for h in hc]
            def sampled(key, low):
                # README 2.4: sampled = has a '##' prior range, or a non-derived cosmological_parameters column
                by_range = {n for n in ranges[key] if n.startswith("cosmological_parameters--")}
                by_name = {n for n in low if n.startswith("cosmological_parameters--")
                           and n.split("--")[-1] not in DERIVED}
                return (by_range | by_name) & set(low)

            cand = sorted(sampled("des_3x2pt", low_d) & sampled("cmb", low_c))
            xa = np.column_stack([des["data"][:, low_d.index(n)] for n in cand]) if cand else None
            xb = np.column_stack([cmb["data"][:, low_c.index(n)] for n in cand]) if cand else None
            has_om = any(n.split("--")[-1] in ("omega_m", "omegam") for n in cand)
            if xa is None or len(cand) < 2 or not has_om:
                fs = {"status": "chains share no sampled parameter beyond Omega_m (or Omega_m is not sampled in both)",
                      "candidates": cand}
            else:
                keep = []
                for i in range(len(cand)):
                    if all(abs(np.cov(xa[:, [i, j]].T, aweights=des["w"])[0, 1]
                               / np.sqrt(np.cov(xa[:, i], aweights=des["w"]) * np.cov(xa[:, j], aweights=des["w"])))
                           <= P["corr_max"] for j in keep):
                        keep.append(i)
                names = [cand[i] for i in keep]
                fs = {"parameters": names,
                      "all": s8diff.full_space_gaussian(xa[:, keep], des["w"], xb[:, keep], cmb["w"], P["max_cond"])}
                if ranges["des_3x2pt"]:
                    con = []
                    for i, n in zip(keep, names):
                        pr = priors["des_3x2pt"].get(n, {})
                        if "gaussian_sigma" in pr:
                            var_prior = pr["gaussian_sigma"] ** 2
                        elif "range" in pr:
                            lo, hi = pr["range"]
                            var_prior = (hi - lo) ** 2 / 12.0
                        else:
                            continue
                        if s8diff.wstd(xa[:, i], des["w"]) ** 2 < P["constrained_ratio"] * var_prior:
                            con.append(i)
                    fs["constrained_parameters"] = [cand[i] for i in con]
                    fs["constrained"] = (s8diff.full_space_gaussian(xa[:, con], des["w"], xb[:, con], cmb["w"], P["max_cond"])
                                         if con else {"status": "no data-constrained parameter"})
                else:
                    fs["constrained"] = {"status": "no prior ranges"}
        r4["full_space"] = fs
    ctx.save("r4", r4)

    # ---------------------------------------------------------------- R5 ----
    r5 = {}
    if cmb is not None:
        for name, (m, sp, sm, ref) in P["probes"].items():
            vals = []
            for seed in P["seeds"]:
                rng = np.random.default_rng(seed)
                x = s8diff.split_normal_draws(m, sp, sm, P["n_probe"], rng)
                ib = rng.choice(len(cmb["w"]), size=P["n_probe"], replace=True, p=cmb["w"])
                vals.append(s8diff.nsigma_binned((x - cmb["s8"][ib])[:, None])["n_sigma"])
            r5[name] = {"mean": m, "sigma_plus": sp, "sigma_minus": sm, "reference": ref,
                        "n_sigma": float(np.mean(vals)), "s": float(np.std(vals, ddof=1))}
    ctx.save("r5", r5)

    return {"r1": {k: v.get("verdict") for k, v in r1.items() if isinstance(v, dict)},
            "r2": {t: r2[t]["verdict"] for t in ("1d", "2d") if t in r2},
            "r2_nsigma": {t: r2[t]["n_sigma"] for t in ("1d", "2d") if t in r2},
            "r3_nsigma": {t: r3[t]["n_sigma"] for t in ("1d", "2d") if t in r3}}
