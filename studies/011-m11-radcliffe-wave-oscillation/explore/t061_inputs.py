"""T-061 input check, before the addendum (README 4.11) is written: layout and names only.

Fetches (via ctx.http, about 113 KB in all) the Zucker et al. 2020 sightline distance table (Major Cloud
Catalog, Dataverse doi:10.7910/DVN/07L7YZ), the Alves et al. 2020 bridging sightlines ("Tenuous
Connections", doi:10.7910/DVN/K16GQX) and K24's best-fit model curve (doi:10.7910/DVN/F98QHY), and reads the
cached K24 12CO table. Prints row counts, column layout, the Zucker names with their sightline counts and how
the 12CO names match them (normalised names; README 4.11 fixes the map by hand); it fits nothing.
"""
import re
from pathlib import Path

import pandas as pd

HANDBOOK_URL = "https://dataverse.harvard.edu/api/access/datafile/4361456"
BRIDGING_URL = "https://dataverse.harvard.edu/api/access/datafile/4361453"
BESTFIT_URL = "https://dataverse.harvard.edu/api/access/datafile/8954305"
CLOUDS_URL = "https://dataverse.harvard.edu/api/access/datafile/7211929"


def norm(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def main(ctx):
    ph = ctx.http(HANDBOOK_URL, label="Zucker et al. 2020 Table A.1 (Dataverse doi:10.7910/DVN/07L7YZ, file 4361456)")
    pb = ctx.http(BRIDGING_URL, label="Alves et al. 2020 bridging sightlines (doi:10.7910/DVN/K16GQX, file 4361453)")
    pf = ctx.http(BESTFIT_URL, label="K24 best-fit model curve (doi:10.7910/DVN/F98QHY, file 8954305)")
    po = ctx.http(CLOUDS_URL, label="K24 12CO cloud table (Dataverse doi:10.7910/DVN/Q7F4PC, file 7211929)")
    out = []
    for lab, p in (("handbook", ph), ("bridging", pb), ("bestfit", pf)):
        raw = Path(p).read_text(encoding="utf-8", errors="replace").splitlines()
        out.append(f"== {lab}: {len(raw)} lines, {Path(p).stat().st_size} bytes")
        out += [f"   head: {ln[:110]}" for ln in raw[:3]]
    co = pd.read_csv(po, sep="\t")
    out.append(f"== 12CO: {len(co)} rows, columns {list(co.columns)}")
    hb = pd.read_csv(ph, sep=r"\s+", comment="#", engine="python")
    br = pd.read_csv(pb, sep=r"\s+", comment="#", engine="python")
    out.append(f"handbook columns {list(hb.columns)}; bridging columns {list(br.columns)}")
    counts = hb["name"].astype(str).value_counts()
    out.append(f"Zucker sightlines: {len(hb)} in {len(counts)} names; bridging: {len(br)}")
    out.append("Zucker names with counts: " + "; ".join(f"{k}:{v}" for k, v in sorted(counts.items())))
    bridges = set(br["name"].astype(str))
    zn = {norm(k): k for k in counts.index}
    rows = []
    for n in co["name"].astype(str):
        if n in bridges:
            rows.append(f"{n}=bridge")
        else:
            rows.append(f"{n}->{zn.get(norm(n), '?')}")
    out.append("12CO names (exact bridge match, or normalised Zucker name): " + ", ".join(rows))
    for ln in out:
        ctx.log(ln[:2000])
