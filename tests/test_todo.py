"""Format checks for the to-do list (TODO.md) and the done log (DONE.md).

Rules: AGENTS.md section 2 and design/006-plan_todo-list-and-done-log-mechanism.md.
Offline; reads only the two files. The check_* functions raise AssertionError on
the first problem, so they can be tested on synthetic input below.
"""
import datetime as dt
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
TODO = ROOT / "TODO.md"
DONE = ROOT / "DONE.md"

TODO_SECTIONS = ["## 进行中（Doing）", "## 下一步（Next）", "## 待办池（Backlog）"]

DATE = r"\d{4}-\d{2}-\d{2}"
ID = r"T-(?P<id>\d{3,})"
TITLE = r"(?P<title>(?:(?! · | — ).)+)"
# Any line that looks like a list item with a checkbox, or that carries a bold ID,
# must be a well-formed top-level item; otherwise it would silently escape the checks.
SUSPECT = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s*\[(?:\s*|[^\]]{1,3}|[\sxX\-]*)\](?!\()|\*\*T-\d+\*\*")
TODO_ITEM = re.compile(rf"^- \[ \] \*\*{ID}\*\* {TITLE} · 登记 (?P<date>{DATE})(?P<rest>(?: · .+)?)$")
TODO_FIELD = re.compile(
    rf"^(?:截止 (?P<due>{DATE})|分支 (?:`[^`]+`|\S+)|计划 \[[^\]]+\]\([^)]+\)|(?:前置|来源) (?P<refs>T-\d{{3,}}(?:、T-\d{{3,}})*))$"
)
DONE_X = re.compile(
    rf"^- \[x\] \*\*{ID}\*\* {TITLE} · 完成 (?P<date>{DATE}) · PR #\d+(?: · 计划 \[[^\]]+\]\([^)]+\))? — \S.*$"
)
DONE_DROP = re.compile(rf"^- \[-\] \*\*{ID}\*\* {TITLE} · 放弃 (?P<date>{DATE})(?: · 计划 \[[^\]]+\]\([^)]+\))? — \S.*$")
MONTH = re.compile(r"^## (\d{4})-(\d{2})$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})(.*)$")


def _date(s, where):
    try:
        return dt.date.fromisoformat(s)
    except ValueError:
        raise AssertionError(f"{where}: invalid date {s!r}") from None


def _lines(text, name):
    """Yield (lineno, line) outside fenced code blocks, trailing whitespace stripped."""
    fence = None
    for n, line in enumerate(text.lstrip("\ufeff").splitlines(), 1):
        m = FENCE.match(line)
        if m:
            run, info = m[1], m[2].strip()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not info:
                fence = None
            continue
        if fence is None:
            yield n, line.rstrip()
    assert fence is None, f"{name}: unclosed code fence"


def check_todo(text):
    """Return ({id: where}, [referenced ids]); raise AssertionError on any problem."""
    ids, refs, headings, current = {}, [], [], None
    for n, line in _lines(text, "TODO.md"):
        where = f"TODO.md:{n}"
        if line.startswith("## "):
            current = line
            headings.append(line)
            continue
        if not SUSPECT.search(line):
            continue
        m = TODO_ITEM.match(line)
        assert m, (
            f"{where}: malformed or not-open item (expected top-level "
            f"'- [ ] **T-NNN** title · 登记 YYYY-MM-DD[ · field ...]'; "
            f"the title must not contain ' · ' or ' — '): {line}"
        )
        assert current in TODO_SECTIONS, f"{where}: item outside the three sections"
        _date(m["date"], where)
        for field in filter(None, m["rest"].split(" · ")):
            f = TODO_FIELD.match(field)
            assert f, (
                f"{where}: unknown or malformed field {field!r} (allowed: 截止 YYYY-MM-DD, 分支 name, "
                f"计划 [text](path), 前置 T-NNN、T-NNN, 来源 T-NNN)"
            )
            if f["due"]:
                _date(f["due"], where)
            if f["refs"]:
                refs += [(int(r[2:]), where) for r in f["refs"].split("、")]
        i = int(m["id"])
        assert i not in ids, f"T-{i:03d} used twice: {ids[i]} and {where}"
        ids[i] = where
    assert headings == TODO_SECTIONS, f"TODO.md sections must be exactly {TODO_SECTIONS}, got {headings}"
    return ids, refs


def check_done(text):
    """Return {id: where}; raise AssertionError on any problem."""
    ids, months, last, month = {}, [], None, None
    for n, line in _lines(text, "DONE.md"):
        where = f"DONE.md:{n}"
        if line.startswith("## "):
            h = MONTH.match(line)
            assert h and 1 <= int(h[2]) <= 12, f"{where}: section headings must be '## YYYY-MM': {line}"
            month = f"{h[1]}-{h[2]}"
            assert not months or month < months[-1], f"{where}: month sections must be unique and newest first"
            months.append(month)
            continue
        if not SUSPECT.search(line):
            continue
        m = DONE_X.match(line) or DONE_DROP.match(line)
        assert m, (
            f"{where}: malformed item (expected top-level "
            f"'- [x] **T-NNN** title · 完成 YYYY-MM-DD · PR #N[ · 计划 [..](..)] — result' "
            f"or '- [-] **T-NNN** title · 放弃 YYYY-MM-DD[ · 计划 [..](..)] — reason'; "
            f"the title must not contain ' · ' or ' — '): {line}"
        )
        assert month, f"{where}: item before the first '## YYYY-MM' section"
        d = _date(m["date"], where)
        assert m["date"][:7] == month, f"{where}: date {m['date']} is not in section {month}"
        assert last is None or d <= last, f"{where}: items must be newest first"
        last = d
        i = int(m["id"])
        assert i not in ids, f"T-{i:03d} used twice: {ids[i]} and {where}"
        ids[i] = where
    return ids


def check_both(todo_text, done_text):
    todo_ids, refs = check_todo(todo_text)
    done_ids = check_done(done_text)
    for i in todo_ids.keys() & done_ids.keys():
        raise AssertionError(f"T-{i:03d} used twice: {todo_ids[i]} and {done_ids[i]}")
    for i, where in refs:
        assert i in todo_ids or i in done_ids, f"{where}: reference to unknown T-{i:03d}"


def test_todo_and_done_files():
    check_both(TODO.read_text(encoding="utf-8"), DONE.read_text(encoding="utf-8"))


# --- the checker itself must reject bad input and accept good input -----------

S0, S1, S2 = TODO_SECTIONS
GOOD_TODO = [
    S0,
    "- [ ] **T-010** title · 登记 2026-11-14 · 分支 `feat/x` · 计划 [006](design/006.md)",
    "  - 计划：1. a；2. b",
    "  - 备注：c",
    S1,
    "- [ ] **T-012** next · 登记 2026-11-14 · 截止 2026-12-02 · 前置 T-010",
    S2,
    "- [ ] **T-011** backlog · 登记 2026-11-15 · 来源 T-010",
    "- [ ] **T-1000** four digits · 登记 2026-11-15",
]
GOOD_DONE = [
    "## 2026-12",
    "- [-] **T-013** dropped · 放弃 2026-12-01 — superseded by T-014",
    "## 2026-11",
    "- [x] **T-014** done · 完成 2026-11-20 · PR #5 · 计划 [006](design/006.md) — result",
    "- [x] **T-015** simple · 完成 2026-11-20 · PR #6 — result",
]


def _todo(*extra, base=GOOD_TODO):
    return "\n".join(list(base) + list(extra))


def test_checker_accepts_examples():
    check_both(_todo("- [ ] **T-016** trailing space · 登记 2026-11-15  "), "\n".join(GOOD_DONE))
    check_both(_todo().replace("\n", "\r\n"), "\ufeff" + "\n".join(GOOD_DONE))
    check_both(_todo("```", "- [x] **T-099** example in a fence", "```"), "")
    check_both(_todo("````md", "```", "- [ ] bogus", "```", "````", "  - [006](design/006.md) link, not an item"), "")
    check_both(_todo("- [ ] **T-017** bare branch · 登记 2026-11-15 · 分支 feat/y · 前置 T-010、T-013"),
               "\n".join(GOOD_DONE + ["- [-] **T-018** dropped with plan · 放弃 2026-11-19 · 计划 [006](d.md) — why"]))


@pytest.mark.parametrize("line", [
    "- [x] **T-020** done but still in TODO · 登记 2026-11-14",
    "- [ ] **T-20** short id · 登记 2026-11-14",
    "- [ ] **T-020** no date",
    "- [ ] **T-020** bad date · 登记 2026-13-40",
    "- [ ]**T-020** missing space · 登记 2026-11-14",
    "- [  ] **T-020** two spaces in box · 登记 2026-11-14",
    "- [    ] T-020 wide box, no bold id · 登记 2026-11-14",
    "- [ x ] T-020 spaced x, no bold id · 登记 2026-11-14",
    "- [!] odd box, no bold id · 登记 2026-11-14",
    "- [] empty box · 登记 2026-11-14",
    "  - [ ] **T-020** indented · 登记 2026-11-14",
    "* [ ] **T-020** star bullet · 登记 2026-11-14",
    "1. [ ] **T-020** numbered · 登记 2026-11-14",
    "- **T-020** no checkbox · 登记 2026-11-14",
    "- [ ] **T-020** dangling field · 登记 2026-11-14 · ",
    "- [ ] **T-020** bad due · 登记 2026-11-14 · 截止 2026-99-99",
    "- [ ] **T-020** unknown field · 登记 2026-11-14 · 优先级 高",
    "- [ ] **T-020** registered last · 截止 2026-12-02 · 登记 2026-11-14",
    "- [ ] **T-020** dangling ref · 登记 2026-11-14 · 来源 T-777",
    "- [ ] **T-010** duplicate id · 登记 2026-11-14",
    "- [ ] **T-0010** zero-padded duplicate · 登记 2026-11-14",
    "- [ ] **T-020** title · with dot · 登记 2026-11-14",
    "```",
])
def test_todo_checker_rejects_item(line):
    with pytest.raises(AssertionError):
        check_both(_todo(line), "")


@pytest.mark.parametrize("base", [
    [S1, S0, S2],
    [S0, S2],
    ["- [ ] **T-020** before sections · 登记 2026-11-14", S0, S1, S2],
])
def test_todo_checker_rejects_sections(base):
    with pytest.raises(AssertionError):
        check_todo(_todo(base=base))


@pytest.mark.parametrize("text", [
    "## 2026-11\n- [ ] **T-020** open item · 完成 2026-11-14 · PR #4 — ok",
    "## 2026-11\n- [X] **T-020** capital X · 完成 2026-11-14 · PR #4 — ok",
    "## 2026-11\n- [x] **T-020** wrong verb · 放弃 2026-11-14 — why",
    "## 2026-11\n- [-] **T-020** wrong verb · 完成 2026-11-14 · PR #4 — ok",
    "## 2026-11\n- [x] **T-020** wrong month · 完成 2026-10-30 · PR #4 — ok",
    "- [x] **T-020** no section · 完成 2026-11-14 · PR #4 — ok",
    "## November\n- [x] **T-020** bad heading · 完成 2026-11-14 · PR #4 — ok",
    "## 2026-11\n- [x] **T-020** nothing after date · 完成 2026-11-14",
    "## 2026-11\n- [x] **T-020** no PR · 完成 2026-11-14 — result",
    "## 2026-11\n- [x] **T-020** no result · 完成 2026-11-14 · PR #4",
    "## 2026-11\n- [x] **T-020** junk field · 完成 2026-11-14 · x",
    "## 2026-11\n- [-] **T-020** no reason · 放弃 2026-11-14 · x",
    "## 2026-11\n  - [x] **T-020** indented · 完成 2026-11-14 · PR #4 — ok",
    "## 2026-11\n- [x] **T-020** a · 完成 2026-11-01 · PR #4 — ok\n- [x] **T-021** b · 完成 2026-11-02 · PR #5 — ok",
    "## 2026-10\n## 2026-11\n- [x] **T-020** months ascending · 完成 2026-11-14 · PR #4 — ok",
    "## 2026-11\n## 2026-11\n- [x] **T-020** month twice · 完成 2026-11-14 · PR #4 — ok",
    "## 2026-13\n## 2026-11\n- [x] **T-020** month 13 · 完成 2026-11-14 · PR #4 — ok",
    "## 2026-11\n- [x] **T-020** a · 完成 2026-11-02 · PR #4 — ok\n- [x] **T-020** b · 完成 2026-11-01 · PR #5 — ok",
    "## 2026-11\n```\n- [x] **T-020** hidden by unclosed fence · 完成 2026-11-14 · PR #4 — ok",
])
def test_done_checker_rejects(text):
    with pytest.raises(AssertionError):
        check_done(text)


def test_ids_unique_across_files():
    with pytest.raises(AssertionError, match="T-010 used twice"):
        check_both(_todo(), "## 2026-11\n- [x] **T-010** also done · 完成 2026-11-20 · PR #5 — r")
