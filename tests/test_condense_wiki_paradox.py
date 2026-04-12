"""
tests/test_condense_wiki_paradox.py — Tests pour condense_wiki_paradox.py
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hansel-tools"))

from condense_wiki_paradox import (
    THEMES,
    clean_page,
    deduplicate_blank_lines,
    is_noise_line,
    remove_section_blocks,
    strip_edit_links,
)


class TestStripEditLinks:
    def test_removes_wiki_edit_block(self) -> None:
        line = "## Effects [[edit][edit source]edit source]"
        result = strip_edit_links(line)
        assert "[edit" not in result
        assert "## Effects" in result

    def test_removes_simple_edit_link(self) -> None:
        line = "## Scopes [edit](/index.php?title=Scopes&action=edit)"
        result = strip_edit_links(line)
        assert "[edit]" not in result
        assert "## Scopes" in result

    def test_leaves_normal_line_unchanged(self) -> None:
        line = "## Effects"
        assert strip_edit_links(line) == "## Effects"


class TestIsNoiseLine:
    def test_detects_jump_to_navigation(self) -> None:
        assert is_noise_line("Jump to navigation")

    def test_detects_retrieved_from(self) -> None:
        assert is_noise_line("Retrieved from https://ck3.paradoxwikis.com")

    def test_detects_navbox_modding(self) -> None:
        assert is_noise_line("**[Modding](/Modding) | [Scripting](/Scripting)")

    def test_detects_edit_source_link(self) -> None:
        assert is_noise_line("[edit source](/index.php?title=Effects&action=edit)")

    def test_passes_normal_content(self) -> None:
        assert not is_noise_line("A trigger is a condition that must be true.")

    def test_passes_code_block(self) -> None:
        assert not is_noise_line("    character = { age >= 16 }")


class TestRemoveSectionBlocks:
    def test_removes_contents_section(self) -> None:
        lines = [
            "## Contents",
            "  * 1 Overview",
            "  * 2 Syntax",
            "## Overview",
            "Real content here.",
        ]
        result = remove_section_blocks(lines)
        assert "## Contents" not in result
        assert "  * 1 Overview" not in result
        assert "## Overview" in result
        assert "Real content here." in result

    def test_removes_see_also_section(self) -> None:
        lines = [
            "## See also",
            "- [[Effects]]",
            "## Next section",
            "Content.",
        ]
        result = remove_section_blocks(lines)
        assert "## See also" not in result
        assert "- [[Effects]]" not in result
        assert "## Next section" in result

    def test_preserves_normal_sections(self) -> None:
        lines = ["## Syntax", "key = value", "## Usage", "More content."]
        result = remove_section_blocks(lines)
        assert result == lines


class TestDeduplicateBlankLines:
    def test_reduces_triple_blank_to_double(self) -> None:
        lines = ["a", "", "", "", "b"]
        result = deduplicate_blank_lines(lines)
        assert result == ["a", "", "", "b"]

    def test_preserves_single_blank(self) -> None:
        lines = ["a", "", "b"]
        result = deduplicate_blank_lines(lines)
        assert result == ["a", "", "b"]

    def test_max_consecutive_one(self) -> None:
        lines = ["a", "", "", "b"]
        result = deduplicate_blank_lines(lines, max_consecutive=1)
        assert result == ["a", "", "b"]


class TestCleanPage:
    def test_removes_source_line(self) -> None:
        raw = "> Source : https://ck3.paradoxwikis.com\n\n## Effects\n\nContent."
        result = clean_page(raw)
        assert "> Source :" not in result
        assert "## Effects" in result

    def test_removes_multiple_noise_types(self) -> None:
        raw = (
            "Jump to navigation\n"
            "## Scripting\n\n"
            "Real content here.\n\n"
            "Retrieved from https://example.com\n"
        )
        result = clean_page(raw)
        assert "Jump to navigation" not in result
        assert "Retrieved from" not in result
        assert "Real content here." in result
        assert "## Scripting" in result

    def test_strips_edit_links_from_headings(self) -> None:
        raw = "## Effects [edit](/index.php?title=Effects&action=edit)\n\nContent."
        result = clean_page(raw)
        assert "[edit]" not in result
        assert "## Effects" in result

    def test_empty_after_cleaning_returns_short_string(self) -> None:
        raw = "Jump to navigation\nRetrieved from https://example.com\n"
        result = clean_page(raw)
        assert len(result) < 100


class TestIntegration:
    """Smoke test : vérifie que le script génère les 7 fichiers attendus."""

    def test_all_theme_keys_defined(self) -> None:
        expected = {
            "01_scripting_core",
            "02_triggers_effects",
            "03_events_decisions",
            "04_characters_history",
            "05_culture_religion_traits",
            "06_localization",
            "07_mod_structure_debug",
        }
        assert set(THEMES.keys()) == expected

    def test_each_theme_has_sources(self) -> None:
        for theme_key, sources in THEMES.items():
            assert len(sources) >= 1, f"{theme_key} n'a aucune source"
            for filename, title in sources:
                assert filename.endswith(".md"), f"{filename} devrait être un .md"
                assert len(title) > 0, f"Titre vide pour {filename} dans {theme_key}"

    def test_generated_files_exist_and_nonempty(self) -> None:
        """Vérifie que le script a bien généré les 7 fichiers dans docs/wiki-paradox/."""
        submod_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(submod_root, "docs", "wiki-paradox")

        if not os.path.isdir(output_dir):
            pytest.skip("docs/wiki-paradox/ non généré — lancer condense_wiki_paradox.py d'abord")

        for theme_key in THEMES:
            output_file = os.path.join(output_dir, f"{theme_key}.md")
            assert os.path.isfile(output_file), f"Fichier manquant : {theme_key}.md"
            with open(output_file, encoding="utf-8") as f:
                content = f.read()
            assert len(content) > 200, f"{theme_key}.md semble vide"

    def test_no_residual_noise_in_generated_files(self) -> None:
        """Vérifie l'absence de bruit MediaWiki dans les fichiers générés."""
        submod_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_dir = os.path.join(submod_root, "docs", "wiki-paradox")

        if not os.path.isdir(output_dir):
            pytest.skip("docs/wiki-paradox/ non généré — lancer condense_wiki_paradox.py d'abord")

        noise_patterns = ["Retrieved from", "Jump to navigation", "edit source]"]
        for theme_key in THEMES:
            output_file = os.path.join(output_dir, f"{theme_key}.md")
            if not os.path.isfile(output_file):
                continue
            with open(output_file, encoding="utf-8") as f:
                content = f.read()
            for pattern in noise_patterns:
                assert pattern not in content, (
                    f"Bruit résiduel '{pattern}' trouvé dans {theme_key}.md"
                )
