"""Loading and load-time checks L1-L7 of study 012 (README section 3), and T1 (README 4.2).

Every tunable arrives as an argument (run.py passes PARAMS values); this module never imports run.
"""
from __future__ import annotations

import hashlib
import math
import re
from pathlib import Path

import numpy as np
import pandas as pd


class StopRun(Exception):
    """A load check that the pre-registration says must stop the run (README sections 2 and 3)."""


# ---------------------------------------------------------------------------------------------
# L1 checksums

def md5_of(path, chunk=1 << 22) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def check_md5(paths: dict, expected: dict) -> dict:
    out = {}
    for name, p in paths.items():
        got = md5_of(p)
        out[name] = {"md5": got, "expected": expected[name], "match": got == expected[name]}
    out["passed"] = all(v["match"] for k, v in out.items() if isinstance(v, dict))
    return out


# ---------------------------------------------------------------------------------------------
# L2 column mapping by name. The candidate names were fixed before any data file was read
# (README 4.13 item 1). A column name is normalised to lower-case letters and digits only
# ("[M/H]" -> "mh", "phot_g_mean_mag" -> "photgmeanmag").

MH_CANDIDATES = {
    "source_id": {"sourceid", "gaiasourceid", "gaiadr3sourceid", "dr3sourceid"},
    "mh": {"mh", "mhxgboost", "mhxgb", "xgbmh", "xgboostmh", "mhpred", "mhxp", "metallicity", "feh"},
    "mh_err": {"mherr", "emh", "mherror", "sigmamh", "mhsigma", "mhuncertainty", "mhstd", "mherrxgboost"},
    "teff": {"teff", "teffxgboost", "teffxgb", "xgbteff", "xgboostteff", "teffpred"},
    "logg": {"logg", "loggxgboost", "loggxgb", "xgblogg", "xgboostlogg", "loggpred"},
    "l": {"l", "glon", "gall", "lgal", "galacticl"},
    "b": {"b", "glat", "galb", "bgal", "galacticb"},
    "ra": {"ra"},
    "dec": {"dec"},
    "parallax": {"parallax", "plx", "parallaxmas"},
    "parallax_error": {"parallaxerror", "parallaxerr", "plxerr", "eparallax", "eplx", "parallaxsigma"},
    "g": {"photgmeanmag", "g", "gmag", "gmeanmag", "photg"},
    "bp_rp": {"bprp", "bpminusrp"},
    "bp": {"photbpmeanmag", "bp", "bpmag", "gbp", "bpmeanmag", "photbp"},
}
KIN_CANDIDATES = {
    "source_id": MH_CANDIDATES["source_id"],
    "jr": {"jr", "actr", "actionr", "jrkpckms"},
    "jphi": {"jphi", "lz", "actphi", "actionphi", "jphikpckms"},
    "jz": {"jz", "actz", "actionz", "jzkpckms"},
    "ecc": {"ecc", "e", "eccentricity"},
    "rapo": {"rapo", "apo", "apocenter", "apocentre", "rmax", "apocenterradius"},
    "x": {"x", "xgc", "xgal", "galcenx"},
    "y": {"y", "ygc", "ygal", "galceny"},
    "z": {"z", "zgc", "zgal", "galcenz"},
    "vx": {"vx", "vxgc", "vxgal", "galcenvx"},
    "vy": {"vy", "vygc", "vygal", "galcenvy"},
    "vz": {"vz", "vzgc", "vzgal", "galcenvz"},
    "vphi": {"vphi", "vphigc"},
    "ra": {"ra"},
    "dec": {"dec"},
    "parallax": MH_CANDIDATES["parallax"],
    "pmra": {"pmra"},
    "pmdec": {"pmdec"},
    "rv": {"radialvelocity", "rv", "vrad", "vlos", "dr3radialvelocity"},
}
MH_REQUIRED = ("source_id", "mh")
KIN_REQUIRED = ("source_id",)


def norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def map_columns(columns, candidates, required, which=""):
    """README 3 L2: map columns by name; several candidates for one quantity, or a missing required
    quantity, stop the run. Returns {quantity: column or None}."""
    by_norm = {}
    for c in columns:
        by_norm.setdefault(norm(c), []).append(c)
    mapping, ambiguous = {}, {}
    for q, names in candidates.items():
        hits = [c for n in sorted(names) for c in by_norm.get(n, [])]
        if len(hits) > 1:
            ambiguous[q] = hits
        mapping[q] = hits[0] if len(hits) == 1 else None
    if ambiguous:
        raise StopRun(f"L2 {which}: several columns are candidates for one quantity {ambiguous}; fix the "
                      "mapping by dated amendment (README 3 L2)")
    missing = [q for q in required if mapping[q] is None]
    if missing:
        raise StopRun(f"L2 {which}: no column for {missing}; columns are {list(columns)} (README 3 L2: stop)")
    return mapping


def presence(mapping, quantities):
    return {q: mapping.get(q) is not None for q in quantities}


def read_mapped(path, mapping, dtype_id="int64"):
    cols = {v: k for k, v in mapping.items() if v is not None}
    df = pd.read_csv(path, usecols=list(cols))
    df = df.rename(columns=cols)
    df["source_id"] = df["source_id"].astype(dtype_id)
    return df


def add_galactic(df):
    """l, b from ra, dec when the file has no l, b (README 4.13 item 2); l wrapped to (-180, 180]."""
    if "l" not in df.columns and "ra" in df.columns and "dec" in df.columns:
        from astropy.coordinates import SkyCoord
        import astropy.units as u
        c = SkyCoord(ra=df["ra"].to_numpy(float) * u.deg, dec=df["dec"].to_numpy(float) * u.deg).galactic
        df["l"] = c.l.deg
        df["b"] = c.b.deg
    if "l" in df.columns:
        df["l"] = wrap_l(df["l"].to_numpy(float))
    return df


def wrap_l(l):
    l = np.mod(np.asarray(l, float), 360.0)
    return np.where(l > 180.0, l - 360.0, l)


# ---------------------------------------------------------------------------------------------
# L3 duplicates

def drop_duplicates(df, which, stop_frac=0.01):
    n = len(df)
    dup = df["source_id"].duplicated(keep=False)
    n_dup_ids = int(df.loc[dup, "source_id"].nunique())
    frac = n_dup_ids / max(df["source_id"].nunique(), 1)
    rec = {"rows": n, "duplicated_source_ids": n_dup_ids, "duplicated_fraction": frac,
           "rows_dropped": int(dup.sum())}
    if frac >= stop_frac:
        raise StopRun(f"L3 {which}: {frac:.2%} of source_ids are duplicated (>= 1%): stop (README section 2)")
    return df.loc[~dup].reset_index(drop=True), rec


# ---------------------------------------------------------------------------------------------
# L4 join

def join(kin, mh, cols=("mh",)):
    m = mh[["source_id", *cols]]
    j = kin.merge(m, on="source_id", how="inner")
    frac = len(j) / max(len(kin), 1)
    return j, {"kin_rows": len(kin), "matched": len(j), "fraction": frac,
               "note": "" if frac >= 0.99 else "below 99%: the join uses the matched rows (README 3 L4)"}


# ---------------------------------------------------------------------------------------------
# L5 units and signs

def check_units(joined, rapo_range=(2.0, 15.0)):
    """Among joined stars with [M/H] > -0.5: median J_phi > 0 (flip if negative, stop if 0) and median
    R_apo within 2-15 kpc (otherwise stop: the unit is fixed by dated amendment)."""
    sel = joined["mh"].to_numpy(float) > -0.5
    rec = {"n_metal_rich": int(sel.sum()), "jphi_flipped": False}
    if "jphi" in joined.columns:
        med = float(np.nanmedian(joined.loc[sel, "jphi"].to_numpy(float))) if sel.any() else float("nan")
        rec["median_jphi"] = med
        if med == 0 or not np.isfinite(med):
            raise StopRun(f"L5: median J_phi of the [M/H] > -0.5 stars is {med}: stop and amend")
        if med < 0:
            rec["jphi_flipped"] = True
    if "rapo" in joined.columns:
        med = float(np.nanmedian(joined.loc[sel, "rapo"].to_numpy(float))) if sel.any() else float("nan")
        rec["median_rapo"] = med
        if not (rapo_range[0] <= med <= rapo_range[1]):
            raise StopRun(f"L5: median R_apo {med} outside {rapo_range} kpc: identify its unit from the "
                          "header and record it by dated amendment before any test")
    return rec


# ---------------------------------------------------------------------------------------------
# L6 cuts between R22's query and the file

L6_SPECS = {
    # quantity: (lower and upper end of the range R22's query allows, bin width)
    "parallax": (-math.inf, 1.0, 0.01),
    "parallax_over_error": (-math.inf, math.inf, 0.1),
    "bp": (-math.inf, 15.5, 0.05),
    "bp_rp": (1.0, 3.5, 0.05),
    "l": (-30.0, 30.0, 0.5),
    "b": (-30.0, 30.0, 0.5),
}
PARALLAX_DEPENDENT = ("parallax", "parallax_over_error")


def detect_cuts(values, lo, hi, width, min_count=50):
    """README 3 L6: a cut at c is declared if, inside the range R22's query allows, the histogram falls
    from at least `min_count` stars per bin to 0 at c (and stays 0 to the end of the range: a hole
    is not a cut; README 4.13 item 3). Bins are aligned to multiples of `width`.
    Returns (cuts, record) with cuts a list of {"side": "upper"/"lower", "c": edge}."""
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    rec = {"n": int(v.size), "outside_query_range": int(np.sum((v <= lo) | (v >= hi)))}
    v = v[(v > lo) & (v < hi)]
    if v.size == 0:
        return [], rec
    a = math.floor(v.min() / width) * width - width
    z = math.ceil(v.max() / width) * width + width
    a = max(a, lo)
    z = min(z, hi)
    nb = int(round((z - a) / width))
    edges = a + width * np.arange(nb + 1)
    edges[-1] = z
    h, _ = np.histogram(v, bins=edges)
    cuts = []
    nz = np.nonzero(h)[0]
    first, last = nz[0], nz[-1]
    # upper: last populated bin has >= min_count and bins after it are 0 up to the range end
    if last < len(h) - 1 and h[last] >= min_count:
        cuts.append({"side": "upper", "c": float(edges[last + 1])})
    if first > 0 and h[first] >= min_count:
        cuts.append({"side": "lower", "c": float(edges[first])})
    rec["min"], rec["max"] = float(v.min()), float(v.max())
    return cuts, rec


def l6_checks(mh_df, min_count=50, plx_snr_frac=1e-4):
    """Returns {"declared": {quantity: [cuts]}, "parallax_dependent": bool, "records": ...}."""
    cols = {}
    if "parallax" in mh_df:
        cols["parallax"] = mh_df["parallax"].to_numpy(float)
        if "parallax_error" in mh_df:
            cols["parallax_over_error"] = cols["parallax"] / mh_df["parallax_error"].to_numpy(float)
    for q in ("bp", "bp_rp", "l", "b"):
        if q in mh_df:
            cols[q] = mh_df[q].to_numpy(float)
    declared, records = {}, {}
    for q, vals in cols.items():
        lo, hi, w = L6_SPECS[q]
        cuts, rec = detect_cuts(vals, lo, hi, w, min_count)
        records[q] = rec
        if cuts:
            declared[q] = cuts
    snr_rule = None
    if "parallax_over_error" in cols:
        s = cols["parallax_over_error"]
        s = s[np.isfinite(s)]
        f = float(np.mean(s < 1.0)) if s.size else float("nan")
        snr_rule = {"fraction_below_1": f, "declared": bool(s.size and f < plx_snr_frac)}
    par_dep = any(q in declared for q in PARALLAX_DEPENDENT) or bool(snr_rule and snr_rule["declared"])
    return {"declared": declared, "snr_below_1_rule": snr_rule, "parallax_dependent_cut": par_dep,
            "records": records, "present": sorted(cols)}


# ---------------------------------------------------------------------------------------------
# L7 metallicity range

def l7_range(mh):
    mh = np.asarray(mh, float)
    mh = mh[np.isfinite(mh)]
    return {"min": float(mh.min()), "max": float(mh.max()), "p0_1": float(np.percentile(mh, 0.1)),
            "n_below_m2p5": int(np.sum(mh < -2.5)), "n_finite": int(mh.size)}


# ---------------------------------------------------------------------------------------------
# T1 (README 4.2)

def t1_counts(mh):
    mh = np.asarray(mh, float)
    return {"lt_m2": int(np.sum(mh < -2.0)), "lt_m1p5": int(np.sum(mh < -1.5)),
            "m2p7_to_m1p5": int(np.sum((mh > -2.7) & (mh < -1.5))), "lt_m1": int(np.sum(mh < -1.0)),
            "total": int(mh.size)}


# R22's statements (README section 2, T1 row): (id, source, count key, kind, value, sample or None)
R22_STATEMENTS = [
    ("abstract", "abstract", "m2p7_to_m1p5", "approx", 18000, 2_000_000),
    ("s3_lt_m2", "Section III.2", "lt_m2", "above", 4000, None),
    ("s3_lt_m1p5", "Section III.2", "lt_m1p5", "approx", 18000, None),
    ("s3_lt_m1", "Section III.2", "lt_m1", "almost100k", 100000, None),
    ("f4_lt_m2", "Fig. 4 caption", "lt_m2", "approx", 5000, 1_700_000),
    ("f4_lt_m1p5", "Fig. 4 caption", "lt_m1p5", "approx", 20000, 1_700_000),
    ("f4_lt_m1", "Fig. 4 caption", "lt_m1", "almost100k", 100000, 1_700_000),
    ("s4_lt_m1p5", "Section IV", "lt_m1p5", "approx", 20000, 2_000_000),
    ("s4_lt_m1", "Section IV", "lt_m1", "approx", 70000, 2_000_000),
]
# each inconsistent pair: (name, statements giving the first number, statements giving the second)
PAIRS = [("18,000/20,000", ("abstract", "s3_lt_m1p5"), ("f4_lt_m1p5", "s4_lt_m1p5")),
         (">4,000/5,000", ("s3_lt_m2",), ("f4_lt_m2",)),
         ("100,000/70,000", ("s3_lt_m1", "f4_lt_m1"), ("s4_lt_m1",))]


def agrees(x, kind, value):
    if kind == "approx":
        return 0.95 * value <= x <= 1.05 * value
    if kind == "almost100k":
        return 90000 <= x <= 99999
    if kind == "above":
        return x > value
    raise ValueError(kind)


def t1_labels(counts):
    total = counts["total"]
    rows = {}
    for sid, src, key, kind, value, sample in R22_STATEMENTS:
        n = counts[key]
        r = {"source": src, "count_key": key, "kind": kind, "r22": value, "ours": n,
             "count_label": "agrees" if agrees(n, kind, value) else "disagrees",
             "poisson_sigma": math.sqrt(n), "sample": sample}
        if sample is not None:
            scaled = n / total * sample
            r["scaled"] = scaled
            r["fraction_label"] = "agrees" if agrees(scaled, kind, value) else "disagrees"
            r["sample_differs"] = abs(sample - total) / total > 0.05
        rows[sid] = r
    pairs = {}
    for name, first, second in PAIRS:
        side_a = any(rows[x]["count_label"] == "agrees" for x in first)
        side_b = any(rows[x]["count_label"] == "agrees" for x in second)
        pairs[name] = {"first": list(first), "second": list(second),
                       "first_supported": side_a, "second_supported": side_b,
                       "supports": "both" if side_a and side_b else ("first" if side_a else
                                                                     ("second" if side_b else "neither"))}
    ab = rows["abstract"]
    return {"statements": rows, "pairs": pairs,
            "summary": "abstract reproduced" if ab["count_label"] == "agrees" else "not reproduced",
            "abstract_fraction_label": ab.get("fraction_label")}
