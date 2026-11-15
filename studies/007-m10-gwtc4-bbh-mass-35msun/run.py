"""M10 GWTC-4.0 BBH mass spectrum: the 35 Msun feature and the event sample

Run with:      python -m astrolab run 007-m10-gwtc4-bbh-mass-35msun
Explore with:  python -m astrolab explore 007-m10-gwtc4-bbh-mass-35msun --tag <topic> --set KEY=VALUE
"""

# Tunable knobs (AGENTS.md section 2). Read them inside main() at call time, never into
# module-level constants, and pass values to helper modules as arguments (a helper that does
# `import run` gets a fresh copy without the override): `astrolab explore --set` overrides
# this dict in memory.
PARAMS = {
    "example_limit": 10,
}


def main(ctx):
    # Fetch (cached, provenance-logged). Keep it MB-scale: filter/aggregate server-side.
    # df = ctx.tap(f"SELECT TOP {PARAMS['example_limit']} source_id, ra, dec FROM gaiadr3.gaia_source",
    #              "gaia", label="example", release="Gaia DR3")

    summary = {"todo": "implement analysis", "params": dict(PARAMS)}
    ctx.save("summary", summary)
    return summary
