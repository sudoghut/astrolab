"""Registry of public TAP services. Prefer server-side filtering/aggregation on these."""
from __future__ import annotations

TAP_SERVICES: dict[str, dict[str, str]] = {
    "gaia": {
        "url": "https://gea.esac.esa.int/tap-server/tap",
        "about": "ESA Gaia archive (gaiadr3.*, gaiadr2.*, external.*).",
    },
    "vizier": {
        "url": "https://tapvizier.cds.unistra.fr/TAPVizieR/tap",
        "about": "CDS VizieR: published catalogs and paper tables (table names like \"J/ApJ/.../table1\").",
    },
    "simbad": {
        "url": "https://simbad.cds.unistra.fr/simbad/sim-tap",
        "about": "SIMBAD object database.",
    },
    "datalab": {
        "url": "https://datalab.noirlab.edu/tap",
        "about": "NOIRLab Astro Data Lab: SDSS, DESI, Legacy Surveys, cross-matches.",
    },
    "mast": {
        "url": "https://mast.stsci.edu/vo-tap/api/v0.1/caom",
        "about": "MAST CAOM observation metadata (HST, JWST, TESS).",
    },
    "irsa": {
        "url": "https://irsa.ipac.caltech.edu/TAP",
        "about": "NASA IRSA: WISE, 2MASS, ZTF, Spitzer.",
    },
    "exoplanet": {
        "url": "https://exoplanetarchive.ipac.caltech.edu/TAP",
        "about": "NASA Exoplanet Archive (ps, pscomppars, ...).",
    },
}


def tap_url(service: str) -> str:
    if service.startswith("http"):
        return service
    try:
        return TAP_SERVICES[service]["url"]
    except KeyError:
        known = ", ".join(sorted(TAP_SERVICES))
        raise KeyError(f"Unknown TAP service {service!r}. Known: {known}, or pass a URL.") from None
