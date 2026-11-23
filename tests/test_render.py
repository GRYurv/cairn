"""Renderer escapes titles."""

from pathlib import Path

from cairn.graph import build_graph
from cairn.parse import read_note
from cairn.render import write_output


def test_title_is_escaped(tmp_path: Path) -> None:
    vault = tmp_path
    note = vault / "odd.md"
    note.write_text("---\ntitle: A < B\n---\n\n# ignored\n", encoding="utf-8")
    graph = build_graph([read_note(vault, note)])
    out = tmp_path / "site"
    write_output(graph, out, "Library")
    html = (out / "index.html").read_text(encoding="utf-8")
    assert "A &lt; B" in html
    assert "A < B" not in html.split("<title>")[1]
    payload = (out / "graph.json").read_text(encoding="utf-8")
    assert '"slug": "odd"' in payload
