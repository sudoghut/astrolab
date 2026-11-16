"""Exploration (T-026, 2026-11-16): is our post-hoc 69-event O1-O3 set the same set as the 69 BBHs of
the GWTC-3 population paper (arXiv:2111.03634)?

Our 69 = the 59 O1-O3 events of `results/sample.json` (names GW19*/GW20*) plus the ten O1/O2 BBHs that
enter only with the FAR fallback (`explore/gwtc1_far.py`). The paper's event list is taken from its
data release's table archive (Zenodo 11254021 `table_data.tar.gz`, 4.9 kB; a supersedes-v1 record
with no changed results). Run with:
    python -m astrolab explore 007 --tag gwtc3-pop-events --script explore/gwtc3_pop_events.py
"""
import io
import json
import re
import tarfile
from pathlib import Path

TABLES_URL = "https://zenodo.org/records/11254021/files/table_data.tar.gz?download=1"
GWTC1 = ["GW150914", "GW151012", "GW151226", "GW170104", "GW170608", "GW170729", "GW170809",
         "GW170814", "GW170818", "GW170823"]
NAME = re.compile(r"GW\d{6}(?:_\d{6})?")


def ours() -> set[str]:
    sample = json.loads((Path(__file__).parents[1] / "results" / "sample.json").read_text(encoding="utf-8"))
    o3 = {e["name"] for e in sample["events"] if e["name"][:4] in ("GW19", "GW20")}
    return o3 | set(GWTC1)


def main(ctx):
    path = ctx.http(TABLES_URL, label="GWTC-3 population tables (Zenodo 11254021)", suffix=".tar.gz",
                    max_bytes=1024**2)
    members, found = [], {}
    with tarfile.open(path, "r:gz") as tar:
        for m in tar.getmembers():
            members.append({"name": m.name, "size": m.size})
            if not m.isfile() or m.size > 1024**2:
                continue
            text = tar.extractfile(m).read().decode("utf-8", "replace")
            names = sorted(set(NAME.findall(text)))
            if names:
                found[m.name] = names
    ctx.log(f"archive members: {members}")
    mine = ours()
    out = {"members": members, "ours_n": len(mine), "tables_with_event_names": {}}
    for member, names in found.items():
        theirs = set(names)
        out["tables_with_event_names"][member] = {
            "n": len(theirs), "only_in_paper": sorted(theirs - mine), "only_in_ours": sorted(mine - theirs)}
        ctx.log(f"{member}: {len(theirs)} names; only in paper {sorted(theirs - mine)}; "
                f"only in ours {sorted(mine - theirs)}")
    if not found:
        ctx.log("no event names in the table archive")

    # The paper's BBH set: Table 1 (all 76 events used) minus the events of Table 3 (the events
    # whose components may be neutron stars). Table 1 has no BBH column, so this rule is our
    # reading; it is checked against the paper's stated count of 69 BBHs. Names are compared after
    # mapping our short names (GW190412) to the full names that start with them (GW190412_053044).
    t1 = set(found.get("table_data/gwtc-3_pop_events_table_1.csv", []))
    t3 = set(found.get("table_data/gwtc-3_pop_ns_classification_table_3.csv", []))
    ns = {n for n in t1 if any(n == s or n.startswith(s + "_") for s in t3)}
    bbh = t1 - ns

    def full(n):
        # a short name maps to the one full name it starts with that is not itself in our set
        # (GW190521 -> GW190521_030229; GW190521_074359 is a different event we list by full name)
        hits = [m for m in bbh if m == n or (m.startswith(n + "_") and m not in mine)]
        return hits[0] if len(hits) == 1 else n

    mine_full = {full(n) for n in mine}
    out["paper_bbh"] = {"n_table1": len(t1), "n_ns_table3": len(ns), "n_bbh": len(bbh),
                        "only_in_paper": sorted(bbh - mine_full), "only_in_ours": sorted(mine_full - bbh),
                        "same_set": bbh == mine_full,
                        "renamed": sorted(f"{n} = {full(n)}" for n in mine if full(n) != n)}
    ctx.log(f"paper BBH set (Table 1 minus Table 3): {len(bbh)}; same set as ours: {bbh == mine_full}; "
            f"only in paper {sorted(bbh - mine_full)}; only in ours {sorted(mine_full - bbh)}")
    ctx.save("gwtc3_pop_events", out)
    return out
