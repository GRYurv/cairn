"""Command line entry points."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cairn.config import Config
from cairn.graph import build_graph
from cairn.index import collect
from cairn.render import write_output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="cairn", description="Index Markdown notes.")
    sub = parser.add_subparsers(dest="command", required=True)

    index = sub.add_parser("index", help="write graph.json and index.html")
    index.add_argument("vault", type=Path)
    index.add_argument("--out", type=Path, default=Path("site"))

    lint = sub.add_parser("lint", help="fail when a wikilink has no target")
    lint.add_argument("vault", type=Path)

    show = sub.add_parser("show", help="print one note and its neighbors")
    show.add_argument("vault", type=Path)
    show.add_argument("query")

    args = parser.parse_args(argv)
    vault = args.vault
    if not vault.is_dir():
        print(f"not a directory: {vault}", file=sys.stderr)
        return 2

    config = Config.load(vault)
    notes = collect(vault, config)
    graph = build_graph(notes)

    if args.command == "index":
        write_output(graph, args.out, config.title)
        print(f"{len(notes)} notes -> {args.out}")
        return 0

    if args.command == "lint":
        broken = graph.missing()
        for edge in broken:
            print(f"{edge.source}:{edge.line}: missing [[{edge.target}]]")
        return 1 if broken else 0

    needle = args.query.casefold()
    matches = [
        node
        for node in graph.nodes.values()
        if not node.missing and (needle in node.title.casefold() or needle in node.slug)
    ]
    if not matches:
        print(f"no note matches {args.query!r}", file=sys.stderr)
        return 1
    for node in matches:
        print(node.title)
        print(f"  slug: {node.slug}")
        print(f"  out:  {', '.join(graph.outbound(node.slug)) or '-'}")
        print(f"  in:   {', '.join(graph.inbound(node.slug)) or '-'}")
    return 0
