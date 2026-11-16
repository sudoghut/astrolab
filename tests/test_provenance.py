"""Templated provenance format (T-033): exact round trip, and small logs keep the plain format."""
import json

from astrolab import provenance as P


def _doc(n):
    recs = [{"source": "tap:gaia", "release": "Gaia DR3", "request":
             f"SELECT a FROM t WHERE ra >= {i * 0.5} AND ra < {i * 0.5 + 0.5} AND dec > -30.0 AND x = 1e-3",
             "rows": i, "sha256": f"{i:064x}", "label": f"r{i:03d}"} for i in range(n)]
    recs.append({"source": "http", "request": "https://example.invalid/a_2.txt?v=3", "bytes": 5})
    recs.append({"source": "tap:gaia", "request": "SELECT {x}, '}{' FROM t2 WHERE z BETWEEN -3 AND 4.25"})
    return {"generated_at": "2026-11-16T00:00:00+00:00", "inputs": recs}


def test_compact_round_trip_is_exact():
    doc = _doc(50)
    c = P.compact(doc)
    assert c["format"] == P.COMPACT_FORMAT
    assert P.expand(json.loads(P._dump_compact(c))) == doc
    # constants are baked into the template; only the varying sky bounds are parameters
    first = next(r for r in c["inputs"] if r.get("label") == "r001")
    assert first["request_params"] == ["0.5", "1.0"]


def test_plain_format_passes_through_expand():
    doc = _doc(3)
    assert P.expand(doc) == doc


def test_write_switches_format_by_size(tmp_path, monkeypatch):
    log = P.ProvenanceLog()
    for r in _doc(5)["inputs"]:
        log.add(r)
    log.write(tmp_path / "small.json")
    small = json.loads((tmp_path / "small.json").read_text(encoding="utf-8"))
    assert "format" not in small and small["inputs"] == log.records

    monkeypatch.setattr(P, "COMPACT_ABOVE_BYTES", 100)
    log.write(tmp_path / "big.json")
    big = json.loads((tmp_path / "big.json").read_text(encoding="utf-8"))
    assert big["format"] == P.COMPACT_FORMAT
    assert P.expand(big)["inputs"] == log.records


def test_adversarial_requests_round_trip():
    reqs = ["a1 x2y 1e5 .5 5. -0 +3 0x1F 1E-7 '12' http://h:8080/p?a=1.5&b=-2", "{1}", "}{2{", "{{}}{}",
            "x{}5", "{-1}", "{} {0} {{1}}", "5e+", "1.2.3", "ü 7 ß", "", "no numbers"]
    doc = {"generated_at": "t", "inputs": [{"source": "s", "request": q, "n": i} for i, q in enumerate(reqs)]}
    assert P.expand(json.loads(P._dump_compact(P.compact(doc)))) == doc


def test_missing_field_is_not_hoisted_as_none():
    doc = {"generated_at": "t", "inputs": [{"source": "a", "release": None, "request": "1"},
                                           {"source": "a", "request": "2"}]}
    assert P.expand(P.compact(doc)) == doc


def test_uncompactable_records_keep_plain_format(tmp_path, monkeypatch):
    monkeypatch.setattr(P, "COMPACT_ABOVE_BYTES", 10)
    for bad in ({"source": "x"}, {"source": "x", "request": "1", "request_params": [1]}):
        log = P.ProvenanceLog()
        log.add(bad)
        log.write(tmp_path / "p.json")
        out = json.loads((tmp_path / "p.json").read_text(encoding="utf-8"))
        assert "format" not in out and out["inputs"] == [bad]


def test_study_004_provenance_expands_to_full_records():
    from pathlib import Path

    p = Path(__file__).parents[1] / "studies/004-m07-wide-binaries-gravity-test/results/provenance.json"
    doc = json.loads(p.read_text(encoding="utf-8"))
    recs = P.expand(doc)["inputs"]
    assert len(recs) == len(doc["inputs"]) > 1000
    assert all(r["request"].startswith("SELECT") and "sha256" in r for r in recs)
