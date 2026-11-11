import numpy as np
import pandas as pd
import pytest

from astrolab import orbits


def test_a0_face_on_circular():
    # face-on circular orbit, omega = Omega = 0, i = 0: A = a, B = 0, F = 0, G = a
    assert orbits.a0_mas(2.0, 0.0, 0.0, 2.0) == pytest.approx(2.0)


def test_a0_inclined_orbit_matches_thiele_innes_definition():
    a, w, W, i = 1.7, 0.4, 1.1, 0.9
    A = a * (np.cos(w) * np.cos(W) - np.sin(w) * np.sin(W) * np.cos(i))
    B = a * (np.cos(w) * np.sin(W) + np.sin(w) * np.cos(W) * np.cos(i))
    F = -a * (np.sin(w) * np.cos(W) + np.cos(w) * np.sin(W) * np.cos(i))
    G = -a * (np.sin(w) * np.sin(W) - np.cos(w) * np.cos(W) * np.cos(i))
    assert orbits.a0_mas(A, B, F, G) == pytest.approx(a)


@pytest.mark.parametrize("m1,m2", [(0.93, 9.62), (1.07, 8.9), (1.0, 1.4), (0.5, 0.1), (2.0, 30.0)])
def test_companion_mass_roundtrip(m1, m2):
    f = m2**3 / (m1 + m2) ** 2
    assert orbits.companion_mass(f, m1) == pytest.approx(m2, rel=1e-8)


def test_mass_function_sun_jupiter_scale():
    # a1 = 1 AU, P = 1 yr -> f = 1 Msun
    assert orbits.mass_function(10.0, 10.0, orbits.DAYS_PER_YEAR) == pytest.approx(1.0)


def _synthetic_row(solution_type="Orbital", seed=1):
    names = [n for n in orbits.solution_parameters(solution_type) if n not in ("c_thiele_innes", "h_thiele_innes")]
    if solution_type == "AstroSpectroSB1":
        names = orbits.solution_parameters(solution_type)
    rng = np.random.default_rng(seed)
    n = len(names)
    row = {"source_id": 1, "nss_solution_type": solution_type}
    for p in orbits.solution_parameters(solution_type):
        row[p], row[f"{p}_error"] = np.nan, np.nan
    for p in names:
        row[p], row[f"{p}_error"] = rng.normal(), rng.uniform(0.1, 1.0)
    row["corr_vec"] = rng.uniform(-0.9, 0.9, n * (n - 1) // 2)
    return pd.Series(row), names


@pytest.mark.parametrize("stype", ["Orbital", "AstroSpectroSB1"])
def test_covariance_matches_official_nsstools(stype):
    nsstools = pytest.importorskip("nsstools")
    row, names = _synthetic_row(stype)
    ours_names, ours = orbits.covariance(row)
    ref = nsstools.NssSource(pd.DataFrame([row])).covmat()
    assert ours_names == list(ref.index) == names
    np.testing.assert_allclose(ours, ref.to_numpy())
