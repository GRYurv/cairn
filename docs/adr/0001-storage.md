# ADR 0001: No database

## Status

Accepted.

## Context

Early builds cached parsed notes in `shelve`. The cache went stale whenever someone edited a file on another machine and pulled. The vault is already the store.

## Decision

The index is a pure function of the current files. Output is written to a directory the user chooses and is safe to delete.

## Consequences

Re-indexing a few thousand notes is fast enough. We do not promise interactive updates while you type.
