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
