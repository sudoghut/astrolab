"""Machine checks for the Lean argument of paper studies (design/007 section 2.2).

Order: 1. scan the source (before any build: `#eval` would run at build time);
2. `lake build --wfail` on a copy outside Dropbox; 3. environment-level audit
(tests/lean_audit/Audit.lean, which does not import the module); 4. check the audit
report in Python (tags, provenance, shapes, NUM bindings).

Skipped when `lake` or the template's Lean toolchain is not installed: a missing
toolchain must never trigger a download (AGENTS.md section 1).
"""
from __future__ import annotations

import json
import math
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
STUDIES = ROOT / "studies"
TEMPLATE = STUDIES / "_template" / "argument"
AUDIT = Path(__file__).resolve().parent / "lean_audit" / "Audit.lean"
WIKI = ROOT / "docs" / "wiki"
ALLOWED_FILES = {"lakefile.toml", "lean-toolchain", "Argument.lean"}

BANNED_IDENTS = {
    "axiom", "sorry", "admit", "native_decide", "unsafe", "implemented_by", "extern",
    "import", "macro", "macro_rules", "syntax", "declare_syntax_cat", "notation", "infix",
    "infixl", "infixr", "prefix", "postfix", "binder_predicate", "elab", "elab_rules",
    "run_cmd", "run_elab", "run_meta", "initialize", "builtin_initialize", "opaque", "partial",
    "app_unexpander", "skipKernelTC", "attribute",
}
# Non-ASCII characters allowed outside comments (logical and bracket symbols only).
ALLOWED_UNICODE = set("→←↔∀∃¬∧∨≠≤≥⟨⟩·×λ▸")
KINDS = ("OBS", "MOD", "STAT", "NUM", "LIT", "GAP")
DOC_RE = re.compile(
    r'^(?P<kind>OBS|MOD|STAT|NUM|LIT|GAP) \[(?:(?P<stated>stated)(?: (?P<paper>[^\s:\]]+))?: "(?P<quote>[^"\]]+)"'
    r'|(?P<implied>implied)|(?P<recon>reconstructed))\](?P<rest>.*)$'
)
NUM_RE = re.compile(
    r"NUM\[(results/[^:\]]+\.json):([A-Za-z0-9_.-]+)\s*(<=|>=|==|<|>)\s*(-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\]"
)
LIT_REF_RE = re.compile(r"(?<![\w./])(\d{4}\.\d{4,5}(?:v\d+)?|[a-z-]+(?:\.[A-Z]{2})?/\d{7}(?:v\d+)?|\d{4}[A-Za-z&][A-Za-z0-9&.]{13}[A-Za-z0-9.])(?![\w/])")


# ---------------------------------------------------------------- 1. source scan

def strip_comments(src: str) -> str:
    """Remove `--` line comments and (nested) `/- -/` block comments; keep newlines."""
    out, i, depth, n = [], 0, 0, len(src)
    while i < n:
        if depth == 0 and src.startswith("--", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
        elif src.startswith("/-", i):
            depth += 1
            i += 2
        elif depth > 0 and src.startswith("-/", i):
            depth -= 1
            i += 2
        else:
            ch = src[i]
            if depth == 0 or ch == "\n":
                out.append(ch)
            i += 1
    if depth:
        raise AssertionError("unterminated block comment")
    return "".join(out)


def normalise(code: str) -> str:
    return " ".join(code.split())


def fixed_blocks() -> tuple[str, str]:
    code = normalise(strip_comments((TEMPLATE / "Argument.lean").read_text(encoding="utf-8")))
    a = re.search(r"inductive Prov where .*? deriving DecidableEq", code)
    b = re.search(r"def Premises .*?def Explicit .*?prem f v", code)
    assert a and b, "template lost its fixed blocks"
    return a.group(0), b.group(0)


def scan_source(src: str) -> list[str]:
    """Problems found before building (fail closed)."""
    problems = []
    try:
        code = strip_comments(src)
    except AssertionError as e:
        return [str(e)]
    hints = {"↦": " (write =>)", "ℕ": " (write Nat)", "ℤ": " (write Int)", "\ufeff": " (save without BOM)"}
    for ch in sorted({c for c in code if ord(c) > 127 and c not in ALLOWED_UNICODE}):
        problems.append(f"character {ch!r} (U+{ord(ch):04X}) outside comments; identifiers must be "
                        f"ASCII{hints.get(ch, '')}")
    for ch, what in (('"', "string literal"), ("'", "character literal or primed name"), ("«", "quoted name")):
        if ch in code:
            problems.append(f"{what} ({ch}) outside comments")
    if "@[" in code:
        problems.append("attributes (@[...]) are not allowed")
    for m in re.finditer(r"#[A-Za-z_]+", code):
        problems.append(f"command {m.group(0)} is not allowed")
    if re.search(r"\+\s*native", code):
        problems.append("decide +native is not allowed")
    for ident in re.findall(r"[A-Za-z_][A-Za-z0-9_!?]*(?:\.[A-Za-z_][A-Za-z0-9_!?]*)*", code):
        for part in ident.split("."):
            if part in BANNED_IDENTS:
                problems.append(f"forbidden token {part!r}")
    for m in re.finditer(r"\bset_option\s+([A-Za-z_][A-Za-z0-9_.]*)", code):
        name = m.group(1)
        if not (name.startswith("linter.") or name == "maxHeartbeats"):
            problems.append(f"set_option {name} is not allowed")
    norm = normalise(code)
    a, b = fixed_blocks()
    if a not in norm:
        problems.append("fixed block A (inductive Prov) differs from the template")
    if b not in norm:
        problems.append("fixed block B (Premises/Without/Stated/Explicit) differs from the template")
    return sorted(set(problems))


def scan_folder(arg: Path) -> list[str]:
    missing = sorted(n for n in ALLOWED_FILES if not (arg / n).is_file())
    if missing:
        return [f"argument/ is missing {missing}"]
    problems = []
    extra = {p.name for p in arg.iterdir()} - ALLOWED_FILES
    if extra:
        problems.append(f"unexpected files in argument/: {sorted(extra)} "
                        "(build outside the project; only lakefile.toml, lean-toolchain, Argument.lean)")
    for name in ("lakefile.toml", "lean-toolchain"):
        mine = (arg / name).read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        tpl = (TEMPLATE / name).read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        if mine != tpl:
            problems.append(f"{name} differs from the template (changing it needs the user's consent)")
    return problems + scan_source((arg / "Argument.lean").read_text(encoding="utf-8"))


# ---------------------------------------------------------------- 2/3. build and audit

def lean_available() -> str | None:
    """Reason to skip, or None when lake and the template toolchain are installed."""
    if not shutil.which("lake") or not shutil.which("elan"):
        return "lake/elan not installed"
    want = (TEMPLATE / "lean-toolchain").read_text(encoding="utf-8").strip()
    out = subprocess.run(["elan", "toolchain", "list"], capture_output=True, text=True, timeout=60).stdout
    if not any(line.split()[0] == want for line in out.splitlines() if line.strip()):
        return f"Lean toolchain {want} not installed (not downloading it)"
    return None


def build_and_audit(arg: Path) -> str:
    """Copy outside Dropbox, build with --wfail, run the audit; return the audit output."""
    with tempfile.TemporaryDirectory(prefix="astrolab-lean-") as tmp:
        work = Path(tmp) / "argument"
        work.mkdir()
        for name in ALLOWED_FILES:
            shutil.copy2(arg / name, work / name)
        shutil.copy2(AUDIT, work / "Audit.lean")
        r = subprocess.run(["lake", "build", "--wfail"], cwd=work, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=600)
        if r.returncode != 0:
            raise AssertionError(f"lake build --wfail failed:\n{r.stdout[-4000:]}\n{r.stderr[-2000:]}")
        r = subprocess.run(["lake", "env", "lean", "Audit.lean"], cwd=work, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=600)
        return r.stdout + r.stderr


# ---------------------------------------------------------------- 4. report checks

@dataclass
class Premise:
    name: str
    prov: str
    head: str
    literal: bool
    proj: bool
    num: str
    forbidden: str
    doc: str
    body: str = ""


@dataclass
class Report:
    premises: list[Premise] = field(default_factory=list)
    conclusion: dict = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    ok: bool = False


def parse_report(text: str) -> Report:
    rep = Report()
    for line in text.splitlines():
        if line.startswith("PREMISE "):
            head, doc = line.split(" | doc=", 1)
            head, body = head.split(" | body=", 1)
            parts = head.split(" | ")
            kv = dict(p.split("=", 1) for p in parts[1:])
            rep.premises.append(Premise(parts[0].split()[1], kv["prov"], kv["head"],
                                        kv["literal"] == "true", kv["proj"] == "true",
                                        kv["num"], kv["forbidden"], doc.strip(), body.strip()))
        elif line.startswith("CONCLUSION "):
            head, doc = line.split(" | doc=", 1)
            head, body = head.split(" | body=", 1) if " | body=" in head else (head, "")
            rep.conclusion = dict(p.split("=", 1) for p in head.split(" | ")[1:])
            rep.conclusion["body"] = body.strip()
            rep.conclusion["doc"] = doc.strip()
        elif line.startswith("ERROR: "):
            rep.errors.append(line[7:])
        elif line.strip() == "AUDIT_OK":
            rep.ok = True
    return rep


def _json_get(data, key: str):
    for part in key.split("."):
        if not isinstance(data, dict) or part not in data:
            raise KeyError(key)
        data = data[part]
    return data


def _compare(x: float, op: str, y: float) -> bool:
    if op == "==":
        return abs(x - y) <= max(1e-9 * abs(y), 1e-12)
    return {"<": x < y, "<=": x <= y, ">": x > y, ">=": x >= y}[op]


def check_report(rep: Report, study_dir: Path | None, meta: dict) -> tuple[list[str], list[str]]:
    """Return (problems, notes)."""
    problems = [f"audit: {e}" for e in rep.errors]
    notes = []
    if not rep.ok:
        problems.append("audit did not finish with AUDIT_OK")
    papers = meta.get("papers") or []
    if any(not isinstance(x, str) for x in papers):
        problems.append("study.yaml papers: quote arXiv ids as strings, e.g. [\"2209.06833\"]")
    papers = [str(x) for x in papers]
    status = meta.get("status", "planned")
    for p in rep.premises:
        where = f"premise {p.name}"
        m = DOC_RE.match(p.doc)
        if not m:
            problems.append(f"{where}: doc comment must start with 'KIND [provenance]': {p.doc!r}")
            continue
        kind = m["kind"]
        prov = "stated" if m["stated"] else "implied" if m["implied"] else "reconstructed"
        if prov != p.prov:
            problems.append(f"{where}: doc says [{prov}] but prov gives .{p.prov}")
        if (kind == "GAP") != (prov == "reconstructed"):
            problems.append(f"{where}: GAP must be used exactly for [reconstructed] premises")
        if prov == "implied" and not m["rest"].strip():
            problems.append(f"{where}: [implied] needs a source after the bracket")
        if prov == "stated" and len(papers) > 1 and not m["paper"]:
            problems.append(f"{where}: several papers: write [stated <arXiv id>: \"...\"]")
        if m["paper"] and papers and re.sub(r"v\d+$", "", m["paper"]) not in papers:
            problems.append(f"{where}: paper {m['paper']} is not listed in study.yaml papers")
        if kind in ("OBS", "NUM", "STAT") and not p.literal:
            problems.append(f"{where}: {kind} must be a literal (atom, negated atom or comparison), got head {p.head}")
        if p.head == "and":
            problems.append(f"{where}: split top-level conjunctions into separate premises")
        if not p.proj:
            problems.append(f"{where}: body mentions no Vocab field")
        if p.forbidden not in ("[]", ""):
            problems.append(f"{where}: helper or foreign constants in prem: {p.forbidden}")
        if kind == "LIT" and not LIT_REF_RE.search(p.doc):
            problems.append(f"{where}: LIT needs an arXiv id or bibcode")
        bindings = NUM_RE.findall(p.doc)
        if kind == "NUM":
            if not bindings:
                problems.append(f"{where}: NUM needs NUM[results/<file>.json:<key> <op> <value>]")
            if p.num == "none":
                problems.append(f"{where}: NUM must have the form 'field op literal'")
        elif bindings:
            problems.append(f"{where}: NUM[...] bindings belong on NUM premises only")
        if kind == "NUM" and p.num != "none":
            lean_op, lean_val = p.num.split(":")
            for path, key, op, val in bindings:
                v = float(val)
                if op != lean_op or not any(math.isclose(v, int(lean_val) / 10 ** k, rel_tol=1e-9, abs_tol=1e-12)
                                            for k in range(10)):
                    problems.append(f"{where}: binding {op} {val} does not match the Lean threshold {lean_op} {lean_val}")
                if study_dir is None:
                    continue
                f = study_dir / path
                if not f.exists():
                    if status in ("reproduced", "concluded"):
                        problems.append(f"{where}: {path} missing but the study is {status}")
                    else:
                        notes.append(f"{where}: {path} not produced yet; binding not checked")
                    continue
                try:
                    x = _json_get(json.loads(f.read_text(encoding="utf-8")), key)
                except KeyError:
                    problems.append(f"{where}: key {key} missing in {path}")
                    continue
                except json.JSONDecodeError as e:
                    problems.append(f"{where}: {path} is not valid JSON ({e})")
                    continue
                if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x):
                    problems.append(f"{where}: {path}:{key} is not a finite number")
                elif not _compare(float(x), op, v):
                    problems.append(f"{where}: {path}:{key} = {x} fails {op} {val}")
    c = rep.conclusion
    if not c:
        problems.append("audit printed no CONCLUSION line")
    else:
        if c.get("forbidden") not in ("[]", ""):
            problems.append(f"Conclusion uses helper or foreign constants: {c.get('forbidden')}")
        if c.get("proj") != "true":
            problems.append("Conclusion mentions no Vocab field")
        if "[stated" not in c.get("doc", ""):
            problems.append("Conclusion needs a doc comment with the paper's [stated: \"...\"] conclusion")
    return problems, notes


def write_review_table(name: str, rep: Report) -> Path:
    """Quote / kind / Lean-body table for the referee, written outside Dropbox."""
    out = Path(tempfile.gettempdir()) / "astrolab-lean-report" / f"{name}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = ["| premise | doc (kind, provenance, quote) | Lean body |", "|---|---|---|"]
    rows += [f"| {p.name} | {p.doc.replace('|', '/')} | `{p.body.replace('|', '/')}` |" for p in rep.premises]
    rows.append(f"\nConclusion: {rep.conclusion.get('doc', '')}  \nLean: `{rep.conclusion.get('body', '')}`")
    out.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return out


def check_argument(arg: Path, study_dir: Path | None, meta: dict, name: str) -> list[str]:
    problems = scan_folder(arg)
    if problems:
        return problems  # never build a file that failed the scan
    out = build_and_audit(arg)
    rep = parse_report(out)
    problems, notes = check_report(rep, study_dir, meta)
    table = write_review_table(name, rep)
    print(f"[{name}] review table: {table}")
    for n in notes:
        print(f"[{name}] note: {n}")
    if not rep.premises and not rep.ok:
        problems.append(f"audit output:\n{out[-3000:]}")
    return problems


# ---------------------------------------------------------------- tests

def _studies():
    for d in sorted(STUDIES.iterdir()):
        if d.is_dir() and not d.name.startswith((".", "_")) and (d / "study.yaml").exists():
            yield d


def _meta(d: Path) -> dict:
    return yaml.safe_load((d / "study.yaml").read_text(encoding="utf-8")) or {}


def _same_as_template(arg: Path) -> bool:
    return all((arg / n).exists() and (arg / n).read_bytes().replace(b"\r\n", b"\n")
               == (TEMPLATE / n).read_bytes().replace(b"\r\n", b"\n") for n in ALLOWED_FILES)


@pytest.fixture(scope="module")
def lean():
    reason = lean_available()
    if reason:
        pytest.skip(reason)


def test_template_scans_clean():
    assert scan_folder(TEMPLATE) == []


@pytest.mark.parametrize("study_dir", [d for d in _studies() if (d / "argument").exists()],
                         ids=lambda d: d.name)
def test_study_argument_scan(study_dir):
    """The source scan needs no Lean, so it runs even where the build is skipped."""
    assert scan_folder(study_dir / "argument") == []


def test_template_argument_passes(lean):
    assert check_argument(TEMPLATE, None, {"status": "planned"}, "_template") == []


@pytest.mark.parametrize("study_dir", [d for d in _studies() if (d / "argument").exists()],
                         ids=lambda d: d.name)
def test_study_argument(study_dir, lean):
    arg = study_dir / "argument"
    if _same_as_template(arg):
        pytest.skip("argument/ is the unchanged template example (non-paper study)")
    problems = check_argument(arg, study_dir, _meta(study_dir), study_dir.name)
    assert problems == [], "\n".join(problems)


@pytest.mark.parametrize("study_dir", list(_studies()), ids=lambda d: d.name)
def test_paper_study_coverage(study_dir):
    meta = _meta(study_dir)
    if meta.get("wiki"):
        page = WIKI / f"{meta['wiki']}.md"
        assert page.exists(), f"study.yaml wiki: {meta['wiki']} but {page} does not exist"
    if meta.get("papers"):
        arg = study_dir / "argument"
        assert arg.exists(), "paper study without argument/"
        assert not _same_as_template(arg), "paper study still has the template's example argument"
        assert all(isinstance(x, str) for x in meta["papers"]), "quote arXiv ids in study.yaml papers"


# --- the checker must reject known shortcuts (scan-only cases need no Lean) ---

def _mutated(tmp_path: Path, *pairs) -> Path:
    """Copy the template and apply (old, new) replacements; `pairs` is old, new or a list of pairs."""
    if len(pairs) == 2 and isinstance(pairs[0], str):
        pairs = [tuple(pairs)]
    else:
        pairs = list(pairs[0])
    arg = tmp_path / "argument"
    shutil.copytree(TEMPLATE, arg)
    src = (arg / "Argument.lean").read_text(encoding="utf-8")
    for old, new in pairs:
        assert old in src, old
        src = src.replace(old, new, 1)
    (arg / "Argument.lean").write_text(src, encoding="utf-8")
    return arg


SCAN_MUTATIONS = {
    "sorry": ("theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=\n  fun h =>",
              "theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=\n  sorry\ntheorem unused_x : True := fun h =>"),
    "axiom": ("end Argument", "axiom cheat : False\nend Argument"),
    "eval": ("end Argument", "#eval 1\nend Argument"),
    "macro": ("end Argument", "macro x:term : term => pure x\nend Argument"),
    "string": ("end Argument", "def s := 0\ndef t := \"x\"\nend Argument"),
    "subscript": ("end Argument", "theorem h\u2081 : True := trivial\nend Argument"),
    "set_option": ("end Argument", "set_option debug.skipKernelTC true\nend Argument"),
    "admit": ("end Argument", "theorem z : True := by admit\nend Argument"),
    "block_b": ("def Stated (v : Vocab) : Prop := ∀ f, prov f = .stated → prem f v",
                "def Stated (v : Vocab) : Prop := ∀ f, prov f ≠ .reconstructed → prem f v"),
}


@pytest.mark.parametrize("name", sorted(SCAN_MUTATIONS))
def test_scan_rejects(name, tmp_path):
    arg = _mutated(tmp_path, *SCAN_MUTATIONS[name])
    assert scan_folder(arg), f"scan accepted mutation {name}"


def test_scan_rejects_extra_files_and_toolchain(tmp_path):
    arg = _mutated(tmp_path, "end Argument", "end Argument")
    (arg / "lake-manifest.json").write_text("{}", encoding="utf-8")
    (arg / "lean-toolchain").write_text("leanprover/lean4:stable\n", encoding="utf-8")
    problems = scan_folder(arg)
    assert any("unexpected files" in p for p in problems)
    assert any("lean-toolchain differs" in p for p in problems)


BUILD_MUTATIONS = {
    # field-versus-field comparison written as an OBS (allowed only in MOD/LIT/GAP)
    "obs_field_field": [("  | .obs_orbit, v => v.Orbit", "  | .obs_orbit, v => v.fm_centi ≥ v.fm_centi"),
                        ("  · exact h ⟨True, 0, False, False, False, False⟩ trivial", "  · exact h ⟨True, 0, False, False, False, False⟩ (by simp [prem])")],
    # Prop equality smuggling a conjunction into an OBS
    "obs_prop_eq": [("  | .obs_orbit, v => v.Orbit", "  | .obs_orbit, v => (v.Orbit ∧ v.Orbit) = True"),
                    ("  · exact h ⟨True, 0, False, False, False, False⟩ trivial", "  · exact h ⟨True, 0, False, False, False, False⟩ (by simp [prem])")],
    # doc says [stated] but prov gives .implied
    "prov_mismatch": ("  | .obs_dark => .stated", "  | .obs_dark => .implied"),
    # wrong statement for a pinned theorem
    "pinned": ("theorem final_nontrivial : ¬ ∀ v : Vocab, Conclusion v :=\n  fun h => h ⟨False, 0, False, False, False, False⟩",
               "theorem final_nontrivial : ∃ v : Vocab, ¬ Conclusion v :=\n  ⟨⟨False, 0, False, False, False, False⟩, fun h => h⟩"),
    # GAP relabelled as MOD while staying [reconstructed]
    "gap_label": ("/-- GAP [reconstructed] the companion is not an inner binary; the paper gives no test -/",
                  "/-- MOD [reconstructed] the companion is not an inner binary; the paper gives no test -/"),
    # NUM binding that does not match the Lean threshold
    "num_binding": ("NUM[results/orbit.json:f_m_msun > 3.0]", "NUM[results/orbit.json:f_m_msun > 2.0]"),
    # a Vocab field type outside the whitelist (still builds, so the audit must catch it)
    "vocab_type": ("  fm_centi : Nat", "  fm_centi : Fin 1000"),
}


EXPECTED_REASON = {
    "pinned": "wrong statement",
    "gap_label": "GAP must be used exactly",
    "num_binding": "does not match the Lean threshold",
    "vocab_type": "disallowed type",
    "obs_field_field": "must be a literal",
    "obs_prop_eq": "must be a literal",
    "prov_mismatch": "but prov gives",
}


@pytest.mark.parametrize("name", sorted(BUILD_MUTATIONS))
def test_audit_rejects(name, tmp_path, lean):
    m = BUILD_MUTATIONS[name]
    arg = _mutated(tmp_path, m) if isinstance(m, list) else _mutated(tmp_path, *m)
    problems = check_argument(arg, None, {"status": "planned"}, f"mutation-{name}")
    assert any(EXPECTED_REASON[name] in p for p in problems), problems
