"""tests/test_lint_effects.py — Tests pour lint_effects.py"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hansel-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hansel-tools", "linters"))

from pathlib import Path
from lint_effects import EffectBlock, check_block, extract_effect_blocks, lint_file
from symbol_db import SymbolDB


def _make_db(
    characters: list[int] | None = None,
    titles: list[str] | None = None,
    modifiers: list[str] | None = None,
    effects: list[str] | None = None,
) -> SymbolDB:
    return SymbolDB(
        characters=frozenset(characters or []),
        titles=frozenset(titles or []),
        modifiers=frozenset(modifiers or []),
        scripted_effects=frozenset(effects or []),
        scripted_triggers=frozenset(),
    )


# ─── extract_effect_blocks ─────────────────────────────────────────────────────

class TestExtractEffectBlocks:
    def test_extrait_un_bloc_simple(self) -> None:
        text = "my_effect = {\n\tadd_prestige = 500\n}\n"
        blocks = extract_effect_blocks(text)
        assert len(blocks) == 1
        assert blocks[0].name == "my_effect"

    def test_extrait_plusieurs_blocs(self) -> None:
        text = (
            "effect_a = {\n\tadd_prestige = 100\n}\n"
            "effect_b = {\n\tadd_gold = 50\n}\n"
        )
        blocks = extract_effect_blocks(text)
        assert len(blocks) == 2
        assert blocks[0].name == "effect_a"
        assert blocks[1].name == "effect_b"

    def test_raw_contient_le_corps(self) -> None:
        text = "my_effect = {\n\tadd_prestige = 500\n}\n"
        blocks = extract_effect_blocks(text)
        assert "add_prestige" in blocks[0].raw

    def test_bloc_avec_accolades_imbriquees(self) -> None:
        text = "my_effect = {\n\tif = {\n\t\tlimit = { always = yes }\n\t}\n}\n"
        blocks = extract_effect_blocks(text)
        assert len(blocks) == 1
        assert "if" in blocks[0].raw

    def test_line_start_correct(self) -> None:
        text = "# comment\n\nmy_effect = {\n\tadd_prestige = 500\n}\n"
        blocks = extract_effect_blocks(text)
        assert blocks[0].line_start == 3


# ─── check_block ───────────────────────────────────────────────────────────────

class TestCheckBlockSansDb:
    def test_sans_db_aucune_violation(self) -> None:
        block = EffectBlock(
            name="my_effect",
            raw="\tcharacter:10005 = { save_scope_as = kilrogg }\n",
            line_start=1,
        )
        violations = check_block(block, db=None)
        assert violations == []


class TestCheckBlockE01:
    def test_character_inconnu_donne_E01(self) -> None:
        db = _make_db(characters=[10005])
        block = EffectBlock(
            name="my_effect",
            raw="\tcharacter:99999 = { save_scope_as = x }\n",
            line_start=1,
        )
        violations = check_block(block, db=db)
        assert any(v.rule_id == "E01" for v in violations)

    def test_character_connu_aucune_violation(self) -> None:
        db = _make_db(characters=[10005])
        block = EffectBlock(
            name="my_effect",
            raw="\tcharacter:10005 = { save_scope_as = kilrogg }\n",
            line_start=1,
        )
        violations = check_block(block, db=db)
        assert not any(v.rule_id == "E01" for v in violations)


class TestCheckBlockE02:
    def test_title_inconnu_donne_E02(self) -> None:
        db = _make_db(titles=["k_gurubashi"])
        block = EffectBlock(
            name="my_effect",
            raw="\ttitle:k_fake_title = { save_scope_as = x }\n",
            line_start=1,
        )
        violations = check_block(block, db=db)
        assert any(v.rule_id == "E02" for v in violations)

    def test_title_connu_aucune_violation(self) -> None:
        db = _make_db(titles=["k_gurubashi"])
        block = EffectBlock(
            name="my_effect",
            raw="\ttitle:k_gurubashi = { save_scope_as = x }\n",
            line_start=1,
        )
        violations = check_block(block, db=db)
        assert not any(v.rule_id == "E02" for v in violations)


class TestCheckBlockE03:
    def test_modifier_inconnu_donne_E03(self) -> None:
        db = _make_db(modifiers=["great_invader_modifier"])
        block = EffectBlock(
            name="my_effect",
            raw="\tadd_character_modifier = { modifier = fake_modifier }\n",
            line_start=1,
        )
        violations = check_block(block, db=db)
        assert any(v.rule_id == "E03" for v in violations)

    def test_modifier_connu_aucune_violation(self) -> None:
        db = _make_db(modifiers=["great_invader_modifier"])
        block = EffectBlock(
            name="my_effect",
            raw="\tadd_character_modifier = { modifier = great_invader_modifier }\n",
            line_start=1,
        )
        violations = check_block(block, db=db)
        assert not any(v.rule_id == "E03" for v in violations)


class TestCheckBlockE04:
    def test_effect_appele_inconnu_donne_E04(self) -> None:
        db = _make_db(effects=["known_effect"])
        block = EffectBlock(
            name="my_effect",
            raw="\tunknown_effect = yes\n",
            line_start=1,
        )
        violations = check_block(block, db=db)
        assert any(v.rule_id == "E04" for v in violations)

    def test_builtin_effect_ignore(self) -> None:
        db = _make_db()
        block = EffectBlock(
            name="my_effect",
            raw="\thidden_effect = { add_prestige = 100 }\n",
            line_start=1,
        )
        violations = check_block(block, db=db)
        assert not any(v.rule_id == "E04" for v in violations)


# ─── lint_file (smoke test) ────────────────────────────────────────────────────

class TestLintFile:
    def test_bleeding_hollow_effects_aucune_erreur(self) -> None:
        """Smoke test : les scripted effects existants doivent passer sans ERROR."""
        project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        effects_file = (
            project_root
            / "common"
            / "scripted_effects"
            / "wc_bleeding_hollow_invasion_effects.txt"
        )

        if not effects_file.exists():
            pytest.skip("Fichier de scripted effects introuvable")

        # Sans db — E01-E04 désactivés, aucune erreur possible
        violations = lint_file(effects_file, db=None)
        errors = [v for v in violations if v.severity == "ERROR"]
        for e in errors:
            print(f"  [{e.severity}] {e.effect_name} — {e.message} ({e.rule_id})")
        assert errors == [], f"{len(errors)} erreur(s) détectée(s)"

    def test_fichier_vide_aucune_violation(self, tmp_path: Path) -> None:
        f = tmp_path / "empty_effects.txt"
        f.write_text("", encoding="utf-8")
        violations = lint_file(f, db=None)
        assert violations == []
