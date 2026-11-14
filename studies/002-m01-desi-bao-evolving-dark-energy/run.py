"""DESI DR2 BAO and evolving dark energy

Run with:      python -m astrolab run 002-m01-desi-bao-evolving-dark-energy
Explore with:  python -m astrolab explore 002-m01-desi-bao-evolving-dark-energy --tag <topic> --set KEY=VALUE
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
