"""Directed graph of notes and unresolved wikilinks."""

from __future__ import annotations

from dataclasses import dataclass, field

from cairn.parse import Note


@dataclass
class Node:
    slug: str
    title: str
    missing: bool = False
    meta: dict[str, str] = field(default_factory=dict)


@dataclass
class Edge:
    source: str
    target: str
    line: int


@dataclass
class Graph:
    nodes: dict[str, Node]
    edges: list[Edge]

    def missing(self) -> list[Edge]:
        return [edge for edge in self.edges if self.nodes[edge.target].missing]

    def inbound(self, slug: str) -> list[str]:
        return sorted({edge.source for edge in self.edges if edge.target == slug})

    def outbound(self, slug: str) -> list[str]:
        return sorted({edge.target for edge in self.edges if edge.source == slug})


def build_graph(notes: list[Note]) -> Graph:
    by_slug = {note.slug: note for note in notes}
    by_title = {note.title.casefold(): note.slug for note in notes}
    nodes = {
        note.slug: Node(slug=note.slug, title=note.title, meta=dict(note.meta))
        for note in notes
    }
    edges: list[Edge] = []
    for note in notes:
        for link in note.links:
            target = _resolve(link.target, by_slug, by_title)
            if target not in nodes:
                nodes[target] = Node(slug=target, title=link.target, missing=True)
            edges.append(Edge(source=note.slug, target=target, line=link.line))
    return Graph(nodes=nodes, edges=edges)


def _resolve(target: str, by_slug: dict[str, Note], by_title: dict[str, str]) -> str:
    direct = target.strip().lower().replace(" ", "-")
    if direct in by_slug:
        return direct
    titled = by_title.get(target.strip().casefold())
    if titled:
        return titled
    return direct
