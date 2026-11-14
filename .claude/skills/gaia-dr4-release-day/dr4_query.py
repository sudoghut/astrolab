"""Release-day helper for the gaia-dr4-release-day skill.

Builds every ADQL string itself (no shell quoting of ADQL), and sends it through the guarded
channel `astrolab.fetch` (AGENTS.md section 1.2). Run from the project root:

  python .claude/skills/gaia-dr4-release-day/dr4_query.py <command> [arg] [--print]

Commands (<schema> is a TAP schema such as gaiadr4; <release> is a key of screen.SCHEMAS such as dr4):
  schemas                      list TAP schemas
  tables   <schema>            tables in a schema (names come back schema-qualified)
  columns  <schema.table>      columns of one table
  types    <schema>            nss_solution_type tally (server-side GROUP BY)
  count    <release>           server-side row count of the M4 screen (cuts read from run.py)
                               and of all astrometric orbits
  ids                          print the DR3 ids the study depends on (no network)
  resolve  <schema>            which of those ids exist in <schema>.gaia_source (with ra, dec, G
                               for an identity check) and which DR4 NSS solutions they have
  followup <schema>            DR4 orbit and RV summary for the DR3 survivors (README s7)

--print shows the ADQL and does not touch the network. Every query is sent with refresh=True, so
a cached answer from a rehearsal is never served on release day.

Coupled to the study code: TARGETS in run.py, the data/ files and the results layout. After any
change to those (T-011), rerun `ids` and every command with --print; tests/test_dr4_query.py does.
"""
import json
import math
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
        raise SystemExit(f"not a schema or table name: {s!r}\n\n{__doc__}")
    return s


def _q(s):
    return f"'{_ident(s)}'"


def dr3_results_dir():
    """The directory holding the DR3 run's results; refuses anything that is not a DR3 run."""
    for d in (STUDY / "results" / "dr3", STUDY / "results"):
        summary = d / "summary.json"
        if summary.exists():
            release = json.loads(summary.read_text(encoding="utf-8")).get("release")
            if release != "dr3":
                raise SystemExit(f"{summary} is from release {release!r}, not dr3: restore the DR3 "
                                 "results (git, or results/dr3/) before using the DR3 survivor list")
            print(f"[dr4_query] DR3 survivors read from {d.relative_to(ROOT)}", file=sys.stderr)
            return d
    raise SystemExit("no DR3 results found (results/dr3/ or results/)")


def _rows(path):
    c = json.loads(path.read_text(encoding="utf-8"))
    return [dict(zip(c, vals)) for vals in zip(*c.values())] if isinstance(c, dict) else c


def study_ids():
    """DR3 source_ids the study is keyed on, by role (read from committed files only)."""
    from run import TARGETS
    ns = json.loads((STUDY / "data" / "ns_candidates_elbadry2024.json").read_text(encoding="utf-8"))
    i = ns["columns"].index("gaia_dr3")
    lit = json.loads((STUDY / "data" / "literature_vetting.json").read_text(encoding="utf-8"))
    rows = _rows(dr3_results_dir() / "bh_candidates.json")
    surv = sorted({int(r["source_id"]) for r in rows
                   if not r["known"] and not r["vetoed"] and r["literature"] != "refuted"})
    return {
        "bh": sorted(int(t["gaia_dr3"]) for t in TARGETS.values()),
        "ns_controls": sorted(int(r[i]) for r in ns["rows"]),
        "literature": sorted(int(r[0]) for r in lit["rows"]),
        "dr3_survivors": surv,
    }


def _in(ids):
    return ", ".join(str(int(x)) for x in ids)


def queries(cmd, arg):
    if cmd == "schemas":
        return {"schemas": "SELECT schema_name FROM tap_schema.schemas"}
    if cmd == "tables":
        return {"tables": f"SELECT table_name FROM tap_schema.tables WHERE schema_name = {_q(arg)}"}
    if cmd == "columns":
        return {"columns": f"SELECT column_name, unit, description FROM tap_schema.columns WHERE table_name = {_q(arg)}"}
    if cmd not in ("types", "resolve", "followup"):
        raise SystemExit(__doc__)
    s = _ident(arg)
    if cmd == "types":
        return {"types": f"SELECT nss_solution_type, COUNT(*) AS n FROM {s}.nss_two_body_orbit GROUP BY nss_solution_type"}
    if cmd == "resolve":
        lst = _in(sorted({x for v in study_ids().values() for x in v}))
        return {"gaia_source": f"SELECT source_id, ra, dec, phot_g_mean_mag FROM {s}.gaia_source WHERE source_id IN ({lst})",
                "nss_two_body_orbit": f"SELECT source_id, nss_solution_type FROM {s}.nss_two_body_orbit WHERE source_id IN ({lst})"}
    lst = _in(study_ids()["dr3_survivors"])
    return {"followup": (
        f"SELECT g.source_id, o.nss_solution_type, o.period, o.period_error, o.eccentricity, o.significance, "
        f"o.parallax, o.a_thiele_innes, o.b_thiele_innes, o.f_thiele_innes, o.g_thiele_innes, "
        f"g.rv_amplitude_robust, g.rv_nb_transits, g.ruwe "
        f"FROM {s}.gaia_source AS g LEFT OUTER JOIN {s}.nss_two_body_orbit AS o ON o.source_id = g.source_id "
        f"WHERE g.source_id IN ({lst})")}


def count_from_wheres(release):
    from run import FM_MIN, PLX_SNR_MIN
    from screen import SCHEMAS, screen_from_where
    if release not in SCHEMAS:
        raise SystemExit(f"count takes a release key of screen.SCHEMAS {sorted(SCHEMAS)}, not {release!r}")
    return {"screen": screen_from_where(release, FM_MIN, PLX_SNR_MIN),
            "astrometric_total": f"{SCHEMAS[release]}.nss_two_body_orbit WHERE a_thiele_innes IS NOT NULL"}


def identity_check(df):
    """Compare DR4 position and G with the DR3 values stored for candidates (epochs differ)."""
    dr3 = {int(r["source_id"]): r for r in _rows(dr3_results_dir() / "bh_candidates.json")}
    for r in df.itertuples():
        old = dr3.get(int(r.source_id))
        if old is None:
            continue
        dra = (r.ra - old["ra"]) * math.cos(math.radians(old["dec"])) * 3600
        ddec = (r.dec - old["dec"]) * 3600
        dg = r.phot_g_mean_mag - old["phot_g_mean_mag"]
        flag = "  <-- check identity" if abs(dg) > 0.3 or math.hypot(dra, ddec) > 2 else ""
        print(f"  {r.source_id}: offset {math.hypot(dra, ddec):.2f} arcsec, dG {dg:+.2f}{flag}")


def main(argv):
    show = "--print" in argv
    argv = [a for a in argv if a != "--print"]
    if not argv:
        raise SystemExit(__doc__)
    cmd, arg = argv[0], (argv[1] if len(argv) > 1 else None)
    if cmd == "ids":
        for role, ids in study_ids().items():
            print(f"{role} ({len(ids)}): {_in(ids)}")
        return
    if cmd != "schemas" and arg is None:
        raise SystemExit(f"{cmd} needs an argument\n\n{__doc__}")
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
        found = set(int(x) for x in out["gaia_source"].source_id)
        for role, ids in study_ids().items():
            miss = [i for i in ids if i not in found]
            print(f"{role}: {len(ids) - len(miss)}/{len(ids)} resolve in gaia_source; missing: {miss or 'none'}")
        print("identity check against the DR3 values stored for candidates:")
        identity_check(out["gaia_source"])


if __name__ == "__main__":
    main(sys.argv[1:])
