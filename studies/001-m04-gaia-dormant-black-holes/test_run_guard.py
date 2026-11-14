"""No-network tests of run.py's results guard and DR3 reference lookup (design plan 008, section 2.4)."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

import importlib.util

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
_spec = importlib.util.spec_from_file_location("m04_run_for_guard_tests", HERE / "run.py")
run = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(run)


def ctx_for(results: Path, formal=True):
    st = SimpleNamespace(results_dir=results)
    return SimpleNamespace(study=st, results=results if formal else results.parent / "explore-out")


def mark(d: Path, release: str, finished="t1"):
    d.mkdir(parents=True, exist_ok=True)
    (d / "release.json").write_text(json.dumps({"release": release}), encoding="utf-8")
    (d / "run_info.json").write_text(json.dumps({"finished_at": finished}), encoding="utf-8")


def test_formal_dr4_run_refused_until_dr3_archived(tmp_path):
    res = tmp_path / "results"
    mark(res, "dr3")
    with pytest.raises(SystemExit, match="archive dr3"):
        run.guard_results(ctx_for(res), "dr4")
    mark(res / "dr3", "dr3")
    run.guard_results(ctx_for(res), "dr4")       # archived: allowed


def test_guard_works_in_both_directions(tmp_path):
    res = tmp_path / "results"
    mark(res, "dr4")
    with pytest.raises(SystemExit, match="archive dr4"):
        run.guard_results(ctx_for(res), "dr3")


def test_guard_falls_back_to_summary_and_skips_explorations(tmp_path):
    res = tmp_path / "results"
    res.mkdir()
    (res / "summary.json").write_text(json.dumps({"release": "dr3"}), encoding="utf-8")
    with pytest.raises(SystemExit):
        run.guard_results(ctx_for(res), "dr4")
    run.guard_results(ctx_for(res, formal=False), "dr4")   # explorations never touch results/
    run.guard_results(ctx_for(res), "dr3")                 # same release: allowed


def test_dr3_reference_prefers_archive(tmp_path):
    res = tmp_path / "results"
    mark(res, "dr3")
    assert run.dr3_reference_dir(ctx_for(res)) == res
    mark(res / "dr3", "dr3")
    assert run.dr3_reference_dir(ctx_for(res)) == res / "dr3"
    mark(res, "dr4")
    assert run.dr3_reference_dir(ctx_for(res)) == res / "dr3"


def test_params_and_releases_are_consistent():
    from screen import SCHEMAS
    assert set(run.RELEASES) == set(SCHEMAS)
    assert run.PARAMS["release"] in run.RELEASES
    assert run.RELEASES["dr4"]["covariance_trusted"] is False   # until confirmed from documentation
    assert run.TARGETS["Gaia BH3"]["m1"] == 0.76 and run.TARGETS["Gaia BH3"]["m1_err"] == 0.05


def test_stale_archive_is_refused(tmp_path):
    res = tmp_path / "results"
    mark(res / "dr3", "dr3", finished="t1")
    mark(res, "dr3", finished="t2")          # DR3 rerun after archiving
    with pytest.raises(SystemExit, match="older"):
        run.guard_results(ctx_for(res), "dr4")


def test_unknown_release_is_refused():
    from types import SimpleNamespace as NS
    old = run.PARAMS["release"]
    run.PARAMS["release"] = "dr5"
    try:
        with pytest.raises(SystemExit, match="release must be one of"):
            run.main(NS())
    finally:
        run.PARAMS["release"] = old
