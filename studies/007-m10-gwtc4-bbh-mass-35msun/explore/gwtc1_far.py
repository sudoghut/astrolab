"""Exploration (post hoc, 2026-11-15): FAR fallback to a lower-precedence list.

In the registered run the ten O1/O2 BBHs come from GWTC-2.1-confident (their v2 re-analysis, which
outranks GWTC-1 under the registered precedence). Those GWOSC rows carry no `far`, so the rule
"no FAR -> excluded" drops them, while the GWTC-1-confident rows of the same events do carry a FAR.

This script keeps the registered precedence for masses but, when the kept row has a null FAR, takes
the FAR from the first lower-precedence list that has one. Every other rule is unchanged. It does
not change results/. Run with:
    python -m astrolab explore 007 --tag gwtc1-far --script explore/gwtc1_far.py
"""
import gwtc
import run

_merge = gwtc.merge_lists


def main(ctx):
    filled = []

    def merge_lists(lists_in_precedence, labels=None):
        merged, overlaps = _merge(lists_in_precedence, labels)
        labels = labels or [str(i) for i in range(len(lists_in_precedence))]
        for name, row in merged.items():
            if row["far"] is not None:
                continue
            for label, rows in zip(labels, lists_in_precedence):
                other = rows.get(name)
                if other is not None and other is not row and other.get("far") is not None:
                    merged[name] = dict(row, far=other["far"])
                    filled.append({"name": name, "far": other["far"], "from": label})
                    break
        return merged, overlaps

    gwtc.merge_lists = merge_lists
    try:
        out = run.main(ctx)
    finally:
        gwtc.merge_lists = _merge
    ctx.save("far_fallback", {"filled": filled})
    ctx.log(f"FAR taken from a lower-precedence list for {len(filled)} events: "
            + ", ".join(f"{f['name']} {f['far']:.2g} ({f['from']})" for f in filled))
    return out
