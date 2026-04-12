#!/usr/bin/env python3
"""Linter pour les fichiers de scripted effects CK3 (.txt).

Valide chaque bloc d'effet contre les règles E01–E04 via symbol_db :
  E01 — character:<ID> introuvable dans le parent mod
  E02 — title:<KEY> introuvable dans le parent mod
  E03 — modifier introuvable dans le parent mod
  E04 — scripted effect appelé introuvable dans le parent mod

Usage:
    python tools/lint_effects.py common/scripted_effects/
    python tools/lint_effects.py common/scripted_effects/wc_foo_effects.txt
    python tools/lint_effects.py --rules
"""

import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))         # hansel-tools/linters/
sys.path.insert(0, str(Path(__file__).parent.parent))  # hansel-tools/
from config import SUBMOD_ROOT
from rules import Severity
from symbol_db import SymbolDB
from _jomini import EFFECT_HEADER, extract_blocks
from _linter_runner import check_symbol_references, make_linter_main


_EFFECT_RULE_MAP = {
    "char": "E01",
    "title": "E02",
    "modifier": "E03",
    "effect": "E04",
}


@dataclass
class EffectBlock:
    """Un bloc de scripted effect extrait d'un fichier .txt CK3."""

    name: str       # ex: "spawn_orc_troops_based_on_culture_effect"
    raw: str        # contenu brut du bloc (entre les accolades)
    line_start: int


@dataclass
class LintViolation:
    """Une violation détectée dans un bloc de scripted effect."""

    rule_id: str
    effect_name: str
    severity: Severity
    message: str
    line: int = 0


def extract_effect_blocks(text: str) -> list[EffectBlock]:
    """Extrait les blocs de scripted effects d'un fichier .txt CK3.

    Utilise la fonction partagée extract_blocks() avec EFFECT_HEADER.
    Wrapper fourni pour la compatibilité avec les tests existants.
    """
    raw_blocks = extract_blocks(text, EFFECT_HEADER)
    return [
        EffectBlock(name=b.id, raw=b.raw, line_start=b.line_start)
        for b in raw_blocks
    ]


def check_block(
    block: EffectBlock, db: SymbolDB | None = None
) -> list[LintViolation]:
    """Applique les règles E01–E04 à un bloc de scripted effect.

    Si db est None (symbols.json absent), les règles sont silencieusement ignorées.
    """
    if db is None:
        return []

    ename = block.name
    line = block.line_start

    def _make_v(rule_id: str, severity: str, message: str) -> LintViolation:
        return LintViolation(
            rule_id=rule_id,
            effect_name=ename,
            severity=severity,  # type: ignore[arg-type]
            message=message,
            line=line,
        )

    return check_symbol_references(block.raw, db, _EFFECT_RULE_MAP, _make_v)


def lint_file(path: Path, db: SymbolDB | None = None) -> list[LintViolation]:
    """Lint un fichier .txt de scripted effects et retourne toutes les violations."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            print(f"Erreur d'encodage dans {path}: {e}", file=sys.stderr)
            return []

    blocks = extract_effect_blocks(text)
    violations: list[LintViolation] = []
    for block in blocks:
        violations.extend(check_block(block, db=db))
    return violations


if __name__ == "__main__":
    symbols_path = SUBMOD_ROOT / "docs" / "symbols.json"
    db = SymbolDB.load_or_none(symbols_path)
    if db is None:
        print(
            "Info : symbols.json absent — règles E01-E04 désactivées.\n"
            "       Générer avec : python tools/extract_symbols.py\n",
            file=sys.stderr,
        )

    def _lint_fn(path: Path) -> list[LintViolation]:
        return lint_file(path, db=db)

    sys.exit(make_linter_main(
        lint_fn=_lint_fn,
        default_path=Path("common/scripted_effects/"),
        label="effects",
        glob_pattern="*.txt",
        rule_prefix="E",
    ))
