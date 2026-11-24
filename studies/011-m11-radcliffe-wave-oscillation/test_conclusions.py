"""Assertions that this study's labels follow from its stored numbers (README section 2).

The decision rules are written out again here, independently of stats011.py, so a slip in either
place shows up. Run the study first: python -m astrolab run 011-m11-radcliffe-wave-oscillation
"""
import json
import math
from pathlib import Path

import pytest
from scipy.stats import chi2

RESULTS = Path(__file__).parent / "results"


def load(name):
    path = RESULTS / f"{name}.json"
    if not path.exists():
        pytest.skip(f"{path.name} missing; run the study first")
    return json.loads(path.read_text(encoding="utf-8"))


def test_summary_exists():
    s = load("summary")
    assert s["status"] == "complete"
    assert s["load_check"]["passed"] and abs(s["load_check"]["weighted_mean_vz"]) < 3.0


def test_files_small():
    for p in RESULTS.glob("*.json"):
        assert p.stat().st_size < 1024 ** 2, p.name


def test_t1_labels():
    t1 = load("t1_t2")["t1"]
    for col in ("col4", "col6"):
        rows = t1[col]["parameters"]
        n = 0
        for k in ("A", "p", "delta", "s0", "gamma", "phi"):
            r = rows[k]
            inside = r["k24"]["median"] - r["k24"]["minus"] <= r["ours"]["median"] <= r["k24"]["median"] + r["k24"]["plus"]
            assert inside == r["inside_k24_1sigma"]
            n += inside
        assert n == t1[col]["n_inside_of_6"]
        want = "reproduced" if n >= 5 else ("partly reproduced" if n >= 3 else "not reproduced")
        assert t1[col]["label"] == want


def test_t2_reported():
    t2 = load("t1_t2")["t2"]
    assert 0.0 <= t2["B"]["p16"] <= t2["B"]["median"] <= t2["B"]["p84"] <= 1.0
    assert 0.0 <= t2["P_B_gt_0p95"] <= 1.0 and 0.0 <= t2["P_B_lt_0p5"] <= 1.0


def _p_boot(k, n):
    return (1 + k) / (1 + n)


def _t3_check(st, d):
    mocks = st["mocks_two_dlnL"]
    k = sum(m >= st["two_dlnL"] for m in mocks)
    assert k == st["k_mocks_at_least_obs"]
    assert st["p_boot"] == pytest.approx(_p_boot(k, len(mocks)))
    assert st["p_raw"] == pytest.approx(chi2.sf(st["two_dlnL"], d))
    m = sum(mocks) / len(mocks)
    if m > 0:
        assert st["p_cal"] == pytest.approx(chi2.sf(st["two_dlnL"] * d / m, d), rel=1e-6, abs=1e-12)
    else:
        assert st["p_cal"] is None


def test_t3_labels():
    t3 = load("t3")
    s, t = t3["standing_stat"], t3["travelling_stat"]
    _t3_check(s, 1)
    _t3_check(t, 2)
    if s["p_cal"] is None:
        want = "not evaluable"
    elif s["p_cal"] < 0.001 and s["p_raw"] < 0.001 and s["k_mocks_at_least_obs"] == 0:
        want = "standing excluded strongly"
    elif s["p_cal"] < 0.05 and s["p_boot"] < 0.05:
        want = "standing excluded"
    else:
        want = "standing not excluded"
    assert t3["standing"] == want
    if t["p_cal"] is None:
        want = "not evaluable"
    elif t["p_cal"] < 0.05 and t["p_boot"] < 0.05:
        want = "pure travelling (B = 1) disfavoured"
    else:
        want = "pure travelling (B = 1) not disfavoured"
    assert t3["pure_travelling"] == want


def _t4_thresholds():
    P = load("t4")["params"]
    return P["t4_p_excl"], P["t4_p_not"], P["t4_power_min"]


def _t4_want(p, power):
    p_excl, p_not, power_min = _t4_thresholds()
    if power < power_min:
        return "undetermined"
    if p < p_excl:
        return "standing excluded by the phases"
    if p > p_not:
        return "standing not excluded by the phases"
    return "undetermined"


def _t4_check(g):
    """p and power from the stored mock counts (and from the stored R values when present)."""
    assert g["p"] == pytest.approx(_p_boot(g["k_standing_at_or_below"], g["n_standing"]))
    assert g["power_B1"] == pytest.approx(g["k_power_B1_p_below"] / g["n_power_B1"])
    assert g["label"] == _t4_want(g["p"], g["power_B1"])


def test_t4_label():
    t4 = load("t4")
    g = t4["gauss"]
    _t4_check(g)
    assert t4["label"] == g["label"]
    if "R_standing" in g:
        st = sorted(g["R_standing"])
        k = sum(r <= t4["R_obs"] for r in st)
        assert k == g["k_standing_at_or_below"]
        n_low = 0
        for r in g["R_power_B1"]:
            kk = sum(x <= r for x in st)
            n_low += _p_boot(kk, len(st)) < _t4_thresholds()[0]
        assert n_low == g["k_power_B1_p_below"]


def _wl_want(lo, hi):
    if lo is None or hi is None:
        return "not evaluable"
    if 0.8 <= lo and hi <= 1.25:
        return "consistent"
    if hi < 0.8 or lo > 1.25:
        return "different"
    return "undetermined"


def _bhat_want(lo, hi, wl, ka):
    if lo is None or hi is None:
        return "not evaluable"
    if wl == "different":
        return "not applicable (wavelengths differ)"
    if not ka:
        return "undetermined"
    if lo > 0.4:
        return "travelling component in K24's direction dominates"
    if hi < 0.4:
        return "no travelling dominance in K24's direction"
    return "undetermined"


def test_t5_labels_and_known_answer():
    t5 = load("t5")
    ka = t5["known_answer"]
    ok = True
    for B, row in ka["injections"].items():
        lo, hi = row["median_mock_interval"]
        if float(B) >= 1.0:
            this = lo is not None and lo > 0.4
        else:
            this = lo is not None and lo <= 2 * float(B) - 1 <= hi
        assert this == row["pass"]
        ok &= this
    assert ok == ka["passed"] == t5["known_answer_passed"]
    wl = _wl_want(*t5["k_ratio_interval"])
    assert t5["wavelengths_label"] == wl
    assert t5["bhat_label"] == _bhat_want(*t5["bhat_interval"], wl, ka["passed"])


def _reduced_standing(obs, factor):
    if factor is None:
        return "not evaluable"
    pc, pr = chi2.sf(obs * factor, 1), chi2.sf(obs, 1)
    if pc < 0.001 and pr < 0.001:
        return "standing excluded strongly"
    return "standing excluded" if pc < 0.05 else "standing not excluded"


def _reduced_travel(obs, factor):
    if factor is None:
        return "not evaluable"
    return ("pure travelling (B = 1) disfavoured" if chi2.sf(obs * factor, 2) < 0.05
            else "pure travelling (B = 1) not disfavoured")


def test_t6_robustness():
    t6 = load("t6")
    assert len(t6["variants"]) == 15
    n_changes = sum(len(v["changed"]) for v in t6["variants"])
    assert n_changes == len(t6["changes"])
    assert t6["label"] == ("robust" if n_changes == 0 else "fragile")
    main_full, main_red = t6["main_labels_full_rule"], t6["main_labels_reduced_rule"]
    t3 = load("t3")
    fs, ft = t3["standing_stat"]["factor"], t3["travelling_stat"]["factor"]
    # the main run's reduced-rule labels, from its own numbers
    assert main_red["standing"] == _reduced_standing(t3["standing_stat"]["two_dlnL"], fs)
    assert main_red["pure_travelling"] == _reduced_travel(t3["travelling_stat"]["two_dlnL"], ft)
    for v in t6["variants"]:
        if v["t3"]["rule"] == "reduced":
            assert v["labels"]["T3 standing"] == _reduced_standing(v["two_dlnL_standing"], fs)
            assert v["labels"]["T3 pure travelling"] == _reduced_travel(v["two_dlnL_travelling"], ft)
        else:
            _t3_check(v["t3"]["standing_stat"], 1)
            _t3_check(v["t3"]["travelling_stat"], 2)
        _t4_check(v["t4"]["gauss"])
        for c in t6["changes"]:
            assert "mcse" in c
    for v in t6["variants"]:
        ref = main_full if v["t3"]["rule"] == "full" else main_red
        assert v["t5"]["known_answer_passed"] == load("t5")["known_answer_passed"]
        changed = []
        for key, mk in (("T3 standing", "standing"), ("T3 pure travelling", "pure_travelling"), ("T4", "t4"),
                        ("T5 wavelengths", "t5_wavelengths"), ("T5 bhat", "t5_bhat")):
            if v["labels"][key] != ref[mk]:
                changed.append(key)
        assert changed == v["changed"], v["variant"]


def test_t7_label():
    t7 = load("t7")
    a, b, c = t7["a_col6_B1"]["m2lnL"], t7["b_vz_zero"]["m2lnL"], t7["c_B0p5"]["m2lnL"]
    want = "CO prefers the travelling wave" if (a + 9 <= b and a + 9 <= c) else "CO does not distinguish"
    assert t7["label"] == want


def test_t8_label():
    t8 = load("t8")
    pb, pk = t8["ln_omega0_broad_prior"], t8["ln_omega0_k24_prior"]
    half = 0.5 * (pb["p84"] - pb["p16"])
    assert half == pytest.approx(t8["halfwidth_broad"])
    narrow = half < 0.5 * 0.17
    stable = abs(pk["median"] - pb["median"]) / half < 0.5
    want = "data-driven" if (narrow and stable) else ("prior-driven" if not (narrow or stable) else "partly data-driven")
    assert t8["label"] == want


def test_overall_reading():
    s = load("summary")
    t1 = s["T1"]["col4"]
    t3, t4, t5, t6 = s["T3"]["standing"], s["T4"]["label"], s["T5"]["bhat"], s["T6"]["label"]
    support = (t1 in ("reproduced", "partly reproduced") and t3 in ("standing excluded", "standing excluded strongly")
               and t4 == "standing excluded by the phases"
               and t5 == "travelling component in K24's direction dominates" and t6 == "robust")
    if support:
        want = "K24's travelling-wave reading is supported by these data"
    elif t3 == "standing not excluded" and t5 == "no travelling dominance in K24's direction":
        want = "not supported"
    else:
        want = "mixed"
    assert s["overall"]["reading"] == want
    both_not = s["T1"]["col4"] == "not reproduced" and s["T1"]["col6"] == "not reproduced"
    assert ("qualifier" in s["overall"]) == both_not
    assert math.isfinite(s["T3"]["two_dlnL_standing"])


# ---------------------------------------------------------------------------------------------
# README 4.10 (T-056, post hoc): R-CONV and T8-P, re-derived from the saved files

SFX = " (best among these 16 candidate conventions, post hoc)"
COUNTED = ("A", "p", "delta", "s0", "gamma", "phi")


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])


def test_rconv_choice_and_labels():
    rc = load("rconv")
    k24 = rc["k24_column3"]
    rows = rc["conventions"]
    assert rc["complete_set"] == (sorted(r["index"] for r in rows) == list(range(16)))
    if rc["params"]["parts"] == ["conv"] and rc["params"].get("conv_indices") == list(range(16)):
        assert rc["complete_set"]
    for r in rows:
        b, s, w = r["index"] // 4, (r["index"] // 2) % 2, r["index"] % 2
        assert r["name"] == f"{'LCYX'[b]}-{'FP'[s]}-{'WR'[w]}"
        assert r["n_factors_differing"] == (b != 0) + (s != 0) + (w != 0)
        n = 0
        ratios = []
        for k in COUNTED:
            o, t = r["parameters"][k], k24[k]
            inside = t["median"] - t["minus"] <= o["median"] <= t["median"] + t["plus"]
            assert inside == r["inside"][k]
            n += inside
            ratios.append(0.5 * (o["p84"] - o["p16"]) / (0.5 * (t["plus"] + t["minus"])))
        assert n == r["count"]
        assert r["width_ratio"] == pytest.approx(_median(ratios), rel=1e-9)
        for k, o in r["parameters"].items():
            dd = o["median"] - k24[k]["median"]
            want = dd / k24[k]["plus"] if dd > 0 else dd / k24[k]["minus"]
            assert r["sigma_scaled_differences"][k] == pytest.approx(want, rel=1e-9, abs=1e-12)
    cand = [r for r in rows if r["count"] >= 3]
    ch = rc["choice"]
    if not cand:
        assert ch["chosen"] is None and rc["reruns"] is None
        assert rc["label"] == "column (3) not reproduced under any candidate convention" + SFX
        return
    inw = [r for r in cand if 2 / 3 <= r["width_ratio"] <= 1.5]
    pool = inw or cand
    best = sorted(pool, key=lambda r: (-r["count"], r["n_factors_differing"], r["index"]))[0]
    assert ch["chosen"] == best["index"] and ch["case"] == ("ii" if inw else "iii")
    status = "reproduced" if best["count"] >= 5 and 2 / 3 <= best["width_ratio"] <= 1.5 else "partly reproduced"
    assert rc["label"] == f"column (3) {status} under {best['name']}" + SFX
    assert rc["reruns"] is not None and rc["reruns"]["convention"] == best["name"]


def test_rconv_reruns():
    rc = load("rconv")
    rr = rc["reruns"]
    if rr is None:
        pytest.skip("no convention chosen: nothing rerun (README 4.10)")
    qual = f"under {rr['convention']}, post hoc"
    for col in ("col4", "col6"):
        t = rr["t1"][col]
        n = sum(t["parameters"][k]["inside_k24_1sigma"] for k in COUNTED)
        for k in COUNTED:
            r = t["parameters"][k]
            assert r["inside_k24_1sigma"] == (r["k24"]["median"] - r["k24"]["minus"] <= r["ours"]["median"]
                                              <= r["k24"]["median"] + r["k24"]["plus"])
        want = "reproduced" if n >= 5 else ("partly reproduced" if n >= 3 else "not reproduced")
        assert t["n_inside_of_6"] == n and t["label"] == want
        assert t["label_qualified"] == f"{want} {qual}" == rr["labels"]["T1_" + col]
    t5 = rr["t5"]
    ka = t5["known_answer"]
    ok = True
    for B, row in ka["injections"].items():
        lo, hi = row["median_mock_interval"]
        this = (lo is not None and lo > 0.4) if float(B) >= 1.0 else (lo is not None and lo <= 2 * float(B) - 1 <= hi)
        assert this == row["pass"]
        ok &= this
    assert sorted(float(b) for b in ka["injections"]) == [0.5, 0.84, 1.0]
    assert ok == ka["passed"] == rr["labels"]["T5_known_answer_passed"]
    # the injection: the chosen convention's column-(3) median, omega0 t from its column-(5) median
    chosen = [r for r in rc["conventions"] if r["index"] == rr["index"]][0]
    for k in ("x0", "y0", "x1", "y1", "x2", "y2", "A", "p", "s0", "phi", "delta", "gamma"):
        assert ka["injected_vector"][k] == pytest.approx(chosen["parameters"][k]["median"], rel=1e-3, abs=1e-2)
    assert ka["injected_vector"]["w0t"] == pytest.approx(rr["col5"]["median"]["w0t"], abs=1e-9)
    wl = _wl_want(*t5["k_ratio_interval"])
    assert t5["wavelengths_label"] == wl and rr["labels"]["T5_wavelengths"] == f"{wl} ({qual})"
    bl = _bhat_want(*t5["bhat_interval"], wl, ka["passed"])
    assert t5["bhat_label"] == bl and rr["labels"]["T5_bhat"] == f"{bl} ({qual})"


def test_t8p_label():
    t = load("t8p")
    pb, pk = t["ln_omega0_broad_prior"], t["ln_omega0_k24_prior"]
    half = 0.5 * (pb["p84"] - pb["p16"])
    assert half == pytest.approx(t["halfwidth_broad"])
    shift = (pk["median"] - pb["median"]) / half
    assert shift == pytest.approx(t["median_shift_in_sigma_broad"])
    med = 1000 * math.exp(pb["median"])
    assert med == pytest.approx(t["broad_median_omega0_kms_kpc"])
    lo, hi = t["broad_bounds_kms_kpc"]
    narrow, stable = half < 0.5 * 0.17, abs(shift) < 0.5
    rule = "data-driven" if narrow and stable else ("prior-driven" if not narrow and not stable else "partly data-driven")
    at_bound = med > 0.95 * hi or med < 1.05 * lo
    assert t["at_bound"] == at_bound and t["width_shift_rule_label"] == rule
    assert t["label"] == ("prior-driven (posterior at the bound)" if at_bound else rule)
    assert t["divisor_kms_kpc"] == 74.0 and t["convention"] == "L-F-W"
    for k in ("k24_priors", "broad_priors"):
        assert set(t[k]) >= {"omega0_kms_kpc", "rho0_msun_pc3", "sun_period_myr"}


def test_standalone_summary_keys():
    s = load("summary")
    # a rerun of the full pipeline rewrites summary.json without these keys: an existing result file must keep its key
    for f, key in (("rconv", "R_CONV"), ("t8p", "T8_P"), ("rdiag", "R_DIAG")):
        if (RESULTS / f"{f}.json").exists():
            assert key in s, f"results/{f}.json exists but summary.json has no {key}: rerun part {f!r} (README section 8)"
    if "R_CONV" in s:
        rc = load("rconv")
        assert s["R_CONV"]["label"] == rc["label"]
        assert s["R_CONV"]["counts"] == {r["name"]: r["count"] for r in rc["conventions"]}
        assert s["R_CONV"]["reruns"] == (rc["reruns"]["labels"] if rc["reruns"] else None)
    if "T8_P" in s:
        t = load("t8p")
        assert s["T8_P"]["label"] == t["label"] and s["T8_P"]["at_bound"] == t["at_bound"]
    if "R_DIAG" in s:
        rd = load("rdiag")
        assert s["R_DIAG"]["reading"] == rd["reading"] and s["R_DIAG"]["labels"] == rd["labels"]
    if "R_CONV" not in s and "T8_P" not in s and "R_DIAG" not in s:
        pytest.skip("R-CONV, T8-P and R-DIAG have not been run (README 4.10, 4.11)")


# ---------------------------------------------------------------------------------------------
# R-DIAG (README 4.11, T-061, post hoc)

def _rdiag_status(count, ratio):
    if count <= 2:
        return "not reproduced"
    return "reproduced" if count >= 5 and 2 / 3 <= ratio <= 1.5 else "partly reproduced"


def _rdiag_step(fit, d6_max=8.781, m6_max=3.192):
    if fit["status"] == "reproduced":
        return 2
    return 1 if fit["status"] == "partly reproduced" and fit["D6"] <= d6_max and fit["M6"] <= m6_max else 0


def test_rdiag_fits_and_labels():
    rd = load("rdiag")
    k24 = {k: v for k, v in load("rconv")["k24_column3"].items()} if (RESULTS / "rconv.json").exists() else None
    zname = f"z☉ = {rd['part_d']['zsun_pc']:g} pc"
    fits = dict(rd["part_b"]["fits"]) | {"c": rd["part_d"]["c"], "zsun": rd["part_d"]["zsun"]}
    whats = {"S": "with sample S", "S_all": "with sample S_all", "S+PT": "with sample S+PT",
             "c": "with the origin free", "zsun": f"with {zname}"}
    for key, f in fits.items():
        n = sum(f["inside"][k] for k in COUNTED)
        assert n == f["count"]
        d = f["sigma_scaled_differences"]
        assert f["D6"] == pytest.approx(sum(abs(d[k]) for k in COUNTED), rel=1e-12)
        assert f["M6"] == pytest.approx(max(abs(d[k]) for k in COUNTED), rel=1e-12)
        if k24:
            ratios = []
            for k in COUNTED:
                o, t = f["parameters"][k], k24[k]
                assert f["inside"][k] == (t["median"] - t["minus"] <= o["median"] <= t["median"] + t["plus"])
                ratios.append(0.5 * (o["p84"] - o["p16"]) / (0.5 * (t["plus"] + t["minus"])))
            assert f["width_ratio"] == pytest.approx(_median(ratios), rel=1e-9)
        st = _rdiag_status(f["count"], f["width_ratio"])
        assert f["status"] == st and f["label"] == f"column (3) {st} {whats[key]}, post hoc"
        assert rd["labels"][key] == f["label"]
    n = {k: v["n_points"] for k, v in rd["part_b"]["samples"].items()}
    assert n["S_all"] == 169 and n["S+PT"] - n["S"] == 28
    for k, v in rd["part_b"]["samples"].items():
        assert len(v["points"]) == v["n_points"] and sum(p["weight"] for p in v["points"]) == pytest.approx(v["n_points"])
        assert sum(p["source"] == "bridging" for p in v["points"]) == 54
    assert rd["part_b"]["fits"]["S"]["n_points"] == n["S"]


def test_rdiag_reading():
    rd = load("rdiag")
    fr = rd["formal_reference"]
    assert fr["count"] == 2 and round(fr["D6"], 3) == 9.781 and round(fr["M6"], 3) == 3.692
    assert fr["D6_max"] == pytest.approx(fr["D6"] - 1.0, abs=5e-4) and fr["M6_max"] == pytest.approx(fr["M6"] - 0.5, abs=5e-4)
    cref = rd["part_d"]["c_ref"]["c_posterior"]
    half = 0.5 * (cref["c"]["p84"] - cref["c"]["p16"])
    assert half == pytest.approx(cref["halfwidth_pc"])
    c_read = "data-driven" if half <= 100.0 else "prior-dominated"
    assert rd["part_d"]["c_reading"] == c_read == rd["labels"]["c_reading"]
    s = rd["part_b"]["fits"]["S"]
    st_s = _rdiag_step(s)
    if st_s == 2:
        want = ("column (3) is reproduced with the reconstructed sightline sample: the difference is consistent with "
                "the input sample")
    elif st_s == 1:
        want = "the reconstructed sightline sample accounts for part of the column-(3) difference"
    else:
        zname = f"z☉ = {rd['part_d']['zsun_pc']:g} pc"
        steps = {"the origin of s free": _rdiag_step(rd["part_d"]["c"]) if c_read == "data-driven" else 0,
                 zname: _rdiag_step(rd["part_d"]["zsun"])}
        best = max(steps.values())
        names = [k for k, v in steps.items() if v == best]
        if best == 0:
            want = "the column-(3) difference remains unexplained (input sample, origin and the Sun's height tested)"
        else:
            base = ("the column-(3) difference comes from the origin of s or the Sun's height" if best == 2 else
                    "the origin of s or the Sun's height accounts for part of the column-(3) difference")
            want = f"{base} ({'variant' if len(names) == 1 else 'variants'}: {' and '.join(names)})"
    assert rd["reading"] == want


def test_rdiag_curve_and_part_a():
    rd = load("rdiag")
    c = rd["part_c"]["comparison"]
    med, p95 = c["xy"]["median"], c["xy"]["p95"]
    want = ("matches K24's published curve" if med <= 5.0 and p95 <= 15.0 else
            ("approximately matches" if med <= 20.0 else "differs from K24's published curve"))
    if c["n_excluded_xy"] > 0.1 * c["n_points"]:
        want += " (more than 10% of the points lie beyond our curve's ends)"
    assert c["label"] == want == rd["part_c"]["label"] == rd["labels"]["curve"]
    assert c["n_points"] == 1500 and -400.0 <= rd["part_c"]["lsq_fit"]["c_pc"] <= 400.0
    a = rd["part_a"]
    assert len(a["objects"]) == 79 and a["map"]["n_starts"] == 2 + rd["params"]["rdiag_map_prior_draws"]
    if rd["params"]["parts"] == ["diag"] and rd["params"]["rdiag_map_prior_draws"] == 19:
        assert a["map"]["n_starts"] == 21
    for k in ("K", "P", "M"):
        v = a["vectors"][k]
        assert v["sum_terms"] == pytest.approx(-v["lnL"] - v["constant"], rel=1e-9)
        assert v["ln_posterior"] == pytest.approx(v["lnL"] + v["ln_prior"], rel=1e-12)
    # the MAP is the best ln posterior of the three vectors (it starts from v_K and v_P)
    assert a["vectors"]["M"]["ln_posterior"] >= max(a["vectors"]["K"]["ln_posterior"], a["vectors"]["P"]["ln_posterior"]) - 1e-6
    for comp, (x, y) in (("K_minus_M", ("t_K", "t_M")), ("K_minus_P", ("t_K", "t_P"))):
        delta = [o[x] - o[y] for o in a["objects"]]
        r = a["comparisons"][comp]
        top = sorted(range(79), key=lambda i: -delta[i])[:10]
        assert [t["name"] for t in r["top"]] == [a["objects"][i]["name"] for i in top]
        pos = sum(max(dd, 0.0) for dd in delta)
        if pos > 0:
            assert r["share_of_positive_sum"] == pytest.approx(sum(max(delta[i], 0.0) for i in top) / pos)
        assert r["sum_named"] + r["sum_bridges"] == pytest.approx(sum(delta), abs=1e-9)
