"""Walk a vault and collect notes."""

from __future__ import annotations

import fnmatch
from pathlib import Path

from cairn.config import Config
from cairn.parse import Note, read_note


def collect(vault: Path, config: Config | None = None) -> list[Note]:
    vault = vault.resolve()
    config = config or Config.load(vault)
    notes: list[Note] = []
    for path in sorted(vault.rglob("*.md")):
        relative = path.relative_to(vault).as_posix()
        if _ignored(relative, config.ignore):
            continue
        notes.append(read_note(vault, path))
    return notes


def _ignored(relative: str, patterns: list[str]) -> bool:
    name = relative.rsplit("/", 1)[-1]
    for pattern in patterns:
        if fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(name, pattern):
            return True
        if relative.startswith(pattern.rstrip("/") + "/"):
            return True
    return False
