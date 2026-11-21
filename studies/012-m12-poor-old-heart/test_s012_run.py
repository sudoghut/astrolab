"""End-to-end test of study 012's run.py on small synthetic CSV files (no network, no Zenodo files).

The synthetic files stand in for R22's two files; checksums, the cache and the context are faked, and
every count (bootstrap, mocks, grids) is reduced so the whole pipeline runs in seconds.
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study012_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


M = _import("model012")
D = _import("data012")


def synthetic_files(tmp, seed=5, n_poor=300, n_rich=1500, kin_cols=None):
    rng = np.random.default_rng(seed)
    # luminosity function: bright giants at 2-4 kpc
    n = 2000
    d = rng.uniform(2, 4, n)
    mg = rng.uniform(-3.5, -1.0, n)
    c = rng.uniform(1.2, 2.0, n)
    g = mg + 5 * np.log10(d * 100)
    lf = M.LFSample(g, c, g + 0.45 * c, 1 / d - 0.02, rng.uniform(5, 30, n))
    errs = M.ErrSampler(rng.uniform(8, 16, 5000), rng.uniform(0.01, 0.04, 5000))
    rows = []
    for nn, mlo, mhi in ((n_poor, -2.6, -1.5), (n_rich, -1.5, 0.3)):
        sim = M.simulate(rng, nn, sigma=2.7, q=1.0, lf=lf, ext=(0.3, 5.0), errs=errs)
        df = pd.DataFrame({"l": np.mod(sim["l"], 360), "b": sim["b"], "parallax": sim["plx"],
                           "parallax_error": sim["err"], "phot_g_mean_mag": sim["g"], "bp_rp": sim["bp_rp"],
                           "phot_bp_mean_mag": sim["bp"]})
        df["mh"] = rng.uniform(mlo, mhi, nn)
        rows.append(df)
    mh = pd.concat(rows, ignore_index=True)
    mh.insert(0, "source_id", np.arange(len(mh)) * 7 + 11)
    mh["teff"] = rng.normal(4500, 200, len(mh))
    mh["logg"] = rng.normal(2.0, 0.3, len(mh))
    # kinematics for 80% of the stars: rotation switches on at [M/H] = -1
    k = mh.sample(frac=0.8, random_state=1).reset_index(drop=True)
    rot = np.where(k["mh"] < -1.0, 0.0, 0.8) + rng.normal(0, 0.2, len(k))
    jtot = rng.uniform(500, 1500, len(k))
    jphi = rot * jtot
    rest = np.sqrt(np.clip(jtot ** 2 - jphi ** 2, 0, None))
    kin = pd.DataFrame({"source_id": k["source_id"], "J_R": rest * 0.7, "J_phi": jphi, "J_z": rest * 0.71414,
                        "ecc": rng.uniform(0, 1, len(k)), "r_apo": rng.uniform(1, 12, len(k))})
    if kin_cols is not None:
        kin = kin[kin_cols]
    pm, pk = tmp / "mh.csv", tmp / "kin.csv"
    mh.to_csv(pm, index=False)
    kin.to_csv(pk, index=False)
    return pm, pk


class FakeCtx:
    def __init__(self, results, files):
        self.results = Path(results)
        self.results.mkdir(parents=True, exist_ok=True)
        self.max_save_bytes = 1024 ** 2
        self.files = files
        self.saved = []
        self.record_suffix = ""
        self.calls = []

    def http(self, url, **kw):
        self.calls.append((url, kw))
        return self.files[url]

    def save(self, name, obj):
        from astrolab.results import write_json
        p = write_json(self.results / f"{name}.json", obj)
        assert p.stat().st_size < 1024 ** 2
        self.saved.append(name)
        return p

    def log(self, msg):
        pass


SMALL = {"grid_nodes": 60, "grid_max_nodes": 120, "grid_check_tol_kpc": 10.0, "t2a_boot": 3, "t2a_mocks": 3,
         "t2b_boot": 2, "t2b_mocks": 3, "t2b_starts": 2, "ext_a_grid": [0.0, 0.5, 0.5],
         "ext_bd_grid_deg": [5.0, 10.0, 5.0], "t3_boot": 30, "t3_w0_mocks": 3, "t4_realisations": 2,
         "t4_noise_dex": [0.1], "t4_boot": 30, "t5_boot": 50, "ref_max_stars": 300, "timing_evals": 1,
         "t2b_bmin_variants_deg": [8.0], "t3_R0_variants_kpc": [8.0], "stop_after_hours": 0.0}


def _setup(tmp_path, monkeypatch, **kw):
    run = _import("run")
    pm, pk = synthetic_files(tmp_path, **kw)
    files = {run.FILES["mh"]["url"]: pm, run.FILES["kin"]["url"]: pk}
    monkeypatch.setitem(run.FILES["mh"], "md5", D.md5_of(pm))
    monkeypatch.setitem(run.FILES["kin"], "md5", D.md5_of(pk))
    monkeypatch.setattr(run, "_cache_dir", lambda: tmp_path / "cache")
    monkeypatch.setattr(run, "MIN_MH_ROWS", 1000)
    for k, v in SMALL.items():
        monkeypatch.setitem(run.PARAMS, k, v)
    ctx = FakeCtx(tmp_path / "out", files)
    return run, ctx


def test_pipeline_end_to_end(tmp_path, monkeypatch):
    run, ctx = _setup(tmp_path, monkeypatch)
    s = run.main(ctx)
    assert s["status"] == "complete", s
    for name in ("load", "t1", "t2", "t3", "t4", "t5", "t6", "summary"):
        assert (ctx.results / f"{name}.json").exists(), name
    # the consent strings went to every fetch, and no download was allowed without first_download
    for _, kw in ctx.calls:
        assert "T-021" in kw["budget_consent"] and "T-021" in kw["cap_consent"]
        assert kw["allow_download"] is False and kw["max_bytes"] > 50 * 1024 ** 2
    lab = s["labels"]
    assert lab["T3a"] in ("no net rotation", "net rotation", "net counter-rotation", "undetermined")
    t1 = json.loads((ctx.results / "t1.json").read_text(encoding="utf-8"))
    assert t1["counts"]["lt_m1p5"] == 300
    load = json.loads((ctx.results / "load.json").read_text(encoding="utf-8"))
    assert load["L2"]["mapping_kin"]["jphi"] == "J_phi" and load["L4"]["fraction"] == 1.0
    assert s["reading_reproduction"]["label"] in ("not reproduced", "partly reproduced",
                                                  "R22's numbers reproduce from the public sample")
    # an exploration keeps its checkpoints apart from the formal run's
    assert "explore" in s["checkpoints"]
    # rerun resumes from the checkpoints and gives the same labels
    s2 = run.main(ctx)
    assert s2["labels"] == s["labels"]
    # the independent label checks of test_conclusions.py hold on these results
    tc = _import("test_conclusions")
    tc.RESULTS = ctx.results
    tc.MIN_ROWS = 1000
    ran = 0
    for name in dir(tc):
        if name.startswith("test_"):
            try:
                getattr(tc, name)()
                ran += 1
            except pytest.skip.Exception:
                pass
    assert ran >= 8


def test_pause_and_resume(tmp_path, monkeypatch):
    run, ctx = _setup(tmp_path, monkeypatch)
    monkeypatch.setitem(run.PARAMS, "stop_after_hours", 1e-9)
    s = run.main(ctx)
    assert s["status"] == "paused"
    assert not (ctx.results / "summary.json").exists()


def test_missing_t2_columns_stop(tmp_path, monkeypatch):
    run, ctx = _setup(tmp_path, monkeypatch)
    # drop the parallax error column from the metallicity file
    url = run.FILES["mh"]["url"]
    df = pd.read_csv(ctx.files[url]).drop(columns=["parallax_error"])
    df.to_csv(ctx.files[url], index=False)
    monkeypatch.setitem(run.FILES["mh"], "md5", D.md5_of(ctx.files[url]))
    s = run.main(ctx)
    assert s["status"].startswith("stopped at load") and "TAP" in s["status"]
    load = json.loads((ctx.results / "load.json").read_text(encoding="utf-8"))
    assert "parallax_error" in load["L2"]["t2_columns_missing"]


def test_too_few_rows_stop(tmp_path, monkeypatch):
    run, ctx = _setup(tmp_path, monkeypatch)
    monkeypatch.setattr(run, "MIN_MH_ROWS", 1_000_000)        # the pre-registered threshold
    s = run.main(ctx)
    assert s["status"].startswith("stopped at load: L3") and "1,000,000" in s["status"]


def test_grid_not_converged(tmp_path, monkeypatch):
    run, ctx = _setup(tmp_path, monkeypatch)
    monkeypatch.setitem(run.PARAMS, "grid_check_tol_kpc", -1.0)   # can never pass
    s = run.main(ctx)
    assert s["status"] == "complete"
    lab = s["labels"]
    g = "undetermined (grid not converged)"
    assert lab["T2a_population"] == g and lab["T2b_shape"] == g and lab["T2b_f5"] == g
    t4 = json.loads((ctx.results / "t4.json").read_text(encoding="utf-8"))
    assert t4["sigma_condition"] == g
    assert not any(q == "sigma" for _, q in t4["broken"])
    assert lab["T4"] == ("sensitive" if t4["broken"] else g)
    assert lab["T2a_reproduction"] == g          # version (i) cannot converge either at tol < 0
    assert s["pending_amendment"] == ["grid_not_converged_i", "grid_not_converged_ii"]
    assert s["pending_amendment"] and s["reading_reproduction"]["pending_amendment"]
    assert s["reading_robustness"]["pending_amendment"]
    tc = _import("test_conclusions")
    tc.RESULTS = ctx.results
    for name in ("test_t2a", "test_t2b", "test_t4_t6", "test_readings"):
        try:
            getattr(tc, name)()
        except pytest.skip.Exception:
            pass


def test_checkpoint_key_survives_first_download_reset(tmp_path):
    run = _import("run")
    C = _import("store012")
    text = (HERE / "run.py").read_text(encoding="utf-8")
    assert '"first_download": False,' in text
    other = tmp_path / "run.py"
    other.write_text(text.replace('"first_download": False,', '"first_download": True,'), encoding="utf-8")
    assert C.source_without_assignment(HERE / "run.py") == C.source_without_assignment(other)
    P = dict(run.PARAMS)
    k0 = run.run_key(P, ["a", "b"])
    assert run.run_key(P | {"first_download": True, "stop_after_hours": 3.0}, ["a", "b"]) == k0
    assert run.run_key(P | {"seed": 1}, ["a", "b"]) != k0
    other.write_text(text.replace("def rng_for(", "def rng_for2(", 1), encoding="utf-8")
    assert C.source_without_assignment(HERE / "run.py") != C.source_without_assignment(other)


def test_md5_mismatch_stops(tmp_path, monkeypatch):
    run, ctx = _setup(tmp_path, monkeypatch)
    monkeypatch.setitem(run.FILES["kin"], "md5", "0" * 32)
    s = run.main(ctx)
    assert "L1" in s["status"]


def test_formal_floors_enforced(monkeypatch):
    run = _import("run")
    monkeypatch.setitem(run.PARAMS, "t2a_mocks", 10)

    class Formal:
        max_save_bytes = None
        results = HERE / "results"
    with pytest.raises(ValueError, match="floors"):
        run.main(Formal())


def test_formal_run_needs_all_parts(monkeypatch):
    run = _import("run")
    monkeypatch.setitem(run.PARAMS, "parts", ["t1"])

    class Formal:
        max_save_bytes = None
        results = HERE / "results"
    with pytest.raises(ValueError, match="all parts"):
        run.main(Formal())


def test_params_defaults_are_preregistered():
    run = _import("run")
    P = run.PARAMS
    assert P["first_download"] is False and P["t2_missing_ok"] is False
    for k, v in run.FLOORS.items():
        assert P[k] == v
    assert P["grid_nodes"] == 300 and P["R0_kpc"] == 8.2 and P["plx_zp_mas"] == 0.02
    assert P["t2_mh_range"][1] == -1.5 and P["subsample_seed"] == 12012
    assert len(run.frange(P["ext_a_grid"])) == 101 and len(run.frange(P["ext_bd_grid_deg"])) == 39
    for k, v in run.FORMAL_FIXED.items():
        assert P[k] == v
    assert run.MIN_MH_ROWS == 1_000_000 and run.mass_r22(20000) == 20000 * 800 * 2.5
    assert run.FILES["mh"]["md5"] == "7257c98622573a4a625571fc973859c5"
    assert run.FILES["kin"]["md5"] == "b220c27aacff1f2f03d5a1f2b5fca147"
