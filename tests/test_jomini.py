"""Tests pour hansel-tools/linters/_jomini.py — parsing primitives."""
from __future__ import annotations

# sys.path est géré par conftest.py

from _jomini import (
    CHAR_REF,
    CK3_BUILTIN_EFFECTS,
    EFFECT_CALL,
    EFFECT_HEADER,
    EVENT_HEADER,
    MODIFIER_NAME,
    TITLE_REF,
    Block,
    extract_blocks,
)


# ─── extract_blocks ─────────────────────────────────────────────────────────────


class TestExtractBlocks:
    def test_extrait_un_event_simple(self) -> None:
        text = "wc_foo.1000 = {\n\ttype = character_event\n}\n"
        blocks = extract_blocks(text, EVENT_HEADER)
        assert len(blocks) == 1
        assert blocks[0].id == "wc_foo.1000"
        assert blocks[0].line_start == 1
        assert "type = character_event" in blocks[0].raw

    def test_extrait_plusieurs_events_sequentiels(self) -> None:
        text = (
            "wc_foo.1 = {\n\tA = 1\n}\n\n"
            "wc_foo.2 = {\n\tB = 2\n}\n"
        )
        blocks = extract_blocks(text, EVENT_HEADER)
        assert [b.id for b in blocks] == ["wc_foo.1", "wc_foo.2"]
        assert blocks[1].line_start == 5

    def test_gere_blocs_imbriques(self) -> None:
        """La state machine doit gérer les accolades imbriquées correctement."""
        text = (
            "wc_foo.1 = {\n"
            "\toption = {\n"
            "\t\ttrigger = { x = yes }\n"
            "\t}\n"
            "}\n"
        )
        blocks = extract_blocks(text, EVENT_HEADER)
        assert len(blocks) == 1
        raw = blocks[0].raw
        assert "option" in raw
        assert "trigger" in raw
        # Toutes les accolades internes doivent être présentes
        assert raw.count("{") == raw.count("}")

    def test_extract_effect_header(self) -> None:
        """EFFECT_HEADER ne doit pas matcher un event (id avec un point)."""
        text = (
            "spawn_orc_troops_effect = {\n"
            "\tadd_troops = yes\n"
            "}\n"
        )
        blocks = extract_blocks(text, EFFECT_HEADER)
        assert len(blocks) == 1
        assert blocks[0].id == "spawn_orc_troops_effect"

    def test_fichier_vide_retourne_liste_vide(self) -> None:
        assert extract_blocks("", EVENT_HEADER) == []
        assert extract_blocks("# just a comment\n", EVENT_HEADER) == []

    def test_line_start_multi_blocks(self) -> None:
        text = "\n\nwc_foo.1 = {\n}\n\nwc_foo.2 = {\n}\n"
        blocks = extract_blocks(text, EVENT_HEADER)
        assert blocks[0].line_start == 3
        assert blocks[1].line_start == 6

    def test_block_est_immutable(self) -> None:
        b = Block(id="x", raw="", line_start=1)
        import dataclasses

        assert dataclasses.is_dataclass(b)
        # frozen=True — les mutations doivent lever FrozenInstanceError
        import pytest

        with pytest.raises(dataclasses.FrozenInstanceError):
            b.id = "y"  # type: ignore[misc]


# ─── Regex references ───────────────────────────────────────────────────────────


class TestCharRef:
    def test_match_character_id(self) -> None:
        matches = CHAR_REF.findall("save_scope_as = kilrogg character:10005 = { }")
        assert matches == ["10005"]

    def test_no_match_on_non_digit(self) -> None:
        assert CHAR_REF.findall("character:kilrogg") == []

    def test_multiple_matches(self) -> None:
        text = "character:10000 and character:10005 fight"
        assert CHAR_REF.findall(text) == ["10000", "10005"]


class TestTitleRef:
    def test_match_title_key(self) -> None:
        assert TITLE_REF.findall("title:e_horde.holder") == ["e_horde"]

    def test_match_county_title(self) -> None:
        assert TITLE_REF.findall("title:c_vekrishe = { }") == ["c_vekrishe"]

    def test_no_match_without_prefix(self) -> None:
        assert TITLE_REF.findall("e_horde = { }") == []


class TestEffectCall:
    def test_match_yes_form(self) -> None:
        assert EFFECT_CALL.findall("horde_bloodshed_effect = yes") == [
            "horde_bloodshed_effect"
        ]

    def test_match_block_form(self) -> None:
        assert EFFECT_CALL.findall("spawn_orc_troops_effect = { owner = yes }") == [
            "spawn_orc_troops_effect"
        ]

    def test_no_match_on_plain_assignment(self) -> None:
        # Doit matcher uniquement si la clé se termine par _effect
        assert EFFECT_CALL.findall("count = 5") == []


class TestModifierName:
    def test_has_modifier(self) -> None:
        groups = MODIFIER_NAME.findall("has_character_modifier = great_invader_modifier")
        # La regex a deux groupes alternatifs
        flat = [g for tup in groups for g in tup if g]
        assert "great_invader_modifier" in flat

    def test_remove_modifier(self) -> None:
        groups = MODIFIER_NAME.findall("remove_county_modifier = recently_sacked_modifier")
        flat = [g for tup in groups for g in tup if g]
        assert "recently_sacked_modifier" in flat

    def test_modifier_assignment(self) -> None:
        groups = MODIFIER_NAME.findall("add_modifier = { modifier = path_to_glory_modifier }")
        flat = [g for tup in groups for g in tup if g]
        assert "path_to_glory_modifier" in flat


class TestEventHeader:
    def test_match_event_id(self) -> None:
        matches = EVENT_HEADER.findall("wc_horde_invasion.1004 = {")
        assert matches == ["wc_horde_invasion.1004"]

    def test_no_match_without_dot(self) -> None:
        assert EVENT_HEADER.findall("my_effect = {") == []


class TestEffectHeader:
    def test_match_effect_name(self) -> None:
        matches = EFFECT_HEADER.findall("spawn_orc_troops_effect = {")
        assert matches == ["spawn_orc_troops_effect"]

    def test_no_match_on_uppercase(self) -> None:
        # La regex exige une minuscule en début
        assert EFFECT_HEADER.findall("SpawnTroops = {") == []


class TestBuiltinEffects:
    def test_contains_hidden_effect(self) -> None:
        assert "hidden_effect" in CK3_BUILTIN_EFFECTS

    def test_contains_random_effect(self) -> None:
        assert "random_effect" in CK3_BUILTIN_EFFECTS

    def test_frozenset_immutable(self) -> None:
        assert isinstance(CK3_BUILTIN_EFFECTS, frozenset)
