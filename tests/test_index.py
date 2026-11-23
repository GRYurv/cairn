"""Vault walk tests."""

from pathlib import Path

from cairn.config import Config
from cairn.index import collect


def test_ignore_patterns(tmp_path: Path) -> None:
    vault = tmp_path
    (vault / "keep.md").write_text("# Keep\n", encoding="utf-8")
    draft = vault / "scratch.draft.md"
    draft.write_text("# Hidden\n", encoding="utf-8")
    nested = vault / "archive" / "raw"
    nested.mkdir(parents=True)
    (nested / "old.md").write_text("# Old\n", encoding="utf-8")
    config = Config(ignore=["*.draft.md", "archive/raw"])
    slugs = [note.slug for note in collect(vault, config)]
    assert slugs == ["keep"]
