"""
condense_wiki_paradox.py — Condense les pages wiki CK3 en référence thématique pour IA.

Sélectionne ~30 pages pertinentes, supprime le bruit MediaWiki, et génère 7 fichiers
thématiques dans docs/wiki-paradox/ — découpés par axe technique pour référence rapide.

Usage:
    python tools/condense_wiki_paradox.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SUBMOD_ROOT
from ui import dim, error, info, success, warn
from wiki_tools._wiki_cleaning import (
    COMMON_LINE_NOISE,
    COMMON_SECTION_NOISE,
    deduplicate_blank_lines,
    strip_edit_links,
)
from wiki_tools._wiki_cleaning import clean_page as _clean_page
from wiki_tools._wiki_cleaning import is_noise_line as _is_noise_line
from wiki_tools._wiki_cleaning import remove_section_blocks as _remove_section_blocks

WIKI_DIR = os.path.join(SUBMOD_ROOT, "docs", "wiki")
OUTPUT_DIR = os.path.join(SUBMOD_ROOT, "docs", "wiki-paradox")

# Mapping thématique : clé → liste de (fichier_wiki, titre_section)
THEMES: dict[str, list[tuple[str, str]]] = {
    "01_scripting_core": [
        ("Scripting.md", "Scripting — syntaxe et concepts"),
        ("Data_types.md", "Data types"),
        ("Variables.md", "Variables"),
        ("Lists.md", "Lists"),
        ("Scopes.md", "Scopes — vue d'ensemble"),
    ],
    "02_triggers_effects": [
        ("Triggers.md", "Triggers — vue d'ensemble"),
        ("Effects.md", "Effects — vue d'ensemble"),
        ("Scripted_effects.md", "Scripted effects"),
        ("Modifiers.md", "Modifiers"),
        ("Weight_modifier.md", "Weight modifier"),
    ],
    "03_events_decisions": [
        ("Event_modding.md", "Events"),
        ("Story_cycles_modding.md", "Story cycles"),
        ("Decisions_modding.md", "Decisions"),
        ("Interactions_modding.md", "Interactions"),
    ],
    "04_characters_history": [
        ("Characters_modding.md", "Characters"),
        ("History_modding.md", "History"),
        ("Title_modding.md", "Titles"),
        ("Dynasties_modding.md", "Dynasties"),
        ("Governments_modding.md", "Governments"),
    ],
    "05_culture_religion_traits": [
        ("Culture_modding.md", "Cultures"),
        ("Religions_modding.md", "Religions"),
        ("Trait_modding.md", "Traits"),
        ("Struggle_modding.md", "Struggles"),
    ],
    "06_localization": [
        ("Localization.md", "Localization"),
        ("Flavorization.md", "Flavorization"),
    ],
    "07_mod_structure_debug": [
        ("Modding.md", "Modding overview"),
        ("Mod_structure.md", "Mod structure"),
        ("Defines.md", "Defines"),
        ("Console_commands.md", "Console commands"),
        ("Mod_troubleshooting.md", "Troubleshooting"),
    ],
}

_LINE_NOISE = COMMON_LINE_NOISE
_SECTION_NOISE = COMMON_SECTION_NOISE


def is_noise_line(line: str) -> bool:
    """Retourne True si la ligne est du bruit MediaWiki à supprimer."""
    return _is_noise_line(line, _LINE_NOISE)


def remove_section_blocks(lines: list[str]) -> list[str]:
    """Supprime les blocs de sections bruyantes (Contents, See also, etc.)."""
    return _remove_section_blocks(lines, _SECTION_NOISE)


def clean_page(raw: str) -> str:
    """Applique le pipeline complet de nettoyage sur le contenu brut d'une page wiki."""
    return _clean_page(raw, _LINE_NOISE, _SECTION_NOISE)


def read_wiki_file(path: str) -> str:
    """Lit un fichier wiki. Retourne '' si le fichier n'existe pas."""
    if not os.path.isfile(path):
        return ""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as exc:
        warn(f"Lecture impossible ({path}): {exc}")
        return ""


def build_theme(
    theme_key: str,
    sources: list[tuple[str, str]],
    wiki_dir: str,
) -> tuple[list[str], list[str], str]:
    """
    Construit le contenu d'un fichier thématique à partir de plusieurs pages wiki.

    Returns:
        (included, skipped, content) — listes des fichiers inclus/sautés + contenu formaté
    """
    included: list[str] = []
    skipped: list[str] = []
    source_names = [fname for fname, _ in sources]

    parts: list[str] = [
        f"# CK3 Modding — {theme_key}\n\n",
        "> Généré par `tools/condense_wiki_paradox.py`\n",
        f"> Sources : {', '.join(source_names)}\n\n",
        "---\n\n",
    ]

    for filename, section_title in sources:
        filepath = os.path.join(wiki_dir, filename)
        raw = read_wiki_file(filepath)

        if not raw:
            warn(f"  Manquant : {filename}")
            skipped.append(filename)
            continue

        cleaned = clean_page(raw)
        if len(cleaned) < 100:
            warn(f"  Vide après nettoyage : {filename}")
            skipped.append(filename)
            continue

        parts.append(f"## {section_title}\n\n")
        parts.append(cleaned)
        parts.append("\n\n---\n\n")
        included.append(filename)
        dim(f"    ✓ {filename} ({len(cleaned.splitlines())} lignes)")

    return included, skipped, "".join(parts)


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    info("Condensation des pages wiki en fichiers thématiques...")

    total_included = 0
    total_skipped: list[str] = []
    total_lines = 0

    for theme_key, sources in THEMES.items():
        info(f"  {theme_key}...")
        included, skipped, content = build_theme(theme_key, sources, WIKI_DIR)

        if not included:
            warn(f"  Aucune source trouvée pour {theme_key}, fichier non généré")
            total_skipped.extend(skipped)
            continue

        output_path = os.path.join(OUTPUT_DIR, f"{theme_key}.md")
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
        except OSError as exc:
            error(f"Écriture impossible ({output_path}): {exc}")
            sys.exit(1)

        line_count = len(content.splitlines())
        total_lines += line_count
        total_included += len(included)
        total_skipped.extend(skipped)
        dim(f"  → {theme_key}.md ({line_count} lignes, {len(included)} sources)")

    success(
        f"docs/wiki-paradox/ généré : {len(THEMES)} fichiers, "
        f"{total_included} sources, {total_lines} lignes totales"
    )
    if total_skipped:
        warn(f"Sources ignorées : {', '.join(total_skipped)}")


__all__ = [
    "THEMES",
    "clean_page",
    "deduplicate_blank_lines",
    "is_noise_line",
    "remove_section_blocks",
    "strip_edit_links",
    "build_theme",
    "read_wiki_file",
    "main",
]


if __name__ == "__main__":
    main()
