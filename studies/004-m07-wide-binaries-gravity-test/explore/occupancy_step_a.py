"""Velocity-free bin occupancy after step A (README section 3; plan 013): applies the section 4.5
cuts that need no velocity column (degrouping, distance, r_sky, RUWE, HR band with the step-A HR
constant c), computes x = r_sky / r_M from velocity-free masses, and counts pairs per x bin with the
pre-registered edges and symmetric outer merging. No velocity column is fetched or used (step A
tables only, all cache hits). These counts are upper bounds: the radial-velocity, sigma(v~) and
v~ cuts of step B can only remove pairs.

Run: python -m astrolab explore 004 --tag occupancy --script explore/occupancy_step_a.py
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

import run
import wb


def main(ctx):
    P = dict(run.PARAMS)
    sa = json.loads((Path(run.__file__).parent / "results" / "step_a.json").read_text(encoding="utf-8"))
    c = sa["hr_constant"]["c"]
    free = run.Budget(float("inf"))
    a1s, a2s, a3s = [], [], []
    for name, r, near in run._regions(P):
        a1s.append(run._a1(ctx, P, name, r, near, free)[1])
        a2s.append(run._a2(ctx, P, name, r, near, "neighbour", free)[1])
        a3s.append(run._a3(ctx, P, name, r, near, free)[1])
    a1 = pd.concat(a1s, ignore_index=True)
    a2 = pd.concat(a2s, ignore_index=True)
    a3 = pd.concat(a3s, ignore_index=True)
    keep = wb.canonical_pairs(a1["source_id_a"].to_numpy(), a1["source_id_b"].to_numpy())
    df = a1.iloc[keep].reset_index(drop=True)
    trace = {"pairs": int(len(df))}

    if a2["source_id"].duplicated().any():
        raise RuntimeError("A2 has duplicate source_id rows; stop (as build_sample)")
    nb = {int(s): (int(n), int(f)) for s, n, f in zip(a2["source_id"], a2["n"], a2["first_neighbour"])}

    def single(sid, partner):
        v = nb.get(int(sid))
        return v is not None and v[0] == 1 and v[1] == int(partner)
    df = df[np.array([single(a, b) and single(b, a) for a, b in zip(df["source_id_a"], df["source_id_b"])], bool)]
    trace["degroup"] = int(len(df))
    pbar, _, _ = wb.weighted_parallax(df["parallax_a"].to_numpy(), df["parallax_error_a"].to_numpy(),
                                      df["parallax_b"].to_numpy(), df["parallax_error_b"].to_numpy())
    df = df.assign(pbar=pbar)
    df = df[df["pbar"] > 1000.0 / P["d_max_pc"]]
    trace["distance"] = int(len(df))
    rsky = wb.sky_separation_au(df["ra_a"].to_numpy(), df["dec_a"].to_numpy(), df["ra_b"].to_numpy(),
                                df["dec_b"].to_numpy(), df["pbar"].to_numpy())
    df = df.assign(rsky=np.asarray(rsky))
    df = df[(df["rsky"] >= P["rsky_min_au"]) & (df["rsky"] <= P["rsky_max_au"])]
    trace["r_sky"] = int(len(df))
    df = df[(df["ruwe_a"] < P["ruwe_max"]) & (df["ruwe_b"] < P["ruwe_max"])]
    trace["ruwe"] = int(len(df))
    for s in ("a", "b"):
        x = df[f"bp_rp_{s}"]
        mg = df[f"phot_g_mean_mag_{s}"] + 5 * np.log10(df["pbar"] / 100.0)
        df = df[(x > 0.5) & (x < 3.5) & (mg > 4) & (mg < 14) & (mg > 3.3 * x + c) & (mg < 3.3 * x + c + 0.8)]
    trace["hr"] = int(len(df))
    flame = (a3.drop_duplicates("source_id").set_index("source_id")["mass_flame"]
             if len(a3) else pd.Series(dtype=float))

    def mass(s):
        m_lum = wb.mass_from_mg(df[f"phot_g_mean_mag_{s}"] + 5 * np.log10(df["pbar"] / 100.0), P["mg_sun"])
        f = df[f"source_id_{s}"].map(flame)
        return np.where(f.notna(), f, m_lum)
    M = mass("a") + mass("b")
    x = df["rsky"].to_numpy() / wb.r_mond_au(M, P["a0"])
    b = wb.bin_index(x, P["edges"])
    counts = [int(np.sum(b == k)) for k in range(len(P["edges"]) + 1)]
    mapping, evaluable = wb.merge_outer(counts, P["min_per_bin"])
    final = {}
    for old, new in enumerate(mapping):
        final[new] = final.get(new, 0) + counts[old]
    out = {"hr_c": c, "trace": trace, "edges": P["edges"], "counts_velocity_free": counts,
           "merge_mapping": [int(m) for m in mapping], "final_counts": [final[k] for k in sorted(final)],
           "evaluable_upper_bound": bool(evaluable),
           "note": "velocity-free upper bounds; step B's RV, sigma(v~) and v~ cuts remove further pairs"}
    ctx.save("occupancy", out)
    ctx.log(f"velocity-free counts per x bin: {counts}; merged {out['final_counts']}; evaluable {evaluable}")
    return out
