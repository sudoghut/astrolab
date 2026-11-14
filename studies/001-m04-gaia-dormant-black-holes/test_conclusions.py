"""Pre-registered criteria of M4 (README section 2 and its DR4 addendum), checked against results/.

DR3 criteria read the archived DR3 run (results/dr3/), or results/ while it still holds the DR3
run. DR4 criteria are checked only when results/ holds a DR4 run. Run the study first:
python -m astrolab run 001
"""
import json
from pathlib import Path

import pytest

RESULTS = Path(__file__).parent / "results"


def _release(d):
    for name in ("release.json", "summary.json"):
        if (d / name).exists():
            return json.loads((d / name).read_text(encoding="utf-8")).get("release")
    return None


def _dir(release):
    for d in (RESULTS / release, RESULTS):
        if _release(d) == release:
            return d
    return None


def load(name, release="dr3"):
    d = _dir(release)
    if d is None or not (d / f"{name}.json").exists():
        pytest.skip(f"no {release} {name}.json; run: python -m astrolab run 001")
    return json.loads((d / f"{name}.json").read_text(encoding="utf-8"))


# --- DR3 (pre-registered 2026-11-11) ---------------------------------------------------------

def test_R1_bh1_mass_consistent_with_paper():
    assert load("summary")["R1_BH1"]["pass_2sigma"]


def test_R2_bh2_mass_consistent_with_paper():
    assert load("summary")["R2_BH2"]["pass_2sigma"]


def test_S1_screen_is_mb_scale_and_recovers_bh1_bh2():
    # As pre-registered: M2 > 3 Msun with the PUBLISHED M1 (corrected after referee review)
    s = load("summary")
    assert s["S1_rows_ok"] and s["S1_pass"]


def test_no_rows_silently_dropped_by_server_sqrt():
    assert load("summary")["rows_dropped_null_a0"] == 0


def test_S2_ns_candidate_recall_at_least_90_percent():
    s = load("summary")
    hit, total = map(int, s["S2_ns_recall"].split("/"))
    assert total == 21 and hit >= 19


def test_bh3_has_no_dr3_orbit():
    bh3 = [r for r in load("reproduction") if r["name"] == "Gaia BH3"][0]
    assert bh3["status"].startswith("no Gaia DR3 orbital solution")


def test_D1_dr4_query_generated():
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from screen import SCHEMAS
    assert load("summary")["D1_dr4_query_ok"]
    q = load("dr4_screen_query")["adql"]
    assert f"{SCHEMAS['dr4']}.nss_two_body_orbit" in q and "gaiadr3" not in q


# --- DR3 post-hoc checks (added after the referee review, 2026-11-11) ------------------------

def test_R1b_bh1_matches_published_dr3_only_solution():
    r = load("summary")["post_hoc"]["R1b_bh1_vs_dr3_only_paper"]
    assert abs(r["a0_dev_sigma"]) < 0.5 and abs(r["m2_dev_sigma"]) < 0.5


def test_post_hoc_vetoes_keep_all_positive_controls():
    p = load("summary")["post_hoc"]
    assert p["controls_checked"] == 23 and p["controls_vetoed"] == []


def test_bh3_is_a_control_without_dr3_solution():
    assert load("summary")["post_hoc"]["controls_without_solution"] == ["4318465066420528000"]


def test_rv_prediction_matches_elbadry_table_e1():
    import pandas as pd
    c = pd.DataFrame(load("bh_candidates"))
    paper = {"3640889032890567040": (674, 154), "4373465352415301632": (165, 20),
             "6281177228434199296": (171, 10), "5870569352746779008": (50, 2), "3664684869697065984": (54, 14)}
    for sid, (val, err) in paper.items():
        pred = c[c.source_id == sid].rv_range_pred.iloc[0]
        assert abs(pred - val) < 2 * err, sid


def test_rv_veto_agrees_with_literature_where_rv_exists():
    import pandas as pd
    c = pd.DataFrame(load("bh_candidates"))
    lit = c[(c.literature != "") & c.rv_amplitude_robust.notna()]
    assert len(lit) >= 4
    assert ((lit.literature == "refuted") == lit.veto_rv.astype(bool)).all()


def test_dr3_reference_for_dr4_is_complete():
    # every DR3 id the DR4 run resolves has a DR3 position and G (design plan 008)
    import pandas as pd
    ref = pd.DataFrame(load("reference_ids"))
    c = pd.DataFrame(load("bh_candidates"))
    assert set(c.source_id) <= set(ref.source_id)
    assert ref[["ra", "dec", "phot_g_mean_mag"]].notna().all().all()
    assert c.period_error.notna().all()


# --- DR4 (pre-registered 2026-11-14, before the release) -------------------------------------

def _dr4():
    return load("summary", "dr4")["dr4"]


def test_dr4_criteria_all_reported():
    d = _dr4()
    for key in ("R", "S1", "S2", "V", "F", "S3", "resolution"):
        assert key in d
    assert sum(d["F"]["counts"].values()) == d["F"]["n"] == 51


def test_dr4_verdicts_are_well_formed():
    d = _dr4()
    ok = {"pass", "fail", "not evaluable"}
    assert d["S1"]["verdict"] in ok and d["S2"]["verdict"] in ok and d["V"]["verdict"] in ok
    assert all(r["verdict"] in ok for r in d["R"].values())
