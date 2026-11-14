"""Release-day helper for the gaia-dr4-release-day skill.

Builds every ADQL string itself (no shell quoting of ADQL), and sends it through the guarded
channel `astrolab.fetch` (AGENTS.md section 1.2). Run from the project root:

  python .claude/skills/gaia-dr4-release-day/dr4_query.py <command> [arg] [--print]

Commands (<schema> is a TAP schema such as gaiadr4; <release> is a key of screen.SCHEMAS such as dr4):
  schemas                      list TAP schemas
  tables   <schema>            tables in a schema (names come back schema-qualified)
  columns  <schema.table>      columns of one table
  types    <schema>            nss_solution_type tally with COUNT(a_thiele_innes): the mechanical
                               rule for astrometric types (README DR4 addendum); aggregate only
  count    <release>           server-side row count of the M4 screen (cuts from run.PARAMS) and of
                               all astrometric orbits
  ids                          print the DR3 ids the DR4 run resolves (no network)
  resolve  <schema>            the pre-registered resolution (selection.resolve_ids, as run.py) of
                               those ids in <schema>.gaia_source, with reasons
  archive  <release>           copy results/*.json to results/<release>/ (no network); refuses if
                               results/ is not that release or the target exists

--print shows the ADQL and does not touch the network. Every query is sent with refresh=True, so
a cached answer from a rehearsal is never served on release day.

This is a skill script, not a study helper module: it imports run.py only to read PARAMS,
RELEASES and TARGETS (AGENTS.md's "helpers do not import run" concerns study modules, whose
PARAMS overrides would not take effect). tests/test_dr4_query.py runs every command with --print.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STUDY = ROOT / "studies" / "001-m04-gaia-dormant-black-holes"
RESULTS = STUDY / "results"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(STUDY))


def _ident(s):
    """Schema or schema.table name; anything else is refused (it is pasted into ADQL)."""
    if not s or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*(\.[A-Za-z_][A-Za-z0-9_]*)?", s):
        raise SystemExit(f"not a schema or table name: {s!r}\n\n{__doc__}")
    return s


def _q(s):
    return f"'{_ident(s)}'"


def _release_of(d):
    for name in ("release.json", "summary.json"):
        if (d / name).exists():
            return json.loads((d / name).read_text(encoding="utf-8")).get("release")
    return None


def dr3_dir():
    for d in (RESULTS / "dr3", RESULTS):
        if _release_of(d) == "dr3":
            print(f"[dr4_query] DR3 reference read from {d.relative_to(ROOT)}", file=sys.stderr)
            return d
    raise SystemExit("no DR3 results (results/dr3/, or results/ with release dr3): restore them from git")


def reference_ids():
    """The archived DR3 reference (source_id, ra, dec, G) the DR4 run resolves."""
    f = dr3_dir() / "reference_ids.json"
    if not f.exists():
        raise SystemExit(f"{f.relative_to(ROOT)} missing: rerun the DR3 study (before 2026-11-25)")
    import pandas as pd
    c = json.loads(f.read_text(encoding="utf-8"))
    ref = pd.DataFrame(c) if isinstance(c, dict) else pd.DataFrame.from_records(c)
    ref["source_id"] = ref.source_id.astype("int64")
    return ref


def _in(ids):
    return ", ".join(str(int(x)) for x in ids)


def queries(cmd, arg):
    if cmd == "schemas":
        return {"schemas": "SELECT schema_name FROM tap_schema.schemas"}
    if cmd == "tables":
        return {"tables": f"SELECT table_name FROM tap_schema.tables WHERE schema_name = {_q(arg)}"}
    if cmd == "columns":
        return {"columns": f"SELECT column_name, unit, description FROM tap_schema.columns WHERE table_name = {_q(arg)}"}
    if cmd == "types":
        s = _ident(arg)
        return {"types": f"SELECT nss_solution_type, COUNT(*) AS n, COUNT(a_thiele_innes) AS n_thiele_innes "
                         f"FROM {s}.nss_two_body_orbit GROUP BY nss_solution_type"}
    if cmd == "resolve":
        s = _ident(arg)
        return {"gaia_source": f"SELECT source_id, ra, dec, pmra, pmdec, phot_g_mean_mag FROM {s}.gaia_source "
                               f"WHERE source_id IN ({_in(reference_ids().source_id)})"}
    raise SystemExit(__doc__)


def count_from_wheres(release):
    from run import PARAMS
    from screen import SCHEMAS, screen_from_where
    if release not in SCHEMAS:
        raise SystemExit(f"count takes a release key of screen.SCHEMAS {sorted(SCHEMAS)}, not {release!r}")
    return {"screen": screen_from_where(release, PARAMS["fm_min"], PARAMS["plx_snr_min"]),
            "astrometric_total": f"{SCHEMAS[release]}.nss_two_body_orbit WHERE a_thiele_innes IS NOT NULL"}


def archive(release, dry):
    from screen import SCHEMAS
    if release not in SCHEMAS:
        raise SystemExit(f"archive takes a release key of screen.SCHEMAS {sorted(SCHEMAS)}, not {release!r}")
    have = _release_of(RESULTS)
    if have != release:
        raise SystemExit(f"results/ holds release {have!r}, not {release!r}: nothing archived")
    dest = RESULTS / release
    if dest.exists():
        raise SystemExit(f"{dest.relative_to(ROOT)} already exists: nothing archived")
    files = sorted(RESULTS.glob("*.json"))
    for f in files:
        print(f"{'would copy' if dry else 'copy'} {f.relative_to(ROOT)} -> {(dest / f.name).relative_to(ROOT)}")
    if not dry:
        dest.mkdir()
        for f in files:
            shutil.copy2(f, dest / f.name)
        print(f"archived {len(files)} files; commit {dest.relative_to(ROOT)} before the next formal run")


def main(argv):
    show = "--print" in argv
    argv = [a for a in argv if a != "--print"]
    if not argv:
        raise SystemExit(__doc__)
    cmd, arg = argv[0], (argv[1] if len(argv) > 1 else None)
    if cmd == "ids":
        ids = reference_ids().source_id
        print(f"DR3 ids resolved by the DR4 run ({len(ids)}): {_in(sorted(ids))}")
        return
    if cmd != "schemas" and arg is None:
        raise SystemExit(f"{cmd} needs an argument\n\n{__doc__}")
    if cmd == "archive":
        archive(arg, show)
        return
    if cmd == "count":
        qs = {k: f"SELECT COUNT(*) AS n FROM {v}" for k, v in count_from_wheres(arg).items()}
    else:
        qs = queries(cmd, arg)
    if show:
        for k, v in qs.items():
            print(f"-- {k}\n{v}\n")
        return
    from astrolab import fetch
    out = {}
    for k, v in qs.items():
        out[k] = df = fetch.tap(v, mode="async", refresh=True, max_rows=5000,
                                note=f"gaia-dr4-release-day {cmd}").data
        print(f"-- {k}: {len(df)} rows")
        print(df.to_string(index=False))
    if cmd == "resolve":
        import selection
        from run import RELEASES
        from screen import SCHEMAS
        release = next((k for k, v in SCHEMAS.items() if v == arg), None)
        if release is None:
            raise SystemExit(f"schema {arg!r} is not in screen.SCHEMAS {SCHEMAS}: update the mapping first")
        res = selection.resolve_ids(reference_ids(), out["gaia_source"], RELEASES[release]["epoch_gap_yr"])
        bad = res[res.dr4_id.isna()]
        print(f"resolved {len(res) - len(bad)}/{len(res)}; unresolved by reason: "
              f"{bad.reason.value_counts().to_dict() or 'none'}")
        if len(bad):
            print(bad.to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1:])
