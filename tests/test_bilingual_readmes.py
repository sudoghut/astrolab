"""Study READMEs are bilingual: README.md (English, authoritative) plus README.zh.md (T-029, plan 023).

A study listed in PENDING may still lack its Chinese file; the list only shrinks (one translation PR
removes its study) and the test fails if a listed study already has README.zh.md.
"""
import re
from pathlib import Path

import pytest

STUDIES = Path(__file__).resolve().parents[1] / "studies"

# studies whose README.zh.md is not written yet (plan 023, stage 2); remove an entry with its translation
PENDING = {
    "000-smoke-test_gaia-dr3-10pc-census",
    "001-m04-gaia-dormant-black-holes",
    "002-m01-desi-bao-evolving-dark-energy",
    "003-m02-hubble-tension-distance-ladder",
    "004-m07-wide-binaries-gravity-test",
    "005-m09-nanograv-gwb-power-law",
    "006-m08-z14-galaxies-number-density",
    "007-m10-gwtc4-bbh-mass-35msun",
    "008-m03-s8-des-y6-cmb-parameter-difference",
    "009-m06-mw-outer-rotation-curve-decline",
    "010-m05-thick-disc-subgiant-ages",
}

FOLDERS = sorted(p for p in STUDIES.iterdir() if p.is_dir() and (p / "README.md").exists())


def _sections(text: str) -> list[str]:
    """Numbers of the level-2 headings, in order ("## 5. Results" -> "5")."""
    return re.findall(r"^## (\d+)\.", text, flags=re.M)


def _tables(text: str) -> int:
    """Number of Markdown tables (separator rows like |---|---|)."""
    return len(re.findall(r"^\|(?:\s*:?-{3,}:?\s*\|)+\s*$", text, flags=re.M))


def test_pending_list_names_real_studies():
    names = {p.name for p in FOLDERS}
    assert PENDING <= names, sorted(PENDING - names)


@pytest.mark.parametrize("folder", FOLDERS, ids=lambda p: p.name)
def test_chinese_companion(folder):
    zh = folder / "README.zh.md"
    if folder.name in PENDING:
        assert not zh.exists(), f"{folder.name} has README.zh.md: remove it from PENDING"
        pytest.skip("translation pending (plan 023)")
    assert zh.exists(), f"{folder.name}: README.zh.md missing (AGENTS.md bilingual rule)"
    en_text = (folder / "README.md").read_text(encoding="utf-8")
    zh_text = zh.read_text(encoding="utf-8")
    assert "README.zh.md" in "\n".join(en_text.splitlines()[:6]), "README.md must link README.zh.md near the top"
    head = "\n".join(zh_text.splitlines()[:6])
    assert "README.md" in head and "以英文" in head, "README.zh.md must link README.md and say English is authoritative"
    assert _sections(zh_text) == _sections(en_text), "section numbers differ between README.md and README.zh.md"
    assert _tables(zh_text) == _tables(en_text), "table count differs between README.md and README.zh.md"
