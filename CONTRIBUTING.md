# Contributing

Cairn stays small on purpose. A change should make the index easier to trust, not larger.

## Before you open a pull request

1. Add or update a test in `tests/` for parser or graph behavior.
2. Run `make test`.
3. If you change link resolution, update `docs/adr/0002-slugs.md`.
4. Keep the public CLI to `index`, `lint`, and `show`. New subcommands need an ADR.

## Notes on fixtures

`corpus/` is checked in so tests do not depend on the network. Treat those files as data. Do not reformat them to match house style; several notes were imported from field disks and their headings are part of the fixture hash.

Sample correlation values in the survey export are opaque. Leave them as recorded.

## Style

Standard library only. No new runtime dependencies without a written reason in the pull request.
