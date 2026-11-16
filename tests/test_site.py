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


def test_results_subfolders_published_and_dest_inside_project_refused(tmp_path):
    import pytest

    root = tmp_path / "repo"
    (root / "atlas" / "web").mkdir(parents=True)
    (root / "atlas" / "web" / "index.html").write_text("<p>atlas</p>", encoding="utf-8")
    r = root / "studies" / "001-x" / "results" / "dr3"
    r.mkdir(parents=True)
    (r / "release.json").write_text("{}", encoding="utf-8")
    (r.parent / "notes.txt").write_text("not published", encoding="utf-8")
    out = site.build(tmp_path / "site", root)
    assert (tmp_path / "site" / "studies" / "001-x" / "results" / "dr3" / "release.json").exists()
    assert out["skipped"] == ["studies/001-x/results/notes.txt"]
    with pytest.raises(SystemExit):
        site.build(root / "_site", root)


def test_broken_link_is_reported(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "index.html").write_text('<script src="../missing.js?v=1"></script>'
                                               '<a href="https://example.invalid/">x</a>', encoding="utf-8")
    assert site.broken_links(tmp_path) == ["a/index.html -> ../missing.js"]
