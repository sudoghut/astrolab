"""Static site for GitHub Pages (T-037): the Atlas and the study pages with the small files they read.

The pages already use relative paths, so the site is a subset of the repository with the same
layout: `atlas/web/`, and for every study `web/`, `results/` and `data/` (committed small tables). A
root `index.html` redirects to the Atlas. Nothing else is published: no code, no caches, no logs.

    python -m astrolab site <dest>      # build into <dest> (must be empty or absent)
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from . import config

# per study folder: the file types published (an allowlist; anything else is skipped and reported)
PUBLISHED = {"web": {".html", ".js", ".css", ".json", ".svg", ".png"},
             "results": {".json"},
             "data": {".csv", ".json"}}
ATLAS_SUFFIXES = {".html", ".js", ".css", ".json", ".svg", ".png"}
MAX_FILE_BYTES = 5 * 1024 ** 2                   # results warning line (AGENTS.md section 1.1)

REDIRECT = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>astrolab</title>
<meta http-equiv="refresh" content="0; url=atlas/web/">
<link rel="canonical" href="atlas/web/"></head>
<body><p><a href="atlas/web/">astrolab Atlas</a></p></body></html>
"""


def _files(root: Path):
    """(file, allowed suffixes): atlas/web and each study's web/, results/ and data/, with subfolders
    (for example results/dr3/, which study 001's page reads after the DR4 release)."""
    for p in sorted((root / "atlas" / "web").rglob("*")):
        yield p, ATLAS_SUFFIXES
    for study in sorted(p for p in (root / "studies").iterdir() if p.is_dir() and not p.name.startswith("_")):
        for sub, suffixes in PUBLISHED.items():
            d = study / sub
            if d.is_dir():
                for p in sorted(d.rglob("*")):
                    yield p, suffixes


def build(dest: Path, root: Path | None = None) -> dict:
    root = Path(root or config.ROOT).resolve()
    dest = Path(dest).resolve()
    if dest == root or root in dest.parents:
        raise SystemExit(f"{dest} is inside the project folder; build the site elsewhere (AGENTS.md 1.7)")
    if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
        raise SystemExit(f"{dest} exists and is not an empty folder")
    copied, skipped = [], []
    for src, suffixes in _files(root):
        if src.is_symlink() or not src.is_file():
            continue
        rel = src.relative_to(root)
        if src.suffix.lower() not in suffixes or src.stat().st_size > MAX_FILE_BYTES:
            skipped.append(str(rel).replace("\\", "/"))
            continue
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)
        copied.append(str(rel).replace("\\", "/"))
    (dest / "index.html").write_text(REDIRECT, encoding="utf-8")
    (dest / ".nojekyll").write_text("", encoding="utf-8")
    return {"files": len(copied), "bytes": sum((dest / f).stat().st_size for f in copied), "skipped": skipped}


_LINK = re.compile(r"""(?:src|href)\s*=\s*["']([^"']+)["']""")
_FETCH = re.compile(r"""fetch\(\s*["'`]([^"'`]+)["'`]""")


def broken_links(site: Path) -> list[str]:
    """Literal relative links in the HTML pages (src/href attributes and fetch() targets, query and
    fragment removed) that do not resolve inside the built site. NOT checked: URLs built at run time
    (template literals with ${...}, for example `../results/${n}.json`), CSS url(), srcset and
    standalone .js files; the per-study results/ and data/ folders are published whole instead."""
    site = Path(site)
    bad = []
    for page in site.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for target in _LINK.findall(text) + _FETCH.findall(text):
            target = re.split(r"[?#]", target)[0]
            if not target:
                continue
            if re.match(r"^[a-z]+:|^//|^\$\{|^mailto:", target) or "${" in target:
                continue
            path = (page.parent / target).resolve()
            if target.endswith("/"):
                path = path / "index.html"
            try:
                path.relative_to(site.resolve())
            except ValueError:
                bad.append(f"{page.relative_to(site).as_posix()} -> {target} (outside the site)")
                continue
            if not path.exists():
                bad.append(f"{page.relative_to(site).as_posix()} -> {target}")
    return sorted(set(bad))


# local machine paths and credential-like strings that must never be published
_SENSITIVE = re.compile(r"""[A-Za-z]:\\Users\\|[A-Za-z]:/Users/|/home/[a-z]|/Users/[A-Za-z]|AppData|Dropbox"""
                        r"""|(?i:password|passwd|secret|api[_-]?key|bearer\s|jsessionid)""")


def sensitive(site: Path) -> list[str]:
    """Published files that contain a local path or a credential-like string (file: first match)."""
    bad = []
    for f in sorted(Path(site).rglob("*")):
        if f.is_file():                              # every published file, images as raw bytes
            m = _SENSITIVE.search(f.read_bytes().decode("latin-1"))
            if m:
                bad.append(f"{f.relative_to(site).as_posix()}: {m.group(0)}")
    return bad
