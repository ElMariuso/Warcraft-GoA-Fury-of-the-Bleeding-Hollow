#!/usr/bin/env python3
"""Shared CLI runner for CK3 linters (lint_events, lint_effects, lint_localization).

Each linter calls run_linter() from its __main__ block — no duplicated
argparse / glob / print / stats logic.
"""
from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, Protocol

from _jomini import (
    CHAR_REF,
    CK3_BUILTIN_EFFECTS,
    EFFECT_CALL,
    MODIFIER_NAME,
    TITLE_REF,
)

if TYPE_CHECKING:
    from symbol_db import SymbolDB


class Violation(Protocol):
    """Structural type for lint violations — matches LintViolation in each linter."""

    rule_id: str
    severity: str
    message: str


LintFn = Callable[[Path], list[Any]]


def run_linter(
    argv: list[str],
    default_path: Path,
    lint_fn: LintFn,
    all_rules: list[Any],
    label: str,
    glob_pattern: str,
    rule_prefix: str,
) -> int:
    """Run a linter from CLI args. Returns exit code (0 = clean, 1 = violations).

    argv          — sys.argv[1:] from the caller
    default_path  — default directory to lint if no path given
    lint_fn       — function(Path) -> list[Violation]
    all_rules     — list of LintRule objects with .id, .severity, .description, .doc_ref
    label         — human label e.g. "events", "localization", "effects"
    glob_pattern  — e.g. "**/*.txt" or "**/*.yml"
    rule_prefix   — e.g. "R", "L", "E" to filter rules for --rules output
    """
    # Handle --rules flag
    if not argv or "--rules" in argv:
        _print_rules(all_rules, rule_prefix)
        if not argv:
            print(
                f"Usage: python tools/lint_{label.lower()}.py <fichier|dossier/>",
                file=sys.stderr,
            )
            sys.exit(1)
        return 0

    # Find the path argument (first non-flag argument)
    target = Path(argv[0])
    if not target.exists():
        print(f"Erreur : introuvable — {target}", file=sys.stderr)
        sys.exit(1)

    # Collect files: single file or glob directory
    if target.is_dir():
        files = sorted(target.rglob(glob_pattern))
    else:
        files = [target]

    if not files:
        print(f"Aucun fichier {glob_pattern} trouvé.", file=sys.stderr)
        sys.exit(1)

    # Lint all files and collect violations
    all_violations: list[Any] = []
    for f in files:
        violations = lint_fn(f)
        if violations:
            print(f"\n{f.name}")
            for v in sorted(violations, key=_violation_sort_key(label)):
                print(_format_violation(v))
        all_violations.extend(violations)

    # Count severity levels
    errors = sum(1 for v in all_violations if v.severity == "ERROR")
    warns = sum(1 for v in all_violations if v.severity == "WARN")
    infos = sum(1 for v in all_violations if v.severity == "INFO")

    # Print summary (French, with label capitalized)
    label_cap = label.capitalize()
    print(
        f"\n─── {label_cap} : {errors} error(s), {warns} warning(s), {infos} info(s) ───"
    )

    # Exit with error code if violations found
    if errors > 0:
        sys.exit(1)

    return 0


def make_linter_main(
    lint_fn: LintFn,
    default_path: Path,
    label: str,
    glob_pattern: str,
    rule_prefix: str,
    description: str = "",
) -> int:
    """Entry point wrapper for a linter's __main__ block.

    Encapsulates the boilerplate common to all three linters: read sys.argv,
    import ALL_RULES, and invoke run_linter. The caller must have already
    inserted hansel-tools/ into sys.path before importing this module.

    description — optional human-facing label (currently unused; kept for
                  signature stability with future --help output)
    """
    from rules import ALL_RULES  # noqa: PLC0415 — lazy import, sys.path set by caller

    return run_linter(
        sys.argv[1:],
        default_path=default_path,
        lint_fn=lint_fn,
        all_rules=ALL_RULES,
        label=label,
        glob_pattern=glob_pattern,
        rule_prefix=rule_prefix,
    )


def check_symbol_references(
    block_raw: str,
    db: SymbolDB,
    rule_map: dict[str, str],
    make_violation: Callable[[str, str, str], Any],
) -> list[Any]:
    """Cross-check CHAR_REF / TITLE_REF / MODIFIER_NAME / EFFECT_CALL against SymbolDB.

    Shared between lint_events (R09–R12) and lint_effects (E01–E04). The caller
    supplies:
      - rule_map: mapping of {"char", "title", "modifier", "effect"} → rule ID
      - make_violation(rule_id, severity, message) → LintViolation (event_id/
        effect_name/line injected by the caller's closure)

    Returns a flat list of LintViolation objects (caller's own type).
    """
    violations: list[Any] = []

    for m in CHAR_REF.finditer(block_raw):
        char_id = int(m.group(1))
        if not db.has_character(char_id):
            violations.append(make_violation(
                rule_map["char"],
                "ERROR",
                f"character:{char_id} introuvable dans le parent mod",
            ))

    for m in TITLE_REF.finditer(block_raw):
        title_key = m.group(1)
        if not db.has_title(title_key):
            violations.append(make_violation(
                rule_map["title"],
                "ERROR",
                f"title:{title_key} introuvable dans le parent mod",
            ))

    seen_modifiers: set[str] = set()
    for m in MODIFIER_NAME.finditer(block_raw):
        name = m.group(1) or m.group(2)
        if name and name not in seen_modifiers and not db.has_modifier(name):
            seen_modifiers.add(name)
            violations.append(make_violation(
                rule_map["modifier"],
                "WARN",
                f"modifier '{name}' introuvable dans le parent mod",
            ))

    seen_effects: set[str] = set()
    for m in EFFECT_CALL.finditer(block_raw):
        name = m.group(1)
        if name in CK3_BUILTIN_EFFECTS:
            continue
        if name not in seen_effects and not db.has_effect(name):
            seen_effects.add(name)
            violations.append(make_violation(
                rule_map["effect"],
                "WARN",
                f"scripted effect '{name}' introuvable dans le parent mod",
            ))

    return violations


def _print_rules(all_rules: list[Any], rule_prefix: str) -> None:
    """Print rules filtered by rule_prefix (e.g., 'L' for localization rules)."""
    filtered_rules = [r for r in all_rules if r.id.startswith(rule_prefix)]
    print(f"Règles disponibles ({rule_prefix}) :\n")
    for rule in filtered_rules:
        print(f"  [{rule.severity:5}] {rule.id} — {rule.description}")
        print(f"         Réf : {rule.doc_ref}")
    print()


def _violation_sort_key(label: str) -> Callable[[Any], tuple[str, Any]]:
    """Return sort key function based on linter type.

    - events: sort by (severity, event_id)
    - localization: sort by (severity, line)
    - effects: sort by (severity, effect_id) [generic fallback]
    """
    if label.lower() == "localization":
        return lambda v: (v.severity, v.line if hasattr(v, "line") else 0)
    elif label.lower() == "events":
        return lambda v: (v.severity, v.event_id if hasattr(v, "event_id") else "")
    else:
        # Generic: try effect_id, fall back to id or empty string
        return lambda v: (
            v.severity,
            getattr(v, "effect_id", getattr(v, "id", "")),
        )


def _format_violation(v: Any) -> str:
    """Format a violation for console output.

    Infers format based on violation attributes (event_id, file, line, etc).
    """
    # Localization format: file:line
    if hasattr(v, "file"):
        loc = f":{v.line}" if hasattr(v, "line") and v.line else ""
        return f"  [{v.severity:5}] {v.file}{loc} — {v.message} ({v.rule_id})"

    # Events format: event_id
    if hasattr(v, "event_id"):
        return f"  [{v.severity:5}] {v.event_id} — {v.message} ({v.rule_id})"

    # Generic fallback: id or empty
    label = getattr(v, "effect_id", getattr(v, "id", ""))
    return f"  [{v.severity:5}] {label} — {v.message} ({v.rule_id})"
