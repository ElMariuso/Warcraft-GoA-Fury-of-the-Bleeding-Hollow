"""tests/test_lint_localization.py — Tests pour lint_localization.py"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hansel-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hansel-tools", "linters"))

from pathlib import Path
from lint_localization import (
    LocKey,
    check_bom,
    check_header,
    check_key,
    extract_loc_keys,
    lint_file,
)

_UTF8_BOM = b"\xef\xbb\xbf"


# ─── check_bom ─────────────────────────────────────────────────────────────────

class TestCheckBom:
    def test_bom_present_aucune_violation(self) -> None:
        raw = _UTF8_BOM + b"l_english:\n"
        violations = check_bom(raw, "test.yml")
        assert violations == []

    def test_bom_absent_donne_L01(self) -> None:
        raw = b"l_english:\n"
        violations = check_bom(raw, "test.yml")
        assert len(violations) == 1
        assert violations[0].rule_id == "L01"
        assert violations[0].severity == "ERROR"

    def test_bom_absent_message_utile(self) -> None:
        raw = b"l_english:\n"
        v = check_bom(raw, "foo.yml")[0]
        assert "BOM" in v.message


# ─── check_header ──────────────────────────────────────────────────────────────

class TestCheckHeader:
    def test_header_correct_aucune_violation(self) -> None:
        violations = check_header("l_english:\n key:0 \"text\"\n", "test.yml")
        assert violations == []

    def test_header_incorrect_donne_L02(self) -> None:
        violations = check_header("l_french:\n key:0 \"text\"\n", "test.yml")
        assert len(violations) == 1
        assert violations[0].rule_id == "L02"

    def test_header_avec_commentaire_avant_ok(self) -> None:
        text = "# comment\nl_english:\n key:0 \"text\"\n"
        violations = check_header(text, "test.yml")
        assert violations == []

    def test_fichier_vide_donne_L02(self) -> None:
        violations = check_header("", "test.yml")
        assert any(v.rule_id == "L02" for v in violations)

    def test_fichier_que_commentaires_donne_L02(self) -> None:
        violations = check_header("# only a comment\n# another\n", "test.yml")
        assert any(v.rule_id == "L02" for v in violations)


# ─── extract_loc_keys ──────────────────────────────────────────────────────────

class TestExtractLocKeys:
    def test_extrait_cle_simple(self) -> None:
        text = 'l_english:\n wc_foo.1000.title:0 "The Title"\n'
        keys = extract_loc_keys(text)
        assert len(keys) == 1
        assert keys[0].key == "wc_foo.1000.title"
        assert keys[0].version == 0
        assert keys[0].value == "The Title"

    def test_extrait_plusieurs_cles(self) -> None:
        text = (
            'l_english:\n'
            ' wc_foo.1000.title:0 "Title"\n'
            ' wc_foo.1000.desc:0 "Desc"\n'
        )
        keys = extract_loc_keys(text)
        assert len(keys) == 2

    def test_ignore_commentaires(self) -> None:
        text = 'l_english:\n # wc_foo.ignored:0 "no"\n wc_foo.1000.title:0 "yes"\n'
        keys = extract_loc_keys(text)
        assert len(keys) == 1
        assert keys[0].key == "wc_foo.1000.title"

    def test_cle_version_non_nulle(self) -> None:
        text = 'l_english:\n wc_foo.1000.title:1 "Title"\n'
        keys = extract_loc_keys(text)
        assert keys[0].version == 1

    def test_numero_de_ligne_correct(self) -> None:
        text = 'l_english:\n wc_foo.1000.title:0 "A"\n wc_foo.1001.title:0 "B"\n'
        keys = extract_loc_keys(text)
        assert keys[0].line == 2
        assert keys[1].line == 3


# ─── check_key ─────────────────────────────────────────────────────────────────

class TestCheckKey:
    def test_cle_valide_aucune_violation(self) -> None:
        key = LocKey(key="wc_foo.1000.title", version=0, value="The Title", line=2)
        violations = check_key(key, "test.yml")
        assert violations == []

    def test_version_non_nulle_donne_L05(self) -> None:
        key = LocKey(key="wc_foo.1000.title", version=1, value="The Title", line=2)
        violations = check_key(key, "test.yml")
        assert any(v.rule_id == "L05" for v in violations)

    def test_placeholder_blablabla_donne_L04(self) -> None:
        key = LocKey(key="wc_foo.1000.title", version=0, value="Blablabla", line=2)
        violations = check_key(key, "test.yml")
        assert any(v.rule_id == "L04" for v in violations)

    def test_placeholder_dans_texte_donne_L04(self) -> None:
        key = LocKey(key="wc_foo.1000.desc", version=0, value="Some Blablabla text here.", line=2)
        violations = check_key(key, "test.yml")
        assert any(v.rule_id == "L04" for v in violations)

    def test_version_0_et_valeur_correcte_aucune_violation(self) -> None:
        key = LocKey(key="wc_foo.1000.a", version=0, value="Lok'tar Ogar!", line=5)
        violations = check_key(key, "test.yml")
        assert violations == []


# ─── lint_file (smoke test) ────────────────────────────────────────────────────

class TestLintFile:
    def test_bleeding_hollow_loc_aucune_erreur(self) -> None:
        """Smoke test : le fichier de localisation existant doit passer sans ERROR."""
        project_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        loc_file = project_root / "localization" / "english" / "wc_bleeding_hollow_invasion_l_english.yml"

        if not loc_file.exists():
            pytest.skip("Fichier de localisation introuvable")

        violations = lint_file(loc_file)
        errors = [v for v in violations if v.severity == "ERROR"]
        for e in errors:
            print(f"  [{e.severity}] {e.file}:{e.line} — {e.message} ({e.rule_id})")
        assert errors == [], f"{len(errors)} erreur(s) détectée(s)"

    def test_fichier_sans_bom_donne_L01(self, tmp_path: Path) -> None:
        f = tmp_path / "test_l_english.yml"
        f.write_bytes(b'l_english:\n wc_foo.1000.title:0 "Title"\n')
        violations = lint_file(f)
        assert any(v.rule_id == "L01" for v in violations)

    def test_fichier_avec_bom_et_header_correct_aucune_erreur(self, tmp_path: Path) -> None:
        f = tmp_path / "test_l_english.yml"
        content = b'\xef\xbb\xbfl_english:\n wc_foo.1000.title:0 "Title"\n'
        f.write_bytes(content)
        violations = lint_file(f)
        errors = [v for v in violations if v.severity == "ERROR"]
        assert errors == []
