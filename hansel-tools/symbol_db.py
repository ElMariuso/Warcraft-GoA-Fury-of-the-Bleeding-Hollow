#!/usr/bin/env python3
"""Gestionnaire de symboles CK3 depuis symbols.json.

Fournit une API de query pour vérifier l'existence de caractères, titres, etc.
Chargé dynamiquement par le linter; gracieux si symbols.json n'existe pas.
"""

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import SUBMOD_ROOT

# Regex pour extraire les noms de scripted_effects/triggers locaux (sous-mod)
_LOCAL_EFFECT_PATTERN = re.compile(r"^([a-z]\w+_effect)\s*=\s*\{", re.MULTILINE)
_LOCAL_TRIGGER_PATTERN = re.compile(r"^([a-z]\w+_trigger)\s*=\s*\{", re.MULTILINE)


def _scan_local_effects(submod_root: Path) -> tuple[frozenset[str], frozenset[str]]:
    """Scanne common/scripted_effects/ et common/scripted_triggers/ du sous-mod."""
    effects: set[str] = set()
    triggers: set[str] = set()

    effects_dir = submod_root / "common" / "scripted_effects"
    if effects_dir.exists():
        for f in effects_dir.rglob("*.txt"):
            text = f.read_text(encoding="utf-8-sig", errors="replace")
            for m in _LOCAL_EFFECT_PATTERN.finditer(text):
                effects.add(m.group(1))

    triggers_dir = submod_root / "common" / "scripted_triggers"
    if triggers_dir.exists():
        for f in triggers_dir.rglob("*.txt"):
            text = f.read_text(encoding="utf-8-sig", errors="replace")
            for m in _LOCAL_TRIGGER_PATTERN.finditer(text):
                triggers.add(m.group(1))

    return frozenset(effects), frozenset(triggers)


@dataclass
class SymbolDB:
    """Base de données immutable de symboles CK3."""

    characters: frozenset[int]
    titles: frozenset[str]
    modifiers: frozenset[str]
    scripted_effects: frozenset[str]
    scripted_triggers: frozenset[str]

    @classmethod
    def load(cls, path: Path) -> "SymbolDB":
        """Charge symbols.json et fusionne les symboles locaux du sous-mod.

        Lève OSError ou json.JSONDecodeError si absent ou invalide.
        """
        data: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))

        chars_data = data.get("characters")
        titles_data = data.get("titles")
        modifiers_data = data.get("modifiers")
        effects_data = data.get("scripted_effects")
        triggers_data = data.get("scripted_triggers")

        parent_effects = frozenset(
            str(x) for x in (effects_data if isinstance(effects_data, list) else [])
            if isinstance(x, str)
        )
        parent_triggers = frozenset(
            str(x) for x in (triggers_data if isinstance(triggers_data, list) else [])
            if isinstance(x, str)
        )

        # Fusionne avec les effets/triggers définis dans ce sous-mod
        local_effects, local_triggers = _scan_local_effects(SUBMOD_ROOT)

        return cls(
            characters=frozenset(
                int(x) for x in (chars_data if isinstance(chars_data, list) else [])
                if isinstance(x, int)
            ),
            titles=frozenset(
                str(x) for x in (titles_data if isinstance(titles_data, list) else [])
                if isinstance(x, str)
            ),
            modifiers=frozenset(
                str(x) for x in (modifiers_data if isinstance(modifiers_data, list) else [])
                if isinstance(x, str)
            ),
            scripted_effects=parent_effects | local_effects,
            scripted_triggers=parent_triggers | local_triggers,
        )

    @classmethod
    def load_or_none(cls, path: Path) -> "SymbolDB | None":
        """Charge symbols.json. Retourne None si absent; propage autres erreurs."""
        if not path.exists():
            return None

        try:
            return cls.load(path)
        except (OSError, json.JSONDecodeError) as e:
            print(
                f"Error: Failed to load {path}: {e}",
                file=sys.stderr,
            )
            return None

    def has_character(self, char_id: int) -> bool:
        """Vérifie si un caractère existe."""
        return char_id in self.characters

    def has_title(self, title_key: str) -> bool:
        """Vérifie si un titre existe."""
        return title_key in self.titles

    def has_modifier(self, modifier_name: str) -> bool:
        """Vérifie si un modifieur existe."""
        return modifier_name in self.modifiers

    def has_effect(self, effect_name: str) -> bool:
        """Vérifie si un effet existe."""
        return effect_name in self.scripted_effects

    def has_trigger(self, trigger_name: str) -> bool:
        """Vérifie si un trigger existe."""
        return trigger_name in self.scripted_triggers
