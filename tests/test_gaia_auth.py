"""Offline tests for the optional Gaia archive session (no network, no credentials)."""
import json

from astrolab import gaia_auth


def test_no_session_without_file(tmp_path, monkeypatch):
    monkeypatch.setenv("ASTROLAB_CACHE_DIR", str(tmp_path / "Cache"))
    assert gaia_auth.load_cookies() is None
    assert gaia_auth.session_for("https://gea.esac.esa.int/tap-server/tap") is None


def test_session_only_for_gaia(tmp_path, monkeypatch):
    monkeypatch.setenv("ASTROLAB_CACHE_DIR", str(tmp_path / "Cache"))
    p = gaia_auth.session_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"cookies": {"JSESSIONID": "x"}}), encoding="utf-8")
    s = gaia_auth.session_for("https://gea.esac.esa.int/tap-server/tap")
    assert s is not None and s.cookies.get("JSESSIONID") == "x"
    assert gaia_auth.session_for("https://datalab.noirlab.edu/tap") is None
    assert not str(p).lower().startswith(str(__import__("astrolab").config.ROOT).lower())


def test_corrupt_file_ignored(tmp_path, monkeypatch):
    monkeypatch.setenv("ASTROLAB_CACHE_DIR", str(tmp_path / "Cache"))
    p = gaia_auth.session_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("not json", encoding="utf-8")
    assert gaia_auth.load_cookies() is None
