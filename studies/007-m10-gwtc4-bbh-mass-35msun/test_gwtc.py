"""Offline tests of gwtc.py (synthetic lists and tar; no network)."""
import importlib.util
import io
import json
import sys
import tarfile
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).parent


def _import(name):
    spec = importlib.util.spec_from_file_location(f"study007_{name}", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


gw = _import("gwtc")


def _event(name, gps, far, m1, m1lo, m1hi, m2, m2lo, version=1):
    return {f"{name}-v{version}": {"commonName": name, "version": version, "GPS": gps, "far": far,
                                   "mass_1_source": m1, "mass_1_source_lower": m1lo, "mass_1_source_upper": m1hi,
                                   "mass_2_source": m2, "mass_2_source_lower": m2lo, "total_mass_source": m1 + m2}}


def _write(tmp_path, name, events):
    p = tmp_path / name
    p.write_text(json.dumps({"events": events}), encoding="utf-8")
    return p


def test_load_list_keeps_latest_version(tmp_path):
    ev = {}
    ev.update(_event("GW230601_000000", 1.37e9, 0.1, 30, -3, 4, 20, -2, version=1))
    ev.update(_event("GW230601_000000", 1.37e9, 0.1, 31, -3, 4, 21, -2, version=2))
    ev["GW000000_000000-v1"] = None
    rows = gw.load_list(_write(tmp_path, "l.json", ev))
    assert rows["GW230601_000000"]["m1"] == 31 and len(rows) == 1


def test_lower_bound_and_cuts():
    row = {"far": 0.5, "m1": 30.0, "m1_lo": -3.0, "m2": 4.0, "m2_lo": -0.5}
    assert gw.lower_bound(4.0, -0.5) == 3.5
    assert gw.passes(row, 1.0, 3.0, "p90")[0]
    row["m2_lo"] = -1.5                                   # bound 2.5 <= 3
    assert not gw.passes(row, 1.0, 3.0, "p90")[0]
    row["far"] = 1.0                                      # far must be strictly below 1
    assert not gw.passes(row, 1.0, 3.0, "median")[0]
    assert gw.passes({"far": None, "m1": 1, "m1_lo": 0, "m2": 1, "m2_lo": 0}, 1, 3, "p90") == (False, "no FAR")
    assert gw.passes({"far": 0.1, "m1": None, "m1_lo": None, "m2": None, "m2_lo": None}, 1, 3, "p90") == (False, "no PE")


def test_name_to_gps():
    # GW150914_095045 is GPS 1126259462 (+0.4); the name truncates to the second
    assert abs(gw.name_to_gps("GW150914_095045") - 1126259462) <= 1
    assert gw.name_to_gps("GW150914") is None
    assert gw.name_to_gps("GW230231_000000") is None          # invalid date


def test_select_o4a_window_and_exclusion(tmp_path):
    ev = {}
    ev.update(_event("GW230601_000000", 1369000000, 0.1, 30, -3, 4, 20, -2))
    ev.update(_event("GW230518_125908", 1368460000, 0.1, 30, -3, 4, 20, -2))     # before O4a
    ev.update(_event("GW230630_070659", 1372000000, 0.1, 30, -3, 4, 20, -2))     # excluded
    rows = gw.load_list(_write(tmp_path, "o4.json", ev))
    sel, why = gw.select_o4a(rows, 1368975618, 1389456018, 1.0, 3.0, "p90", {"GW230630_070659"})
    assert set(sel) == {"GW230601_000000"}
    assert why["GW230518_125908"] == "outside O4a" and why["GW230630_070659"].startswith("excluded")


def test_merge_precedence():
    a = {"GW1": {"src": "a", "m1": 1, "m2": 1, "far": 0.1}}
    b = {"GW1": {"src": "b", "m1": 2, "m2": 2, "far": 0.2}, "GW2": {"src": "b"}}
    out, overlaps = gw.merge_lists([a, b], ["A", "B"])
    assert out["GW1"]["src"] == "a" and out["GW2"]["src"] == "b"
    assert overlaps == [{"name": "GW1", "kept": "A", "dropped": "B", "kept_m1_m2_far": [1, 1, 0.1],
                         "dropped_m1_m2_far": [2, 2, 0.2]}]


def test_same_event():
    assert gw.same_event("GW200105_162426-v2", "GW200105_162426")
    assert gw.same_event("GW200105", "GW200105_162426")
    assert not gw.same_event("GW200105_162426", "GW200106_000000")


def test_r1_verdict_edges():
    base = dict(target_size=84, n_target_expected=84, missing=[], extras=[], extra_m2_max=5.0, m_min=3.0,
                max_extras=2, n_o3=69, n_o3_target=69, n_o3_tol=2, n_type_i=0, named_pass=[True] * 7)
    assert gw.r1_verdict(**base)["verdict"] == "reproduced"
    assert gw.r1_verdict(**dict(base, n_o3=71, n_type_i=1))["verdict"] == "not reproduced"
    assert gw.r1_verdict(**dict(base, n_o3=71, n_type_i=2))["verdict"] == "reproduced"
    assert gw.r1_verdict(**dict(base, n_o3=67))["verdict"] == "reproduced"
    assert gw.r1_verdict(**dict(base, n_o3=72, n_type_i=5))["verdict"] == "not reproduced"
    assert gw.r1_verdict(**dict(base, extras=[5.0]))["verdict"] == "reproduced"
    assert gw.r1_verdict(**dict(base, extras=[5.01]))["verdict"] == "not reproduced"
    assert gw.r1_verdict(**dict(base, extras=[4.0, 4.0, 4.0]))["verdict"] == "not reproduced"
    assert gw.r1_verdict(**dict(base, target_size=83))["verdict"] == "described"
    assert gw.r1_verdict(**dict(base, target_size=83, named_pass=[False] + [True] * 6))["verdict"] == "not reproduced"
    assert gw.r1_verdict(**dict(base, missing=["GW1"]))["verdict"] == "not reproduced"


def test_tar_names(tmp_path):
    p = tmp_path / "x.tar"
    with tarfile.open(p, "w") as tf:
        data = b"GW230601_000000 label1\nGW231123_135430 label2\nnotanevent\n"
        info = tarfile.TarInfo("o4a/events.txt")
        info.size = len(data)
        tf.addfile(info, io.BytesIO(data))
    names, members = gw.tar_names(p)
    assert names == {"GW230601_000000", "GW231123_135430"} and members == ["o4a/events.txt"]
    q = tmp_path / "y.tar"
    with tarfile.open(q, "w") as tf:
        info = tarfile.TarInfo("GW230702_000000.h5")
        info.size = 0
        tf.addfile(info, io.BytesIO(b""))
    assert gw.tar_names(q)[0] == {"GW230702_000000"}
    assert not gw.NAME_RE.fullmatch("GW2306011")


def test_vt_continuous_and_r2_prediction():
    assert np.isclose(gw.vt(49.999, 2.2, 50.0), gw.vt(50.0, 2.2, 50.0), rtol=1e-3)
    # with no turnover p ~ m^0.5 on [10, 100]; analytic fraction above 35
    f = gw.r2_prediction(1.7, 2.2, None, 10.0, 35.0, 100.0, 20001)
    expect = (100 ** 1.5 - 35 ** 1.5) / (100 ** 1.5 - 10 ** 1.5)
    assert abs(f - expect) < 1e-4
    # a turnover lowers the high-mass fraction
    assert gw.r2_prediction(1.7, 2.2, 30.0, 10.0, 35.0, 100.0, 2001) < f


def test_binom():
    assert np.isclose(gw.binom_le(0, 10, 0.5), 0.5 ** 10)


def test_model_density_normalised():
    grid = np.linspace(10, 100, 2000)
    for kind, th in (("A", [1.7, 4.5, 35.0]), ("B", [1.7, 4.5, 35.0, 33.0, 4.0, 0.3])):
        d = gw.model_density(th, kind, grid, 2.2, 50.0)
        assert abs(gw.trapz(d, grid) - 1) < 1e-9 and np.all(d > 0)


def test_fit_recovers_break():
    """Sample from a known broken power law (flat VT) and recover lam2 > lam1."""
    grid = np.linspace(10, 100, 4000)
    dens = gw.model_density([1.5, 5.0, 35.0], "A", grid, 0.0, None)
    cdf = np.cumsum(dens) / np.sum(dens)
    rng = np.random.default_rng(1)
    masses = np.interp(rng.uniform(size=3000), cdf, grid)
    a = gw.fit("A", masses, grid, 0.0, None, 8, 0)
    lam1, lam2, mb = a["theta"]
    assert lam2 - lam1 > 2 and abs(mb - 35) < 5
    b = gw.fit("B", masses, grid, 0.0, None, 8, 0, extra_starts=[a["theta"] + [35.0, 5.0, 0.0]])
    assert b["nll"] <= a["nll"] + 1e-6          # B nests A, so 2 dlnL >= 0
