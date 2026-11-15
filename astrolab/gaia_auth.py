"""Optional authenticated session for the ESA Gaia archive (longer TAP job limits than anonymous).

The user logs in themselves with ``python -m astrolab gaia-login`` in their own terminal: the
username and password are read with getpass (never echoed, never stored); only the session cookie
returned by the archive is saved, outside the project (Dropbox) folder, next to the cache. Agents
never see or handle the credentials; ``astrolab.fetch`` attaches the saved cookie to Gaia queries.
"""
from __future__ import annotations

import getpass
import json
import os
from pathlib import Path

from . import config

LOGIN_URL = "https://gea.esac.esa.int/tap-server/login"
LOGOUT_URL = "https://gea.esac.esa.int/tap-server/logout"
GAIA_HOST = "gea.esac.esa.int"


def session_path() -> Path:
    return config.cache_dir().parent / "gaia_session.json"


def load_cookies() -> dict | None:
    """Saved session cookies, or None when the user has not logged in."""
    p = session_path()
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    cookies = data.get("cookies")
    return cookies if isinstance(cookies, dict) and cookies else None


def session_for(url: str):
    """A requests.Session carrying the Gaia cookies when `url` is the Gaia archive, else None."""
    if GAIA_HOST not in url:
        return None
    cookies = load_cookies()
    if not cookies:
        return None
    import requests

    s = requests.Session()
    for k, v in cookies.items():
        s.cookies.set(k, v, domain=GAIA_HOST)
    return s


def login() -> None:
    """Interactive login; run by the user in their own terminal."""
    import requests

    user = input("Gaia archive username: ").strip()
    pw = getpass.getpass("Gaia archive password (not echoed): ")
    r = requests.post(LOGIN_URL, data={"username": user, "password": pw}, timeout=60)
    pw = None
    if r.status_code != 200 or not r.cookies:
        raise SystemExit(f"login failed (HTTP {r.status_code})")
    p = session_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"cookies": r.cookies.get_dict()}), encoding="utf-8")
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass
    print(f"logged in; session cookie saved to {p} (delete it or run gaia-logout to end the session)")


def logout() -> None:
    import requests

    s = session_for("https://" + GAIA_HOST)
    if s is not None:
        try:
            s.post(LOGOUT_URL, timeout=30)
        except requests.RequestException:
            pass
    session_path().unlink(missing_ok=True)
    print("Gaia session removed")
