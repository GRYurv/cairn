"""Config loader tests."""

from pathlib import Path

from cairn.config import Config


def test_defaults_when_file_is_missing(tmp_path: Path) -> None:
    config = Config.load(tmp_path)
    assert config.title == "Notes"
    assert ".git" in config.ignore


def test_toml_subset(tmp_path: Path) -> None:
    (tmp_path / "cairn.toml").write_text(
        'title = "Field library"\nignore = ["archive/raw", "*.draft.md"]\n',
        encoding="utf-8",
    )
    config = Config.load(tmp_path)
    assert config.title == "Field library"
    assert config.ignore == ["archive/raw", "*.draft.md"]
