"""Offline tests for the optional Gaia archive session (no network, no real credentials)."""
import json

from astrolab import gaia_auth


def _no_creds(monkeypatch, tmp_path):
    monkeypatch.delenv("GAIA_USERNAME", raising=False)
    monkeypatch.delenv("GAIA_PASSWORD", raising=False)
    monkeypatch.setattr(gaia_auth.config, "ROOT", tmp_path)       # ignore the user's real .env in tests


def test_no_session_without_file(tmp_path, monkeypatch):
    _no_creds(monkeypatch, tmp_path)
    monkeypatch.setenv("ASTROLAB_CACHE_DIR", str(tmp_path / "Cache"))
    assert gaia_auth.load_cookies() is None
    assert gaia_auth.session_for("https://gea.esac.esa.int/tap-server/tap") is None


def test_session_only_for_gaia(tmp_path, monkeypatch):
    _no_creds(monkeypatch, tmp_path)
    monkeypatch.setenv("ASTROLAB_CACHE_DIR", str(tmp_path / "Cache"))
    p = gaia_auth.session_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"cookies": {"JSESSIONID": "x"}}), encoding="utf-8")
    s = gaia_auth.session_for("https://gea.esac.esa.int/tap-server/tap")
    assert s is not None and s.cookies.get("JSESSIONID") == "x"
    assert gaia_auth.session_for("https://datalab.noirlab.edu/tap") is None


def test_corrupt_file_ignored(tmp_path, monkeypatch):
    _no_creds(monkeypatch, tmp_path)
    monkeypatch.setenv("ASTROLAB_CACHE_DIR", str(tmp_path / "Cache"))
    p = gaia_auth.session_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("not json", encoding="utf-8")
    assert gaia_auth.load_cookies() is None


def test_credentials_from_env_then_dotenv(tmp_path, monkeypatch):
    _no_creds(monkeypatch, tmp_path)
    dot = tmp_path / ".env"
    assert gaia_auth.credentials(dot) is None
    dot.write_text("# comment\nGAIA_USERNAME=u1\nGAIA_PASSWORD='p1'\n", encoding="utf-8")
    assert gaia_auth.credentials(dot) == ("u1", "p1")
    monkeypatch.setenv("GAIA_USERNAME", "u2")
    monkeypatch.setenv("GAIA_PASSWORD", "p2")
    assert gaia_auth.credentials(dot) == ("u2", "p2")


def test_empty_template_values_mean_not_configured(tmp_path, monkeypatch):
    _no_creds(monkeypatch, tmp_path)
    dot = tmp_path / ".env"
    dot.write_text("GAIA_USERNAME=\nGAIA_PASSWORD=\n", encoding="utf-8")
    assert gaia_auth.credentials(dot) is None


def test_env_file_is_git_ignored():
    from astrolab import config
    lines = (config.ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    assert ".env" in [line.strip() for line in lines]
    example = (config.ROOT / ".env.example").read_text(encoding="utf-8")
    assert "GAIA_USERNAME=\n" in example and "GAIA_PASSWORD=\n" in example   # placeholders only


def test_refresh_session_drops_stale_cookie_only(tmp_path, monkeypatch):
    _no_creds(monkeypatch, tmp_path)
    monkeypatch.setenv("ASTROLAB_CACHE_DIR", str(tmp_path / "Cache"))
    url = "https://gea.esac.esa.int/tap-server/tap"
    p = gaia_auth.session_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"cookies": {"JSESSIONID": "new"}}), encoding="utf-8")
    # another thread already logged in again: the newer cookie is kept and reused
    s, used = gaia_auth.refresh_session(url, {"JSESSIONID": "old"})
    assert s is not None and s.cookies.get("JSESSIONID") == "new" and used == {"JSESSIONID": "new"}
    # the stale cookie is dropped; without configured credentials the session becomes anonymous
    assert gaia_auth.refresh_session(url, {"JSESSIONID": "new"}) == (None, None)
    assert not p.exists()
