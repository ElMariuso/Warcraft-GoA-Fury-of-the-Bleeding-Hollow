"""
_wiki_cleaning.py — Logique partagée de nettoyage des pages wiki MediaWiki (CK3).

Fournit le pipeline de nettoyage utilisé par condense_wiki_paradox.py et
condense_wiki_docs.py. Les appelants passent leurs propres listes de patterns
pour personnaliser le bruit filtré.
"""

from __future__ import annotations

import re

# Patterns de lignes à supprimer intégralement (bruit MediaWiki commun).
COMMON_LINE_NOISE: list[re.Pattern[str]] = [
    re.compile(r"Jump to navigation"),
    re.compile(r"Retrieved from"),
    re.compile(r"This article is \[timeless\]"),
    re.compile(r"This article has been \[verified\]"),
    re.compile(r"Please help improve this article"),
    re.compile(r"Please help with verifying"),
    re.compile(r"^\s*\|\s*Please help"),
    re.compile(r"\*\*\[Modding\]\(/Modding"),
    re.compile(r"\| \[Scripting\]\(/Scripting"),
    re.compile(r"edit source\]\(/index\.php"),
    re.compile(r"At least some were last verified"),
    re.compile(r"This article is for the PC version"),
]

# Titres de sections entières à supprimer (avec leur contenu).
COMMON_SECTION_NOISE: list[re.Pattern[str]] = [
    re.compile(r"^#{1,4} (Contents|See also|References|Categories|Related)\b"),
]

HEADING_EDIT_LINK = re.compile(r"\[\[edit\].*?\[edit source\].*?\]", re.DOTALL)
HEADING_EDIT_SIMPLE = re.compile(r"\[edit\]\(.*?\)")


def strip_edit_links(line: str) -> str:
    """Supprime les liens [[edit]...[edit source]...] des titres de section."""
    line = HEADING_EDIT_LINK.sub("", line)
    line = HEADING_EDIT_SIMPLE.sub("", line)
    return line.rstrip()


def is_noise_line(line: str, patterns: list[re.Pattern[str]]) -> bool:
    """Retourne True si la ligne correspond à un pattern de bruit."""
    return any(p.search(line) for p in patterns)


def remove_section_blocks(
    lines: list[str],
    section_patterns: list[re.Pattern[str]],
) -> list[str]:
    """Supprime les blocs de sections correspondant aux patterns donnés.

    Une section est supprimée depuis son titre jusqu'au prochain titre de
    niveau égal ou supérieur.
    """
    result: list[str] = []
    skip = False
    skip_level = 0

    for line in lines:
        heading_match = re.match(r"^(#{1,4}) ", line)

        if any(p.match(line) for p in section_patterns):
            skip = True
            skip_level = len(heading_match.group(1)) if heading_match else 2
            continue

        if skip and heading_match:
            current_level = len(heading_match.group(1))
            if current_level <= skip_level:
                skip = False

        if not skip:
            result.append(line)

    return result


def deduplicate_blank_lines(lines: list[str], max_consecutive: int = 2) -> list[str]:
    """Réduit les lignes vides consécutives à max_consecutive."""
    result: list[str] = []
    blank_count = 0
    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= max_consecutive:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)
    return result


def clean_page(
    raw: str,
    line_patterns: list[re.Pattern[str]] | None = None,
    section_patterns: list[re.Pattern[str]] | None = None,
) -> str:
    """Pipeline complet de nettoyage d'une page wiki MediaWiki.

    Étapes :
    1. Supprime la ligne `> Source : …`
    2. Nettoie les liens [edit] dans les titres
    3. Supprime les lignes de bruit
    4. Supprime les blocs de sections bruyantes
    5. Réduit les blancs consécutifs à 2
    """
    if line_patterns is None:
        line_patterns = COMMON_LINE_NOISE
    if section_patterns is None:
        section_patterns = COMMON_SECTION_NOISE

    lines = raw.splitlines()
    lines = [ln for ln in lines if not ln.startswith("> Source :")]
    lines = [strip_edit_links(ln) if ln.startswith("#") else ln for ln in lines]
    lines = [ln for ln in lines if not is_noise_line(ln, line_patterns)]
    lines = remove_section_blocks(lines, section_patterns)
    lines = deduplicate_blank_lines(lines)
    return "\n".join(lines).strip()
