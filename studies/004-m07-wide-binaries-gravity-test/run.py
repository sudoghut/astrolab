"""M7: wide binaries, Newton or MOND at low acceleration (pre-registration: README sections 1-4).

Run with:      python -m astrolab run 004-m07-wide-binaries-gravity-test
Explore with:  python -m astrolab explore 004-m07-wide-binaries-gravity-test --tag <topic> --set KEY=VALUE

Steps (README section 3, two-step fetch for blinding):
  A  velocity-free: per region, count then fetch candidate pairs (A1) and neighbour counts (A2);
     saves only counts, byte estimates and the HR-band constant c (results/step_a.json).
  B  after the dated pre-registration commit: velocities for the pairs (B1), then the analysis.
"""
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd

import queries as Q
import wb

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    "step": "A",                       # "A" (velocity-free) or "B" (after the pre-registration commit)
    "parent": "parallax > 6.6667 AND parallax_over_error > 40",
    "neighbour": ("parallax_over_error > 40 AND phot_g_mean_flux_over_error > 5"
                  " AND parallax + 3 * parallax_error > 6.6667"),
    "neighbour_relaxed": ("parallax_over_error > 5 AND phot_g_mean_flux_over_error > 5"
                          " AND parallax + 3 * parallax_error > 6.6667"),
    "near_plx": 34.0, "near_b": "parallax + 3 * parallax_error > 28",
    "vcap_kms": 15.0,
    "max_rows": 50000,
    "bytes_per_row_pair": 400, "bytes_per_row_count": 40,
    "budget_bytes": 200 * 1024 ** 2,
    "workers": 4,
    "region_limit": None,              # exploration only: run the first N regions
}


def _count(ctx, q, label):
    df = ctx.tap(q, "gaia", label=f"count {label}", max_rows=2, mode="async", release="Gaia DR3")
    return int(df["n"].iloc[0])


def _regions(P):
    plan = wb.strip_plan()
    regs = [("r%03d" % k, r, False) for k, r in enumerate(plan)]
    regs.append(("near", dict(ra0=0.0, ra1=360.0, dec0=-90.0, dec1=90.0, bra0=0.0, bra1=360.0,
                              bdec0=-90.0, bdec1=90.0), True))
    if P["region_limit"]:
        regs = regs[: int(P["region_limit"])]
    return regs


class Budget:
    """Cumulative byte estimate shared by the worker threads; checked BEFORE each fetch."""

    def __init__(self, limit):
        self.limit, self.used, self.lock = limit, 0, threading.Lock()

    def reserve(self, nbytes, what):
        with self.lock:
            if self.used + nbytes > self.limit:
                raise RuntimeError(f"{what}: cumulative estimate {(self.used + nbytes) / 1e6:.1f} MB exceeds "
                                   "the study budget; stop and ask the user (README section 3)")
            self.used += nbytes


def _a1(ctx, P, name, r, near, budget):
    parent = P["parent"]
    qc = Q.pair_query(r, parent, P["vcap_kms"], "COUNT(*) AS n", near=near) if not near else \
        Q.pair_query(r, parent, P["vcap_kms"], "COUNT(*) AS n", near=True).replace(
            f"FROM gaiadr3.gaia_source WHERE {parent}) AS b",
            f"FROM gaiadr3.gaia_source WHERE {parent} AND {P['near_b']}) AS b")
    n = _count(ctx, qc, f"A1 {name}")
    if n >= P["max_rows"]:
        raise RuntimeError(f"A1 {name}: {n} rows >= {P['max_rows']}; split this region (README section 3)")
    budget.reserve(n * P["bytes_per_row_pair"], f"A1 {name}")
    q = qc.replace("SELECT COUNT(*) AS n", "SELECT " + Q.a1_select(), 1)
    df = ctx.tap(q, "gaia", label=f"A1 {name}", max_rows=P["max_rows"], mode="async", release="Gaia DR3")
    return n, df


def _a2(ctx, P, name, r, near, neighbour_key, budget):
    nb = P[neighbour_key]
    if near:
        nb = f"{nb} AND {P['near_b']}"
    qc = Q.neighbour_query(r, P["parent"], nb, "count", near=near)
    n = _count(ctx, qc, f"A2 {name}")
    if n >= P["max_rows"]:
        raise RuntimeError(f"A2 {name}: {n} rows >= {P['max_rows']}; split this region (README section 3)")
    budget.reserve(n * P["bytes_per_row_count"], f"A2 {name}")
    q = Q.neighbour_query(r, P["parent"], nb, "rows", near=near)
    df = ctx.tap(q, "gaia", label=f"A2 {name}", max_rows=P["max_rows"], mode="async", release="Gaia DR3")
    return n, df


def step_a(ctx, P):
    regs = _regions(P)
    t0 = time.time()
    counts = {}
    budget = Budget(P["budget_bytes"])

    def one(item):
        name, r, near = item
        n1, d1 = _a1(ctx, P, name, r, near, budget)
        n2, d2 = _a2(ctx, P, name, r, near, "neighbour", budget)
        return name, n1, d1, n2, d2

    a1_parts, a2_parts = [], []
    with ThreadPoolExecutor(max_workers=int(P["workers"])) as ex:
        for name, n1, d1, n2, d2 in ex.map(one, regs):
            counts[name] = {"A1": n1, "A2": n2}
            a1_parts.append(d1)
            a2_parts.append(d2)
    a1 = pd.concat(a1_parts, ignore_index=True) if a1_parts else pd.DataFrame()
    a2 = pd.concat(a2_parts, ignore_index=True) if a2_parts else pd.DataFrame()
    if len(a1):
        keep = wb.canonical_pairs(a1["source_id_a"].to_numpy(), a1["source_id_b"].to_numpy())
        a1 = a1.iloc[keep].reset_index(drop=True)
    c_band = hr_constant(a1)
    out = {"step": "A", "regions": len(regs), "n_pairs_a1": int(len(a1)), "n_stars_a2": int(len(a2)),
           "est_bytes": int(budget.used), "hr_constant": c_band, "seconds": time.time() - t0,
           "counts_per_region": counts}
    ctx.save("step_a", out)
    return out


def hr_constant(a1):
    """README section 4.5: c from deduplicated A1 stars (own parallax), velocity-free."""
    if not len(a1):
        return {"c": None, "n": 0, "window": None}
    rows = []
    for s in ("a", "b"):
        rows.append(pd.DataFrame({"source_id": a1[f"source_id_{s}"], "parallax": a1[f"parallax_{s}"],
                                  "g": a1[f"phot_g_mean_mag_{s}"], "bp_rp": a1[f"bp_rp_{s}"],
                                  "ruwe": a1[f"ruwe_{s}"]}))
    st = pd.concat(rows).drop_duplicates("source_id")
    st = st[st["bp_rp"].notna() & (st["ruwe"] < 1.25) & (st["parallax"] > 7.6923)]
    mg = st["g"] + 5 * np.log10(st["parallax"] / 100.0)
    for w in (0.05, 0.15):
        sel = (st["bp_rp"] - 1.8).abs() < w
        if int(sel.sum()) >= 30:
            c = float(np.median(mg[sel] - 3.3 * st["bp_rp"][sel]) - 0.4)
            return {"c": c, "n": int(sel.sum()), "window": w}
    return {"c": None, "n": int(((st["bp_rp"] - 1.8).abs() < 0.15).sum()), "window": None}


def main(ctx):
    P = dict(PARAMS)
    if P["step"] == "A":
        out = step_a(ctx, P)
        ctx.log(f"step A: {out['n_pairs_a1']} candidate pairs, {out['n_stars_a2']} stars with neighbours, "
                f"est {out['est_bytes'] / 1e6:.1f} MB, c = {out['hr_constant']}")
        ctx.save("summary", {"params": P, "step_a": {k: v for k, v in out.items() if k != "counts_per_region"}})
        return out
    raise RuntimeError("step B is implemented only after the pre-registration commit (README section 3)")
