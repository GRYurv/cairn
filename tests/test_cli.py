"""CLI exit codes."""

from pathlib import Path

from cairn.cli import main


def test_lint_fails_on_missing_link(tmp_path: Path, capsys) -> None:
    (tmp_path / "a.md").write_text("# A\n\n[[nowhere]]\n", encoding="utf-8")
    assert main(["lint", str(tmp_path)]) == 1
    assert "missing [[nowhere]]" in capsys.readouterr().out


def test_index_writes_site(tmp_path: Path) -> None:
    vault = tmp_path / "notes"
    vault.mkdir()
    (vault / "a.md").write_text("# A\n", encoding="utf-8")
    out = tmp_path / "site"
    assert main(["index", str(vault), "--out", str(out)]) == 0
    assert (out / "graph.json").is_file()
    assert (out / "index.html").is_file()


def test_missing_vault(tmp_path: Path) -> None:
    assert main(["lint", str(tmp_path / "nope")]) == 2
