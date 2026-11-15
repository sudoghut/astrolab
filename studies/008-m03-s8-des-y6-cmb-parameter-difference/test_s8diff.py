"""Offline tests of s8diff.py (synthetic chains; no network)."""
import importlib.util
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study008_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


sd = _import("s8diff")


def _write(tmp_path, text):
    p = tmp_path / "c.txt"
    p.write_text(text, encoding="utf-8")
    return p


def test_header_and_columns(tmp_path):
    text = ("#cosmological_parameters--omega_m\tCOSMOLOGICAL_PARAMETERS--SIGMA_8\tlog_weight\tprior\tpost\n"
            "#sampler=nautilus\n## [cosmological_parameters]\n## omega_m = 0.1 0.3 0.9\n"
            "0.30 0.80 -1.0 0 0\n0.31 0.81 -2.0 0 0\n")
    fmt = sd.read_format(_write(tmp_path, text))
    assert fmt["ncols"] == 5 and fmt["nrows"] == 2 and fmt["sampler"] == "nautilus"
    cmap, status = sd.column_map(fmt, "x", positional_ok=False)
    assert status == "mapped" and cmap["omega_m"] == 0 and cmap["sigma_8"] == 1 and cmap["log_weight"] == 2
    chain, info = sd.load_chain(_write(tmp_path, text), cmap, 0.0)
    assert np.isclose(chain["w"].sum(), 1) and chain["w"][0] > chain["w"][1]
    assert np.allclose(chain["s8"], chain["sigma_8"] * np.sqrt(chain["omega_m"] / 0.3))


def test_weight_priority_and_ambiguity(tmp_path):
    fmt = {"header": ["omega_m", "sigma8", "old_weight", "weight", "log_weight"], "ncols": 5}
    cmap, status = sd.column_map(fmt, "x", positional_ok=False)
    assert status == "mapped" and cmap["weight"] == 3 and cmap["log_weight"] is None
    fmt = {"header": ["omega_m", "omegam", "sigma_8"], "ncols": 3}
    assert sd.column_map(fmt, "x", positional_ok=False)[0] is None


def test_no_header_rules(tmp_path):
    fmt = {"header": None, "ncols": 12}
    assert sd.column_map(fmt, "cmb", positional_ok=False)[0] is None
    cmap, _ = sd.column_map(fmt, "des", positional_ok=True)
    assert cmap["omega_m"] == 0 and cmap["sigma_8"] == 5 and cmap["log_weight"] == 9


def test_burn_in():
    assert sd.burn_in_fraction("nautilus", 0.3)[0] == 0.0
    assert sd.burn_in_fraction("emcee", 0.3)[0] == 0.3
    assert sd.burn_in_fraction(None, 0.3)[0] == 0.0


def test_nsigma_binned_gaussian():
    rng = np.random.default_rng(0)
    x = rng.standard_normal((400_000, 1)) + 2.0
    r = sd.nsigma_binned(x)
    assert abs(r["n_sigma"] - 2.0) < 0.05 and r["outside_grid"] < 10 and r["cell_over_h"] < 1 / 3


def test_parameter_difference_pairs():
    rng = np.random.default_rng(1)
    a = rng.normal(0.79, 0.012, 50_000)[:, None]
    b = rng.normal(0.836, 0.0125, 50_000)[:, None]
    w = np.ones(50_000)
    r = sd.parameter_difference(a, w, b, w, 400_000, [0, 1])
    expect = 0.046 / np.hypot(0.012, 0.0125)
    assert abs(r["n_sigma"] - expect) < 0.1


def test_split_normal_mean():
    rng = np.random.default_rng(2)
    x = sd.split_normal_draws(0.766, 0.020, 0.014, 2_000_000, rng)
    assert abs(x.mean() - 0.766) < 2e-4


def test_interval_and_equal_tail():
    rng = np.random.default_rng(3)
    x = rng.normal(0.8, 0.01, 200_000)
    w = np.ones_like(x)
    iv = sd.interval_around_mean(x, w, 0.68, 2000)
    assert abs(iv["mean"] - 0.8) < 1e-3 and abs(iv["hi"] - iv["lo"] - 0.0199) < 1e-3
    et = sd.equal_tail(rng.normal(2.0, 1.0, 400_000))
    assert abs(et["n_sigma"] - 2.0) < 0.05


def test_convolution_check():
    rng = np.random.default_rng(4)
    a = rng.normal(0.79, 0.012, 100_000)
    b = rng.normal(0.836, 0.0125, 100_000)
    w = np.ones_like(a)
    r = sd.convolution_check(a, w, b, w, 1e-4)
    assert abs(r["n_sigma"] - 0.046 / np.hypot(0.012, 0.0125)) < 0.1


def test_full_space_gaussian():
    rng = np.random.default_rng(5)
    a = rng.normal([0, 0], 1, (100_000, 2))
    b = rng.normal([3, 0], 1, (100_000, 2))
    w = np.ones(100_000)
    r = sd.full_space_gaussian(a, w, b, w, 1e8)
    assert r["status"] == "ok" and r["k"] == 2 and abs(r["chi2"] - 4.5) < 0.2


def _import_run():
    sys.path.insert(0, str(HERE))
    try:
        return _import("run")
    finally:
        sys.path.remove(str(HERE))


def test_parse_priors_long_params_block(tmp_path):
    run = _import_run()
    lines = ["## START_OF_PARAMS_INI", "## [some_module]", "## omega_m = 0.2 0.3 0.4"] + \
        [f"## key{i} = {i}" for i in range(300)] + ["## END_OF_PARAMS_INI",
             "## START_OF_VALUES_INI", "## [cosmological_parameters]", "## omega_m = 0.1 0.3 0.9 ; comment",
             "## n_s = 0.87 0.97 1.07", "## h0 = 0.7", "## END_OF_VALUES_INI",
             "## START_OF_PRIORS_INI", "## [cosmological_parameters]", "## n_s = gaussian 0.96 0.01",
             "## omega_m = uniform 0.15 0.8",
             "## END_OF_PRIORS_INI"]
    pr = run._parse_priors(lines)
    assert pr["cosmological_parameters--omega_m"]["range"] == (0.15, 0.8)
    assert "some_module--omega_m" not in pr
    assert pr["cosmological_parameters--n_s"]["gaussian_sigma"] == 0.01
    assert "cosmological_parameters--h0" not in pr
    text = "#omega_m sigma_8 weight\n" + "\n".join(lines) + "\n0.3 0.8 1\n"
    fmt = sd.read_format(_write(tmp_path, text))
    assert len(fmt["prior_lines"]) == len(lines) and fmt["ragged_rows"] == 0


def test_support_names_only_omega_m_and_amplitude():
    run = _import_run()
    names = ["cosmological_parameters--omega_m", "cosmological_parameters--n_s", "cosmological_parameters--a_s",
             "cosmological_parameters--h0", "intrinsic_alignment--a1"]
    assert run._support_names(names) == ["cosmological_parameters--a_s", "cosmological_parameters--omega_m"]


def test_ragged_rows_counted(tmp_path):
    fmt = sd.read_format(_write(tmp_path, "#a b c\n1 2 3\n1 2\n"))
    assert fmt["ragged_rows"] == 1


def test_whitening_identity_and_singular():
    rng = np.random.default_rng(6)
    x = rng.multivariate_normal([2.0, 0.0], [[1.0, 0.9], [0.9, 2.0]], 400_000)
    r = sd.nsigma_binned(x)
    assert np.isfinite(r["n_sigma"])
    bad = np.column_stack([np.ones(1000), np.ones(1000)])
    assert "error" in sd.nsigma_binned(bad)
