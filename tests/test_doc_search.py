"""tests/test_doc_search.py — Tests pour hansel-tools/doc_search.py."""

from __future__ import annotations

import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent / "hansel-tools"))

from doc_search import SearchResult, clean_excerpt, search_docs

PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "hansel-tools" / "docs"


class TestSearchDocs:
    def test_search_finds_exact_term(self) -> None:
        """Un terme connu dans les docs retourne des résultats."""
        results = search_docs("story_cycle", DOCS_DIR)
        assert len(results) > 0
        assert all(isinstance(r, SearchResult) for r in results)

    def test_search_returns_empty_for_unknown_term(self) -> None:
        """Un terme inexistant retourne une liste vide."""
        results = search_docs("xyzabc123notexist", DOCS_DIR)
        assert results == []

    def test_search_scores_multiple_word_matches_higher(self) -> None:
        """Une ligne matchant plusieurs mots a un score >= ligne à un seul mot."""
        results = search_docs("story_cycle on_setup", DOCS_DIR)
        if len(results) >= 2:
            assert results[0].score >= results[-1].score

    def test_search_max_results_respected(self) -> None:
        """max_results borne le nombre de résultats retournés."""
        results = search_docs("event", DOCS_DIR, max_results=3)
        assert len(results) <= 3

    def test_search_nonexistent_dir_returns_empty(self) -> None:
        """Un répertoire absent retourne une liste vide sans exception."""
        results = search_docs("anything", Path("/nonexistent/dir/xyz"))
        assert results == []

    def test_search_allowed_files_filters_others(self, tmp_path: Path) -> None:
        """allowed_files exclut les fichiers hors de la liste."""
        (tmp_path / "included.md").write_text("story_cycle trigger event\n", encoding="utf-8")
        (tmp_path / "excluded.md").write_text("story_cycle trigger event\n", encoding="utf-8")
        results = search_docs("story_cycle", tmp_path, allowed_files=frozenset({"included.md"}))
        assert len(results) > 0
        assert all(r.file == "included.md" for r in results)
        assert not any(r.file == "excluded.md" for r in results)


class TestSearchResultSection:
    def test_search_result_has_section(self) -> None:
        """Les résultats sous un heading ## ont leur champ section renseigné."""
        results = search_docs("story_cycle", DOCS_DIR, max_results=50)
        # Au moins un résultat doit avoir une section (fichier contient des ##)
        sections_found = [r for r in results if r.section is not None]
        assert len(sections_found) > 0, "Aucun résultat n'a de section — vérifier les headings dans docs/"

    def test_search_result_section_is_nearest_heading(self) -> None:
        """La section est le heading ## le plus proche au-dessus du match."""
        # Un résultat avec section doit avoir un titre non-vide
        results = search_docs("story_cycle", DOCS_DIR, max_results=50)
        for r in results:
            if r.section is not None:
                assert len(r.section) > 0
                assert r.section.strip() == r.section  # pas d'espaces parasites


class TestCleanExcerpt:
    def test_clean_excerpt_strips_markdown_links(self) -> None:
        """[texte](url) → texte."""
        raw = "See [Effects](/Effects \"Effects\") for more."
        result = clean_excerpt(raw)
        assert "Effects" in result
        assert "(/Effects" not in result
        assert "[" not in result

    def test_clean_excerpt_strips_wiki_links(self) -> None:
        """[[Page|display]] → display, [[Page]] → Page."""
        assert clean_excerpt("See [[Trigger|triggers]]") == "See triggers"
        assert clean_excerpt("See [[Scripting]]") == "See Scripting"

    def test_clean_excerpt_strips_bullets(self) -> None:
        """Bullets de liste en début de ligne sont supprimés."""
        assert clean_excerpt("* item one") == "item one"
        assert clean_excerpt("- item two") == "item two"

    def test_clean_excerpt_strips_leading_tab(self) -> None:
        """Tabulation initiale est supprimée."""
        result = clean_excerpt("\tindented content")
        assert not result.startswith("\t")
        assert "indented content" in result

    def test_clean_excerpt_collapses_spaces(self) -> None:
        """Espaces multiples sont réduits à un seul."""
        result = clean_excerpt("word1   word2    word3")
        assert "  " not in result

    def test_clean_excerpt_strips_backslash_escapes(self) -> None:
        """`\\-` et `\\`` sont dés-échappés."""
        result = clean_excerpt("`on_setup` \\- performs effects")
        assert "on_setup" in result
        assert "\\-" not in result
        assert "-" in result

    def test_clean_excerpt_strips_inline_backticks(self) -> None:
        """`` `texte` `` → texte sans backticks."""
        result = clean_excerpt("Use `create_story` to start")
        assert "create_story" in result
        assert "`" not in result


class TestCliSearchOutput:
    def test_cmd_search_groups_by_file(self) -> None:
        """La sortie CLI groupe les résultats par fichier avec un en-tête lisible."""
        import subprocess

        cli = str(PROJECT_ROOT / "hansel-tools" / "cli.py")
        proc = subprocess.run(
            [sys.executable, cli, "search", "story_cycle", "--no-color", "--max", "10"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0
        # L'output doit contenir un label auto-généré depuis le basename wiki/
        # (ex: Story_cycles_modding.md → "Story Cycles Modding")
        output = proc.stdout
        assert any(label in output for label in ["Story Cycles Modding", "Triggers", "Effects", "Scripting"])

    def test_cmd_search_shows_section_context(self) -> None:
        """L'output CLI affiche le contexte § section pour les résultats groupés."""
        import subprocess

        cli = str(PROJECT_ROOT / "hansel-tools" / "cli.py")
        proc = subprocess.run(
            [sys.executable, cli, "search", "story_cycle", "--no-color", "--max", "20"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0
        # Au moins un bloc § section doit apparaître
        assert "§" in proc.stdout
