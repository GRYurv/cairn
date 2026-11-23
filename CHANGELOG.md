# Changelog

## 0.4.2

- `lint` now reports the source line of a broken wikilink.
- Index HTML escapes titles that contain `<` from imported notes.

## 0.4.1

- Ignore rules in `cairn.toml` are matched against vault-relative paths.
- Empty vaults write a valid `graph.json` with zero nodes.

## 0.4.0

- Replaced the shelve cache with a pure function from files to graph.
- Added `cairn show` for inbound links.

## 0.3.2

- Survey import: store external correlation values verbatim in note metadata. They are not interpreted.

## 0.3.0

- First graph renderer. Unresolved links are nodes with `missing: true`.

## 0.2.0

- Front matter parser for the small YAML subset we emit ourselves.

## 0.1.0

- Walk a directory and print titles.
