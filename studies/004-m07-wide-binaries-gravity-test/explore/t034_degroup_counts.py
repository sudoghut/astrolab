"""T-034, velocity-free and cache-only (README section 2.1). Counts pairs per x bin at d < 130 pc
or < 150 pc (D_MAX) with r_sky >= 300 AU, both stars with an available RV (rv_method_used not null),
the RUWE cut and the HR band. Three degrouping rules are compared: none; relaxed neighbours (A2);
and approximate C25 neighbours (other parent stars within 100 kAU and 3 sigma, taken from the
cached A1). No velocity column is read. It stops on any cache miss and never queries the archive.

Run: python -m astrolab explore 004 --tag t034-degroup --script explore/t034_degroup_counts.py
"""
import numpy as np
import pandas as pd

import run
import wb

D_LIST, RSKY_MIN = (130.0, 150.0), 300.0


class CacheOnly:
    """Wraps ctx: every TAP query must already be in the cache (no network)."""

    def __init__(self, ctx):
        from astrolab import cache, fetch
        from astrolab.services import tap_url
        self.ctx, self.cache, self.fetch, self.url = ctx, cache, fetch, tap_url("gaia")

    def tap(self, q, service, label=None, **kw):
        key = self.cache.key_for("tap", {"url": self.url, "adql": self.fetch._normalize_adql(q)})
        if self.cache.get(key, ".parquet") is None:
            raise RuntimeError(f"cache miss for {label}; stop (this script never queries the archive)")
        return self.ctx.tap(q, service, label=label, **kw)

    def log(self, m):
        self.ctx.log(m)


def main(ctx):
    P = dict(run.PARAMS)
    co, free = CacheOnly(ctx), run.Budget(float("inf"))
    a1s, a2s, a3s = [], [], []
    for name, r, near in run._regions(P):
        a1s.append(run._a1(co, P, name, r, near, free)[1])
        a2s.append(run._a2(co, P, name, r, near, "neighbour", free)[1])
        a3s.append(run._a3(co, P, name, r, near, free)[1])
    a1 = pd.concat(a1s, ignore_index=True)
    a2 = pd.concat(a2s, ignore_index=True)
    a3 = pd.concat(a3s, ignore_index=True)
    a1 = a1.iloc[wb.canonical_pairs(a1["source_id_a"].to_numpy(), a1["source_id_b"].to_numpy())].reset_index(drop=True)
    pb, _, _ = wb.weighted_parallax(a1["parallax_a"].values, a1["parallax_error_a"].values,
                                    a1["parallax_b"].values, a1["parallax_error_b"].values)
    a1 = a1.assign(pbar=pb, rsky=wb.sky_separation_au(a1["ra_a"].values, a1["dec_a"].values,
                                                      a1["ra_b"].values, a1["dec_b"].values, pb))
    links = a1[a1["rsky"] <= 100000.0]
    deg = pd.concat([links["source_id_a"], links["source_id_b"]]).value_counts()
    nb = {int(s): (int(n), int(f)) for s, n, f in zip(a2["source_id"], a2["n"], a2["first_neighbour"])}
    flame = a3.drop_duplicates("source_id").set_index("source_id")["mass_flame"]
    out = {}
    for dmax in D_LIST:
        df = a1[(a1["pbar"] > 1000.0 / dmax) & (a1["rsky"] >= RSKY_MIN) & (a1["rsky"] <= P["rsky_max_au"])
                & a1["rv_method_used_a"].notna() & a1["rv_method_used_b"].notna()
                & (a1["ruwe_a"] < P["ruwe_max"]) & (a1["ruwe_b"] < P["ruwe_max"])]
        c = P["hr_c"]
        for s in ("a", "b"):
            x = df[f"bp_rp_{s}"]
            mg = df[f"phot_g_mean_mag_{s}"] + 5 * np.log10(df["pbar"] / 100.0)
            df = df[(x > 0.5) & (x < 3.5) & (mg > 4) & (mg < 14) & (mg > 3.3 * x + c) & (mg < 3.3 * x + c + 0.8)]

        def mass(s):
            m = wb.mass_from_mg(df[f"phot_g_mean_mag_{s}"] + 5 * np.log10(df["pbar"] / 100.0), P["mg_sun"])
            f = df[f"source_id_{s}"].map(flame)
            return np.where(f.notna(), f, m)
        b = wb.bin_index(df["rsky"].values / wb.r_mond_au(mass("a") + mass("b"), P["a0"]), P["edges"])

        def single(sid, partner):
            v = nb.get(int(sid))
            return v is not None and v[0] == 1 and v[1] == int(partner)
        ids = list(zip(df["source_id_a"], df["source_id_b"]))
        rel = np.array([single(p, q) and single(q, p) for p, q in ids], bool)
        c25 = np.array([deg.get(p, 0) == 1 and deg.get(q, 0) == 1 for p, q in ids], bool)
        cnt = lambda m: [int(np.sum(m & (b == k))) for k in range(len(P["edges"]) + 1)]
        out[f"d{dmax:g}"] = {"none": cnt(np.ones(len(df), bool)), "relaxed": cnt(rel), "c25_approx": cnt(c25)}
        ctx.log(f"d < {dmax:g} pc: {out[f'd{dmax:g}']}")
    ctx.save("t034_degroup_counts", out)
    return out
