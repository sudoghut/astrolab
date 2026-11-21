"""Download-limit exceptions in study code are traceable (AGENTS.md section 1.6).

Every ``budget_consent=`` / ``cap_consent=`` in a study's Python files (run.py, helper modules,
explore/ scripts) must be a string literal (or a module-level string constant) naming an existing
to-do item T-NNN (in TODO.md or DONE.md), and the study's log.md must record that exception: a
paragraph naming the T-number and the budget ("budget"/"预算") or cap ("cap"/"上限") exception.
Offline; reads only repository files.
"""
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYWORDS = {"budget_consent": ("budget", "预算"), "cap_consent": ("cap", "上限")}
TNUM = re.compile(r"\bT-\d{3,}\b")


def _string_constants(tree: ast.Module) -> dict[str, str]:
    out = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = node.value.value
    return out


def consent_problems(study_dir: Path, known_ids: set[str]) -> list[str]:
    files = sorted(study_dir.glob("*.py")) + sorted((study_dir / "explore").glob("*.py"))
    log = study_dir / "log.md"
    paragraphs = re.split(r"\n\s*\n", log.read_text(encoding="utf-8")) if log.exists() else []
    problems = []
    for f in files:
        tree = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        consts = _string_constants(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            for kw in node.keywords:
                if kw.arg not in KEYWORDS:
                    continue
                where = f"{f.relative_to(study_dir.parent)}:{kw.value.lineno} {kw.arg}"
                v = kw.value
                if isinstance(v, ast.Constant) and v.value is None:
                    continue
                if isinstance(v, ast.Constant) and isinstance(v.value, str):
                    text = v.value
                elif isinstance(v, ast.Name) and v.id in consts:
                    text = consts[v.id]
                else:
                    problems.append(f"{where}: use a string literal or module-level string constant")
                    continue
                ids = [t for t in TNUM.findall(text) if t in known_ids]
                if not ids:
                    problems.append(f"{where}: consent {text!r} names no T-NNN in TODO.md or DONE.md")
                    continue
                words = KEYWORDS[kw.arg]
                if not any(re.search(rf"\b{t}\b", p) and any(re.search(rf"\b{w}", p, re.I) for w in words)
                           for t in ids for p in paragraphs):
                    problems.append(f"{where}: log.md has no paragraph naming {'/'.join(ids)} with "
                                    f"{' or '.join(words)}")
    return problems


def _known_ids() -> set[str]:
    text = "".join((ROOT / n).read_text(encoding="utf-8") for n in ("TODO.md", "DONE.md"))
    return set(re.findall(r"\*\*(T-\d{3,})\*\*", text))


def test_repo_consents_are_recorded():
    known = _known_ids()
    problems = []
    for d in sorted((ROOT / "studies").iterdir()):
        if d.is_dir() and not d.name.startswith("_"):
            problems += consent_problems(d, known)
    assert not problems, "\n".join(problems)


def test_consent_checker_on_synthetic_study(tmp_path):
    d = tmp_path / "studies" / "099-x"
    (d / "explore").mkdir(parents=True)
    (d / "run.py").write_text(
        'WHY = "user consent 2026-11-21, TODO.md T-021"\n'
        "def main(ctx):\n"
        "    ctx.http('u', budget_consent=WHY)\n"
        "    ctx.http('v', max_bytes=1, cap_consent='user consent, TODO.md T-021, log.md')\n"
        "    ctx.http('w', budget_consent=None)\n", encoding="utf-8")
    (d / "log.md").write_text("## 2026-11-21\n\nT-021: the user agreed to a budget exception.\n",
                              encoding="utf-8")
    probs = consent_problems(d, {"T-021"})
    assert len(probs) == 1 and "cap_consent" in probs[0] and "log.md" in probs[0]
    (d / "log.md").write_text("T-021: budget exception and cap exception agreed.\n", encoding="utf-8")
    assert consent_problems(d, {"T-021"}) == []
    assert any("T-NNN" in p for p in consent_problems(d, {"T-001"}))
    (d / "explore" / "e.py").write_text("def main(ctx):\n    ctx.http('u', cap_consent=f'{1}')\n",
                                        encoding="utf-8")
    assert any("string literal" in p for p in consent_problems(d, {"T-021"}))
