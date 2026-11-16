"""Static site for GitHub Pages (T-037): built from the repository, all relative links resolve."""
from astrolab import config, site


def test_site_builds_with_no_broken_links(tmp_path):
    dest = tmp_path / "site"
    r = site.build(dest, config.ROOT)
    assert r["files"] > 10 and r["bytes"] < 50 * 1024 ** 2
    assert (dest / "index.html").exists() and (dest / ".nojekyll").exists()
    assert (dest / "atlas" / "web" / "index.html").exists()
    assert not list(dest.rglob("*.py")) and not list(dest.rglob("*.md"))
    assert site.broken_links(dest) == []


def test_broken_link_is_reported(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "index.html").write_text('<script src="../missing.js"></script>'
                                               '<a href="https://example.invalid/">x</a>', encoding="utf-8")
    assert site.broken_links(tmp_path) == ["a/index.html -> ../missing.js"]
