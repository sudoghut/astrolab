"""Release-day helper for the gaia-dr4-release-day skill.

Builds every ADQL string itself (no shell quoting of ADQL), and sends it through the guarded
channel `astrolab.fetch` (AGENTS.md section 1.2). Run from the project root:

  python .claude/skills/gaia-dr4-release-day/dr4_query.py <command> [args] [--print]

Commands:
  schemas                      list TAP schemas
  tables  <schema>             tables in a schema (names come back schema-qualified)
  columns <schema.table>       columns of one table
  types   <schema>             nss_solution_type tally (server-side GROUP BY)
  count   <release>            server-side row count of the M4 screen and of all astrometric orbits
  ids                          print the DR3 ids the study depends on (no network)
  resolve <schema>             which of those ids exist in <schema>.gaia_source / nss_two_body_orbit

--print shows the ADQL and does not touch the network. All queries use refresh=True, so a
cached answer from a rehearsal is never served on release day.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STUDY = ROOT / "studies" / "001-m04-gaia-dormant-black-holes"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(STUDY))


def _ident(s):
    """Schema or schema.table name; anything else is refused (it is pasted into ADQL)."""
    if not s or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?", s):
        raise SystemExit(f"not a schema or table name: {s!r}")
    return s


def _q(s):
    return f"'{_ident(s)}'"


def study_ids():
    """DR3 source_ids the study is keyed on, by role (read from committed files only)."""
    from run import TARGETS
    bh = {name: t["gaia_dr3"] for name, t in TARGETS.items()}
    ns = json.loads((STUDY / "data" / "ns_candidates_elbadry2024.json").read_text(encoding="utf-8"))
    i = ns["columns"].index("gaia_dr3")
    lit = json.loads((STUDY / "data" / "literature_vetting.json").read_text(encoding="utf-8"))
    # the DR3 survivors: prefer the archived DR3 copy (step 3), since a DR4 run overwrites results/
    dr3 = STUDY / "results" / "dr3" / "bh_candidates.json"
    c = json.loads((dr3 if dr3.exists() else STUDY / "results" / "bh_candidates.json").read_text(encoding="utf-8"))
    rows = [dict(zip(c, vals)) for vals in zip(*c.values())] if isinstance(c, dict) else c
    surv = sorted({int(r["source_id"]) for r in rows
                   if not r["known"] and not r["vetoed"] and r["literature"] != "refuted"})
    return {
        "bh": sorted(bh.values()),
        "ns_controls": sorted(int(r[i]) for r in ns["rows"]),
        "literature": sorted(int(r[0]) for r in lit["rows"]),
        "dr3_survivors": surv,
    }


def queries(cmd, arg):
    if cmd == "schemas":
        return {"schemas": "SELECT schema_name FROM tap_schema.schemas"}
    if cmd == "tables":
        return {"tables": f"SELECT table_name FROM tap_schema.tables WHERE schema_name = {_q(arg)}"}
    if cmd == "columns":
        return {"columns": f"SELECT column_name, unit, description FROM tap_schema.columns WHERE table_name = {_q(arg)}"}
    if cmd == "types":
        return {"types": f"SELECT nss_solution_type, COUNT(*) AS n FROM {_ident(arg)}.nss_two_body_orbit GROUP BY nss_solution_type"}
    if cmd == "resolve":
        arg = _ident(arg)
        ids = sorted({x for v in study_ids().values() for x in v})
        lst = ", ".join(map(str, ids))
        return {"gaia_source": f"SELECT source_id FROM {arg}.gaia_source WHERE source_id IN ({lst})",
                "nss_two_body_orbit": f"SELECT source_id, nss_solution_type FROM {arg}.nss_two_body_orbit WHERE source_id IN ({lst})"}
    raise SystemExit(__doc__)


def main(argv):
    show = "--print" in argv
    argv = [a for a in argv if a != "--print"]
    if not argv:
        raise SystemExit(__doc__)
    cmd, arg = argv[0], (argv[1] if len(argv) > 1 else None)
    if cmd == "ids":
        for role, ids in study_ids().items():
            print(f"{role} ({len(ids)}): {', '.join(map(str, ids))}")
        return
    if cmd == "count":
        from screen import SCHEMAS, screen_from_where
        fw = {"screen": screen_from_where(arg),
              "astrometric_total": f"{SCHEMAS[arg]}.nss_two_body_orbit WHERE a_thiele_innes IS NOT NULL"}
        if show:
            for k, v in fw.items():
                print(f"-- {k}\nSELECT COUNT(*) AS n FROM {v}\n")
            return
        from astrolab import fetch
        for k, v in fw.items():
            print(k, fetch.tap_count(v, refresh=True))
        return
    if arg is None and cmd != "schemas":
        raise SystemExit(__doc__)
    qs = queries(cmd, arg)
    if show:
        for k, v in qs.items():
            print(f"-- {k}\n{v}\n")
        return
    from astrolab import fetch
    for k, v in qs.items():
        df = fetch.tap(v, mode="async", refresh=True, max_rows=5000).data
        print(f"-- {k}: {len(df)} rows")
        print(df.to_string(index=False))
    if cmd == "resolve":
        want = study_ids()
        found = set(int(x) for x in fetch.tap(qs["gaia_source"], mode="async", max_rows=5000).data.source_id)
        for role, ids in want.items():
            miss = [i for i in ids if i not in found]
            print(f"{role}: {len(ids) - len(miss)}/{len(ids)} resolve in gaia_source; missing: {miss or 'none'}")


if __name__ == "__main__":
    main(sys.argv[1:])
