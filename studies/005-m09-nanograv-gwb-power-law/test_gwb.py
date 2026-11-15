"""Offline tests of gwb.py on a synthetic free spectrum (no network)."""
import importlib.util
import io
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).parent


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study005_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


gwb = _import("gwb")
table_a1 = _import("table_a1")

T_YR = 16.03
T_S = T_YR * gwb.YEAR_S
FREQS = np.arange(1, 31) / T_S
GRID = np.linspace(-10.0, -5.0, 501)
TRUE = (np.log10(2.4e-15), 13.0 / 3.0)


def _density(sigma=0.15, log10_a=TRUE[0], gamma=TRUE[1]):
    mu = gwb.log10rho_powerlaw(log10_a, gamma, FREQS, T_S)
    d = -0.5 * ((GRID[None, :] - mu[:, None]) / sigma) ** 2
    d -= np.log(np.exp(d).sum(axis=1, keepdims=True) * (GRID[1] - GRID[0]))
    return d[None, :, :]


def _zip(tmp_path, arrays=None, dirname="30f_fs{hd}_ceffyl", extra=()):
    arrays = arrays or {"freqs.npy": FREQS, "log10rhogrid.npy": GRID, "density.npy": _density()}
    path = tmp_path / "prod.zip"
    with zipfile.ZipFile(path, "w") as zf:
        for name, arr in arrays.items():
            buf = io.BytesIO()
            np.save(buf, arr, allow_pickle=False)
            zf.writestr(f"data/{dirname}/{name}", buf.getvalue())
        for name, payload in extra:
            zf.writestr(name, payload)
    return path


LIMITS = dict(max_member_bytes=50 * 2 ** 20, max_total_bytes=150 * 2 ** 20, max_members=10000)
CHECKS = dict(n_freq_file=30, t_yr=T_YR, freq_tol=0.01, grid_rtol=1e-6)


@pytest.fixture
def prod(tmp_path):
    return gwb.check_product(gwb.load_product(_zip(tmp_path), "30f_fs{hd}", **LIMITS), **CHECKS)


def test_load_and_check(prod):
    assert prod["density"].shape == (30, GRID.size)
    assert abs(prod["T"] / gwb.YEAR_S - T_YR) < 1e-9
    assert prod["binedges"][-1] == GRID[-1] and prod["binedges"].size == GRID.size + 1


def test_unsafe_and_missing(tmp_path):
    with pytest.raises(gwb.NotEvaluable):
        gwb.load_product(_zip(tmp_path, extra=[("../evil.txt", b"x")]), "30f_fs{hd}", **LIMITS)
    with pytest.raises(gwb.NotEvaluable):
        gwb.load_product(_zip(tmp_path, dirname="30f_fs{cp}_ceffyl"), "30f_fs{hd}", **LIMITS)
    small = dict(LIMITS, max_member_bytes=100)
    with pytest.raises(gwb.NotEvaluable):
        gwb.load_product(_zip(tmp_path), "30f_fs{hd}", **small)


def test_bad_shapes(tmp_path):
    bad = {"freqs.npy": FREQS, "log10rhogrid.npy": GRID, "density.npy": _density()[0, :20]}
    p = gwb.load_product(_zip(tmp_path, arrays=bad), "30f_fs{hd}", **LIMITS)
    with pytest.raises(gwb.NotEvaluable):
        gwb.check_product(p, **CHECKS)
    p = gwb.load_product(_zip(tmp_path), "30f_fs{hd}", **LIMITS)
    with pytest.raises(gwb.NotEvaluable):
        gwb.check_product(p, **dict(CHECKS, t_yr=15.0))


def test_lnlike_bins(prod):
    k = 2
    d = prod["density"]
    # exactly on a grid node -> that node; below the grid -> bottom cell (clip) or -inf
    x = np.array([[GRID[10], GRID[20]]])
    assert np.isclose(gwb.lnlike(prod, x, below_grid="clip")[0], d[0, 10] + d[1, 20])
    lo = np.array([[GRID[0] - 1.0, GRID[20]]])
    assert np.isclose(gwb.lnlike(prod, lo, below_grid="clip")[0], d[0, 0] + d[1, 20])
    assert gwb.lnlike(prod, lo, below_grid="neg_inf")[0] == -np.inf
    # top edge equals grid[-1]: at the edge it is the last cell, just above it is -inf
    top = np.array([[GRID[-1], GRID[20]]])
    assert np.isclose(gwb.lnlike(prod, top, below_grid="clip")[0], d[0, -1] + d[1, 20])
    assert gwb.lnlike(prod, top + np.array([[1e-9, 0.0]]), below_grid="clip")[0] == -np.inf
    assert k == x.shape[-1]


def test_two_piece_quantiles():
    x = np.linspace(-16.0, -13.0, 30001)
    m = np.log10(2.4e-15)
    s_lo = (m - np.log10(1.8e-15)) / 1.645
    s_hi = (np.log10(3.1e-15) - m) / 1.645
    q = gwb.two_piece_pdf(x, m, s_lo, s_hi)
    q05, q50, q95 = gwb.quantiles(x, q, (0.05, 0.5, 0.95))
    assert abs(q05 - np.log10(1.8e-15)) < 1e-3
    assert abs(q50 - m) < 1e-3
    assert abs(q95 - np.log10(3.1e-15)) < 1e-3
    assert gwb.hellinger(x, q, q) < 1e-6


R1KW = dict(n_freq=14, gamma=13.0 / 3.0, lo=-18.0, hi=-14.0, step=0.001, below_grid="clip",
            l8_a=[2.4e-15, 1.8e-15, 3.1e-15], edge_frac=0.01, edge_max=0.01, h_max=0.15)


def test_r1_recovers_amplitude(prod):
    out = gwb.r1(prod, **R1KW)
    assert abs(out["log10A_median"] - TRUE[0]) < 0.02
    assert out["q05_A"] < out["median_A"] < out["q95_A"]
    assert out["edge_mass_log10A"] < 1e-6


def test_r1_edge_rule(tmp_path):
    p = gwb.check_product(gwb.load_product(
        _zip(tmp_path, arrays={"freqs.npy": FREQS, "log10rhogrid.npy": GRID,
                               "density.npy": _density(log10_a=-14.0)}), "30f_fs{hd}", **LIMITS), **CHECKS)
    with pytest.raises(gwb.NotEvaluable):
        gwb.r1(p, **R1KW)


R2KW = dict(n_freq=14, lo_a=-18.0, hi_a=-11.0, lo_g=0.0, hi_g=7.0, step=0.02, below_grid="clip",
            gamma_line=13.0 / 3.0, edge_frac=0.01, edge_max=0.01, chunk=16)


def test_r2_truth_on_line(prod):
    out = gwb.r2(prod, **R2KW)
    assert out["q_hpd_13_3"] < 0.5          # the true gamma is 13/3: the line runs through the peak
    assert out["q_hpd_13_3"] <= out["q_hpd_13_3_ge"]
    assert abs(out["gamma_median"] - TRUE[1]) < 0.5


def test_r2_truth_off_line(tmp_path):
    p = gwb.check_product(gwb.load_product(
        _zip(tmp_path, arrays={"freqs.npy": FREQS, "log10rhogrid.npy": GRID,
                               "density.npy": _density(sigma=0.05, log10_a=np.log10(6.4e-15), gamma=2.0)}),
        "30f_fs{hd}", **LIMITS), **CHECKS)
    out = gwb.r2(p, **R2KW)
    assert out["q_hpd_13_3"] > 0.95
    assert gwb.category(out["q_hpd_13_3"], 0.95, 0.997).endswith("(descriptive category)")


def test_r2b_closed_intervals():
    table = [("a", 1.0e-15, 2.4e-15), ("b", 2.5e-15, 3.0e-15), ("c", 1e-16, 2e-16), ("d", 1e-16, 2e-16)]
    out = gwb.r2b(2.0e-15, 2.4e-15, 3.0e-15, table)
    assert out["n_models_overlap_ci90"] == 2          # a (endpoint), b
    assert out["n_models_contain_median"] == 1        # a: 2.4e-15 equals p84 -> included
    assert out["n_rows"] == 4 and out["n_rows_merged"] == 3


def test_r4_runs(prod):
    out = gwb.r4(prod, n_freq=14, gamma=13.0 / 3.0, lo_a=-18.0, hi_a=-11.0, lo_fb=-9.0, hi_fb=-7.5,
                 lo_k=0.0, hi_k=7.0, steps=(0.05, 0.1, 0.5), below_grid="clip", edge_frac=0.01,
                 edge_max=0.01, chunk=4)
    assert np.isfinite(out["ln_bf_turnover_vs_pl"])
    # data are a pure power law: the turnover cannot be strongly favoured
    assert out["ln_bf_turnover_vs_pl"] < 1.0


def test_table_matches_readme():
    text = (HERE / "README.md").read_text(encoding="utf-8")
    rows = re.findall(r"^\| (\d+) \| (.+?) \| ([0-9.e+-]+) \| ([0-9.e+-]+) \|$", text, flags=re.M)
    assert len(rows) == 24
    for (i, model, p16, p84), (m2, a, b) in zip(rows, table_a1.TABLE_A1):
        assert model == m2 and float(p16) == a and float(p84) == b
