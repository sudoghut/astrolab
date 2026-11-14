"""No-network checks of the DR4 release-day helper (.claude/skills/gaia-dr4-release-day/dr4_query.py).

The helper is coupled to the M4 study code (TARGETS, data/ files, results layout); these tests
make a change there that breaks it fail now rather than on release day.
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / ".claude" / "skills" / "gaia-dr4-release-day" / "dr4_query.py"


def run(*args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    return subprocess.run([sys.executable, str(HELPER), *args], capture_output=True, text=True,
                          encoding="utf-8", env=env, cwd=ROOT, timeout=120)


def test_ids_lists_every_role():
    r = run("ids")
    assert r.returncode == 0, r.stderr
    counts = {line.split(" (")[0]: int(line.split("(")[1].split(")")[0]) for line in r.stdout.splitlines()}
    assert counts["bh"] == 3 and counts["ns_controls"] == 21 and counts["literature"] == 6
    assert counts["dr3_survivors"] > 0


@pytest.mark.parametrize("args, expect", [
    (["schemas"], "FROM tap_schema.schemas"),
    (["tables", "gaiadr4"], "schema_name = 'gaiadr4'"),
    (["columns", "gaiadr4.gaia_source"], "table_name = 'gaiadr4.gaia_source'"),
    (["types", "gaiadr4"], "FROM gaiadr4.nss_two_body_orbit GROUP BY nss_solution_type"),
    (["count", "dr4"], "FROM gaiadr4.nss_two_body_orbit WHERE a_thiele_innes IS NOT NULL"),
    (["resolve", "gaiadr4"], "FROM gaiadr4.gaia_source WHERE source_id IN ("),
    (["followup", "gaiadr4"], "LEFT OUTER JOIN gaiadr4.nss_two_body_orbit"),
])
def test_print_builds_adql_without_network(args, expect):
    r = run(*args, "--print")
    assert r.returncode == 0, r.stderr
    assert expect in r.stdout


@pytest.mark.parametrize("args", [["count"], ["count", "gaiadr4"], ["tables", "x' OR 1=1"], ["types", "a;b"]])
def test_bad_arguments_are_refused_with_a_message(args):
    r = run(*args, "--print")
    assert r.returncode != 0
    assert "Traceback" not in r.stderr
