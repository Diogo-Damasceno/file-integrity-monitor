"""Testes do file-integrity-monitor."""

from __future__ import annotations

import json
from pathlib import Path

from fim import core
from fim.cli import BASELINE_FILE, build_parser, main


def test_hash_file_stable(tmp_path: Path):
    f = tmp_path / "a.txt"
    f.write_text("conteudo")
    h1 = core.hash_file(str(f))
    h2 = core.hash_file(str(f))
    assert h1 == h2
    assert len(h1) == 64


def test_build_baseline_file(tmp_path: Path):
    (tmp_path / "x").write_text("1")
    (tmp_path / "y").write_text("2")
    bl = core.build_baseline([str(tmp_path / "x"), str(tmp_path / "y")])
    assert len(bl) == 2


def test_build_baseline_dir(tmp_path: Path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "z").write_text("3")
    bl = core.build_baseline([str(tmp_path)])
    assert str(tmp_path / "sub" / "z") in bl


def test_compare_detects_change(tmp_path: Path):
    (tmp_path / "f").write_text("abc")
    baseline = core.build_baseline([str(tmp_path / "f")])
    (tmp_path / "f").write_text("def")
    current = core.build_baseline([str(tmp_path / "f")])
    diff = core.compare(baseline, current)
    assert diff["modified"] == [str(tmp_path / "f")]
    assert diff["added"] == []
    assert diff["removed"] == []


def test_compare_detects_added_and_removed(tmp_path: Path):
    (tmp_path / "keep").write_text("k")
    (tmp_path / "gone").write_text("g")
    baseline = core.build_baseline([str(tmp_path / "keep"), str(tmp_path / "gone")])
    (tmp_path / "gone").unlink()
    (tmp_path / "new").write_text("n")
    current = core.build_baseline([str(tmp_path / "keep"), str(tmp_path / "new")])
    diff = core.compare(baseline, current)
    assert diff["removed"] == [str(tmp_path / "gone")]
    assert diff["added"] == [str(tmp_path / "new")]


def test_cli_init_check_detects_modification(tmp_path: Path, monkeypatch):
    target = tmp_path / "work"
    target.mkdir()
    f = target / "doc.txt"
    f.write_text("original")
    monkeypatch.chdir(tmp_path)
    assert main(["init", str(f)]) == 0
    assert (tmp_path / BASELINE_FILE).exists()

    f.write_text("alterado")
    assert main(["check"]) == 1


def test_cli_init_check_clean(tmp_path: Path, monkeypatch):
    target = tmp_path / "work"
    target.mkdir()
    f = target / "doc.txt"
    f.write_text("estavel")
    monkeypatch.chdir(tmp_path)
    main(["init", str(f)])
    assert main(["check"]) == 0


def test_cli_diff_json(tmp_path: Path, monkeypatch, capsys):
    target = tmp_path / "work"
    target.mkdir()
    f = target / "doc.txt"
    f.write_text("v1")
    monkeypatch.chdir(tmp_path)
    main(["init", str(f)])
    f.write_text("v2")
    rc = main(["diff"])
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["modified"] == [str(f)]
