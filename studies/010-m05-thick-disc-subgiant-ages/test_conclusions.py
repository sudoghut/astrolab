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
