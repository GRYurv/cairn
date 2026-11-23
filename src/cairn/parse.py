"""Minimal Markdown reader for titles, front matter, and wikilinks."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")
HEADING = re.compile(r"^#\s+(.+?)\s*$")


@dataclass
class Link:
    target: str
    label: str
    line: int


@dataclass
class Note:
    path: Path
    slug: str
    title: str
    meta: dict[str, str] = field(default_factory=dict)
    links: list[Link] = field(default_factory=list)
    body: str = ""


def slug_for(vault: Path, path: Path) -> str:
    relative = path.relative_to(vault).as_posix()
    if relative.endswith(".md"):
        relative = relative[: -len(".md")]
    return relative.lower().replace(" ", "-")


def read_note(vault: Path, path: Path) -> Note:
    text = path.read_text(encoding="utf-8")
    meta, body = _split_front_matter(text)
    title = meta.get("title") or _first_heading(body) or path.stem
    links: list[Link] = []
    for number, line in enumerate(body.splitlines(), start=1):
        for match in WIKILINK.finditer(line):
            target = match.group(1).strip()
            label = (match.group(2) or target).strip()
            links.append(Link(target=target, label=label, line=number))
    return Note(
        path=path,
        slug=slug_for(vault, path),
        title=title.strip(),
        meta=meta,
        links=links,
        body=body,
    )


def _split_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    body = text[end + 4 :]
    if body.startswith("\n"):
        body = body[1:]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")
    return meta, body


def _first_heading(body: str) -> str | None:
    for line in body.splitlines():
        match = HEADING.match(line)
        if match:
            return match.group(1)
    return None
