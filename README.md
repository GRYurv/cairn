# cairn

Local backlink index for a folder of Markdown notes. Cairn reads a vault, extracts titles and `[[wikilinks]]`, and writes a static graph you can open without a server.

It is meant for people who already keep notes in git and do not want another database.

## What it does

- Walks a directory of `.md` files and ignores anything in `.cairnignore`.
- Parses YAML front matter, ATX headings, and wikilinks.
- Builds a directed graph of notes and unresolved links.
- Renders a single `index.html` plus `graph.json` for anything else you want to script.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Python 3.11 or newer.

## Use

```bash
cairn index ./notes --out ./site
cairn lint ./notes
cairn show ./notes "field methods"
```

`index` rewrites the output directory. `lint` exits non-zero when a wikilink has no target. `show` prints the note and its inbound links.

## Configuration

Optional `cairn.toml` at the vault root:

```toml
title = "Field library"
ignore = ["archive/raw", "*.draft.md"]
```

Keys you do not set keep the defaults in `src/cairn/config.py`.

## Layout

```
src/cairn/     library and CLI
tests/         parser, graph, and index tests
docs/          architecture notes and ADRs
examples/      a small vault you can index immediately
corpus/        longer sample notes used by the fixture tests
```

## Status

The parser covers the subset of Markdown this project actually needs. Tables, footnotes, and nested lists are left as text. See `docs/architecture.md` before changing link rules.

## License

MIT. See `LICENSE`.
