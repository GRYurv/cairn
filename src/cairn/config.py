"""Vault configuration loaded from an optional cairn.toml."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    title: str = "Notes"
    ignore: list[str] = field(default_factory=lambda: [".git", ".cairn-cache"])

    @classmethod
    def load(cls, vault: Path) -> "Config":
        path = vault / "cairn.toml"
        if not path.is_file():
            return cls()
        data: dict[str, object] = {"title": "Notes", "ignore": [".git", ".cairn-cache"]}
        section = None
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].strip()
                continue
            if "=" not in line or section not in (None, "cairn"):
                continue
            key, value = (part.strip() for part in line.split("=", 1))
            data[key] = _parse_value(value)
        ignore = data.get("ignore", [])
        if not isinstance(ignore, list):
            ignore = [str(ignore)]
        return cls(title=str(data.get("title", "Notes")), ignore=[str(item) for item in ignore])


def _parse_value(value: str) -> object:
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip('"').strip("'") for part in inner.split(",")]
    if value.startswith(("'", '"')) and value.endswith(("'", '"')):
        return value[1:-1]
    return value
