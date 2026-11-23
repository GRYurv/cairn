"""Corpus fixtures stay resolvable."""

from pathlib import Path

from cairn.graph import build_graph
from cairn.index import collect

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"


def test_corpus_links_resolve() -> None:
    notes = collect(CORPUS)
    graph = build_graph(notes)
    assert graph.missing() == []
    assert "survey-window" in graph.outbound("reading-list")


def test_survey_sidecar_is_not_indexed_as_a_note() -> None:
    slugs = [note.slug for note in collect(CORPUS)]
    assert "survey/2019-11-04-window" not in slugs
    assert (CORPUS / "survey" / "2019-11-04-window.json").is_file()
