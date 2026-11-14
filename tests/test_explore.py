"""Offline tests of `astrolab explore` (AGENTS.md section 2, design/007 section 2.3)."""
import datetime as dt
import json
from pathlib import Path

import pytest

from astrolab import study

RUN_PY = '''
PARAMS = {"n": 3, "scale": 1.5, "label": "base"}


def main(ctx):
    ctx.save("out", {"n": PARAMS["n"], "scale": PARAMS["scale"], "label": PARAMS["label"]})
    return {"n": PARAMS["n"]}
'''


@pytest.fixture
def fake_study(tmp_path):
    d = tmp_path / "studies" / "042-fake"
    (d / "results").mkdir(parents=True)
    (d / "explore").mkdir()
    (d / "run.py").write_text(RUN_PY, encoding="utf-8")
    (d / "results" / "out.json").write_text('{"canonical": true}', encoding="utf-8")
    return study.Study(d)


def _out_dir(s, tag):
    return s.path / "explore" / f"{dt.date.today().isoformat()}-{tag}"


def test_explore_overrides_in_memory_and_leaves_results(fake_study):
    study.explore(fake_study, "bigger-n", ["n=7", "scale=2"])
    out = _out_dir(fake_study, "bigger-n")
    assert json.loads((out / "out.json").read_text())["n"] == 7
    assert json.loads((out / "out.json").read_text())["scale"] == 2.0
    info = json.loads((out / "run_info.json").read_text())
    assert info["overrides"] == {"n": 7, "scale": 2.0}
    assert (out / "provenance.json").exists()
    # canonical results and the committed PARAMS are untouched
    assert json.loads((fake_study.path / "results" / "out.json").read_text()) == {"canonical": True}
    assert '"n": 3' in (fake_study.path / "run.py").read_text()
    # a second run without overrides sees the original value (fresh module)
    study.explore(fake_study, "baseline")
    assert json.loads((_out_dir(fake_study, "baseline") / "out.json").read_text())["n"] == 3


def test_explore_same_tag_overwrites(fake_study):
    study.explore(fake_study, "t", ["n=1"])
    (_out_dir(fake_study, "t") / "stale.json").write_text("{}")
    study.explore(fake_study, "t", ["n=2"])
    assert not (_out_dir(fake_study, "t") / "stale.json").exists()


@pytest.mark.parametrize("tag", ["../results", "a/b", "UPPER", "", "x" * 41, "..", "a b"])
def test_explore_rejects_bad_tags(fake_study, tag):
    with pytest.raises(SystemExit):
        study.explore(fake_study, tag)
    assert json.loads((fake_study.path / "results" / "out.json").read_text()) == {"canonical": True}


@pytest.mark.parametrize("sets", [["nope=1"], ["n=abc"], ["n=1.5"], ["n=true"], ["n"],
                                  ["scale=1e400"], ["scale=NaN"], ["scale=" + "9" * 400]])
def test_explore_rejects_bad_overrides(fake_study, sets):
    with pytest.raises(SystemExit):
        study.explore(fake_study, "x", sets)


def test_explore_string_param_takes_text(fake_study):
    study.explore(fake_study, "label", ["label=12"])
    assert json.loads((_out_dir(fake_study, "label") / "out.json").read_text())["label"] == "12"


def test_save_rejects_path_names(fake_study):
    (fake_study.path / "explore" / "sneaky.py").write_text(
        "def main(ctx):\n    ctx.save('../../results/out', {'x': 1})\n", encoding="utf-8")
    with pytest.raises(ValueError, match="plain file name"):
        study.explore(fake_study, "sneaky", script="explore/sneaky.py")
    assert json.loads((fake_study.path / "results" / "out.json").read_text()) == {"canonical": True}


def test_failing_main_leaves_results_and_sys_path(fake_study):
    import sys
    before = list(sys.path)
    (fake_study.path / "explore" / "boom.py").write_text("def main(ctx):\n    raise RuntimeError('x')\n",
                                                        encoding="utf-8")
    with pytest.raises(RuntimeError):
        study.explore(fake_study, "boom", script="explore/boom.py")
    assert sys.path == before
    assert json.loads((fake_study.path / "results" / "out.json").read_text()) == {"canonical": True}


def test_explore_script_inside_explore_only(fake_study, tmp_path):
    (fake_study.path / "explore" / "probe.py").write_text(
        "def main(ctx):\n    ctx.save('probe', {'ok': 1})\n", encoding="utf-8")
    study.explore(fake_study, "probe", script="explore/probe.py")
    assert (_out_dir(fake_study, "probe") / "probe.json").exists()
    (fake_study.path / "elsewhere.py").write_text("def main(ctx):\n    pass\n", encoding="utf-8")
    (fake_study.path / "explore" / "sub").mkdir()
    (fake_study.path / "explore" / "sub" / "deep.py").write_text("def main(ctx):\n    pass\n")
    for bad in ["elsewhere.py", "explore/../elsewhere.py", "explore\\..\\elsewhere.py", "run.py",
                "explore/missing.py", str(tmp_path / "abs.py"), "explore/sub/deep.py"]:
        with pytest.raises(SystemExit):
            study.explore(fake_study, "probe", script=bad)
    with pytest.raises(SystemExit):
        study.explore(fake_study, "probe", ["n=1"], script="explore/probe.py")


def test_explore_caps_output_size(fake_study):
    (fake_study.path / "explore" / "big.py").write_text(
        "def main(ctx):\n    ctx.save('big', {'x': 'a' * (2 * 1024 * 1024)})\n", encoding="utf-8")
    with pytest.raises(ValueError, match="under 1 MB"):
        study.explore(fake_study, "big", script="explore/big.py")
    assert not (_out_dir(fake_study, "big") / "big.json").exists()


def test_explore_refuses_linked_explore_folder(tmp_path):
    d = tmp_path / "studies" / "043-linked"
    (d / "results").mkdir(parents=True)
    (d / "run.py").write_text(RUN_PY, encoding="utf-8")
    try:
        (d / "explore").symlink_to(d / "results", target_is_directory=True)
    except OSError:
        pytest.skip("cannot create symlinks here")
    with pytest.raises(SystemExit, match="real folder"):
        study.explore(study.Study(d), "t")
    assert list((d / "results").iterdir()) == []


def test_explore_requires_params(fake_study):
    (fake_study.path / "run.py").write_text("def main(ctx):\n    pass\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="PARAMS"):
        study.explore(fake_study, "x")


def test_template_has_params_and_argument():
    tpl = Path(__file__).resolve().parents[1] / "studies" / "_template"
    assert "PARAMS = {" in (tpl / "run.py").read_text(encoding="utf-8")
    assert "## 8. Exploring via chat" in (tpl / "README.md").read_text(encoding="utf-8")
    assert {p.name for p in (tpl / "argument").iterdir()} == {"lakefile.toml", "lean-toolchain", "Argument.lean"}
