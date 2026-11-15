"""M9 NANOGrav 15-yr GWB: power-law amplitude and spectral index from the KDE free spectrum

Run with:      python -m astrolab run 005-m09-nanograv-gwb-power-law
Explore with:  python -m astrolab explore 005-m09-nanograv-gwb-power-law --tag <topic> --set KEY=VALUE
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
