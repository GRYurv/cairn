"""Parser tests."""

from pathlib import Path

from cairn.parse import read_note


def test_front_matter_and_wikilink(tmp_path: Path) -> None:
    vault = tmp_path
    note = vault / "methods.md"
    note.write_text(
        "---\ntitle: Field methods\nstatus: draft\n---\n\n"
        "See [[plot-14|the north plot]] for bearings.\n",
        encoding="utf-8",
    )
    parsed = read_note(vault, note)
    assert parsed.title == "Field methods"
    assert parsed.meta["status"] == "draft"
    assert parsed.slug == "methods"
    assert parsed.links[0].target == "plot-14"
    assert parsed.links[0].label == "the north plot"
    assert parsed.links[0].line == 2


def test_heading_is_title_when_front_matter_is_absent(tmp_path: Path) -> None:
    vault = tmp_path
    note = vault / "loose note.md"
    note.write_text("# Loose note\n\nBody.\n", encoding="utf-8")
    parsed = read_note(vault, note)
    assert parsed.title == "Loose note"
    assert parsed.slug == "loose-note"
