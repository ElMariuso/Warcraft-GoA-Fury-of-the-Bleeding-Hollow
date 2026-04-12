"""Tests pour hansel-tools/linters/_linter_runner.py.

Note : on teste l'interface publique existante (`run_linter`). Si Stream B
introduit `make_linter_main`, ajouter des tests dédiés à ce moment-là.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pytest

# sys.path est géré par conftest.py

from _linter_runner import run_linter
from rules import LintRule


# ─── Types de support pour les tests ───────────────────────────────────────────


@dataclass
class FakeEventViolation:
    """Violation-like minimale compatible avec le formateur 'events'."""

    rule_id: str
    severity: str
    message: str
    event_id: str


@dataclass
class FakeLocViolation:
    """Violation-like minimale compatible avec le formateur 'localization'."""

    rule_id: str
    severity: str
    message: str
    file: str
    line: int


FAKE_RULES = [
    LintRule(id="R01", severity="ERROR", description="Test rule 1", doc_ref="doc1"),
    LintRule(id="R02", severity="WARN", description="Test rule 2", doc_ref="doc2"),
    LintRule(id="L01", severity="ERROR", description="Loc rule 1", doc_ref="doc3"),
]


# ─── run_linter : chemins heureux ──────────────────────────────────────────────


class TestRunLinterHappyPath:
    def test_no_violations_returns_zero(
        self, write_file, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Fichier clean → exit 0, pas d'appel à sys.exit."""
        target = write_file("foo.txt", "ok")

        result = run_linter(
            argv=[str(target)],
            default_path=target.parent,
            lint_fn=lambda _p: [],
            all_rules=FAKE_RULES,
            label="events",
            glob_pattern="**/*.txt",
            rule_prefix="R",
        )

        assert result == 0
        out = capsys.readouterr().out
        assert "0 error(s)" in out

    def test_warning_only_returns_zero(
        self, write_file, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Uniquement des warnings → exit 0."""
        target = write_file("foo.txt", "x")
        warn = FakeEventViolation(
            rule_id="R02", severity="WARN", message="warn!", event_id="wc_foo.1"
        )

        result = run_linter(
            argv=[str(target)],
            default_path=target.parent,
            lint_fn=lambda _p: [warn],
            all_rules=FAKE_RULES,
            label="events",
            glob_pattern="**/*.txt",
            rule_prefix="R",
        )

        assert result == 0
        out = capsys.readouterr().out
        assert "1 warning(s)" in out
        assert "wc_foo.1" in out

    def test_error_triggers_sys_exit_one(
        self, write_file, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Au moins une ERROR → sys.exit(1)."""
        target = write_file("foo.txt", "x")
        err = FakeEventViolation(
            rule_id="R01", severity="ERROR", message="boom", event_id="wc_foo.2"
        )

        with pytest.raises(SystemExit) as exc:
            run_linter(
                argv=[str(target)],
                default_path=target.parent,
                lint_fn=lambda _p: [err],
                all_rules=FAKE_RULES,
                label="events",
                glob_pattern="**/*.txt",
                rule_prefix="R",
            )

        assert exc.value.code == 1
        out = capsys.readouterr().out
        assert "1 error(s)" in out


# ─── run_linter : glob de répertoire ────────────────────────────────────────────


class TestRunLinterGlob:
    def test_directory_is_globbed(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Un répertoire doit être glob-é via le pattern."""
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        (tmp_path / "c.yml").write_text("c")  # doit être ignoré

        seen: list[str] = []

        def lint(p: Path) -> list[FakeEventViolation]:
            seen.append(p.name)
            return []

        run_linter(
            argv=[str(tmp_path)],
            default_path=tmp_path,
            lint_fn=lint,
            all_rules=FAKE_RULES,
            label="events",
            glob_pattern="**/*.txt",
            rule_prefix="R",
        )

        assert sorted(seen) == ["a.txt", "b.txt"]

    def test_single_file_lint(
        self, write_file, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Un fichier unique doit être passé tel quel au linter."""
        target = write_file("events/foo.txt", "content")
        seen: list[Path] = []

        def lint(p: Path) -> list[FakeEventViolation]:
            seen.append(p)
            return []

        run_linter(
            argv=[str(target)],
            default_path=target.parent,
            lint_fn=lint,
            all_rules=FAKE_RULES,
            label="events",
            glob_pattern="**/*.txt",
            rule_prefix="R",
        )

        assert seen == [target]


# ─── run_linter : erreurs d'usage ───────────────────────────────────────────────


class TestRunLinterCliErrors:
    def test_missing_argv_prints_rules_and_exits(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Sans arguments → affiche les règles puis sys.exit(1)."""
        with pytest.raises(SystemExit) as exc:
            run_linter(
                argv=[],
                default_path=Path("."),
                lint_fn=lambda _p: [],
                all_rules=FAKE_RULES,
                label="events",
                glob_pattern="**/*.txt",
                rule_prefix="R",
            )

        assert exc.value.code == 1
        err = capsys.readouterr()
        # Les règles filtrées par rule_prefix="R" doivent apparaître
        assert "R01" in err.out
        assert "R02" in err.out
        # La règle L01 ne commence pas par "R" — ne doit pas apparaître
        assert "L01" not in err.out

    def test_rules_flag_only_shows_matching_prefix(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """--rules avec rule_prefix='L' ne doit afficher que L01."""
        result = run_linter(
            argv=["--rules"],
            default_path=Path("."),
            lint_fn=lambda _p: [],
            all_rules=FAKE_RULES,
            label="localization",
            glob_pattern="**/*.yml",
            rule_prefix="L",
        )

        assert result == 0
        out = capsys.readouterr().out
        assert "L01" in out
        assert "R01" not in out

    def test_nonexistent_path_exits_with_error(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        ghost = tmp_path / "does_not_exist.txt"

        with pytest.raises(SystemExit) as exc:
            run_linter(
                argv=[str(ghost)],
                default_path=tmp_path,
                lint_fn=lambda _p: [],
                all_rules=FAKE_RULES,
                label="events",
                glob_pattern="**/*.txt",
                rule_prefix="R",
            )

        assert exc.value.code == 1
        err = capsys.readouterr().err
        assert "introuvable" in err

    def test_empty_directory_exits_with_error(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Un répertoire sans fichiers matchant doit afficher un message clair."""
        empty = tmp_path / "empty"
        empty.mkdir()

        with pytest.raises(SystemExit) as exc:
            run_linter(
                argv=[str(empty)],
                default_path=empty,
                lint_fn=lambda _p: [],
                all_rules=FAKE_RULES,
                label="events",
                glob_pattern="**/*.txt",
                rule_prefix="R",
            )

        assert exc.value.code == 1
        err = capsys.readouterr().err
        assert "Aucun fichier" in err


# ─── Formateur localization (chemin séparé) ─────────────────────────────────────


class TestRunLinterLocalizationFormat:
    def test_localization_violation_formatted_with_line(
        self, write_file, capsys: pytest.CaptureFixture[str]
    ) -> None:
        target = write_file("loc.yml", "x")
        v = FakeLocViolation(
            rule_id="L01",
            severity="ERROR",
            message="missing BOM",
            file="loc.yml",
            line=3,
        )

        with pytest.raises(SystemExit):
            run_linter(
                argv=[str(target)],
                default_path=target.parent,
                lint_fn=lambda _p: [v],
                all_rules=FAKE_RULES,
                label="localization",
                glob_pattern="**/*.yml",
                rule_prefix="L",
            )

        out = capsys.readouterr().out
        assert "loc.yml:3" in out
        assert "missing BOM" in out
        assert "L01" in out
