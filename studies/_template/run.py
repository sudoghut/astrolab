"""{{TITLE}}

Run with:  python -m astrolab run {{ID}}
"""


def main(ctx):
    # Fetch (cached, provenance-logged). Keep it MB-scale: filter/aggregate server-side.
    # df = ctx.tap("SELECT TOP 10 source_id, ra, dec FROM gaiadr3.gaia_source", "gaia",
    #              label="example", release="Gaia DR3")

    summary = {"todo": "implement analysis"}
    ctx.save("summary", summary)
    return summary
