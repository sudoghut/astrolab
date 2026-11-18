"""Assertions that this study's conclusions still hold, read from results/.

Run the study first: python -m astrolab run 004-m07-wide-binaries-gravity-test
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


def test_r1_different_sample():
    r1 = load("summary")["R1"]
    assert r1["verdict"] == "different sample"
    assert r1["N_main"] == 639
    assert r1["target"] == 1421 and not r1["within_20pct"]


def test_r2_cannot_distinguish():
    s = load("summary")
    L = s["R2_L"]
    # pre-registered thresholds (README section 2): >= 100 Newton, <= 1/100 MOND, else cannot distinguish
    derived = "Newton" if L >= 100 else "MOND" if L <= 1 / 100 else "cannot distinguish"
    assert derived == "cannot distinguish"
    assert s["R2"].startswith(derived)
    assert abs(L - 0.4857) < 5e-4


def test_mad_errors_favour_mond():
    # C26's stated MAD/sqrt(N) errors turn the same medians into "MOND favoured":
    # the error convention, not the data, decides (Lean gap gap_err).
    mad = load("variants")["main"]["reproduction"]["mad"]
    assert mad["valid"] and mad["L"] < 1 / 100


def test_r3_variants():
    # descriptive (README R3): six fits invalid by the >5%-redrawn rule, every valid one
    # "cannot distinguish"
    v = load("variants")
    invalid = {k for k, m in v.items() if m["primary"]["verdict"].startswith("invalid")}
    assert invalid == {"cleanest_vt1.5_ipd0", "no_hr", "hr_c_plus_0.2", "hr_c_minus_0.2",
                       "d150_ipd0", "ipd0"}
    for k, m in v.items():
        if k not in invalid:
            assert m["primary"]["verdict"].startswith("cannot distinguish"), k
            assert 1 / 100 < m["primary"]["L"] < 100, k


# ---------------------------------------------------------------- R5 (README 2.1, T-034)
def test_r5_label_rederived_from_saved_results():
    """Re-derive the R5 label from results/r5.json with the pre-registered table (skip if R5 has
    not been run)."""
    s = load("r5")
    if "label" not in s:
        pytest.skip("r5.json holds a retry record, not a final outcome")
    label = s["label"]
    if "g1b" in s:
        g = s["g1b"]
        if g.get("evaluable", True) and "L_N" in g:
            assert g["passes"] == (g["L_N"] >= 100 and g["L_M"] <= 0.01)
        if g["passes"]:
            assert "insufficient predicted power" not in label
    unbl = bool(s.get("blinding", {}).get("n4_read_before_merge"))
    prefix = "R5 (unblinded, descriptive): " if unbl else "R5: "
    if "g1b" in s and not s["g1b"]["passes"]:
        assert label == "R5: not run (insufficient predicted power)"
        return
    if "main" not in s:
        assert label in ("R5: not run (data not obtained)", "R5: not run (insufficient predicted power)") \
            or s.get("stopped_after_g1b")
        return
    m = s["main"]
    if not m.get("valid"):
        assert label == prefix + "invalid fit (no label)"
        return
    L, g2 = m["fit"]["L"], m["fit"]["g2"]["passes"]
    gg = m["fit"]["g2"]
    assert g2 == (gg["L_N_data"] >= 100 and gg["L_M_data"] <= 0.01)
    if g2:
        body = ("Newton has the higher relative likelihood (agrees with C26's conclusion)" if L >= 100 else
                "MOND has the higher relative likelihood (contradicts C26)" if L <= 0.01 else "cannot distinguish")
    else:
        grade = ("Newton weakly preferred" if L >= 10 else "MOND weakly preferred" if L <= 0.1 else "no preference")
        body = f"no verdict at C26's strength (insufficient power, data-conditional); {grade} (descriptive)"
    assert label == prefix + body
    # G2 is the symmetric rule: both noise-free values recorded
    assert {"L_N_data", "L_M_data", "passes"} <= set(m["fit"]["g2"])


def test_r5_variant_grades_consistent():
    s = load("r5")
    if "label" not in s:
        pytest.skip("r5.json holds a retry record, not a final outcome")
    for name, v in s.get("variants", {}).items():
        if v.get("valid"):
            L = v["fit"]["L"]
            want = "Newton" if L >= 10 else "MOND" if L <= 0.1 else "no preference"
            assert v["fit"]["grade"].startswith(want), name
