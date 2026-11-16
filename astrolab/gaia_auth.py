"""Optional authenticated session for the ESA Gaia archive (longer TAP job limits than anonymous).

Credentials come from the user only, in this order: the environment variables GAIA_USERNAME and
GAIA_PASSWORD, then a git-ignored ``.env`` file at the project root (template: ``.env.example``),
then the interactive ``python -m astrolab gaia-login`` (getpass, never echoed). The password is never
stored by astrolab; only the session cookie returned by the archive is saved, outside the project
folder, next to the cache. ``astrolab.fetch`` attaches the cookie to Gaia queries and, when no cookie
exists but credentials are configured, logs in once without prompting. Agents never read, print or
handle the credentials.
"""
from __future__ import annotations

import getpass
import json
import os
import threading
from pathlib import Path

from . import config

LOGIN_URL = "https://gea.esac.esa.int/tap-server/login"
LOGOUT_URL = "https://gea.esac.esa.int/tap-server/logout"
GAIA_HOST = "gea.esac.esa.int"


def session_path() -> Path:
    return config.cache_dir().parent / "gaia_session.json"


def _dotenv(path: Path) -> dict:
    """Minimal KEY=VALUE parser for the git-ignored .env file (no interpolation)."""
    out = {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return out
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def credentials(dotenv: Path | None = None) -> tuple[str, str] | None:
    """(username, password) from the environment or .env, or None when not configured."""
    user = os.environ.get("GAIA_USERNAME", "")
    pw = os.environ.get("GAIA_PASSWORD", "")
    if not (user and pw):
        env = _dotenv(dotenv or (config.ROOT / ".env"))
        user = user or env.get("GAIA_USERNAME", "")
        pw = pw or env.get("GAIA_PASSWORD", "")
    return (user, pw) if user and pw else None


def _post_login(user: str, pw: str) -> None:
    import requests

    r = requests.post(LOGIN_URL, data={"username": user, "password": pw}, timeout=60)
    if r.status_code != 200 or not r.cookies:
        raise RuntimeError(f"Gaia archive login failed (HTTP {r.status_code})")
    p = session_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"cookies": r.cookies.get_dict()}), encoding="utf-8")
    try:
        os.chmod(p, 0o600)
    except OSError:
        pass


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


_RELOGIN_LOCK = threading.Lock()


def refresh_session(url: str, stale: dict | None):
    """After an HTTP 401 with the saved cookie `stale`: drop that cookie and build a new session
    (a fresh non-interactive login when credentials are configured, else anonymous). Threads that
    hit the same 401 log in once: a cookie that already differs from `stale` is reused."""
    with _RELOGIN_LOCK:
        if load_cookies() == stale:
            try:
                session_path().unlink()
            except OSError:
                pass
        return session_for(url)


def session_for(url: str):
    """A requests.Session carrying the Gaia cookies when `url` is the Gaia archive, else None."""
    if GAIA_HOST not in url:
        return None
    cookies = load_cookies()
    if not cookies:
        creds = credentials()
        if creds is None:
            return None
        try:
            _post_login(*creds)        # non-interactive login from the user's configured credentials
        except Exception as exc:      # noqa: BLE001 - fall back to anonymous access
            print(f"  Gaia login from configured credentials failed ({exc}); continuing anonymously")
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
    """Log in: configured credentials (environment or .env) if present, else interactive prompts."""
    creds = credentials()
    if creds is None:
        user = input("Gaia archive username: ").strip()
        pw = getpass.getpass("Gaia archive password (not echoed): ")
        creds = (user, pw)
    else:
        print("using GAIA_USERNAME / GAIA_PASSWORD from the environment or .env")
    try:
        _post_login(*creds)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from None
    finally:
        creds = None
    print(f"logged in; session cookie saved to {session_path()} (delete it or run gaia-logout to end the session)")


def logout() -> None:
    import requests

    cookies = load_cookies()          # never log in just to log out
    s = None
    if cookies:
        s = requests.Session()
        for k, v in cookies.items():
            s.cookies.set(k, v, domain=GAIA_HOST)
    if s is not None:
        try:
            s.post(LOGOUT_URL, timeout=30)
        except requests.RequestException:
            pass
    session_path().unlink(missing_ok=True)
    print("Gaia session removed")
