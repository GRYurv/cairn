"""Writers for graph.json and a single index.html page."""

from __future__ import annotations

import html
import json
from pathlib import Path

from cairn.graph import Graph


def write_output(graph: Graph, out: Path, title: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    payload = {
        "title": title,
        "nodes": [
            {
                "slug": node.slug,
                "title": node.title,
                "missing": node.missing,
                "meta": node.meta,
            }
            for node in sorted(graph.nodes.values(), key=lambda item: item.slug)
        ],
        "edges": [
            {"source": edge.source, "target": edge.target, "line": edge.line}
            for edge in graph.edges
        ],
    }
    (out / "graph.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    (out / "index.html").write_text(_html(graph, title), encoding="utf-8")


def _html(graph: Graph, title: str) -> str:
    rows = []
    for node in sorted(graph.nodes.values(), key=lambda item: item.title.lower()):
        if node.missing:
            continue
        outbound = ", ".join(html.escape(slug) for slug in graph.outbound(node.slug)) or "—"
        inbound = ", ".join(html.escape(slug) for slug in graph.inbound(node.slug)) or "—"
        rows.append(
            "<section>"
            f"<h2>{html.escape(node.title)}</h2>"
            f"<p><code>{html.escape(node.slug)}</code></p>"
            f"<p>Out: {outbound}</p>"
            f"<p>In: {inbound}</p>"
            "</section>"
        )
    body = "\n".join(rows) or "<p>No notes.</p>"
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        f"<title>{html.escape(title)}</title>\n"
        "</head>\n<body>\n"
        f"<h1>{html.escape(title)}</h1>\n"
        f"{body}\n"
        "</body>\n</html>\n"
    )
