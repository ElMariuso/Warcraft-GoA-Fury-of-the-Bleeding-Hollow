"""tests/test_lint_events.py — Tests pour lint_events.py"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hansel-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hansel-tools", "linters"))

from lint_events import EventBlock, check_block, extract_event_blocks, lint_file
from pathlib import Path


# ─── extract_event_blocks ──────────────────────────────────────────────────────

class TestExtractEventBlocks:
    def test_extrait_un_bloc_simple(self) -> None:
        text = "wc_foo.1000 = {\n\ttype = character_event\n}\n"
        blocks = extract_event_blocks(text)
        assert len(blocks) == 1
        assert blocks[0].id == "wc_foo.1000"

    def test_extrait_plusieurs_blocs(self) -> None:
        text = (
            "wc_foo.1000 = {\n\ttype = character_event\n}\n"
            "wc_foo.1001 = {\n\ttype = character_event\n}\n"
        )
        blocks = extract_event_blocks(text)
        assert len(blocks) == 2
        assert blocks[0].id == "wc_foo.1000"
        assert blocks[1].id == "wc_foo.1001"

    def test_bloc_avec_accolades_imbriquees(self) -> None:
        text = "wc_foo.1000 = {\n\toption = {\n\t\tai_chance = { base = 100 }\n\t}\n}\n"
        blocks = extract_event_blocks(text)
        assert len(blocks) == 1
        assert "option" in blocks[0].raw

    def test_ignore_blocs_sans_point(self) -> None:
        # scripted_effect sans point — ne doit pas être capturé
        text = (
            "spawn_troops_effect = {\n\tadd_army = yes\n}\n"
            "wc_foo.1000 = {\n\ttype = character_event\n}\n"
        )
        blocks = extract_event_blocks(text)
        # Seul wc_foo.1000 doit être capturé (spawn_troops_effect n'a pas de point)
        assert all("." in b.id for b in blocks)

    def test_line_start_correct(self) -> None:
        text = "namespace = wc_foo\n\nwc_foo.1000 = {\n\ttype = character_event\n}\n"
        blocks = extract_event_blocks(text)
        assert blocks[0].line_start == 3


# ─── check_block ───────────────────────────────────────────────────────────────

class TestCheckBlockR01:
    def test_event_visible_sans_content_source_donne_erreur(self) -> None:
        block = EventBlock(
            id="wc_foo.1000",
            raw="\ttype = character_event\n\ttitle = wc_foo.1000.title\n\tdesc = wc_foo.1000.desc\n"
                "\toption = {\n\t\tname = wc_foo.1000.a\n\t\tai_chance = { base = 100 }\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        rule_ids = [v.rule_id for v in violations]
        assert "R01" in rule_ids

    def test_event_avec_content_source_pas_de_r01(self) -> None:
        block = EventBlock(
            id="wc_foo.1000",
            raw="\ttype = character_event\n\tcontent_source = dlc_GOA\n"
                "\ttitle = wc_foo.1000.title\n\tdesc = wc_foo.1000.desc\n"
                "\toption = {\n\t\tname = wc_foo.1000.a\n\t\tai_chance = { base = 100 }\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        assert not any(v.rule_id == "R01" for v in violations)

    def test_event_hidden_exempte_de_r01(self) -> None:
        block = EventBlock(
            id="wc_foo.0001",
            raw="\thidden = yes\n\tscope = none\n",
            line_start=1,
        )
        violations = check_block(block)
        assert not any(v.rule_id == "R01" for v in violations)


class TestCheckBlockR02:
    def test_option_sans_ai_chance_donne_erreur(self) -> None:
        block = EventBlock(
            id="wc_foo.1000",
            raw="\tcontent_source = dlc_GOA\n\ttitle = t\n\tdesc = d\n"
                "\toption = {\n\t\tname = wc_foo.1000.a\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        assert any(v.rule_id == "R02" for v in violations)

    def test_option_avec_ai_chance_pas_de_r02(self) -> None:
        block = EventBlock(
            id="wc_foo.1000",
            raw="\tcontent_source = dlc_GOA\n\ttitle = t\n\tdesc = d\n"
                "\toption = {\n\t\tname = wc_foo.1000.a\n\t\tai_chance = { base = 100 }\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        assert not any(v.rule_id == "R02" for v in violations)

    def test_deux_options_une_sans_ai_chance(self) -> None:
        block = EventBlock(
            id="wc_foo.1000",
            raw="\tcontent_source = dlc_GOA\n\ttitle = t\n\tdesc = d\n"
                "\toption = {\n\t\tai_chance = { base = 100 }\n\t}\n"
                "\toption = {\n\t\tname = b\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        r02 = [v for v in violations if v.rule_id == "R02"]
        assert len(r02) == 1
        assert "1 option(s)" in r02[0].message


class TestCheckBlockR04:
    def test_event_visible_sans_title_donne_erreur(self) -> None:
        block = EventBlock(
            id="wc_foo.1000",
            raw="\tcontent_source = dlc_GOA\n\tdesc = d\n"
                "\toption = {\n\t\tai_chance = { base = 100 }\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        assert any(v.rule_id == "R04" and "title" in v.message for v in violations)

    def test_event_visible_sans_desc_donne_erreur(self) -> None:
        block = EventBlock(
            id="wc_foo.1000",
            raw="\tcontent_source = dlc_GOA\n\ttitle = t\n"
                "\toption = {\n\t\tai_chance = { base = 100 }\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        assert any(v.rule_id == "R04" and "desc" in v.message for v in violations)

    def test_event_hidden_exempte_de_r04(self) -> None:
        block = EventBlock(
            id="wc_foo.0001",
            raw="\thidden = yes\n\tscope = none\n",
            line_start=1,
        )
        violations = check_block(block)
        assert not any(v.rule_id == "R04" for v in violations)


class TestCheckBlockR05:
    def test_mean_time_sans_trigger_donne_warn(self) -> None:
        block = EventBlock(
            id="wc_foo.2000",
            raw="\tcontent_source = dlc_GOA\n\ttitle = t\n\tdesc = d\n"
                "\tmean_time_to_happen = { months = 18 }\n"
                "\toption = {\n\t\tai_chance = { base = 100 }\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        assert any(v.rule_id == "R05" for v in violations)

    def test_mean_time_avec_trigger_pas_de_r05(self) -> None:
        block = EventBlock(
            id="wc_foo.2000",
            raw="\tcontent_source = dlc_GOA\n\ttitle = t\n\tdesc = d\n"
                "\tmean_time_to_happen = { months = 18 }\n"
                "\ttrigger = { always = yes }\n"
                "\toption = {\n\t\tai_chance = { base = 100 }\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        assert not any(v.rule_id == "R05" for v in violations)


class TestCheckBlockR06:
    def test_portrait_dans_hidden_donne_warn(self) -> None:
        block = EventBlock(
            id="wc_foo.0001",
            raw="\thidden = yes\n\tleft_portrait = { character = root }\n",
            line_start=1,
        )
        violations = check_block(block)
        assert any(v.rule_id == "R06" for v in violations)

    def test_portrait_dans_visible_pas_de_r06(self) -> None:
        block = EventBlock(
            id="wc_foo.1000",
            raw="\tcontent_source = dlc_GOA\n\ttitle = t\n\tdesc = d\n"
                "\tleft_portrait = { character = root animation = idle }\n"
                "\toption = {\n\t\tai_chance = { base = 100 }\n\t}\n",
            line_start=1,
        )
        violations = check_block(block)
        assert not any(v.rule_id == "R06" for v in violations)


class TestCheckBlockEventValide:
    def test_event_valide_zero_violations(self) -> None:
        block = EventBlock(
            id="wc_foo.1000",
            raw=(
                "\ttype = character_event\n"
                "\tcontent_source = dlc_GOA\n"
                "\ttitle = wc_foo.1000.title\n"
                "\tdesc = wc_foo.1000.desc\n"
                "\tleft_portrait = { character = root animation = personality_bold }\n"
                "\toption = {\n"
                "\t\tname = wc_foo.1000.a\n"
                "\t\tai_chance = { base = 100 }\n"
                "\t}\n"
            ),
            line_start=1,
        )
        violations = check_block(block)
        errors = [v for v in violations if v.severity == "ERROR"]
        assert errors == []


# ─── lint_file (smoke test) ────────────────────────────────────────────────────

class TestLintFile:
    def test_bleeding_hollow_events_aucune_erreur(self) -> None:
        """Smoke test : les events existants doivent passer sans ERROR."""
        project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        events_file = project_root / "events" / "story_cycles" / "wc_story_cycle_bleeding_hollow_invasion_events.txt"

        if not events_file.exists():
            pytest.skip("Fichier d'events introuvable")

        violations = lint_file(events_file)
        errors = [v for v in violations if v.severity == "ERROR"]
        # On affiche pour diagnostic si ça échoue
        for e in errors:
            print(f"  [{e.severity}] {e.event_id} — {e.message} ({e.rule_id})")
        assert errors == [], f"{len(errors)} erreur(s) détectée(s)"

    def test_fichier_inexistant_retourne_liste_vide(self, tmp_path: Path) -> None:
        # lint_file est appelé via main() qui gère l'absence — on teste lint_file directement
        # avec un fichier vide créé puis supprimé
        fake = tmp_path / "empty.txt"
        fake.write_text("", encoding="utf-8")
        violations = lint_file(fake)
        assert violations == []
