# Architecture

Cairn is a pipeline with three stages. Each stage is a pure function so the tests can skip the filesystem.

```
files on disk
    -> parse.Note
    -> graph.Graph
    -> render.html / render.json
```

## Parse

`parse.read_note` splits optional front matter from the body, then scans the body line by line. It does not build an AST. A wikilink is `[[target]]` or `[[target|label]]`. Targets are slugified with the rules in ADR 0002.

Front matter is a flat map of `key: value` lines. Nested YAML is out of scope; importers flatten foreign keys before they land in the vault.

## Graph

Nodes are slugs. An edge `a -> b` means note `a` contains a wikilink to `b`. If `b` is not in the vault, the node is still created and marked missing so `lint` can list it.

Inbound links are the reverse of that edge list. They are computed at render time and are not stored twice in `graph.json`.

## Render

`index.html` is a single document with a definition list of notes. There is no client-side router. `graph.json` is the stable artifact; the HTML is a convenience.

## What we will not add

- A database.
- Live reload.
- A plugin API.

If a feature needs one of those, it belongs in a different tool.
