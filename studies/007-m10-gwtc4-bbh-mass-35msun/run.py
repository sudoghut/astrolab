"""M10 GWTC-4.0 BBH mass spectrum: the 35 Msun feature and the event sample.

Pre-registration: README sections 1-4. Run with:
    python -m astrolab run 007-m10-gwtc4-bbh-mass-35msun
Explore with:
    python -m astrolab explore 007-m10-gwtc4-bbh-mass-35msun --tag <topic> --set KEY=VALUE

R1  Rebuild P26's 153-event BBH sample from GWOSC lists; compare the O4a part with P26's list.
R2  Counts above and below 35 Msun against a single power law times a toy VT (descriptive).
R3  Point-estimate toy fits: broken power law with and without a peak (exploration).
R4  GW231123's total-mass percentile in the rebuilt sample (descriptive).
"""
import numpy as np

import gwtc

# Tunable knobs (AGENTS.md section 2). Read inside main() and passed on as arguments.
PARAMS = {
    "lists": {
        "GWTC-4.0": "https://gwosc.org/eventapi/json/GWTC-4.0/",
        "GWTC-1-confident": "https://gwosc.org/eventapi/json/GWTC-1-confident/",
        "GWTC-2.1-confident": "https://gwosc.org/eventapi/json/GWTC-2.1-confident/",
        "GWTC-3-confident": "https://gwosc.org/eventapi/json/GWTC-3-confident/",
        "GWTC-2.1-marginal": "https://gwosc.org/eventapi/json/GWTC-2.1-marginal/",
        "GWTC-3-marginal": "https://gwosc.org/eventapi/json/GWTC-3-marginal/",
    },
    "o3_precedence": ["GWTC-3-confident", "GWTC-3-marginal", "GWTC-2.1-confident", "GWTC-2.1-marginal",
                      "GWTC-1-confident"],
    "o4a_tar": "https://zenodo.org/records/16911563/files/o4a_event_list.tar?download=1",
    "gps_o4a": [1368975618, 1389456018],
    "exclude_o4a": ["GW230630_070659"],
    "far_max": 1.0,
    "m_min": 3.0,
    "mass_bound": "p90",
    "extra_m2_max": 5.0,
    "max_extras": 2,
    "n_o4a_target": 84,
    "n_o3_target": 69, "n_o3_tol": 2,
    "named_checks": ["GW170817", "GW190425", "GW190814", "GW190917_114630", "GW190426_152155",
                     "GW200105_162426", "GW200115_042309"],
    "gwtc1_bbhs": ["GW150914", "GW151012", "GW151226", "GW170104", "GW170608", "GW170729", "GW170809",
                   "GW170814", "GW170818", "GW170823"],
    # R2 / R3 / R4
    "lambda1": 1.7, "vt_slope": 2.2, "turnovers": [30.0, 50.0, 80.0, None],
    "m_range": [10.0, 100.0], "m_split": 35.0, "n_grid": 2000,
    "n_starts": 20, "seed": 0,
    "gw231123": "GW231123_135430",
}


def _strip(name):
    return name.split("-v")[0]


def main(ctx):
    P = dict(PARAMS)
    rows = {}
    for label, url in P["lists"].items():
        path = ctx.http(url, label=f"GWOSC {label}", suffix=".json")
        rows[label] = gwtc.load_list(path)
        ctx.log(f"{label}: {len(rows[label])} events")
    tar_path = ctx.http(P["o4a_tar"], label="P26 o4a_event_list.tar", suffix=".tar")
    names, members = gwtc.tar_names(tar_path)

    # ---------------- R1 ----------------
    lo, hi = P["gps_o4a"]
    s_o4a, why_o4a = gwtc.select_o4a(rows["GWTC-4.0"], lo, hi, P["far_max"], P["m_min"], P["mass_bound"],
                                     set(P["exclude_o4a"]))
    target = set()
    for n in names:
        g = gwtc.name_to_gps(n)
        if g is not None and lo <= g < hi:
            target.add(n)
    ambiguous = (len(target) == 0) or (len(target) != P["n_o4a_target"])
    s_names = {_strip(n) for n in s_o4a}
    missing = sorted(target - s_names)
    extra = sorted(s_names - target)
    extra_rows = []
    for n in extra:
        r = next(v for k, v in s_o4a.items() if _strip(k) == n)
        b2 = gwtc.lower_bound(r["m2"], r["m2_lo"])
        extra_rows.append({"name": n, "m2_p5": b2, "type_a": bool(b2 is not None and P["m_min"] < b2 <= P["extra_m2_max"])})
    o4a_ok = (not ambiguous) and not missing and all(e["type_a"] for e in extra_rows) and len(extra_rows) <= P["max_extras"]

    merged = gwtc.merge_lists([rows[k] for k in P["o3_precedence"]])
    s_o3, why_o3 = gwtc.select_o3(merged, P["far_max"], P["m_min"], P["mass_bound"])
    n_o3 = len(s_o3)
    n_type_i = sum(1 for r in s_o3.values()
                   if gwtc.lower_bound(r["m2"], r["m2_lo"]) is not None
                   and P["m_min"] < gwtc.lower_bound(r["m2"], r["m2_lo"]) <= P["extra_m2_max"])
    o3_count_ok = abs(n_o3 - P["n_o3_target"]) <= P["n_o3_tol"] and (
        n_o3 <= P["n_o3_target"] or n_type_i >= n_o3 - P["n_o3_target"])
    named = {}
    for n in P["named_checks"]:
        hit = [k for k in merged if _strip(k) == n or _strip(k).startswith(n)]
        if not hit:
            named[n] = {"status": "not in lists", "pass": True}
            continue
        k = hit[0]
        if k in s_o3:
            named[n] = {"status": "selected", "pass": False}
        else:
            reason = why_o3.get(k, "")
            named[n] = {"status": "excluded (no PE)" if reason == "no PE or FAR" else f"excluded: {reason}",
                        "pass": True}
    gwtc1_missing = [n for n in P["gwtc1_bbhs"] if not any(_strip(k) == n for k in merged)]
    o3_ok = o3_count_ok and all(v["pass"] for v in named.values())
    if not o3_ok:
        verdict = "not reproduced"
    elif ambiguous:
        verdict = "described"
    else:
        verdict = "reproduced" if o4a_ok else "not reproduced"
    r1 = {"tar_members": members, "tar_names": sorted(names), "target_size": len(target),
          "target_ambiguous": ambiguous, "n_o4a": len(s_o4a), "missing": missing, "extra": extra_rows,
          "o4a_part": "ambiguous" if ambiguous else ("reproduced" if o4a_ok else "not reproduced"),
          "n_o3": n_o3, "n_o3_type_i_candidates": n_type_i, "o3_part": "reproduced" if o3_ok else "not reproduced",
          "named_checks": named, "gwtc1_missing": gwtc1_missing, "verdict": verdict,
          "far_note": "GWOSC far is documented as the lowest FAR over search pipelines"}
    ctx.log(f"R1: O4a {len(s_o4a)} (target {len(target)}), missing {len(missing)}, extra {len(extra)}; "
            f"O3 {n_o3}; verdict {verdict}")
    ctx.save("r1", r1)

    # sample for R2-R4
    o4a_rows = ({k: v for k, v in s_o4a.items() if _strip(k) in target} if r1["o4a_part"] == "reproduced" else s_o4a)
    sample = list(o4a_rows.values()) + list(s_o3.values())
    ctx.save("sample", {"events": [{"name": r["name"], "m1": r["m1"], "m2": r["m2"], "mtot": r["mtot"],
                                    "far": r["far"]} for r in sample]})
    m1 = np.array([r["m1"] for r in sample])
    m_lo, m_hi = P["m_range"]
    inside = (m1 >= m_lo) & (m1 <= m_hi)
    mm = m1[inside]

    # ---------------- R2 ----------------
    n_lo = int(np.sum(mm < P["m_split"]))
    n_hi = int(np.sum(mm >= P["m_split"]))
    per_mt = []
    for mt in P["turnovers"]:
        f = gwtc.r2_prediction(P["lambda1"], P["vt_slope"], mt, m_lo, P["m_split"], m_hi, P["n_grid"])
        per_mt.append({"m_t": mt, "f_pred": f, "frac_obs": n_hi / (n_lo + n_hi),
                       "ratio": (n_hi / (n_lo + n_hi)) / f, "binom_p": gwtc.binom_le(n_hi, n_lo + n_hi, f)})
    widths = [(r["m1_hi"] - r["m1_lo"]) / r["m1"] for r in sample
              if r["m1"] is not None and 30 <= r["m1"] <= 40 and r["m1_hi"] is not None and r["m1_lo"] is not None]
    r2 = {"n_lo": n_lo, "n_hi": n_hi, "n_outside_range": int(np.sum(~inside)),
          "outside": [r["name"] for r, ok in zip(sample, inside) if not ok], "per_turnover": per_mt,
          "width_30_40": float(np.median(widths)) if widths else None, "n_width": len(widths),
          "caveat": "descriptive; [10, 35) contains the 10 Msun peak, so the prediction is biased"}
    ctx.log(f"R2: n_lo {n_lo}, n_hi {n_hi}; " + "; ".join(f"Mt {p['m_t']}: ratio {p['ratio']:.2f}" for p in per_mt))
    ctx.save("r2", r2)

    # ---------------- R3 ----------------
    grid = np.linspace(m_lo, m_hi, P["n_grid"])
    r3 = []
    for mt in P["turnovers"]:
        a = gwtc.fit("A", mm, grid, P["vt_slope"], mt, P["n_starts"], P["seed"])
        b = gwtc.fit("B", mm, grid, P["vt_slope"], mt, P["n_starts"], P["seed"],
                     extra_starts=[a["theta"] + [35.0, 5.0, 0.0]])
        r3.append({"m_t": mt, "A": a, "B": b, "dlam": a["theta"][1] - a["theta"][0],
                   "two_dlnl": 2 * (a["nll"] - b["nll"]), "break_at_bound": a["at_bound"][2]})
    ctx.log("R3: " + "; ".join(f"Mt {r['m_t']}: dlam {r['dlam']:.2f}, 2dlnL {r['two_dlnl']:.2f}" for r in r3))
    ctx.save("r3", {"fits": r3, "note": "exploration only; point estimates, toy VT, no injections"})

    # ---------------- R4 ----------------
    mt_all = np.array([r["mtot"] for r in sample if r["mtot"] is not None])
    g = [r for r in sample if r["name"].startswith(P["gw231123"].split("_")[0])]
    r4 = {"in_sample": bool(g)}
    if g and g[0]["mtot"] is not None:
        r4.update({"mtot": g[0]["mtot"], "percentile": float(100 * np.mean(mt_all <= g[0]["mtot"])),
                   "n": int(mt_all.size)})
    ctx.save("r4", r4)
    summary = {"params": {k: v for k, v in P.items() if k not in ("lists",)},
               "r1": {k: r1[k] for k in ("verdict", "n_o4a", "target_size", "n_o3", "o4a_part", "o3_part")},
               "r2": {"n_lo": n_lo, "n_hi": n_hi}, "r4": r4}
    ctx.save("summary", summary)
    return summary
