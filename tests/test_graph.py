"""Graph resolution tests."""

from pathlib import Path

from cairn.graph import build_graph
from cairn.parse import read_note


def test_title_match_and_missing_target(tmp_path: Path) -> None:
    vault = tmp_path
    (vault / "field-methods.md").write_text("# Field methods\n\n[[Missing page]]\n", encoding="utf-8")
    (vault / "log.md").write_text("# Log\n\n[[Field Methods]]\n", encoding="utf-8")
    notes = [read_note(vault, path) for path in sorted(vault.glob("*.md"))]
    graph = build_graph(notes)
    assert graph.outbound("log") == ["field-methods"]
    assert graph.inbound("field-methods") == ["log"]
    assert graph.nodes["missing-page"].missing is True
    assert len(graph.missing()) == 1
