"""Fitting machinery of study 011: checkpoints, MCMC, maximum likelihood, mocks, the T5 pipeline.

Every tunable arrives as an argument (run.py passes PARAMS values); this module never imports run.
"""
from __future__ import annotations

import hashlib
import math
import os
import pickle
import time
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

import stats011 as S
import wave011 as W


# ---------------------------------------------------------------------------------------------
# Checkpoints (outside the project folder) and the time guard

def replace_with_retry(src, dst, tries=5, wait=0.2):
    """os.replace with retries: on Windows a scanner or sync client can hold the file briefly."""
    for i in range(tries):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            if i == tries - 1:
                raise
            time.sleep(wait * (2 ** i))


class Paused(Exception):
    """Raised when the run's time budget is used up; rerunning continues from the checkpoints."""


class Store:
    def __init__(self, root: Path, key: str, stop_after_s: float | None = None):
        self.dir = Path(root) / key
        self.dir.mkdir(parents=True, exist_ok=True)
        self.t0 = time.time()
        self.stop_after_s = stop_after_s

    def _p(self, name):
        return self.dir / f"{name}.pkl"

    def has(self, name):
        return self._p(name).exists()

    def get(self, name, default=None):
        p = self._p(name)
        if not p.exists():
            return default
        with open(p, "rb") as f:
            return pickle.load(f)

    def put(self, name, obj):
        p = self._p(name)
        tmp = p.with_suffix(".tmp")
        with open(tmp, "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
        replace_with_retry(tmp, p)

    def check_time(self, where=""):
        if self.stop_after_s is not None and time.time() - self.t0 > self.stop_after_s:
            raise Paused(f"time budget used up at {where}; rerun to continue from {self.dir}")

    def cached(self, name, fn):
        """Return the stored value of `name`, computing and storing it if missing."""
        if self.has(name):
            return self.get(name)
        self.check_time(name)
        val = fn()
        self.put(name, val)
        return val

    def delete(self, name):
        p = self._p(name)
        if p.exists():
            p.unlink()

    def size_bytes(self):
        return sum(f.stat().st_size for f in self.dir.glob("*") if f.is_file())

    def remove_all(self):
        """Delete this run's checkpoint folder (after all results are written)."""
        import shutil
        shutil.rmtree(self.dir, ignore_errors=True)
        return not self.dir.exists()


class NullStore(Store):
    """No checkpoints (unit tests)."""

    def __init__(self):
        self.t0 = time.time()
        self.stop_after_s = None
        self._mem = {}

    def has(self, name):
        return name in self._mem

    def get(self, name, default=None):
        return self._mem.get(name, default)

    def put(self, name, obj):
        self._mem[name] = obj

    def delete(self, name):
        self._mem.pop(name, None)

    def size_bytes(self):
        return 0

    def remove_all(self):
        self._mem.clear()
        return True


def checkpoint_key(params: dict, sources: list[Path], data_sha: list[str]) -> str:
    h = hashlib.sha256()
    h.update(repr(sorted((k, repr(v)) for k, v in params.items())).encode())
    for p in sources:
        h.update(Path(p).read_bytes())
    for s in data_sha:
        h.update(str(s).encode())
    return h.hexdigest()[:20]


# ---------------------------------------------------------------------------------------------
# MCMC (emcee), chunked and resumable

def init_walkers(model: W.Model, center_vec, n_walkers, rng, ball=0.05):
    th0 = model.theta_of(center_vec)
    sc = model.scales()
    pos = []
    tries = 0
    while len(pos) < n_walkers:
        tries += 1
        if tries > 200 * n_walkers:
            raise RuntimeError("could not place walkers at a finite posterior")
        p = th0 + ball * sc * rng.standard_normal(len(th0))
        if np.isfinite(model.logpost(p)):
            pos.append(p)
    return np.array(pos)


def keep_mask(start, n, burn, thin):
    """Which of the steps start .. start + n - 1 are kept: post-burn and every thin-th after burn."""
    g = np.arange(start, start + n)
    return (g >= burn) & ((g - burn) % thin == 0)


def run_mcmc(model: W.Model, center_vec, *, seed, n_walkers, n_steps, n_burn, store: Store, name: str,
             chunk=250, log=print, min_tau_mult=50.0, thin_keep=10):
    """emcee with n_walkers x n_steps; reruns once with twice the steps if the post-burn chain is
    shorter than min_tau_mult autocorrelation times (README 4.2). Returns a summary dict with the
    post-burn samples thinned by thin_keep.

    Checkpoints are compact (README 4.9, item 13): only the walkers' last state and the post-burn chain
    thinned by thin_keep are stored. The autocorrelation time is estimated on that thinned chain and
    multiplied by thin_keep. The running state is deleted once the chain's final summary is stored."""
    import emcee

    def one(steps, burn, tag):
        key = f"{name}_{tag}"
        done = store.get(key + "_final")
        if done is not None:
            return done
        st = store.get(key + "_state")
        ndim = len(model.setup.free)
        if st is None:
            rng = np.random.default_rng(seed)
            p0 = init_walkers(model, center_vec, n_walkers, rng)
            rs = np.random.RandomState(seed % (2 ** 32))
            st = {"n_done": 0, "kept": np.zeros((0, n_walkers, ndim), np.float32),
                  "lnp": np.zeros((0, n_walkers), np.float32),
                  "state": emcee.State(p0, random_state=rs.get_state()), "accepted": np.zeros(n_walkers)}
        while st["n_done"] < steps:
            store.check_time(f"{key} step {st['n_done']}")
            n = min(chunk, steps - st["n_done"])
            sampler = emcee.EnsembleSampler(n_walkers, ndim, model.logpost)
            state = sampler.run_mcmc(st["state"], n, progress=False)
            m = keep_mask(st["n_done"], n, burn, thin_keep)
            st["kept"] = np.concatenate([st["kept"], sampler.get_chain()[m].astype(np.float32)])
            st["lnp"] = np.concatenate([st["lnp"], sampler.get_log_prob()[m].astype(np.float32)])
            st["accepted"] = st["accepted"] + sampler.backend.accepted
            st["state"] = state
            st["n_done"] += n
            store.put(key + "_state", st)
        post = st["kept"].astype(float)
        tau = emcee.autocorr.integrated_time(post, tol=0) * thin_keep
        res = {"samples": st["kept"].reshape(-1, ndim), "lnp": st["lnp"].reshape(-1), "tau": tau.tolist(),
               "tau_max": float(np.max(tau)), "n_steps": steps, "n_burn": burn, "n_walkers": n_walkers,
               "thin": thin_keep, "acceptance": float(np.mean(st["accepted"]) / steps),
               "long_enough": bool(np.all(np.isfinite(tau)) and steps - burn >= min_tau_mult * np.max(tau)),
               "free": list(model.setup.free)}
        store.put(key + "_final", res)
        store.delete(key + "_state")
        return res

    res = one(n_steps, n_burn, "a")
    res["rerun"] = False
    if not res["long_enough"]:
        log(f"{name}: post-burn chain {n_steps - n_burn} < {min_tau_mult} tau ({res['tau_max']:.0f}); "
            f"rerunning with {2 * n_steps} steps")
        res = one(2 * n_steps, 2 * n_burn, "b")
        res["rerun"] = True
    res["chain_short"] = not res["long_enough"]
    return res


def posterior_median_vector(model: W.Model, samples):
    return model.full(np.median(samples, axis=0))


# ---------------------------------------------------------------------------------------------
# Maximum likelihood

def wrap_w0t(model: W.Model, theta):
    th = np.array(theta, float)
    if "w0t" in model.setup.free:
        i = model.setup.free.index("w0t")
        th[i] = float(W.wrap_pi(th[i]))
    return th


def canonical(model: W.Model, theta):
    """Map (w0t, phi) to the identical model with w0t in [-pi/2, pi/2) and phi nearest its prior mean.

    (w0t + pi, phi + pi) gives the same z and v_z, so the MCMC prior range U(-pi/2, pi/2) loses nothing."""
    th = wrap_w0t(model, theta)
    f = model.setup.free
    if "w0t" in f and "phi" in f:
        i, j = f.index("w0t"), f.index("phi")
        if th[i] >= math.pi / 2:
            th[i] -= math.pi
            th[j] -= math.pi
        elif th[i] < -math.pi / 2:
            th[i] += math.pi
            th[j] += math.pi
    if "phi" in f:
        j = f.index("phi")
        mu = W.PRIOR_GAUSS["phi"][0]
        th[j] = mu + float(W.wrap_pi(th[j] - mu))
    return th


def _bounds(model: W.Model):
    b = []
    for n in model.setup.free:
        b.append((0.0, 1.0) if n == "B" else (None, None))
    return b


def optimise(model: W.Model, start, *, nm_maxfev, lbfgs_maxfun=3000, objective="like", bounds=None):
    """Nelder-Mead then L-BFGS-B from one start; w0t periodic (wrapped), B in [0, 1].

    objective: "like" (log likelihood), "post" (log posterior) or a callable theta -> value to maximise
    (README 4.11 Part C's curve fit); a non-finite value scores 1e12. bounds: per free parameter (lo, hi)
    with None for unbounded, replacing the default (only B bounded)."""
    if callable(objective):
        fn = objective
    else:
        fn = model.loglike if objective == "like" else model.logpost
    n_eval = [0]

    def f(th):
        n_eval[0] += 1
        th = wrap_w0t(model, th)
        val = fn(th)
        return -val if np.isfinite(val) else 1e12

    x0 = np.array(start, float)
    bnds = _bounds(model) if bounds is None else [tuple(b) for b in bounds]
    for i, (lo, hi) in enumerate(bnds):
        if lo is not None:
            x0[i] = min(max(x0[i], lo), hi)
    sc = model.scales()
    simplex = [x0]
    for i in range(len(x0)):
        x = x0.copy()
        step = 0.5 * sc[i]
        lo, hi = bnds[i]
        if hi is not None and x[i] + step > hi:
            step = -step
        x[i] += step
        simplex.append(x)
    r1 = minimize(f, x0, method="Nelder-Mead", bounds=bnds,
                  options={"maxfev": nm_maxfev, "initial_simplex": np.array(simplex),
                           "xatol": 1e-4, "fatol": 1e-5, "adaptive": True})
    x1 = r1.x
    r2 = minimize(f, x1, method="L-BFGS-B", bounds=bnds, options={"maxfun": lbfgs_maxfun})
    x2, f2 = (r2.x, r2.fun) if r2.fun <= r1.fun else (x1, r1.fun)
    return {"theta": wrap_w0t(model, x2), "value": -float(f2), "n_eval": n_eval[0]}


def ml_fit(model: W.Model, starts, *, nm_maxfev, lbfgs_maxfun=3000, with_map=True):
    """Best of several starts (maximum likelihood). Returns theta, lnL, inliers, MAP alongside."""
    best = None
    vals = []
    n_eval = 0
    for st in starts:
        r = optimise(model, st, nm_maxfev=nm_maxfev, lbfgs_maxfun=lbfgs_maxfun)
        n_eval += r["n_eval"]
        vals.append(r["value"])
        if best is None or r["value"] > best["value"]:
            best = r
    th = best["theta"]
    v = model.full(th)
    ev = model.evaluate(v)
    out = {"theta": th, "vector": v, "lnL": float(best["value"]), "start_values": vals, "n_eval": n_eval,
           "inlier": (~ev["cl_outlier"]) if "cl_outlier" in ev else None}
    if with_map:
        r = optimise(model, canonical(model, th), nm_maxfev=nm_maxfev, lbfgs_maxfun=lbfgs_maxfun, objective="post")
        out["map_theta"] = r["theta"]
        out["map_vector"] = model.full(r["theta"])
        out["map_logpost"] = r["value"]
    return out


def to_model(src: W.Model, dst: W.Model, theta):
    """Express src's theta in dst's free parameters (fixed values of src become values in dst)."""
    return dst.theta_of(src.full(theta))


# ---------------------------------------------------------------------------------------------
# Mocks (README 4.3)

def mock_vectors(model: W.Model, v_gen, base_data: W.Data, inlier, rng, *, noise="gauss", sigma=47.0,
                 resid=None):
    """Return (x, y, z, vz) arrays of one mock: each inlier placed at the generating model's point
    closest to it (4-D) plus noise; outliers keep their observed values."""
    m = model.clone(data=base_data)
    ev = m.evaluate(v_gen)
    wv = ev["wave"]
    div = m.divisor(v_gen)
    D = m.cluster_vectors(v_gen)
    Mp = m.model_vectors(wv, v_gen)[ev["cl_idx"]]
    sig_meas = base_data.csig / np.array([1.0, 1.0, 1.0, div])
    new = D.copy()
    ii = np.flatnonzero(inlier)
    if noise == "gauss":
        sd = np.sqrt(sigma ** 2 + sig_meas[ii] ** 2)
        new[ii] = Mp[ii] + rng.normal(0.0, 1.0, (len(ii), 4)) * sd
    elif noise == "resid":
        pool = resid if resid is not None else ev["cl_res"][ii]
        new[ii] = Mp[ii] + pool[rng.integers(0, len(pool), len(ii))]
    else:
        raise ValueError(noise)
    return new[:, 0], new[:, 1], new[:, 2], new[:, 3] * div


def known_answer_vectors(model: W.Model, v_inj, data_sel: W.Data, rng, sigma=47.0):
    """T5 known-answer mock: each selected cluster at the injected model's point closest to its
    position (x, y, z; no velocity is used), plus the T3 noise on all four components."""
    wv = W.wave_on_grid(v_inj, model.grid, model.setup.u1_mode)
    vi = np.flatnonzero(wv["valid"])
    div = model.divisor(v_inj)
    M4 = np.column_stack([wv["x"], wv["y"], wv["z"], wv["vz"] / div])[vi]
    P = np.column_stack([data_sel.cx, data_sel.cy, data_sel.cz])
    j = W.closest(P, M4[:, :3])
    sig_meas = data_sel.csig / np.array([1.0, 1.0, 1.0, div])
    sd = np.sqrt(sigma ** 2 + sig_meas ** 2)
    new = M4[j] + rng.normal(0.0, 1.0, M4[j].shape) * sd
    return new[:, 0], new[:, 1], new[:, 2], new[:, 3] * div


# ---------------------------------------------------------------------------------------------
# T5 pipeline (README 4.4)

def t5_curve(v_clouds, grid: W.Grid, u1_mode="half", omega0=W.OMEGA0_ADOPTED,
             mu0_kpc=W.MU0_ADOPTED_KPC, r0=W.R0_ADOPTED):
    """Baseline, Lambda, envelope shape, the clouds-only model z, and omega(s) with z_max = |zeta|."""
    v = np.array(v_clouds, float)
    v[W.IDX["w0t"]] = 0.0
    v[W.IDX["B"]] = 1.0
    wv = W.wave_on_grid(v, grid, u1_mode)
    if wv is None:
        return None
    vi = np.flatnonzero(wv["valid"])
    zeta = wv["zeta"]
    peak = np.max(np.abs(zeta))
    r = np.hypot(W.R_SUN - wv["x"], wv["y"])
    om = W.omega_eq3(np.abs(zeta), r, omega0, mu0_kpc * 1e-3, r0)
    return {"x": wv["x"][vi], "y": wv["y"][vi], "z": wv["z"][vi], "s": wv["s"][vi],
            "Lambda": wv["Lambda"][vi], "env": np.abs(zeta[vi]) / peak, "omega": om[vi]}


def t5_select(curve, cx, cy, cz, *, cut):
    """Positions only: project on the baseline (x-y), drop clusters whose closest point is an end of
    the valid grid, and apply the position cut (each of the x, y, z residuals below `cut`; None keeps
    all). Returns the closest indices, the end-of-grid mask and the kept mask. Fits nothing."""
    j = W.closest(np.column_stack([cx, cy]), np.column_stack([curve["x"], curve["y"]]))
    n = len(curve["x"])
    end = (j == 0) | (j == n - 1)
    keep = ~end
    if cut is not None:
        res = np.column_stack([cx - curve["x"][j], cy - curve["y"][j], cz - curve["z"][j]])
        keep &= np.all(np.abs(res) < cut, axis=1)
    return j, end, keep


def t5_analyse(curve, cx, cy, cz, cvz, csig, *, cut, bandwidth, sigma=47.0, k_range=(0.3, 3.0, 0.01)):
    """t5_select, then fit z and v_z/omega(s) on the kept clusters."""
    j, end, keep = t5_select(curve, cx, cy, cz, cut=cut)
    out = {"n_in": int(len(cx)), "n_end": int(end.sum()), "n_kept": int(keep.sum())}
    if keep.sum() < 6:
        out["fit"] = None
        return out
    jj = j[keep]
    s = curve["s"][jj]
    w = W.kde_weights(s, bandwidth)
    om = curve["omega"][jj]
    ez2 = csig[keep, 2] ** 2 + sigma ** 2
    yv = cvz[keep] / om
    ev2 = (csig[keep, 3] / om) ** 2 + sigma ** 2
    out["fit"] = S.t5_fit(curve["Lambda"][jj], curve["env"][jj], cz[keep], w / ez2, yv, w / ev2, k_range)
    out["kept_mask"] = keep
    return out


def t5_bootstrap(samples_vectors, grid, cx, cy, cz, cvz, csig, rng, *, n_boot, cut, bandwidth, u1_mode,
                 omega0=W.OMEGA0_ADOPTED, k_range=(0.3, 3.0, 0.01), sigma=47.0):
    """Resample the clusters; each resample also draws one clouds-only posterior sample."""
    n = len(cx)
    rows = []
    n_fail = 0
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        v = samples_vectors[rng.integers(0, len(samples_vectors))]
        cur = t5_curve(v, grid, u1_mode, omega0=omega0)
        if cur is None:
            n_fail += 1
            continue
        r = t5_analyse(cur, cx[idx], cy[idx], cz[idx], cvz[idx], csig[idx], cut=cut, bandwidth=bandwidth,
                       sigma=sigma, k_range=k_range)
        if r["fit"] is None:
            n_fail += 1
            continue
        f = r["fit"]
        rows.append((f["bhat"], f["k_ratio"], f["Delta"], f["rho"], f["k_z"], f["k_vz"], f["k_shared"]))
    arr = np.array(rows) if rows else np.zeros((0, 7))
    return {"bhat": arr[:, 0], "k_ratio": arr[:, 1], "Delta": arr[:, 2], "rho": arr[:, 3],
            "k_z": arr[:, 4], "k_vz": arr[:, 5], "k_shared": arr[:, 6], "n_fail": n_fail}


def circ_interval(x, level=0.95):
    """Interval of an angle: percentiles after centring on the circular mean."""
    x = np.asarray(x, float)
    if len(x) == 0:
        return None, None
    c = math.atan2(np.mean(np.sin(x)), np.mean(np.cos(x)))
    d = W.wrap_pi(x - c)
    lo, hi = S.interval(d, level)
    return c + lo, c + hi


def synthetic_clusters(grid: W.Grid, n, rng, B=0.84, w0t=-0.38, sigma=47.0):
    """Clusters drawn on K24's column-(6) model with noise (timing and tests; no data involved)."""
    v = W.k24_vector(6, w0t=w0t, B=B)
    wv = W.wave_on_grid(v, grid)
    vi = np.flatnonzero(wv["valid"])
    vi = vi[(wv["s"][vi] > -200) & (wv["s"][vi] < 2400)]
    j = rng.choice(vi, n)
    om = math.exp(v[W.IDX["ln_omega0"]])
    return W.Data(cx=wv["x"][j] + rng.normal(0, sigma, n), cy=wv["y"][j] + rng.normal(0, sigma, n),
                  cz=wv["z"][j] + rng.normal(0, sigma, n), cvz=wv["vz"][j] + rng.normal(0, sigma * om, n),
                  csig=np.ones((n, 4)), ox=np.zeros(0), oy=np.zeros(0), oz=np.zeros(0))
