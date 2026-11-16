"""R6-FLOW (README section 2.6), project-environment side: prior support, export, subprocess, verdict.

The flows run in the separate TF environment (flowshift.py). This module writes the needed columns
into one temporary .npz in the cache staging area, starts that environment, reads its JSON result and
applies the pre-registered verdict rule. It does not import run.py; run.py passes PARAMS values in.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

from astrolab import cache, config

HERE = Path(__file__).resolve().parent


def tf_python():
    """The TF environment's interpreter, resolved at run time (never stored in PARAMS or results)."""
    base = os.environ.get("LOCALAPPDATA")
    if not base:
        return None
    exe = Path(base) / "astrolab" / "venv-tf" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    return exe if exe.exists() else None


def support_all(names, chains, formats, ranges, frac_max):
    """README 2.6: the R2 prior-support rule over all six parameters."""
    out, bad, not_checkable = {}, False, []
    for name in names:
        fr = {}
        for a, b in (("des_3x2pt", "cmb"), ("cmb", "des_3x2pt")):
            low = [h.lower() for h in formats[a]["header"]]
            if name not in ranges[b]:
                fr[f"{a}_outside_{b}"] = None
                continue
            x = chains[a]["data"][:, low.index(name)]
            lo, hi = ranges[b][name]
            fr[f"{a}_outside_{b}"] = float(np.sum(chains[a]["w"][(x < lo) | (x > hi)]))
        if all(v is None for v in fr.values()):
            not_checkable.append(name)
        out[name] = fr
        bad = bad or any(isinstance(v, float) and v > frac_max for v in fr.values())
    return {"parameters": out, "fails": bad, "not_checkable": not_checkable,
            "rule": f"weight of each chain outside the other chain's prior range > {frac_max} -> descriptive"}


def columns(chains, formats, names):
    """{'des_<short>': array, 'cmb_<short>': array, ..., 'des_w', 'cmb_w'}; S8 and omega_m included."""
    arrays = {}
    for key, tag in (("des_3x2pt", "des"), ("cmb", "cmb")):
        c = chains[key]
        low = [h.lower() for h in formats[key]["header"]]
        cols = {n.split("--")[-1]: c["data"][:, low.index(n)] for n in names}
        cols["s8"] = c["s8"]
        cols["omega_m"] = c["omega_m"]
        ok = np.all([np.isfinite(v) for v in cols.values()], axis=0)
        for short, v in cols.items():
            arrays[f"{tag}_{short}"] = np.asarray(v[ok], dtype=float)
        arrays[f"{tag}_w"] = np.asarray(c["w"][ok], dtype=float)
    return arrays


def run_flows(arrays, cfg, log):
    """Write the temporary input, run flowshift.py in the TF environment, return its JSON."""
    exe = tf_python()
    if exe is None:
        return {"status": "not evaluable (no TF environment)"}
    tmp_in = cache.staging_path(".npz")
    tmp_cfg = cache.staging_path(".json")
    tmp_out = cache.staging_path(".json")
    proc = None
    try:
        np.savez(tmp_in, **arrays)
        tmp_cfg.write_text(json.dumps(cfg), encoding="utf-8")
        env = dict(os.environ, TF_USE_LEGACY_KERAS="1", PYTHONNOUSERSITE="1", TF_CPP_MIN_LOG_LEVEL="3",
                   MPLBACKEND="Agg")
        env.pop("PYTHONPATH", None)
        workdir = config.cache_dir() / "_staging"
        proc = subprocess.Popen([str(exe), "-I", str(HERE / "flowshift.py"), str(tmp_in), str(tmp_cfg), str(tmp_out)],
                                cwd=workdir, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8", errors="replace")
        tail = []
        for line in proc.stderr:                    # progress, live
            line = line.rstrip("\n")
            tail = (tail + [line])[-5:]
            if line.startswith(("  ", "known-answer", "case ")):
                log(line)
        code = proc.wait()
        partial = json.loads(tmp_out.read_text(encoding="utf-8")) if tmp_out.exists() else {}
        if code != 0 or not partial.get("complete"):
            msg = re.sub(r"[A-Za-z]:[\\/][^\s'\"]*|/(?:home|Users)/[^\s'\"]*", "<path>", "\n".join(tail))
            return {"status": f"not evaluable (TF subprocess failed, code {code})", "stderr_tail": msg[-1000:],
                    "partial": partial}
        return partial
    finally:
        if proc is not None and proc.poll() is None:   # interrupted: do not leave the TF child training
            proc.kill()
            proc.wait()
        for p in (tmp_in, tmp_cfg, tmp_out, tmp_out.with_name(tmp_out.name + ".part")):
            try:
                p.unlink(missing_ok=True)
            except OSError:                             # never mask the original exception
                pass


def verdict(res, support, gate_r1, published, tol, s_max, lb_margin):
    """README 2.6 verdict for the main case; returns (verdict, reason)."""
    if not gate_r1:
        return "not evaluable", "R1 gate failed"
    if "status" in res:
        return "not evaluable", res["status"]
    if not res["gate"]["passed"]:
        return "not evaluable", "known-answer gate failed"
    main = res.get("main")
    reps = main["repetitions"] if main else []
    if not reps or any("n_sigma" not in r or r["n_sigma"] is None or not np.isfinite(r["n_sigma"]) for r in reps):
        return "not evaluable", "a repetition failed or gave a non-finite n_sigma"
    if not all(r["converged"] for r in reps):
        return "not evaluable", "an estimate did not converge"
    if support["fails"]:                            # README 2.6 order: (4) prior support
        return "descriptive (prior support)", "more than 1% of a chain's weight outside the other's prior range"
    if any(r["lower_bound"] for r in reps):         # (5) README 2.6: n_bar and s are not used
        low = min(r["n_sigma"] for r in reps if r["lower_bound"])
        if low > published + tol + lb_margin:
            return "not reproduced", f"smallest lower bound {low:.3f} > {published + tol + lb_margin:.2f}"
        return "not evaluable", "a lower bound not above the fixed band"
    n_bar, s = main["n_bar"], main["s"]
    if s is None or s > s_max:
        return "not evaluable", f"s = {s} > {s_max}"
    band = tol + 2 * s
    return ("reproduced" if abs(n_bar - published) <= band else "not reproduced"), f"band {band:.4f}"
