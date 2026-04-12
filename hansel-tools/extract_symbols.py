#!/usr/bin/env python3
"""Extracteur de symboles CK3 depuis le mod parent.

Scanne les fichiers .txt du parent mod et génère docs/symbols.json
avec tous les caractères, titres, modifieurs, effects et triggers.

Usage:
    python tools/extract_symbols.py
    python tools/extract_symbols.py --output docs/symbols.json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import SUBMOD_ROOT, PARENT_MOD_ROOT


# ─── Types ─────────────────────────────────────────────────────────────────────

@dataclass
class ExtractionStats:
    """Statistiques d'extraction."""

    characters: int
    titles: int
    modifiers: int
    scripted_effects: int
    scripted_triggers: int


# ─── Patterns Jomini ────────────────────────────────────────────────────────────

# Characters: numéro au début de ligne
_CHAR_PATTERN = re.compile(r"^\s*(\d+)\s*=\s*\{", re.MULTILINE)

# Titles: clé composée d'une lettre (e/k/d/c/b) + underscore + alphanumérique
_TITLE_PATTERN = re.compile(r"\b([eEkKdDcCbB]_[a-z0-9_]+)\s*=\s*\{")

# Modifiers: clé terminant par "_modifier"
_MODIFIER_PATTERN = re.compile(r"^(\w+_modifier)\s*=\s*\{", re.MULTILINE)

# Scripted effects: clé terminant par "_effect"
# Définition dans common/scripted_effects/ (nom seul en début de ligne)
_EFFECT_PATTERN = re.compile(r"^(\w+_effect)\s*=\s*\{", re.MULTILINE)
# Définition inline dans events/ : `scripted_effect name = {`
_INLINE_EFFECT_PATTERN = re.compile(r"^\s*scripted_effect\s+(\w+_effect)\s*=\s*\{", re.MULTILINE)

# Scripted triggers: clé terminant par "_trigger"
_TRIGGER_PATTERN = re.compile(r"^(\w+_trigger)\s*=\s*\{", re.MULTILINE)


# ─── Extracteurs ───────────────────────────────────────────────────────────────

def extract_characters(root: Path) -> list[int]:
    """Extrait tous les IDs de caractères depuis history/characters/*.txt."""
    chars: set[int] = set()
    char_dir = root / "history" / "characters"

    if not char_dir.exists():
        return []

    for txt_file in char_dir.rglob("*.txt"):
        try:
            content = txt_file.read_text(encoding="utf-8-sig", errors="replace")
            for match in _CHAR_PATTERN.finditer(content):
                raw_id = match.group(1)
                try:
                    char_id = int(raw_id)
                    chars.add(char_id)
                except ValueError:
                    warnings.warn(
                        f"{txt_file}: could not parse character id {raw_id!r}",
                        stacklevel=2,
                    )
        except (OSError, UnicodeDecodeError) as e:
            print(f"Warning: Failed to read {txt_file}: {e}", file=sys.stderr)

    return sorted(chars)


def extract_titles(root: Path) -> list[str]:
    """Extrait tous les clés de titres depuis common/landed_titles/**/*.txt."""
    titles: set[str] = set()
    titles_dir = root / "common" / "landed_titles"

    if not titles_dir.exists():
        return []

    for txt_file in titles_dir.rglob("*.txt"):
        try:
            content = txt_file.read_text(encoding="utf-8-sig", errors="replace")
            for match in _TITLE_PATTERN.finditer(content):
                title_key = match.group(1)
                titles.add(title_key)
        except (OSError, UnicodeDecodeError) as e:
            print(f"Warning: Failed to read {txt_file}: {e}", file=sys.stderr)

    return sorted(titles)


def extract_modifiers(root: Path) -> list[str]:
    """Extrait tous les noms de modifieurs depuis common/modifiers/*.txt."""
    modifiers: set[str] = set()
    modifiers_dir = root / "common" / "modifiers"

    if not modifiers_dir.exists():
        return []

    for txt_file in modifiers_dir.rglob("*.txt"):
        try:
            content = txt_file.read_text(encoding="utf-8-sig", errors="replace")
            for match in _MODIFIER_PATTERN.finditer(content):
                modifier_name = match.group(1)
                modifiers.add(modifier_name)
        except (OSError, UnicodeDecodeError) as e:
            print(f"Warning: Failed to read {txt_file}: {e}", file=sys.stderr)

    return sorted(modifiers)


def extract_scripted_effects(root: Path) -> list[str]:
    """Extrait tous les noms d'effets depuis common/scripted_effects/ et events/."""
    effects: set[str] = set()

    # 1. common/scripted_effects/ (définitions standalone)
    effects_dir = root / "common" / "scripted_effects"
    if effects_dir.exists():
        for txt_file in effects_dir.rglob("*.txt"):
            try:
                content = txt_file.read_text(encoding="utf-8-sig", errors="replace")
                for match in _EFFECT_PATTERN.finditer(content):
                    effects.add(match.group(1))
            except (OSError, UnicodeDecodeError) as e:
                print(f"Warning: Failed to read {txt_file}: {e}", file=sys.stderr)

    # 2. events/ (définitions inline `scripted_effect name = {`)
    events_dir = root / "events"
    if events_dir.exists():
        for txt_file in events_dir.rglob("*.txt"):
            try:
                content = txt_file.read_text(encoding="utf-8-sig", errors="replace")
                for match in _INLINE_EFFECT_PATTERN.finditer(content):
                    effects.add(match.group(1))
            except (OSError, UnicodeDecodeError) as e:
                print(f"Warning: Failed to read {txt_file}: {e}", file=sys.stderr)

    return sorted(effects)


def extract_scripted_triggers(root: Path) -> list[str]:
    """Extrait tous les noms de triggers depuis common/scripted_triggers/*.txt."""
    triggers: set[str] = set()
    triggers_dir = root / "common" / "scripted_triggers"

    if not triggers_dir.exists():
        return []

    for txt_file in triggers_dir.rglob("*.txt"):
        try:
            content = txt_file.read_text(encoding="utf-8-sig", errors="replace")
            for match in _TRIGGER_PATTERN.finditer(content):
                trigger_name = match.group(1)
                triggers.add(trigger_name)
        except (OSError, UnicodeDecodeError) as e:
            print(f"Warning: Failed to read {txt_file}: {e}", file=sys.stderr)

    return sorted(triggers)


def generate_symbols_json(output_path: Path) -> ExtractionStats:
    """Génère le fichier symbols.json depuis le parent mod."""
    print(f"Extracting symbols from {PARENT_MOD_ROOT}...")

    chars = extract_characters(PARENT_MOD_ROOT)
    titles = extract_titles(PARENT_MOD_ROOT)
    modifiers = extract_modifiers(PARENT_MOD_ROOT)
    effects = extract_scripted_effects(PARENT_MOD_ROOT)
    triggers = extract_scripted_triggers(PARENT_MOD_ROOT)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    data: dict[str, object] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "characters": chars,
        "titles": titles,
        "modifiers": modifiers,
        "scripted_effects": effects,
        "scripted_triggers": triggers,
    }

    try:
        output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except (OSError, json.JSONDecodeError) as e:
        print(f"Error: Failed to write {output_path}: {e}", file=sys.stderr)
        sys.exit(1)

    stats = ExtractionStats(
        characters=len(chars),
        titles=len(titles),
        modifiers=len(modifiers),
        scripted_effects=len(effects),
        scripted_triggers=len(triggers),
    )

    return stats


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Extract CK3 symbols from parent mod")
    parser.add_argument(
        "--output",
        default=str(SUBMOD_ROOT / "docs" / "symbols.json"),
        help="Output path for symbols.json"
    )
    args = parser.parse_args()
    output_path = Path(args.output)

    stats = generate_symbols_json(output_path)

    print(f"\nSymbols extracted to {output_path}:")
    print(f"  Characters:        {stats.characters}")
    print(f"  Titles:            {stats.titles}")
    print(f"  Modifiers:         {stats.modifiers}")
    print(f"  Scripted effects:  {stats.scripted_effects}")
    print(f"  Scripted triggers: {stats.scripted_triggers}")


if __name__ == "__main__":
    main()
