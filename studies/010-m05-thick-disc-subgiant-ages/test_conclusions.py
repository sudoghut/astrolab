"""Assertions that this study's results follow the pre-registered rules (README 2.1–2.3), read from
results/. They recompute each verdict from the saved numbers.

Run the study first: python -m astrolab run 010-m05-thick-disc-subgiant-ages
"""
import json
from pathlib import Path

import pytest

RESULTS = Path(__file__).parent / "results"


def load(name):
    path = RESULTS / f"{name}.json"
    if not path.exists():
        pytest.skip(f"{path.name} missing; run the study first")
    return json.loads(path.read_text(encoding="utf-8"))


def test_checks_and_mock_budget():
    s = load("summary")
    assert s["checks"]["n_rows"] == s["params"]["n_rows"]
    assert s["checks"]["id_unique"]
    m = s["mocks"]
    expected = s["params"]["n_mock"] if m["mode"] == "full" else s["params"]["n_mock_reduced"]
    assert m["n_per_set"] == expected
    assert m["n_sets"] == 66


def test_r1_bins_follow_threshold_rule():
    r1 = load("r1")
    for sample, bins in r1["bins"].items():
        for b in bins:
            assert b["d_star"] <= 0.25 + 1e-12
            assert b["almost_disjoint"] == (b["d"] < b["d_star"] and b["edge"] is not None)
            assert b["resolvable"] == all(v >= 0.80 for v in b["power"].values())


def test_r1_verdict_rule():
    r1 = load("r1")
    for sample, bins in r1["bins"].items():
        res = [b for b in bins if b["resolvable"]]
        disj = [b for b in res if b["almost_disjoint"]]
        v = r1["verdict"][sample]["verdict"]
        if len(res) < 3:
            assert v == "undetermined"
            continue
        edges = sorted(b["edge"] for b in disj if b["edge"] is not None)
        med = None
        if edges:
            n = len(edges)
            med = edges[n // 2] if n % 2 else 0.5 * (edges[n // 2 - 1] + edges[n // 2])
        ok = len(disj) >= 3 and med is not None and 6.5 <= med <= 9.5
        assert v == ("reproduced" if ok else "not reproduced")
    assert r1["robust"] == (r1["verdict"]["S15"]["verdict"] == r1["verdict"]["Full"]["verdict"])


def test_r2_verdict_rule():
    r2 = load("r2")
    mu = r2["primary"]["mu"]
    assert r2["verdict"] == ("reproduced" if 12.5 <= mu <= 13.5 else "not reproduced")


def test_r34_recovery_and_primary():
    r34 = load("r34")
    rec = r34["recovery"]
    for mech, v in rec.items():
        ok = abs(v["sigma"]["bias"]) <= 0.1 and abs(v["a"]["bias"]) <= 0.2
        assert v["pass"] == ok, mech
    if rec["rA"]["pass"]:
        assert r34["primary"].startswith("S15")
    elif rec["rtau"]["pass"]:
        assert r34["primary"].startswith("Full")
    else:
        assert r34["verdict"]["R3"] == "cannot determine"
        assert r34["verdict"]["R4"] == "cannot determine"


def test_r34_verdict_rules():
    r34 = load("r34")
    R3, R4 = r34["verdict"]["R3"], r34["verdict"]["R4"]
    if R3 == "cannot determine":
        return
    fit = r34["sampleA"] if r34["primary"].startswith("S15") else r34["sampleA_sensitivity"]["full"]
    assert R3.startswith("reproduced") == (4.5 <= fit["span"] <= 6.5)
    assert R4.startswith("reproduced") == (abs(fit["sigma"] - 0.82) <= 0.1)


def test_intrinsic_scatter_rule():
    r34 = load("r34")
    v = r34["verdict"]["intrinsic"]
    biased = any(abs(b["bias"]) > 0.1 for b in r34["sampleB_mock_bias"].values())
    s, se = r34["sampleB"]["sigma"], r34["sampleB_se_used"]
    assert se >= r34["sampleB"]["sigma_err"] - 1e-12
    if biased:
        assert v == "cannot determine"
    elif s + 1.645 * se < 0.82:
        assert v == "confirmed"
    elif s - 1.645 * se >= 0.82:
        assert v == "not confirmed"
    else:
        assert v == "cannot determine"


def test_summary_matches_parts():
    s, r1, r2, r34 = load("summary"), load("r1"), load("r2"), load("r34")
    assert s["R1"] == r1["verdict"]
    assert s["R2"]["verdict"] == r2["verdict"]
    assert s["R3"] == r34["verdict"]["R3"] and s["R4"] == r34["verdict"]["R4"]
    assert s["intrinsic"]["verdict"] == r34["verdict"]["intrinsic"]


def test_result_files_small():
    for path in RESULTS.glob("*.json"):
        assert path.stat().st_size < 1024 ** 2, path.name



# ---------------------------------------------------------------------------------------------
# R-SEL re-test (README 2.5, T-031): every -SEL label and qualifier re-derived from the saved files
# ---------------------------------------------------------------------------------------------
NMOCK = 50
NONFINITE = "cannot determine (non-finite mock results)"


def _median(xs):
    xs = sorted(xs)
    n = len(xs)
    return None if not n else (xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2]))


def _r1_verdict(bins):
    res = [b for b in bins if b["resolvable"]]
    disj = [b for b in res if b["almost_disjoint"]]
    if len(res) < 3:
        return "undetermined"
    med = _median([b["edge"] for b in disj if b["edge"] is not None])
    return "reproduced" if (len(disj) >= 3 and med is not None and 6.5 <= med <= 9.5) else "not reproduced"


def _cat(label):
    i = label.find(" (")
    return label[:i] if i >= 0 and label.endswith(")") else label


def _sel_qual(e, n):
    return "selection-term robust" if _cat(e) == _cat(n) else "selection-term sensitive"


def _rob_word(x):
    return "robust" if x else "not robust"


def _edge_loop(trace):
    """SEL-3 edge loop re-derived from the saved trace [edge, has valley, true d]: returns the kept
    edge, its true d and validity, and checks the trace follows the loop."""
    assert abs(trace[0][0] - 7.0) < 1e-9
    for i in range(1, len(trace)):
        assert abs(trace[i][0] - (trace[i - 1][0] - 0.5)) < 1e-9
        assert trace[i - 1][1] and trace[i - 1][2] > 0.1          # lowered only while valley and d > 0.1
    e, v, d = trace[-1]
    if v and d <= 0.1:
        return e, d, True
    if not v:
        return (e, d, False) if len(trace) == 1 else (trace[-2][0], trace[-2][2], False)
    assert abs(e - 2.0) < 1e-9                                     # lowest candidate reached
    return e, d, False


def _sel_sets_expected():
    out = []
    for v in ("S15E", "S15N", "Full"):
        for b in range(5):
            for kind in ("null_sn", "null_sp", "power"):
                for mech in ("rtau", "rA"):
                    out.append(("R1", v, b, kind, mech, "primary"))
    for term in ("E", "N"):
        for mech in ("rtau", "rA"):
            out.append(("A_rec", term, "rec", mech))
    for term in ("E", "N"):
        for kind in ("id", "mis"):
            for mech in ("rtau", "rA"):
                out.append(("B", term, kind, mech))
    for term in ("E", "N"):
        for mech in ("rtau", "rA"):
            out.append(("diag", term, "diag", mech))
    for v in ("S15E", "S15N", "Full"):
        for b in (2, 3, 4):
            for mech in ("rtau", "rA"):
                out.append(("R1", v, b, "power", mech, "sens"))
    return out


def _set_tuple(s):
    if s["tag"] == "R1":
        return ("R1", s["variant"], s["bin"], s["kind"], s["mech"], s["floor"])
    return (s["tag"], s["term"], s["kind"], s["mech"])


def _r1_bins_check(bins, null_from=None, sens=False):
    nf = 0
    for i, b in enumerate(bins):
        nfb = 0                                  # non-finite mocks of this bin only
        src = null_from[i] if null_from is not None else b
        q = []
        for key in ("null_sn_rtau", "null_sn_rA", "null_sp_rtau", "null_sp_rA"):
            m = src["mocks"][key]
            assert len(m["d"]) == NMOCK and len(m["valley"]) == NMOCK
            assert m["k"] < 90
            nfb += sum(d is None for d in m["d"])
            ds = sorted(d for d, v in zip(m["d"], m["valley"]) if v and d is not None)
            q.append(ds[2] if len(ds) >= 3 else 0.25)
        dstar = min([0.25] + q)
        if not nfb:
            assert abs(b["d_star"] - dstar) < 1e-12
        pm = b["power_model"]
        for mech in ("rtau", "rA"):
            m = b["mocks"]["power_" + mech]
            assert len(m["d"]) == NMOCK
            nfb += sum(d is None for d in m["d"])
            in_sens = sens and i in (2, 3, 4)
            assert (m["k"] >= 106) == in_sens
            pw = sum(1 for d, v in zip(m["d"], m["valley"]) if v and d is not None and d < dstar) / NMOCK
            if not nfb:
                assert abs(b["power"][mech] - pw) < 1e-12
        floor = 0.20 if (sens and i in (2, 3, 4)) else 0.12
        assert pm["floor"] == floor and pm["w_old"] == max(pm["w_old_raw"], floor)
        edge, td, valid = _edge_loop(pm["edge_trace"])
        assert pm["young"][1] == edge and pm["true_d"] == td and pm["valid"] == valid
        assert b["power_model_invalid"] == (not valid)
        res = all(v >= 0.80 for v in b["power"].values()) and valid
        assert b["resolvable"] == res
        assert b["almost_disjoint"] == bool(b["valley"] and b["d"] < b["d_star"] and b["edge"] is not None)
        nf += nfb
    return nf


def test_sel_r1_labels():
    r1, sel = load("r1_sel"), load("sel")
    assert r1["n_mock"] == NMOCK and r1["q_rank"] == 3 and r1["floor"] == 0.12 and r1["floor_sens"] == 0.20
    for name in ("S15E", "S15N", "Full"):
        var = r1["variants"][name]
        nf = _r1_bins_check(var["bins"])
        assert bool(nf) == bool(var["nonfinite"])
        assert var["verdict"] == (NONFINITE if nf else _r1_verdict(var["bins"]))
        sens = r1["floor_sensitivity"][name]
        nfs = _r1_bins_check(sens["bins"], null_from=var["bins"], sens=True)
        assert bool(nfs) == bool(sens["nonfinite"])
        assert sens["verdict"] == (NONFINITE if nfs else _r1_verdict(sens["bins"]))
    for key, part in (("label", "variants"), ("label_floor_sensitivity", "floor_sensitivity")):
        e, n, f = (r1[part][x]["verdict"] for x in ("S15E", "S15N", "Full"))
        lab = r1[key]
        rob = _cat(e) == _cat(f)
        assert lab["bare"] == e and lab["robust"] == rob and lab["selection_term"] == _sel_qual(e, n)
        assert lab["label"] == e + " (" + _rob_word(rob) + "; " + _sel_qual(e, n) + ")"
    assert sel["labels"]["R1-SEL"] == r1["label"]["label"]
    assert sel["labels"]["R1-SEL_floor_0.20"] == r1["label_floor_sensitivity"]["label"]


def _with_robust(v, rob):
    return v + ("" if v != "reproduced" else (", robust" if rob else ", not robust"))


def _bias(values, true):
    d = [x - true for x in values]
    mu = sum(d) / len(d)
    mc = (sum((x - mu) ** 2 for x in d) / (len(d) - 1)) ** 0.5 / len(d) ** 0.5
    return mu, mc


def _near(saved, mu, mc, tol):
    assert abs(saved["bias"] - mu) < 1e-9 and abs(saved["mc_err"] - mc) < 1e-9
    return abs(abs(mu) - tol) <= mc


def test_sel_r34_labels():
    r34, sel = load("r34_sel"), load("sel")
    assert r34["n_mock"] == NMOCK
    bare = {}
    for t in ("E", "N"):
        T = r34["terms"][t]
        rec = T["recovery"]
        nf = any(x is None for m in rec.values() for x in m["sigma_values"] + m["a_values"])
        assert nf == bool(T["nonfinite"])
        if not nf:
            for mech, x in rec.items():
                assert len(x["sigma_values"]) == NMOCK and len(x["a_values"]) == NMOCK
                bs, ms = _bias(x["sigma_values"], T["sampleA"]["sigma"])
                ba, ma = _bias(x["a_values"], T["sampleA"]["a"])
                near = _near(x["sigma"], bs, ms, 0.1) or _near(x["a"], ba, ma, 0.2)
                assert x["near_tolerance"] == near
                assert x["pass"] == (abs(bs) <= 0.1 and abs(ba) <= 0.2)
        if nf:
            prim, fit = None, None
        elif rec["rA"]["pass"]:
            prim, fit = "S15", T["sampleA"]
            assert T["flag_rtau_recovery_failed"] == (not rec["rtau"]["pass"])
        elif rec["rtau"]["pass"]:
            prim, fit = "Full", r34["shared_full_fits"]["full"]
        else:
            prim, fit = None, None
        assert T["primary"] == prim
        es = T["error_scale"]
        f_ii = (1 + T["sampleA"]["sigma"] ** 2 / es["e2_mean"]) ** 0.5
        assert abs(es["f_ii"] - f_ii) < 1e-9 and abs(es["f_max"] - min(es["f_i"], f_ii)) < 1e-9
        fits = {**r34["shared_full_fits"], **T["robustness_fits"]}
        if prim == "S15":
            r3s, r4s = {"full", "feh_err", "f_min", "f_max"}, {"full", "feh_err"}
        elif prim == "Full":
            r3s, r4s = {"feh_err_full", "full_f_min", "full_f_max"}, {"feh_err_full"}
        else:
            r3s = r4s = set()
        assert set(T["R3"]["set"]) == r3s and set(T["R4"]["set"]) == r4s
        if nf:
            r3 = r4 = NONFINITE
        elif fit is None:
            r3 = r4 = "cannot determine"
        else:
            r3 = "reproduced" if 4.5 <= fit["span"] <= 6.5 else "not reproduced"
            r4 = "reproduced" if abs(fit["sigma"] - 0.82) <= 0.1 else "not reproduced"
        rob3 = bool(r3s) and all(4.5 <= fits[k]["span"] <= 6.5 for k in r3s)
        rob4 = bool(r4s) and all(abs(fits[k]["sigma"] - 0.82) <= 0.1 for k in r4s)
        assert T["R3"]["bare"] == r3 and T["R4"]["bare"] == r4
        assert T["R3"]["label"] == _with_robust(r3, rob3) and T["R4"]["label"] == _with_robust(r4, rob4)
        bare[t] = (r3, r4)
    for i, name in enumerate(("R3", "R4")):
        q = _sel_qual(bare["E"][i], bare["N"][i])
        assert r34["terms"]["E"][name]["label_full"] == r34["terms"]["E"][name]["label"] + "; " + q
        assert r34["labels"][name + "-SEL"] == r34["terms"]["E"][name]["label_full"]
        assert sel["labels"][name + "-SEL"] == r34["labels"][name + "-SEL"]
        assert r34["labels"]["term_N"][name] == r34["terms"]["N"][name]["label"]


def test_sel_intrinsic_labels():
    r34, sel = load("r34_sel"), load("sel")
    bare = {}
    for t in ("E", "N"):
        I = r34["intrinsic"][t]
        assert len(I["mock_bias"]) == 4
        nf = any(x is None for b in I["mock_bias"].values() for x in b["sigma_values"])
        assert nf == bool(I["nonfinite"])
        if nf:
            v0, vf = NONFINITE, {k: NONFINITE for k in I["sampleB_f"]}
            assert I["bare"] == v0 and I["f_labels"] == vf
        else:
            for b in I["mock_bias"].values():
                assert len(b["sigma_values"]) == NMOCK
                mu, mc = _bias(b["sigma_values"], I["sampleB"]["sigma"])
                assert b["near_tolerance"] == _near(b, mu, mc, 0.1)
            ids = I["mock_bias"]["id_rtau"]["sigma_values"] + I["mock_bias"]["id_rA"]["sigma_values"]
            mu = sum(ids) / len(ids)
            sd = (sum((x - mu) ** 2 for x in ids) / (len(ids) - 1)) ** 0.5
            assert abs(sd - I["sd_id"]) < 1e-9
            biased = any(abs(b["bias"]) > 0.1 for b in I["mock_bias"].values())

            def lab(fit):
                if fit["sigma_err"] is None:
                    return "cannot determine (non-finite standard error)", None
                se = max(fit["sigma_err"], sd)
                if biased:
                    return "cannot determine", se
                if fit["sigma"] + 1.645 * se < 0.82:
                    return "confirmed", se
                if fit["sigma"] - 1.645 * se >= 0.82:
                    return "not confirmed", se
                return "cannot determine", se
            v0, se0 = lab(I["sampleB"])
            assert I["bare"] == v0
            assert (I["se_used"] is None and se0 is None) or abs(I["se_used"] - se0) < 1e-12
            vf = {k: lab(x)[0] for k, x in I["sampleB_f"].items()}
            assert I["f_labels"] == vf
        rob = _cat(v0) == _cat(vf["f_min"]) == _cat(vf["f_max"])
        assert I["robust"] == rob and I["label"] == v0 + ", " + _rob_word(rob)
        bare[t] = v0
    E = r34["intrinsic"]["E"]
    assert E["label_full"] == E["label"] + "; " + _sel_qual(bare["E"], bare["N"])
    assert sel["labels"]["intrinsic-SEL"] == E["label_full"] == r34["labels"]["intrinsic-SEL"]
    assert r34["labels"]["term_N"]["intrinsic"] == r34["intrinsic"]["N"]["label"]


def test_sel_mock_counts_and_seeds():
    sel = load("sel")
    m = sel["mocks"]
    assert m["n_per_set"] == NMOCK and m["n_sets"] == 124 and m["n_main_sets"] == 106
    assert [s["k"] for s in sel["sets"]] == list(range(124))
    assert [_set_tuple(s) for s in sel["sets"]] == _sel_sets_expected()     # SEL-8 loop nest
    assert sel["params"]["sel_seed_tag"] == 31 and sel["params"]["sel_n_mock"] == NMOCK
    for p in m["projections"]:                       # the run stops before remaining mocks above the limit
        assert p["mocks_left"] == 0 or p["projection_h"] <= p["limit_h"]
