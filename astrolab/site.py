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

PUBLISHED = ("web", "results", "data")          # per study
SUFFIXES = {".html", ".js", ".css", ".json", ".csv", ".svg", ".png", ".txt"}
MAX_FILE_BYTES = 5 * 1024 ** 2                   # results warning line (AGENTS.md section 1.1)

REDIRECT = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>astrolab</title>
<meta http-equiv="refresh" content="0; url=atlas/web/">
<link rel="canonical" href="atlas/web/"></head>
<body><p><a href="atlas/web/">astrolab Atlas</a></p></body></html>
"""


def _files(root: Path):
    yield from sorted(p for p in (root / "atlas" / "web").rglob("*") if p.is_file())
    for study in sorted(p for p in (root / "studies").iterdir() if p.is_dir() and not p.name.startswith("_")):
        for sub in PUBLISHED:
            d = study / sub
            if d.is_dir():
                # top level of results/ and data/ only; web/ may have subfolders
                it = d.rglob("*") if sub == "web" else d.iterdir()
                yield from sorted(p for p in it if p.is_file())


def build(dest: Path, root: Path | None = None) -> dict:
    root = Path(root or config.ROOT)
    dest = Path(dest)
    if dest.exists() and any(dest.iterdir()):
        raise SystemExit(f"{dest} is not empty")
    copied, skipped = [], []
    for src in _files(root):
        rel = src.relative_to(root)
        if src.suffix.lower() not in SUFFIXES or src.stat().st_size > MAX_FILE_BYTES:
            skipped.append(str(rel).replace("\\", "/"))
            continue
        out = dest / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, out)
        copied.append(str(rel).replace("\\", "/"))
    (dest / "index.html").write_text(REDIRECT, encoding="utf-8")
    (dest / ".nojekyll").write_text("", encoding="utf-8")
    return {"files": len(copied), "bytes": sum((dest / f).stat().st_size for f in copied), "skipped": skipped}


_LINK = re.compile(r"""(?:src|href)\s*=\s*["']([^"'#?]+)["']""")
_FETCH = re.compile(r"""fetch\(\s*["'`]([^"'`$]+)["'`]\s*\)""")


def broken_links(site: Path) -> list[str]:
    """Static relative links (src/href attributes and literal fetch() targets) that do not resolve
    inside the built site. Template links (with ${...}) and absolute URLs are not checked."""
    site = Path(site)
    bad = []
    for page in site.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for target in _LINK.findall(text) + _FETCH.findall(text):
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
