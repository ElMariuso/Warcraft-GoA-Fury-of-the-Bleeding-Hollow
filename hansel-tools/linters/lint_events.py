#!/usr/bin/env python3
"""Linter pour les fichiers d'events CK3 (.txt).

Valide chaque event contre les règles CK3 définies dans rules.py,
extraites de docs/wiki-paradox/ et du parent mod (via symbol_db.py).

Usage:
    python tools/lint_events.py events/story_cycles/
    python tools/lint_events.py events/story_cycles/wc_foo_events.txt
    python tools/lint_events.py --rules          # liste les règles disponibles
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))         # hansel-tools/linters/
sys.path.insert(0, str(Path(__file__).parent.parent))  # hansel-tools/
from config import SUBMOD_ROOT
from rules import Severity
from symbol_db import SymbolDB
from _jomini import EVENT_HEADER, extract_blocks
from _linter_runner import check_symbol_references, make_linter_main


_EVENT_RULE_MAP = {
    "char": "R09",
    "title": "R10",
    "modifier": "R11",
    "effect": "R12",
}


@dataclass
class EventBlock:
    """Un bloc d'event extrait d'un fichier .txt CK3."""

    id: str          # ex: "wc_horde_invasion.1004"
    raw: str         # contenu brut du bloc (entre les accolades)
    line_start: int  # numéro de ligne dans le fichier source


@dataclass
class LintViolation:
    """Une violation détectée dans un bloc d'event."""

    rule_id: str
    event_id: str
    severity: Severity
    message: str
    line: int = 0  # ligne approximative dans le fichier source


def _is_hidden(raw: str) -> bool:
    return bool(re.search(r"\bhidden\s*=\s*yes\b", raw))


def _has_field(raw: str, field: str) -> bool:
    return bool(re.search(rf"\b{re.escape(field)}\s*=", raw))


def _has_trigger(raw: str) -> bool:
    return bool(re.search(r"\btrigger\s*=\s*\{", raw))


def _has_mean_time(raw: str) -> bool:
    return bool(re.search(r"\bmean_time_to_happen\s*=\s*\{", raw))


def _count_options(raw: str) -> int:
    return len(re.findall(r"\boption\s*=\s*\{", raw))


def _count_ai_chance(raw: str) -> int:
    return len(re.findall(r"\bai_chance\s*=\s*\{", raw))


def _has_portrait(raw: str) -> bool:
    return bool(re.search(r"\b(?:left_portrait|right_portrait|lower_right_portrait)\s*=", raw))


def extract_event_blocks(text: str) -> list[EventBlock]:
    """Extrait les blocs d'events d'un fichier .txt CK3.

    Utilise la fonction partagée extract_blocks() avec EVENT_HEADER.
    Wrapper fourni pour la compatibilité avec les tests existants.
    """
    raw_blocks = extract_blocks(text, EVENT_HEADER)
    return [
        EventBlock(id=b.id, raw=b.raw, line_start=b.line_start)
        for b in raw_blocks
    ]


def check_block(block: EventBlock, db: SymbolDB | None = None) -> list[LintViolation]:
    """Applique les règles R01–R12 à un bloc d'event.

    Si db est None (symbols.json absent), les règles R09-R12 sont silencieusement ignorées.
    """
    violations: list[LintViolation] = []
    raw = block.raw
    eid = block.id
    line = block.line_start

    hidden = _is_hidden(raw)

    if not hidden and not _has_field(raw, "content_source"):
        violations.append(LintViolation(
            rule_id="R01",
            event_id=eid,
            severity="ERROR",
            message="content_source = dlc_GOA manquant (event visible)",
            line=line,
        ))

    n_options = _count_options(raw)
    n_ai = _count_ai_chance(raw)
    if n_options > 0 and n_ai < n_options:
        missing = n_options - n_ai
        violations.append(LintViolation(
            rule_id="R02",
            event_id=eid,
            severity="ERROR",
            message=f"{missing} option(s) sans ai_chance sur {n_options}",
            line=line,
        ))

    if not hidden:
        if not _has_field(raw, "title"):
            violations.append(LintViolation(
                rule_id="R04",
                event_id=eid,
                severity="ERROR",
                message="title manquant sur un event visible",
                line=line,
            ))
        if not _has_field(raw, "desc"):
            violations.append(LintViolation(
                rule_id="R04",
                event_id=eid,
                severity="ERROR",
                message="desc manquant sur un event visible",
                line=line,
            ))

    if _has_mean_time(raw) and not _has_trigger(raw):
        violations.append(LintViolation(
            rule_id="R05",
            event_id=eid,
            severity="WARN",
            message="mean_time_to_happen présent mais aucun trigger — event jamais déclenché",
            line=line,
        ))

    if hidden and _has_portrait(raw):
        violations.append(LintViolation(
            rule_id="R06",
            event_id=eid,
            severity="WARN",
            message="Portrait défini sur un event hidden = yes",
            line=line,
        ))

    try:
        parts = eid.rsplit(".", 1)
        if len(parts) == 2:
            num = int(parts[1])
            if 1 <= num <= 999 and not hidden:
                violations.append(LintViolation(
                    rule_id="R08",
                    event_id=eid,
                    severity="INFO",
                    message=f"ID {num} dans la plage 1–999 (réservée setup/hidden)",
                    line=line,
                ))
    except ValueError:
        pass

    if db is not None:
        def _make_v(rule_id: str, severity: str, message: str) -> LintViolation:
            return LintViolation(
                rule_id=rule_id,
                event_id=eid,
                severity=severity,  # type: ignore[arg-type]
                message=message,
                line=line,
            )

        violations.extend(
            check_symbol_references(raw, db, _EVENT_RULE_MAP, _make_v)
        )

    return violations


def lint_file(path: Path, db: SymbolDB | None = None) -> list[LintViolation]:
    """Lint un fichier .txt CK3 et retourne toutes les violations."""
    try:
        text = path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            print(f"Erreur d'encodage dans {path}: {e}", file=sys.stderr)
            return []

    blocks = extract_event_blocks(text)
    violations: list[LintViolation] = []
    for block in blocks:
        violations.extend(check_block(block, db=db))
    return violations


if __name__ == "__main__":
    symbols_path = SUBMOD_ROOT / "docs" / "symbols.json"
    db = SymbolDB.load_or_none(symbols_path)
    if db is None:
        print(
            "Info : symbols.json absent — règles R09-R12 désactivées.\n"
            "       Générer avec : python tools/extract_symbols.py\n",
            file=sys.stderr,
        )

    def _lint_fn(path: Path) -> list[LintViolation]:
        return lint_file(path, db=db)

    sys.exit(make_linter_main(
        lint_fn=_lint_fn,
        default_path=Path("events/story_cycles/"),
        label="events",
        glob_pattern="*.txt",
        rule_prefix="R",
    ))
