"""Diagnose host-column identification: which checks (ii)-(iv) link each column to which host."""
import numpy as np
from scipy import linalg

import run as R
from astrolab import infer


def main(ctx):
    C, L, y, lsq = R.load(ctx)
    hosts = list(dict.fromkeys(h for h, *_ in R.TABLE6))
    nz, cls, counts = R.row_classes(L, y)
    base = infer.gls(L, y, c_factor=linalg.cho_factor(C, lower=True))
    comp, det, ncep, rows_y, sn = R.host_compat(nz, cls, y, base["q"][:R.NH], hosts, R.PARAMS["sn_match_tol"])
    out = []
    for j in range(R.NH):
        out.append({"column": j, "mu_fit": round(float(base["q"][j]), 3), "ceph_rows": int(ncep[j]),
                    "rows_y": [round(float(v), 3) for v in rows_y[j]],
                    "ii": [hosts[k] for k in np.flatnonzero(det["ii"][j])],
                    "iii": [hosts[k] for k in np.flatnonzero(det["iii"][j])],
                    "iv": [hosts[k] for k in np.flatnonzero(det["iv"][j])],
                    "all": [hosts[k] for k in np.flatnonzero(comp[j])]})
    no_col = [hosts[k] for k in range(R.NH) if not comp[:, k].any()]
    ctx.save("diag", {"columns": out, "hosts_without_column": no_col})
    for o in out:
        print(o["column"], o["mu_fit"], o["ceph_rows"], o["rows_y"], "ii:", o["ii"], "iv:", o["iv"], "ALL:", o["all"])
    print("hosts without compatible column:", no_col)
    return {"hosts_without_column": no_col}
