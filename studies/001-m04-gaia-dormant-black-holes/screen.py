"""Server-side ADQL for the dark-companion screen, parameterised by Gaia release.

The mass function is evaluated on the Gaia server in nested subqueries
(the archive's ADQL parser rejects the fully inlined expression in a WHERE clause):

  q1: astrometric-orbit solutions, quality pre-cut, G filled for pseudo-circular orbits
  q2: photocentre semi-major axis a0 [mas] from Thiele-Innes constants (DR3 doc eq. 7.15)
  q3: astrometric mass function f_M [Msun] = (a0/parallax)^3 / P_yr^2
  outer: f_M threshold + join photometry (gaia_source) and FLAME masses (astrophysical_parameters)

Kept separate from run.py so it can be inspected or run on DR4 release day.
"""

ASTROMETRIC_TYPES = (
    "Orbital", "AstroSpectroSB1",
    "OrbitalTargetedSearch", "OrbitalTargetedSearchValidated",
    "OrbitalAlternative", "OrbitalAlternativeValidated",
)

SCHEMAS = {"dr3": "gaiadr3", "dr4": "gaiadr4"}  # dr4 schema name: confirm via TAP_SCHEMA on release day

_COLS = "source_id, nss_solution_type, period, period_error, eccentricity, parallax, parallax_error, significance, goodness_of_fit, flags"


def mass_function_subquery(release="dr3", plx_snr_min=5.0) -> str:
    s = SCHEMAS[release]
    types = ", ".join(f"'{t}'" for t in ASTROMETRIC_TYPES)
    q1 = (
        f"SELECT {_COLS}, a_thiele_innes AS ta, b_thiele_innes AS tb, f_thiele_innes AS tf, "
        f"COALESCE(g_thiele_innes, -a_thiele_innes*f_thiele_innes/b_thiele_innes) AS tg "
        f"FROM {s}.nss_two_body_orbit "
        f"WHERE nss_solution_type IN ({types}) AND parallax > 0 AND parallax/parallax_error > {plx_snr_min}"
    )
    u = "0.5*(q1.ta*q1.ta+q1.tb*q1.tb+q1.tf*q1.tf+q1.tg*q1.tg)"
    v = "(q1.ta*q1.tg-q1.tb*q1.tf)"
    cols1 = ", ".join(f"q1.{c.strip()}" for c in _COLS.split(","))
    q2 = f"SELECT {cols1}, SQRT({u}+SQRT(POWER({u},2)-POWER({v},2))) AS a0_mas FROM ({q1}) AS q1"
    cols2 = ", ".join(f"q2.{c.strip()}" for c in _COLS.split(","))
    q3 = (
        f"SELECT {cols2}, q2.a0_mas, "
        f"POWER(q2.a0_mas/q2.parallax, 3)/POWER(q2.period/365.25, 2) AS f_m FROM ({q2}) AS q2"
    )
    return q3


def screen_from_where(release="dr3", fm_min=0.25, plx_snr_min=5.0) -> str:
    """FROM ... WHERE ... clause, usable with fetch.tap_count for a server-side size check."""
    return f"({mass_function_subquery(release, plx_snr_min)}) AS q WHERE q.f_m > {fm_min}"


FLAME_COLS = ("mass_flame", "mass_flame_lower", "mass_flame_upper", "radius_flame")


def screen_adql(release="dr3", fm_min=0.25, plx_snr_min=5.0, flame=True) -> str:
    """Screen query. flame=True selects all FLAME_COLS (the DR3 text); a list selects only those
    (a release lacking some); False/[] drops the FLAME join. The caller fills missing ones with NaN."""
    s = SCHEMAS[release]
    cols = ", ".join(f"q.{c.strip()}" for c in _COLS.split(","))
    ap = list(FLAME_COLS) if flame is True else [c for c in FLAME_COLS if flame and c in flame]
    ap_cols = ", " + ", ".join(f"ap.{c}" for c in ap) + " " if ap else " "
    ap_join = f"LEFT OUTER JOIN {s}.astrophysical_parameters AS ap ON ap.source_id = q.source_id " if ap else ""
    return (
        f"SELECT {cols}, q.a0_mas, q.f_m, "
        f"g.ra, g.dec, g.l, g.b, g.phot_g_mean_mag, g.bp_rp, g.ruwe"
        f"{ap_cols}"
        f"FROM ({mass_function_subquery(release, plx_snr_min)}) AS q "
        f"JOIN {s}.gaia_source AS g ON g.source_id = q.source_id "
        f"{ap_join}"
        f"WHERE q.f_m > {fm_min}"
    )
