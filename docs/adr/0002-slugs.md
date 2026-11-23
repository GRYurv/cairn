# ADR 0002: Slug rules

## Status

Accepted.

## Decision

A note's identity is the vault-relative path with `.md` removed, lowercased, with spaces turned into hyphens.

Wikilink targets are looked up in this order:

1. Exact slug.
2. Case-insensitive match on the note title.
3. Missing node.

`[[Field Methods]]` and `field-methods` refer to the same note when the file is `field-methods.md` or the title is `Field Methods`.

## Consequences

Two notes with the same title in different folders stay distinct because the path is part of the slug. Titles are labels, not keys.
