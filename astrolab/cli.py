"""Command line: ``python -m astrolab <command>``. Output is kept short for agents."""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import sys

from . import cache, claims, config, study


def cmd_status(args) -> None:
    studies = study.discover()
    cl = claims.load_all()
    print(f"astrolab @ {config.ROOT}")
    print(f"studies: {len(studies)}")
    for s in studies:
        m = s.meta
        print(f"  {s.id:<48} {m.get('level', '?'):<3} {m.get('status', '?')}")
    print(f"claims: {len(cl)}")
    for c in cl:
        repro = (c.get("reproduction") or {}).get("status", "?")
        print(f"  {c.get('id', c['_file']):<40} {c.get('level', '?'):<3} {c.get('grade', '?'):<12} repro={repro}")
    problems = claims.validate_all()
    if problems:
        print(f"claim problems: {sum(map(len, problems.values()))} (run: python -m astrolab claims check)")
    print("cache:", cache.info())


def cmd_new(args) -> None:
    s = study.new(args.slug, args.title, args.level)
    print(f"created {s.path.relative_to(config.ROOT)}")
    print("next: fill title_zh / question_zh in study.yaml (bilingual rule),")
    print("      then README.md (question, hypothesis, criteria) BEFORE writing run.py")


def cmd_run(args) -> None:
    study.run(study.resolve(args.study), refresh=args.refresh)


def cmd_claims(args) -> None:
    if args.action == "check":
        problems = claims.validate_all()
        if not problems:
            print(f"all {len(claims.load_all())} claims valid")
            return
        for f, errs in problems.items():
            for e in errs:
                print(f"{f}: {e}")
        sys.exit(1)
    for c in claims.load_all():
        print(f"{c.get('id'):<40} {c.get('level'):<3} {c.get('grade'):<12} {c.get('title')}")


def cmd_atlas(args) -> None:
    from .results import write_json

    data = claims.atlas_data()
    out = write_json(config.ATLAS / "web" / "data" / "atlas.json", data)
    print(f"wrote {out.relative_to(config.ROOT)}: {len(data['claims'])} claims, {len(data['studies'])} studies")


def cmd_cache(args) -> None:
    if args.action == "prune":
        print(f"removed {cache.prune()} entries")
    elif args.action == "clear":
        print(f"removed {cache.clear()} entries")
    print(json.dumps(cache.info()))


def cmd_serve(args) -> None:
    cmd_atlas(args)
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(config.ROOT))
    with http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler) as httpd:
        base = f"http://127.0.0.1:{args.port}"
        print(f"atlas:   {base}/atlas/web/")
        for s in study.discover():
            if (s.path / "web" / "index.html").exists():
                print(f"study:   {base}/studies/{s.id}/web/")
        print("Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="astrolab", description="Laptop-scale astronomy research environment")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="overview of studies, claims, cache").set_defaults(func=cmd_status)

    sp = sub.add_parser("new", help="create a study folder from the template")
    sp.add_argument("slug")
    sp.add_argument("title")
    sp.add_argument("--level", default="L0", choices=study.LEVELS)
    sp.set_defaults(func=cmd_new)

    sp = sub.add_parser("run", help="run a study (name, number, or path)")
    sp.add_argument("study")
    sp.add_argument("--refresh", action="store_true", help="ignore cache and re-fetch")
    sp.set_defaults(func=cmd_run)

    sp = sub.add_parser("claims", help="list or check claims")
    sp.add_argument("action", nargs="?", default="list", choices=["list", "check"])
    sp.set_defaults(func=cmd_claims)

    sub.add_parser("atlas", help="build atlas/web/data/atlas.json").set_defaults(func=cmd_atlas)

    sp = sub.add_parser("cache", help="cache info / prune / clear")
    sp.add_argument("action", nargs="?", default="info", choices=["info", "prune", "clear"])
    sp.set_defaults(func=cmd_cache)

    sp = sub.add_parser("serve", help="serve project over http for the web pages")
    sp.add_argument("--port", type=int, default=8765)
    sp.set_defaults(func=cmd_serve)

    args = p.parse_args(argv)
    args.func(args)
