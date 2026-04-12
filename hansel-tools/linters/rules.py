"""Règles de validation CK3 extraites des docs wiki-paradox/.

Chaque règle cite la section de documentation source.
Utilisé par lint_events.py pour valider les fichiers .txt CK3.
"""

from dataclasses import dataclass
from typing import Literal

Severity = Literal["ERROR", "WARN", "INFO"]


@dataclass(frozen=True)
class LintRule:
    """Règle de validation CK3."""

    id: str
    severity: Severity
    description: str
    doc_ref: str  # Section exacte dans docs/wiki-paradox/


ALL_RULES: list[LintRule] = [
    LintRule(
        id="R01",
        severity="ERROR",
        description="content_source = dlc_GOA manquant sur un event non-hidden",
        doc_ref="CLAUDE.md §Key Patterns",
    ),
    LintRule(
        id="R02",
        severity="ERROR",
        description="Option sans bloc ai_chance",
        doc_ref="03_events_decisions.md §Options ligne 1098",
    ),
    LintRule(
        id="R03",
        severity="WARN",
        description="Option avec ai_chance.base = 0 sans commentaire non-canon",
        doc_ref="CLAUDE.md §Key Patterns — ai_chance",
    ),
    LintRule(
        id="R04",
        severity="ERROR",
        description="Event visible sans title ou sans desc",
        doc_ref="03_events_decisions.md §Structure ligne 603",
    ),
    LintRule(
        id="R05",
        severity="WARN",
        description="mean_time_to_happen présent mais aucun trigger — event jamais déclenché",
        doc_ref="03_events_decisions.md §Trigger ligne 851",
    ),
    LintRule(
        id="R06",
        severity="WARN",
        description="Portrait (left_portrait, right_portrait) dans un event hidden = yes",
        doc_ref="03_events_decisions.md §Flags ligne 659",
    ),
    LintRule(
        id="R07",
        severity="WARN",
        description='Placeholder "Blablabla" non remplacé dans la localisation',
        doc_ref="CLAUDE.md §Localization",
    ),
    LintRule(
        id="R08",
        severity="INFO",
        description="ID d'event hors plage attendue (1xxx=unique, 2xxx=aléatoire)",
        doc_ref="CLAUDE.md §Event ID Numbering",
    ),
    LintRule(
        id="R09",
        severity="ERROR",
        description="character:<ID> référencé mais ID inexistant dans le parent mod",
        doc_ref="docs/ck3_symbols.md §Characters",
    ),
    LintRule(
        id="R10",
        severity="ERROR",
        description="title:<KEY> référencé mais clé inexistante dans le parent mod",
        doc_ref="docs/ck3_symbols.md §Titres",
    ),
    LintRule(
        id="R11",
        severity="WARN",
        description="Modificateur référencé introuvable dans le parent mod",
        doc_ref="docs/ck3_symbols.md §Modificateurs",
    ),
    LintRule(
        id="R12",
        severity="WARN",
        description="Scripted effect appelé introuvable dans le parent mod",
        doc_ref="docs/ck3_symbols.md §Scripted Effects",
    ),
    # ── Localization ──────────────────────────────────────────────────────────
    LintRule(
        id="L01",
        severity="ERROR",
        description="BOM UTF-8 absent — le fichier doit commencer par \\xef\\xbb\\xbf",
        doc_ref="CLAUDE.md §Localization",
    ),
    LintRule(
        id="L02",
        severity="ERROR",
        description="Header l_english: absent ou mal formaté (première ligne non-commentaire)",
        doc_ref="CLAUDE.md §Localization",
    ),
    LintRule(
        id="L03",
        severity="WARN",
        description="Format de clé invalide — attendu : key:0 \"text\"",
        doc_ref="06_localization.md §Format",
    ),
    LintRule(
        id="L04",
        severity="WARN",
        description='Valeur placeholder "Blablabla" non remplacée',
        doc_ref="CLAUDE.md §Localization",
    ),
    LintRule(
        id="L05",
        severity="WARN",
        description="Version de clé non nulle (:1, :2…) — doit être :0",
        doc_ref="06_localization.md §Version suffix",
    ),
    # ── Scripted effects ───────────────────────────────────────────────────────
    LintRule(
        id="E01",
        severity="ERROR",
        description="character:<ID> référencé mais ID inexistant dans le parent mod",
        doc_ref="docs/ck3_symbols.md §Characters",
    ),
    LintRule(
        id="E02",
        severity="ERROR",
        description="title:<KEY> référencé mais clé inexistante dans le parent mod",
        doc_ref="docs/ck3_symbols.md §Titres",
    ),
    LintRule(
        id="E03",
        severity="WARN",
        description="Modificateur référencé introuvable dans le parent mod",
        doc_ref="docs/ck3_symbols.md §Modificateurs",
    ),
    LintRule(
        id="E04",
        severity="WARN",
        description="Scripted effect appelé introuvable dans le parent mod",
        doc_ref="docs/ck3_symbols.md §Scripted Effects",
    ),
]

RULES_BY_ID: dict[str, LintRule] = {r.id: r for r in ALL_RULES}
