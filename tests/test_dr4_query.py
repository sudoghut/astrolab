"""No-network checks of the DR4 release-day helper (.claude/skills/gaia-dr4-release-day/dr4_query.py).

The helper is coupled to the M4 study (run.PARAMS/RELEASES, screen.SCHEMAS, results/reference_ids.json);
these tests make a change there that breaks it fail now rather than on release day.
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / ".claude" / "skills" / "gaia-dr4-release-day" / "dr4_query.py"
RESULTS = ROOT / "studies" / "001-m04-gaia-dormant-black-holes" / "results"


def run(*args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, str(HELPER), *args], capture_output=True, text=True,
                          encoding="utf-8", env=env, cwd=ROOT, timeout=120)


needs_reference = pytest.mark.skipif(
    not (RESULTS / "reference_ids.json").exists() and not (RESULTS / "dr3" / "reference_ids.json").exists(),
    reason="run the DR3 study first (reference_ids.json)")


@needs_reference
def test_ids_lists_the_reference_ids():
    r = run("ids")
    assert r.returncode == 0, r.stderr
    n = int(r.stdout.split("(")[1].split(")")[0])
    assert n >= 100   # 87 DR3 candidates + 21 NS + BH3 + literature, overlapping: 109 on DR3


@pytest.mark.parametrize("args, expect", [
    (["schemas"], "FROM tap_schema.schemas"),
    (["tables", "gaiadr4"], "schema_name = 'gaiadr4'"),
    (["columns", "gaiadr4.gaia_source"], "table_name = 'gaiadr4.gaia_source'"),
    (["types", "gaiadr4"], "COUNT(a_thiele_innes) AS n_thiele_innes FROM gaiadr4.nss_two_body_orbit GROUP BY"),
    (["count", "dr4"], "FROM gaiadr4.nss_two_body_orbit WHERE a_thiele_innes IS NOT NULL"),
    pytest.param(["resolve", "gaiadr4"], "FROM gaiadr4.gaia_source WHERE source_id IN (", marks=needs_reference),
])
def test_print_builds_adql_without_network(args, expect):
    r = run(*args, "--print")
    assert r.returncode == 0, r.stderr
    assert expect in r.stdout


def _current_release():
    import json
    for name in ("release.json", "summary.json"):
        f = RESULTS / name
        if f.exists():
            return json.loads(f.read_text(encoding="utf-8")).get("release")
    return None


@pytest.mark.skipif(_current_release() is None, reason="no results/ yet")
def test_archive_dry_run_refuses_wrong_release():
    other = "dr4" if _current_release() == "dr3" else "dr3"
    r = run("archive", other, "--print")
    assert r.returncode != 0 and "nothing archived" in r.stderr and "Traceback" not in r.stderr


@pytest.mark.parametrize("args", [["count"], ["count", "gaiadr4"], ["tables", "x' OR 1=1"], ["types", "a;b"],
                                  ["archive", "dr9"], ["followup", "gaiadr4"]])
def test_bad_arguments_are_refused_with_a_message(args):
    r = run(*args, "--print")
    assert r.returncode != 0
    assert "Traceback" not in r.stderr
