"""Bookkeeping of the R-SEL re-test (README 2.5): the mock-set list and seed numbering (SEL-8),
the R1 power-model edge loop (SEL-3), the runtime projection with the 16 h stop, per-mock
checkpoints in the system cache, and the label rules. Pure helpers: nothing here reads PARAMS or
imports run.py; every setting is an argument.
"""
from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path

import numpy as np

R1_VARIANTS = ("S15E", "S15N", "Full")          # SEL-8 order; R1 data-fit sample codes below
R1_CODES = {"S15E": 0, "Full": 1, "S15N": 2}
R1_KINDS = ("null_sn", "null_sp", "power")
TERMS = ("E", "N")
B_KINDS = ("id", "mis")


# --------------------------------------------------------------------------------------------
# mock sets and seeds (SEL-8)
# --------------------------------------------------------------------------------------------
def sel_sets(nbins, mechs, sens_bins):
    """All re-test mock sets in the SEL-8 loop nest, numbered k = 0, 1, ...; 'group' is the
    projection kind (R1, AB = samples A/B, diag = SEL-2 diagnostic)."""
    sets = []

    def add(**kw):
        sets.append({"k": len(sets), **kw})
    for v in R1_VARIANTS:
        for b in range(nbins):
            for kind in R1_KINDS:
                for mech in mechs:
                    add(tag="R1", variant=v, bin=b, kind=kind, mech=mech, floor="primary", group="R1")
    for term in TERMS:
        for mech in mechs:
            add(tag="A_rec", term=term, kind="rec", mech=mech, group="AB")
    for term in TERMS:
        for kind in B_KINDS:
            for mech in mechs:
                add(tag="B", term=term, kind=kind, mech=mech, group="AB")
    for term in TERMS:
        for mech in mechs:
            add(tag="diag", term=term, kind="diag", mech=mech, group="diag")
    for v in R1_VARIANTS:
        for b in sens_bins:
            for mech in mechs:
                add(tag="R1", variant=v, bin=b, kind="power", mech=mech, floor="sens", group="R1")
    return sets


def mock_rng(seed, tag, k, j):
    """Per-mock stream default_rng([seed, 31, k, j]) (SEL-8)."""
    return np.random.default_rng([int(seed), int(tag), int(k), int(j)])


# --------------------------------------------------------------------------------------------
# R1 power model: young-edge loop (SEL-3)
# --------------------------------------------------------------------------------------------
def candidate_edges(start, step, stop):
    out = []
    x = float(start)
    while x >= stop - 1e-9:
        out.append(round(x, 9))
        x -= step
    return out


def edge_loop(evaluate, *, start=7.0, step=0.5, stop=2.0, dmax=0.1):
    """evaluate(edge) -> (has_valley, d). The edge is lowered only while the generating model has
    a valley with d > dmax; the first edge with a valley and d <= dmax is the power model. No
    valley at the start edge: edge kept, invalid. Valley lost at a lower edge: the last edge with
    a valley is kept, invalid. Lowest candidate reached without d <= dmax: invalid."""
    cands = candidate_edges(start, step, stop)
    trace = []
    v, d = evaluate(cands[0])
    trace.append([cands[0], bool(v), float(d)])
    if not v:
        return {"edge": cands[0], "true_d": float(d), "valid": False,
                "reason": "no valley at the start edge", "trace": trace}
    if d <= dmax:
        return {"edge": cands[0], "true_d": float(d), "valid": True, "reason": None, "trace": trace}
    last = (cands[0], float(d))
    for edge in cands[1:]:
        v, d = evaluate(edge)
        trace.append([edge, bool(v), float(d)])
        if not v:
            return {"edge": last[0], "true_d": last[1], "valid": False,
                    "reason": "valley lost at a lower edge (last edge with a valley kept)", "trace": trace}
        last = (edge, float(d))
        if d <= dmax:
            return {"edge": edge, "true_d": float(d), "valid": True, "reason": None, "trace": trace}
    return {"edge": last[0], "true_d": last[1], "valid": False,
            "reason": "lowest candidate edge reached with d > dmax", "trace": trace}


# --------------------------------------------------------------------------------------------
# runtime projection (SEL-8)
# --------------------------------------------------------------------------------------------
def projection_h(elapsed_s, state, n_mock):
    """elapsed + sum over unfinished sets of (remaining mocks x the mean time per mock of finished
    sets of the same group; a group without a finished set uses each set's first-mock time).
    state: k -> {'group', 'times': [seconds per finished mock, in mock order]}."""
    fin = {}
    for st in state.values():
        if len(st["times"]) >= n_mock:
            fin.setdefault(st["group"], []).extend(st["times"][:n_mock])
    rem = 0.0
    for st in state.values():
        left = n_mock - len(st["times"])
        if left <= 0:
            continue
        if st["group"] in fin:
            rem += left * float(np.mean(fin[st["group"]]))
        elif st["times"]:
            rem += left * float(st["times"][0])
    return (elapsed_s + rem) / 3600.0


def peak_memory_mb():
    """Peak working set (Windows) or peak resident size of this process, if psutil is available."""
    try:
        import psutil
    except ImportError:
        return None
    mi = psutil.Process().memory_info()
    peak = getattr(mi, "peak_wset", None)
    if peak is None:
        try:
            import resource
            peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024
        except Exception:
            peak = mi.rss
    return round(peak / 1024 ** 2, 1)


# --------------------------------------------------------------------------------------------
# per-mock checkpoints in the system cache (SEL-8)
# --------------------------------------------------------------------------------------------
class StopRun(RuntimeError):
    """Raised when the runtime projection exceeds the stop limit (SEL-8)."""


class MockStore:
    """One folder per key (PARAMS, code, catalogue) under root. Each finished mock is a JSON file
    written atomically; a session ledger accumulates elapsed time across sessions. A folder left by
    a 16 h stop (stopped.json) is resumed only when resume_consent.txt exists (the user's consent,
    recorded in log.md); the consent is used once."""

    def __init__(self, root, key, *, stale_days=7.0):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        for old in self.root.iterdir():        # abandoned folders of older keys
            try:
                if (old.is_dir() and old.name != key and not (old / "lock").exists()
                        and not (old / "stopped.json").exists()
                        and time.time() - old.stat().st_mtime > stale_days * 86400):
                    shutil.rmtree(old, ignore_errors=True)
            except OSError:
                pass
        self.dir = self.root / key
        self.dir.mkdir(parents=True, exist_ok=True)
        self.lock = self.dir / "lock"
        try:
            fd = os.open(self.lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(fd)
        except FileExistsError:
            raise RuntimeError(f"another run is using the R-SEL checkpoint folder {self.dir}; if no other "
                               "run is active, delete its lock file and rerun") from None
        stopped, consent = self.dir / "stopped.json", self.dir / "resume_consent.txt"
        self.resumed = False
        if stopped.exists():
            if not consent.exists():
                self.release()
                raise StopRun(f"the R-SEL run was stopped by the runtime rule ({stopped}). Resuming needs "
                              "the user's explicit consent (README 2.5 SEL-8): record it in log.md, then "
                              f"create {consent} and rerun.")
            info = {"stopped": json.loads(stopped.read_text(encoding="utf-8")),
                    "consent": consent.read_text(encoding="utf-8").strip(), "resumed_at": time.time()}
            hist = self.dir / "resumes.json"
            prev = json.loads(hist.read_text(encoding="utf-8")) if hist.exists() else []
            self._write(hist, prev + [info])
            stopped.unlink()
            consent.unlink()
            self.resumed = True
        self.sessions = self.dir / "sessions"
        self.sessions.mkdir(exist_ok=True)
        self.session = self.sessions / f"{time.time_ns()}_{os.getpid()}.json"
        self.t0 = time.time()
        self.tick()

    @staticmethod
    def _write(path, obj):
        tmp = path.with_name(path.name + f".{os.getpid()}.tmp")
        tmp.write_text(json.dumps(obj), encoding="utf-8")
        os.replace(tmp, path)

    def _path(self, k, j):
        return self.dir / f"k{int(k):03d}_j{int(j):02d}.json"

    def get(self, k, j):
        p = self._path(k, j)
        if not p.exists():
            return None
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(rec, dict) and "result" in rec and "seconds" in rec:
                return rec
        except ValueError:
            pass
        p.unlink(missing_ok=True)              # damaged: computed again
        return None

    def put(self, k, j, result, seconds):
        self._write(self._path(k, j), {"result": result, "seconds": float(seconds)})
        self.tick()

    def tick(self):
        self._write(self.session, {"seconds": time.time() - self.t0})

    def elapsed_s(self):
        """Total elapsed time over all sessions of this folder."""
        self.tick()
        tot = 0.0
        for p in self.sessions.glob("*.json"):
            try:
                tot += float(json.loads(p.read_text(encoding="utf-8"))["seconds"])
            except (ValueError, KeyError, OSError):
                pass
        return tot

    def stop(self, info):
        self._write(self.dir / "stopped.json", info)
        self.release()

    def release(self):
        try:
            self.lock.unlink(missing_ok=True)
        except OSError:
            pass

    def finish(self):
        self.release()
        shutil.rmtree(self.dir, ignore_errors=True)


# --------------------------------------------------------------------------------------------
# labels (README 2.1, 2.3, 2.5)
# --------------------------------------------------------------------------------------------
def r1_verdict(bins, min_bins=3, edge_range=(6.5, 9.5)):
    """2.1 verdict from per-bin dicts with resolvable, almost_disjoint, edge."""
    res = [b for b in bins if b["resolvable"]]
    disj = [b for b in res if b["almost_disjoint"]]
    if len(res) < min_bins:
        return "undetermined", None
    edges = [b["edge"] for b in disj if b["edge"] is not None]
    med = float(np.median(edges)) if edges else None
    ok = len(disj) >= min_bins and med is not None and edge_range[0] <= med <= edge_range[1]
    return ("reproduced" if ok else "not reproduced"), med


def selterm(bare_e, bare_n):
    return "selection-term robust" if bare_e == bare_n else "selection-term sensitive"


def r1_label(v_e, v_n, v_full):
    """R1-SEL: the S15 term-E verdict; robust if Full gives the same verdict; selection-term
    qualifier from S15 term N."""
    rob = v_e == v_full
    return {"bare": v_e, "robust": bool(rob), "selection_term": selterm(v_e, v_n),
            "label": f"{v_e} ({'robust' if rob else 'not robust'}; {selterm(v_e, v_n)})"}


def recovery_pass(bias_sigma, bias_a, tol_sigma, tol_a):
    return abs(bias_sigma) <= tol_sigma and abs(bias_a) <= tol_a


def primacy(pass_ra, pass_rtau):
    """2.3 / SEL-4: 'S15' (flag if only rtau fails), 'Full', or None (cannot determine)."""
    if pass_ra:
        return "S15", (not pass_rtau)
    if pass_rtau:
        return "Full", False
    return None, False


def r34_bare(primary_fit, span_range, sigma_paper, sigma_tol):
    if primary_fit is None:
        return "cannot determine", "cannot determine"
    r3 = "reproduced" if span_range[0] <= primary_fit["span"] <= span_range[1] else "not reproduced"
    r4 = "reproduced" if abs(primary_fit["sigma"] - sigma_paper) <= sigma_tol else "not reproduced"
    return r3, r4


def with_robust(v, rob):
    """2.3 labelling: only a 'reproduced' verdict carries ', robust' / ', not robust'."""
    return v + ("" if v != "reproduced" else (", robust" if rob else ", not robust"))


def intrinsic_bare(sigma, se, biases, tol, z, sigma_paper):
    if any(abs(b) > tol for b in biases):
        return "cannot determine"
    if sigma + z * se < sigma_paper:
        return "confirmed"
    if sigma - z * se >= sigma_paper:
        return "not confirmed"
    return "cannot determine"
