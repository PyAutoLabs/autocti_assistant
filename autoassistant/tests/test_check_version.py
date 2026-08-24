"""test_check_version.py — what --check-version gates on, and what it only reports.

Two things are deliberately NOT gated:

* The per-module ``__version__`` equality, dropped in PyAutoMind build-chain #155
  Phase 4 task 3. Releases no longer commit the stamp back to library ``main``,
  so a source checkout's frozen stamp vs a wheel-derived baseline is a permanent
  false positive that the API-surface comparison already proves spurious.
* **Additions** to the public surface (autocti_assistant#25). The check hashes
  the entire public surface of autoarray and autofit, almost none of which this
  assistant documents, and the workflow installs those libraries from their
  ``main`` source clones — so the clock was every upstream merge that exported a
  name. A symbol appearing cannot break a doc; a symbol disappearing can.

These tests monkeypatch ``compute_baseline`` so they need no installed stack.
"""

from __future__ import annotations

import json
from pathlib import Path

from autoassistant import audit_skill_apis as a


def _surface(symbols_by_module):
    """Build an ``api_surface`` block whose hash follows from its symbols.

    The real ``compute_baseline`` derives both from one sorted list, so a
    fixture that let them disagree would test a state that cannot occur.
    """
    return {
        module: {
            "hash": "h:" + ",".join(sorted(symbols)),
            "n_symbols": len(symbols),
            "symbols": sorted(symbols),
        }
        for module, symbols in symbols_by_module.items()
    }


def _bl(versions, symbols_by_module):
    return {
        "generated": "2026-08-24",
        "versions": versions,
        "api_surface": _surface(symbols_by_module),
    }


def _legacy_bl(versions, hashes):
    """A baseline written before symbol recording: hash and count only."""
    return {
        "generated": "2026-07-09",
        "versions": versions,
        "api_surface": {m: {"hash": h, "n_symbols": 1} for m, h in hashes.items()},
    }


def _write(root, baseline):
    path = root / a.BASELINE_REL_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(baseline), encoding="utf-8")


VERSIONS = {m: "2026.8.24.1" for m in a.VERSIONED_MODULES}
MOVED = a.BASELINE_MODULES[-1]


def _symbols(**overrides):
    base = {m: ["Alpha", "Beta"] for m in a.BASELINE_MODULES}
    base.update(overrides)
    return base


def test_identical_surface_is_clean(tmp_path, monkeypatch, capsys):
    _write(tmp_path, _bl(VERSIONS, _symbols()))
    monkeypatch.setattr(a, "compute_baseline", lambda: _bl(VERSIONS, _symbols()))

    assert a.check_version(tmp_path) == 0
    assert "clean" in capsys.readouterr().out


def test_version_stamp_differs_but_surface_matches_is_clean(
    tmp_path, monkeypatch, capsys
):
    _write(tmp_path, _bl({m: "2026.7.9.1" for m in a.VERSIONED_MODULES}, _symbols()))
    monkeypatch.setattr(a, "compute_baseline", lambda: _bl(VERSIONS, _symbols()))

    assert a.check_version(tmp_path) == 0  # was 1 before build-chain #155
    out = capsys.readouterr().out
    assert "clean" in out
    assert "not gated" in out


def test_additions_alone_do_not_gate_and_are_named(tmp_path, monkeypatch, capsys):
    """The whole point of #25: eleven new autofit exports must not go red.

    The red that prompted this was 12 additions and 2 removals, none of the 14
    cited anywhere in wiki/, skills/ or modes/.
    """
    _write(tmp_path, _bl(VERSIONS, _symbols()))
    monkeypatch.setattr(
        a,
        "compute_baseline",
        lambda: _bl(VERSIONS, _symbols(**{MOVED: ["Alpha", "Beta", "Gamma"]})),
    )

    assert a.check_version(tmp_path) == 0
    captured = capsys.readouterr()
    assert "additions only (not gated)" in captured.out
    assert "+ added:   Gamma" in captured.out
    # Not gating must not mean not reporting — the drift is still real, and the
    # baseline is still stale.
    assert "--write-baseline" in captured.out
    assert captured.err == ""


def test_a_removal_gates_and_names_the_symbol(tmp_path, monkeypatch, capsys):
    _write(tmp_path, _bl(VERSIONS, _symbols()))
    monkeypatch.setattr(
        a,
        "compute_baseline",
        lambda: _bl(VERSIONS, _symbols(**{MOVED: ["Alpha"]})),
    )

    assert a.check_version(tmp_path) == 1
    err = capsys.readouterr().err
    assert "REMOVALS" in err
    assert "- removed: Beta" in err
    # The old report said only "public API surface changed: <module>", which is
    # why reconstructing the diff needed worktrees at the baseline's commits.
    assert MOVED in err
    assert "--scope all" in err


def test_a_removal_gates_even_alongside_additions(tmp_path, monkeypatch, capsys):
    """A module that both gained and lost symbols must still fail."""
    _write(tmp_path, _bl(VERSIONS, _symbols()))
    monkeypatch.setattr(
        a,
        "compute_baseline",
        lambda: _bl(VERSIONS, _symbols(**{MOVED: ["Alpha", "Gamma", "Delta"]})),
    )

    assert a.check_version(tmp_path) == 1
    err = capsys.readouterr().err
    assert "- removed: Beta" in err
    assert "+ added:   Delta, Gamma" in err


def test_removal_in_one_module_gates_despite_a_clean_addition_elsewhere(
    tmp_path, monkeypatch, capsys
):
    other = a.BASELINE_MODULES[0]
    assert other != MOVED
    _write(tmp_path, _bl(VERSIONS, _symbols()))
    monkeypatch.setattr(
        a,
        "compute_baseline",
        lambda: _bl(
            VERSIONS,
            _symbols(**{MOVED: ["Alpha"], other: ["Alpha", "Beta", "Gamma"]}),
        ),
    )

    assert a.check_version(tmp_path) == 1
    err = capsys.readouterr().err
    assert "- removed: Beta" in err
    assert "+ added:   Gamma" in err


def test_legacy_baseline_without_symbols_still_gates_on_any_drift(
    tmp_path, monkeypatch, capsys
):
    """A pre-#25 baseline cannot tell an addition from a removal.

    Treating an undiagnosable change as additive would wave a real removal
    through, so the old, noisy behaviour is kept — with a line saying why and
    how to upgrade.
    """
    base_hashes = {m: "deadbeef" for m in a.BASELINE_MODULES}
    _write(tmp_path, _legacy_bl(VERSIONS, base_hashes))
    cur_hashes = dict(base_hashes, **{MOVED: "cafef00d"})
    monkeypatch.setattr(
        a, "compute_baseline", lambda: _legacy_bl(VERSIONS, cur_hashes)
    )

    assert a.check_version(tmp_path) == 1
    err = capsys.readouterr().err
    assert "public API surface changed" in err and MOVED in err
    assert "cannot support a symbol diff" in err
    assert "--write-baseline" in err


def test_legacy_baseline_with_no_drift_is_still_clean(tmp_path, monkeypatch):
    hashes = {m: "deadbeef" for m in a.BASELINE_MODULES}
    _write(tmp_path, _legacy_bl(VERSIONS, hashes))
    monkeypatch.setattr(a, "compute_baseline", lambda: _legacy_bl(VERSIONS, hashes))

    assert a.check_version(tmp_path) == 0


def test_missing_baseline_is_drift(tmp_path):
    assert a.check_version(tmp_path) == 1


def test_shipped_baseline_records_symbols_for_every_module():
    """The committed baseline must be on the new schema, not the legacy path.

    Without this the repo could ship a hash-only baseline and quietly keep the
    old all-or-nothing gate while the code claimed otherwise.
    """
    root = Path(__file__).resolve().parents[2]
    baseline = json.loads(
        (root / a.BASELINE_REL_PATH).read_text(encoding="utf-8")
    )
    for module in a.BASELINE_MODULES:
        entry = baseline["api_surface"][module]
        assert entry["symbols"], f"{module} records no symbols"
        assert len(entry["symbols"]) == entry["n_symbols"]
        assert entry["symbols"] == sorted(entry["symbols"])
        assert entry["hash"] == a._api_hash_from_names(entry["symbols"])


def test_module_absent_from_the_baseline_gates_and_says_so(
    tmp_path, monkeypatch, capsys
):
    """Adding a module to BASELINE_MODULES must not read as "old baseline".

    It is a different situation with the same symptom — no symbols to diff — and
    the report should not send the reader looking for a schema upgrade that is
    already done.
    """
    new_module = a.BASELINE_MODULES[-1]
    partial = _bl(VERSIONS, _symbols())
    del partial["api_surface"][new_module]
    _write(tmp_path, partial)
    monkeypatch.setattr(a, "compute_baseline", lambda: _bl(VERSIONS, _symbols()))

    assert a.check_version(tmp_path) == 1
    err = capsys.readouterr().err
    assert "not in the baseline at all" in err
    assert new_module in err
