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


def _clean(text):
    return re.sub(r"[A-Za-z]:[\\/][^\s'\"]*|/(?:home|Users)/[^\s'\"]*", "<path>", text)


def run_flows(arrays, cfg, log):
    """Run flowshift.py in the TF environment, one job per process (TensorFlow memory is freed when
    each process exits). Each finished job is kept in a folder in the cache keyed by the input, the
    configuration and flowshift.py, so a stopped run resumes and repeats at most the unfinished job;
    the folder is removed once all jobs are done. Returns the assembled results (README 2.6)."""
    import hashlib
    import shutil
    import sys

    exe = tf_python()
    if exe is None:
        return {"status": "not evaluable (no TF environment)"}
    if str(HERE) not in sys.path:
        sys.path.insert(0, str(HERE))
    import flowshift                     # pure helpers only; no TensorFlow import at module level

    h = hashlib.sha256()                 # content key (np.savez files carry timestamps)
    for k in sorted(arrays):
        h.update(k.encode())
        h.update(np.ascontiguousarray(arrays[k]).tobytes())
    h.update(json.dumps(cfg, sort_keys=True).encode())
    h.update((HERE / "flowshift.py").read_bytes())
    jobdir = config.cache_dir() / "r6flow_jobs" / h.hexdigest()[:24]
    jobdir.mkdir(parents=True, exist_ok=True)
    inp, cfgp = jobdir / "input.npz", jobdir / "config.json"
    if not inp.exists():
        tmp_in = cache.staging_path(".npz")
        np.savez(tmp_in, **arrays)
        os.replace(tmp_in, inp)
    cfgp.write_text(json.dumps(cfg), encoding="utf-8")
    env = dict(os.environ, TF_USE_LEGACY_KERAS="1", PYTHONNOUSERSITE="1", TF_CPP_MIN_LOG_LEVEL="3",
               MPLBACKEND="Agg")
    env.pop("PYTHONPATH", None)

    def job(*parts):
        out = jobdir / ("_".join(str(p) for p in parts) + ".json")
        if out.exists():                 # finished in an earlier, stopped run
            return json.loads(out.read_text(encoding="utf-8"))
        proc = subprocess.Popen([str(exe), "-I", str(HERE / "flowshift.py"), str(inp), str(cfgp), str(out),
                                 *[str(p) for p in parts]], cwd=jobdir, env=env,
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8", errors="replace")
        try:
            err = proc.stderr.read()
            code = proc.wait()
        finally:
            if proc.poll() is None:      # interrupted: do not leave the TF child training
                proc.kill()
                proc.wait()
        if code != 0 or not out.exists():
            raise RuntimeError(f"job {parts} failed (code {code}): {_clean(err)[-800:]}")
        return json.loads(out.read_text(encoding="utf-8"))

    try:
        res = job("meta")
        exact = job("exact")
        reps = []
        for k in cfg["gate"]["seeds"]:
            r = job("gate", k)
            reps.append(r)
            log(f"  gate seed {k}: {r.get('n_sigma', r.get('error'))} (exact {exact['n_sigma']:.4f})")
        res["gate"] = flowshift.gate_summary(exact, reps, cfg["gate"])
        if res["gate"]["passed"]:
            for name, case in cfg["cases"].items():
                log(f"case {name}: {case['columns']}")
                creps = []
                for k in case["seeds"]:
                    r = job("case", name, k)
                    creps.append(r)
                    log(f"  {name} seed {k}: {r.get('n_sigma', r.get('error'))}")
                res[name] = flowshift.case_summary(creps, case["columns"])
    except RuntimeError as exc:
        return {"status": "not evaluable (TF subprocess failed)", "error": str(exc)[-1000:],
                "resume": "rerun: finished jobs are kept in the cache and reused"}
    shutil.rmtree(jobdir, ignore_errors=True)
    res["complete"] = True
    return flowshift.finite(res)


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
