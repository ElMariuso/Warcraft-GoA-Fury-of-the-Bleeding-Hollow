"""hansel-tools/doc_search.py — Recherche par mots-clés dans docs/wiki-paradox/."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SearchResult:
    """Un résultat de recherche dans la documentation."""

    file: str         # basename du fichier source (ex: "03_events_decisions.md")
    line: int         # numéro de ligne (1-based)
    excerpt: str      # ligne correspondante nettoyée (sans bruit Markdown)
    score: int        # nombre de mots-clés trouvés dans cette ligne
    section: str | None = None  # heading ## le plus proche au-dessus du match


_NAVBOX_RE = re.compile(r"^\s*\w[\w\s]+\s*\|\s*\[")


def _is_navbox_line(line: str) -> bool:
    r"""Détecte les lignes de navbox wiki.

    Les fichiers wiki/ générés par html2text ont des navboxes du type :
        Scripting  |  [AI](/AI_modding) \u{2022} [Bookmarks](/Bookmarks_modding) ...
        Documentation  |  [Scripting](/Scripting) \u{2022} [Scopes](/Scopes) ...
        ---|---

    Ces lignes apparaissent dans chaque fichier et polluent les scores.
    Pattern : "Mot(s) | [lien" en début de ligne.
    """
    if line.strip() == "---|---":
        return True
    return bool(_NAVBOX_RE.match(line))


def _tokenize(text: str) -> list[str]:
    """Découpe un texte en tokens lowercase, en retirant la ponctuation."""
    return [t.lower() for t in re.split(r"[\s,;:()\[\]]+", text) if t]


def clean_excerpt(raw: str) -> str:
    """Retire le bruit Markdown/MediaWiki d'une ligne pour affichage terminal.

    - [text](url) → text
    - [[Page|display]] → display  (liens MediaWiki)
    - leading * ou - de liste → supprimé
    - leading \\t → supprimé
    - espaces multiples → un seul
    """
    text = raw.strip()
    # Liens Markdown : [texte](url) → texte
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    # Liens MediaWiki : [[Page|display]] → display, [[Page]] → Page
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    # Bullets de liste en début de ligne
    text = re.sub(r'^[*\-]\s+', '', text)
    # Tabulation initiale
    text = text.lstrip('\t')
    # Espaces multiples
    text = re.sub(r'  +', ' ', text)
    # Backslash-escapes Markdown : \- → -, \* → *, \_ → _, \` → `
    text = re.sub(r'\\([*_`\-])', r'\1', text)
    # Backticks inline : `texte` → texte
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text.strip() or raw.strip()


def _clean_heading(raw: str) -> str:
    """Supprime les liens d'édition wiki des titres de section.

    Les pages issues de html2text produisent des headings du type :
        Events[[edit](/url) | [edit source](/url)]
    On veut récupérer seulement la partie textuelle ("Events").
    """
    # Stratégie : trouver le premier [ d'édition et couper tout ce qui suit
    # Pattern : [[edit] ou [\\[edit] ou [ | [edit
    text = re.sub(r'\[\[?edit.*$', '', raw, flags=re.IGNORECASE)
    # Liens Markdown résiduels : [text](url) → text
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    # Parenthèses orphelines résiduelles (fragments d'URL)
    text = re.sub(r'\([^)]*\)\]?', '', text)
    return text.strip()


def _build_heading_index(lines: list[str]) -> list[tuple[int, str]]:
    """Retourne la liste (lineno, title) des headings Markdown dans le fichier."""
    headings: list[tuple[int, str]] = []
    for i, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith('#'):
            title = _clean_heading(re.sub(r'^#+\s*', '', stripped))
            if title:
                headings.append((i, title))
    return headings


def _nearest_section(lineno: int, headings: list[tuple[int, str]]) -> str | None:
    """Retourne le titre du heading le plus proche au-dessus de lineno."""
    result: str | None = None
    for hline, title in headings:
        if hline <= lineno:
            result = title
        else:
            break
    return result


def search_docs(
    query: str,
    docs_dir: Path,
    max_results: int = 20,
    allowed_files: frozenset[str] | None = None,
) -> list[SearchResult]:
    """Recherche query dans tous les .md de docs_dir.

    Retourne au plus max_results résultats triés par score DESC (puis file, line).
    Chaque résultat inclut l'excerpt nettoyé et la section (heading) de contexte.
    Retourne une liste vide si docs_dir n'existe pas ou si aucun résultat.

    allowed_files : si fourni, restreint la recherche aux fichiers dont le basename
    est dans le frozenset. Utile pour filtrer docs/wiki/ aux pages CK3 core seulement.
    """
    if not docs_dir.exists():
        return []

    tokens = _tokenize(query)
    if not tokens:
        return []

    results: list[SearchResult] = []

    for md_file in sorted(docs_dir.glob("*.md")):
        if allowed_files is not None and md_file.name not in allowed_files:
            continue
        try:
            lines = md_file.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue

        headings = _build_heading_index(lines)

        for lineno, raw_line in enumerate(lines, start=1):
            if _is_navbox_line(raw_line):
                continue
            line_lower = raw_line.lower()
            score = sum(1 for t in tokens if t in line_lower)
            if score > 0:
                results.append(
                    SearchResult(
                        file=md_file.name,
                        line=lineno,
                        excerpt=clean_excerpt(raw_line),
                        score=score,
                        section=_nearest_section(lineno, headings),
                    )
                )

    results.sort(key=lambda r: (-r.score, r.file, r.line))
    return results[:max_results]
