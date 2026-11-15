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
    s_names = {_strip(n) for n in s_o4a}
    missing = sorted(target - s_names)
    missing_reasons = {n: why_o4a.get(n, "not in GWTC-4.0 list") for n in missing}
    extra = sorted(s_names - target)
    extra_rows = []
    for n in extra:
        r = next(v for k, v in s_o4a.items() if _strip(k) == n)
        b2 = gwtc.lower_bound(r["m2"], r["m2_lo"])
        extra_rows.append({"name": n, "m2_p5": b2,
                           "type_a": bool(b2 is not None and P["m_min"] < b2 <= P["extra_m2_max"])})

    labels = P["o3_precedence"]
    merged, overlaps = gwtc.merge_lists([rows[k] for k in labels], labels)
    s_o3, why_o3 = gwtc.select_o3(merged, P["far_max"], P["m_min"], P["mass_bound"])
    n_o3 = len(s_o3)
    n_type_i = sum(1 for r in s_o3.values()
                   if gwtc.lower_bound(r["m2"], r["m2_lo"]) is not None
                   and P["m_min"] < gwtc.lower_bound(r["m2"], r["m2_lo"]) <= P["extra_m2_max"])
    named = {}
    for n in P["named_checks"]:
        hits = [k for k in merged if gwtc.same_event(k, n)]
        if not hits:
            named[n] = {"status": "not in lists", "pass": False}
            continue
        statuses, ok = [], True
        for k in hits:
            if k in s_o3:
                statuses.append(f"{k}: selected")
                ok = False
            else:
                reason = why_o3.get(k, "")
                statuses.append(f"{k}: " + ("excluded (no PE)" if reason == "no PE or FAR" else f"excluded: {reason}"))
        named[n] = {"status": "; ".join(statuses), "pass": ok}
    gwtc1 = {n: {"in_lists": any(_strip(k) == n for k in merged), "in_sample": any(_strip(k) == n for k in s_o3)}
             for n in P["gwtc1_bbhs"]}
    v = gwtc.r1_verdict(len(target), P["n_o4a_target"], missing, [e["m2_p5"] for e in extra_rows],
                        P["extra_m2_max"], P["m_min"], P["max_extras"], n_o3, P["n_o3_target"],
                        P["n_o3_tol"], n_type_i, [x["pass"] for x in named.values()])
    r1 = {"tar_members": members, "tar_names": sorted(names), "target_size": len(target),
          "target_ambiguous": v["ambiguous"], "n_o4a": len(s_o4a), "missing": missing,
          "missing_reasons": missing_reasons, "extra": extra_rows,
          "o4a_part": "ambiguous" if v["ambiguous"] else ("reproduced" if v["o4a_ok"] else "not reproduced"),
          "n_o3": n_o3, "n_o3_type_i_candidates": n_type_i,
          "o3_part": "reproduced" if v["o3_ok"] else "not reproduced",
          "named_checks": named, "gwtc1": gwtc1,
          "gwtc1_missing": [n for n, x in gwtc1.items() if not x["in_lists"]],
          "excluded_o4a": {k: why for k, why in why_o4a.items() if why != "outside O4a"},
          "excluded_o3": why_o3, "precedence_overlaps": overlaps, "verdict": v["verdict"],
          "far_note": "GWOSC far is documented as the lowest FAR over search pipelines"}
    ctx.log(f"R1: O4a {len(s_o4a)} (target {len(target)}), missing {len(missing)}, extra {len(extra)}; "
            f"O3 {n_o3}; verdict {v['verdict']}")
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
    in_3040 = [r for r in sample if r["m1"] is not None and 30 <= r["m1"] <= 40]
    widths = [(r["m1_hi"] - r["m1_lo"]) / r["m1"] for r in in_3040 if r["m1_hi"] is not None and r["m1_lo"] is not None]
    r2 = {"n_lo": n_lo, "n_hi": n_hi, "n_outside_range": int(np.sum(~inside)),
          "outside": [r["name"] for r, ok in zip(sample, inside) if not ok], "per_turnover": per_mt,
          "width_30_40": float(np.median(widths)) if widths else None, "n_width": len(widths),
          "n_width_skipped": len(in_3040) - len(widths),
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
                   "peak_mu": b["theta"][3], "peak_sigma": b["theta"][4], "peak_w": b["theta"][5],
                   "two_dlnl": 2 * (a["nll"] - b["nll"]), "break_at_bound": a["at_bound"][2]})
    ctx.log("R3: " + "; ".join(f"Mt {r['m_t']}: dlam {r['dlam']:.2f}, 2dlnL {r['two_dlnl']:.2f}" for r in r3))
    ctx.save("r3", {"fits": r3, "note": "exploration only; point estimates, toy VT, no injections"})

    # ---------------- R4 ----------------
    # dated pre-data amendment (2026-11-15, README section 2 R4): a null total mass is replaced by
    # m1 + m2 (sum of the medians) and counted
    mt_rows = []
    n_filled = []
    for r in sample:
        mt = r["mtot"]
        if mt is None and r["m1"] is not None and r["m2"] is not None:
            mt = r["m1"] + r["m2"]
            n_filled.append(r["name"])
        if mt is not None:
            mt_rows.append((r["name"], mt))
    mt_all = np.array([m for _, m in mt_rows])
    exact = [(n, m) for n, m in mt_rows if _strip(n) == P["gw231123"]]
    if not exact:
        stem_hits = [(n, m) for n, m in mt_rows if gwtc.same_event(n, P["gw231123"])]
        exact = stem_hits if len(stem_hits) == 1 else []
    r4 = {"in_sample": bool(exact), "n": int(mt_all.size), "n_mtot_filled": len(n_filled), "filled": n_filled}
    if exact:
        r4.update({"mtot": exact[0][1], "percentile": float(100 * np.mean(mt_all <= exact[0][1]))})
    ctx.save("r4", r4)
    summary = {"params": {k: v for k, v in P.items() if k not in ("lists",)},
               "r1": {k: r1[k] for k in ("verdict", "n_o4a", "target_size", "n_o3", "o4a_part", "o3_part")},
               "r2": {"n_lo": n_lo, "n_hi": n_hi}, "r4": r4}
    ctx.save("summary", summary)
    return summary
