"""
condense_wiki_docs.py — Condense les pages wiki CK3 core en une référence développeur.

Sélectionne les pages de scripting essentielles, supprime le bruit MediaWiki (navboxes,
notices, "Retrieved from"), et fusionne en docs/ck3_modding_reference.md.

Usage:
    python tools/condense_wiki_docs.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SUBMOD_ROOT
from ui import dim, info, success, warn
from wiki_tools._wiki_cleaning import clean_page

WIKI_DIR = os.path.join(SUBMOD_ROOT, "docs", "wiki")
OUTPUT_FILE = os.path.join(SUBMOD_ROOT, "docs", "ck3_modding_reference.md")

# Pages incluses dans la référence, dans l'ordre logique pour un dev
CORE_PAGES: list[tuple[str, str]] = [
    ("Modding.md", "Vue d'ensemble du modding CK3"),
    ("Mod_structure.md", "Structure d'un mod"),
    ("Scripting.md", "Scripting — syntaxe et concepts"),
    ("Data_types.md", "Types de données"),
    ("Variables.md", "Variables"),
    ("Scopes.md", "Scopes — vue d'ensemble"),
    ("Scopes_list.md", "Scopes — liste complète"),
    ("Triggers.md", "Triggers — vue d'ensemble"),
    ("Triggers_list.md", "Triggers — liste complète"),
    ("Effects.md", "Effects — vue d'ensemble"),
    ("Effects_list.md", "Effects — liste complète"),
    ("Modifier_list.md", "Modifiers — liste complète"),
    ("Weight_modifier.md", "Weight modifier"),
    ("Scripted_effects.md", "Scripted effects"),
    ("Event_modding.md", "Event modding"),
    ("Story_cycles_modding.md", "Story cycles"),
    ("Decisions_modding.md", "Decisions modding"),
    ("Characters_modding.md", "Characters modding"),
    ("History_modding.md", "History modding"),
    ("Localization.md", "Localisation"),
    ("Flavorization.md", "Flavorization"),
    ("Trait_modding.md", "Traits modding"),
    ("Culture_modding.md", "Culture modding"),
    ("Religions_modding.md", "Religions modding"),
    ("Title_modding.md", "Titles modding"),
    ("Dynasties_modding.md", "Dynasties modding"),
    ("Console_commands.md", "Console commands"),
    ("Mod_troubleshooting.md", "Troubleshooting"),
]


def main() -> None:
    info("Condensation des pages wiki CK3 core...")

    sections: list[str] = [
        "# CK3 Modding — Référence Développeur\n",
        "> Généré depuis `docs/wiki/` (fetch_wiki_docs.py + condense_wiki_docs.py)\n",
        "> Couvre uniquement les pages de scripting core — sans les mods tiers.\n\n",
        "---\n\n",
        "## Table des matières\n",
    ]

    for _, title in CORE_PAGES:
        anchor = (
            title.lower()
            .replace(" ", "-")
            .replace("'", "")
            .replace("é", "e")
            .replace("è", "e")
        )
        sections.append(f"- [{title}](#{anchor})\n")
    sections.append("\n---\n\n")

    included: list[str] = []
    skipped: list[str] = []

    for filename, section_title in CORE_PAGES:
        filepath = os.path.join(WIKI_DIR, filename)
        if not os.path.isfile(filepath):
            warn(f"Manquant : {filename}")
            skipped.append(filename)
            continue

        with open(filepath, encoding="utf-8") as f:
            raw = f.read()

        cleaned = clean_page(raw)
        if len(cleaned) < 50:
            warn(f"Contenu vide après nettoyage : {filename}")
            skipped.append(filename)
            continue

        sections.append(f"## {section_title}\n\n")
        sections.append(cleaned)
        sections.append("\n\n---\n\n")
        included.append(filename)
        dim(f"  ✓ {filename} ({len(cleaned.splitlines())} lignes)")

    output = "".join(sections)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(output)

    total_lines = len(output.splitlines())
    success(
        f"Référence générée : docs/ck3_modding_reference.md "
        f"({total_lines} lignes, {len(included)} sections)"
    )
    if skipped:
        warn(f"Pages ignorées : {', '.join(skipped)}")


if __name__ == "__main__":
    main()
