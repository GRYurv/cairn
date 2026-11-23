# Usage

## Index a vault

```bash
cairn index ./notes --out ./site
```

Open `site/index.html`. Scripts should read `site/graph.json` instead of scraping the HTML.

## Lint before you commit notes

```bash
cairn lint ./notes
```

Exit status is `0` when every wikilink resolves, `1` when any target is missing, and `2` when the vault path is not a directory.

## Show one note

```bash
cairn show ./notes "field methods"
```

Prints the title, the slug, outbound links, and notes that point at it.

## Ignore generated folders

```toml
ignore = ["site", "exports/*.csv"]
```

Patterns are matched with `fnmatch` against the vault-relative path and the filename.
