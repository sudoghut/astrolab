"""Assertions that this study's conclusions still hold, read from results/.

Run the study first: python -m astrolab run 003-m02-hubble-tension-distance-ladder
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


def test_summary_exists():
    assert load("summary")


def test_r1_printed_baseline_reproduced():
    r1 = load("r1")
    assert abs(r1["fivelogh0"] - 9.318) < 0.001          # R22: H0 = 73.04
    assert abs(r1["chi2_dof"] - 1.03) < 0.005
    assert r1["verdict"] == "not reproduced"              # the public lstsq file is a different fit


def test_r2_anchor_step_reproduced():
    a = load("r2")["anchor_step"]
    assert a["verdict"] == "reproduced"
    assert abs(a["shift"] - (-0.0158)) <= 0.005


def test_r2_host_step_amended():
    h = load("r2")["host_step"]
    assert h["preregistered_verdict"] == "not evaluable (host identification)"
    assert "amended" in h["status"]
    assert h["z"] <= -2 and abs(h["shift"] - (-0.0405)) <= 2 * h["shift_sigma"] + 0.02
    assert abs(h["shift_check_ay"] - h["shift"]) < 1e-8
    assert abs(h["nested_var_check"] - h["shift_sigma"] ** 2) < 1e-8


def test_host_labelling_unique_cchp_set():
    i = load("host_identification")
    assert i["matching_found"] and not i["alt_changes_cchp_set"]


def test_r3_same_hosts_agree():
    r3 = load("r3")
    assert r3["cchp_match"] == "matched"
    assert abs(r3["d"]) < 2 * r3["sigma_d"]


def test_r4_descriptive():
    r4 = load("r4")
    assert r4["draws"] >= 2000 and 0 <= r4["percentile"] <= 100


def test_r2_re_rule_and_headline():
    """R2-RE (README section 2, addendum 2026-11-16): verdict row recomputed from the saved numbers
    with R2's table, and the headline rule (R2-RE's row is the public host-step verdict)."""
    re_ = load("r2_re")
    s = load("summary")
    h = load("r2")["host_step"]
    est = re_["reml"]
    assert min(est["grid_m2l"]) >= est["m2l_min"] - 1e-9            # tau_hat is at least the grid minimum
    if est["at_upper_bound"]:
        assert re_["status"] == "not evaluable (bound)"
    if re_["status"] != "evaluated":
        assert s["R2_host_headline_source"].startswith("R2 (C errors)")
        return
    hs = re_["host_step"]
    assert abs(hs["z"] - hs["shift"] / hs["shift_sigma"]) < 1e-9
    assert abs(hs["nested_var_check"] - hs["shift_sigma"] ** 2) < 1e-8 * hs["shift_sigma"] ** 2 + 1e-12
    z, d, sh = hs["z"], hs["shift"], hs["shift_sigma"]
    if z <= -2 and abs(d - (-0.0405)) <= 2 * sh + 0.02:
        exp = "host selection significantly lowers H0, by the size the paper reports (supports the paper)"
    elif z <= -2:
        exp = "host selection significantly lowers H0, but by a different size"
    elif abs(z) < 2:
        exp = "no host-selection effect detected in these data (does not support the paper's quantitative claim)"
    else:
        exp = "host selection raises H0 (contradicts the paper)"
    assert re_["verdict"] == exp
    assert h["verdict"].startswith(exp) and s["R2_host"] == h["verdict"]
    assert s["R2_host_headline_source"] == "R2-RE"
    # R2 with C errors stays recorded
    assert h["criterion_outcome"].startswith("host selection significantly lowers H0")
    lo, hi = re_["interval_68"]
    assert (lo == 0.0 or lo <= re_["tau_hat"]) and (not isinstance(hi, float) or hi >= re_["tau_hat"])
