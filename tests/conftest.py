"""Fixtures partagées pour la suite de tests hansel-tools.

Centralise le hack `sys.path.insert` que chaque module de test dupliquait,
plus quelques helpers réutilisables (SymbolDB vide, blocs Jomini échantillons).
"""
from __future__ import annotations

import os
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

# Path hack identique à celui utilisé par les scripts hansel-tools.
_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(_ROOT / "hansel-tools"))
sys.path.insert(0, str(_ROOT / "hansel-tools" / "linters"))
sys.path.insert(0, str(_ROOT / "hansel-tools" / "watchers"))


# ─── Blocs Jomini ──────────────────────────────────────────────────────────────

JOMINI_EVENT_SAMPLE = """\
wc_horde_invasion.1000 = {
\ttype = character_event
\ttitle = wc_horde_invasion.1000.title
\tdesc = wc_horde_invasion.1000.desc
\tcontent_source = dlc_GOA
\toption = {
\t\tname = wc_horde_invasion.1000.a
\t\tai_chance = { base = 100 }
\t}
}
"""

JOMINI_EFFECT_SAMPLE = """\
spawn_orc_troops_based_on_culture_effect = {
\tif = {
\t\tlimit = { has_culture = culture:blackrock }
\t\tspawn_army = yes
\t}
}
"""

JOMINI_MULTI_EVENT_SAMPLE = """\
wc_horde_invasion.1000 = {
\ttype = character_event
}

wc_horde_invasion.1001 = {
\ttype = character_event
\toption = {
\t\tname = ok
\t}
}
"""


@pytest.fixture
def jomini_event_text() -> str:
    """Texte brut d'un event Jomini valide (un seul bloc)."""
    return JOMINI_EVENT_SAMPLE


@pytest.fixture
def jomini_effect_text() -> str:
    """Texte brut d'un scripted_effect Jomini valide."""
    return JOMINI_EFFECT_SAMPLE


@pytest.fixture
def jomini_multi_event_text() -> str:
    """Texte brut avec deux events top-level dans le même fichier."""
    return JOMINI_MULTI_EVENT_SAMPLE


@pytest.fixture
def write_file(tmp_path: Path) -> Callable[[str, str], Path]:
    """Factory : écrit un fichier dans tmp_path et retourne le Path.

    Usage :
        def test_xxx(write_file):
            p = write_file("events/foo.txt", "wc_foo.1 = {}")
    """

    def _write(rel: str, content: str, *, encoding: str = "utf-8") -> Path:
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding=encoding)
        return target

    return _write


# ─── SymbolDB ──────────────────────────────────────────────────────────────────


@pytest.fixture
def empty_symbol_db():
    """Retourne un SymbolDB minimal (listes vides) — utile pour forcer les
    linters dépendant de la DB à traiter tous les refs comme inconnus."""
    from symbol_db import SymbolDB  # import tardif — path hack appliqué

    return SymbolDB(
        characters=frozenset(),
        titles=frozenset(),
        modifiers=frozenset(),
        scripted_effects=frozenset(),
        scripted_triggers=frozenset(),
    )


@pytest.fixture
def minimal_symbol_db():
    """SymbolDB avec quelques symboles connus pour tester le happy path."""
    from symbol_db import SymbolDB

    return SymbolDB(
        characters=frozenset({10000, 10005, 10015}),
        titles=frozenset({"e_horde", "k_bleeding_hollow_clan", "c_vekrishe"}),
        modifiers=frozenset({"great_invader_modifier", "horde_conqueror_modifier"}),
        scripted_effects=frozenset(
            {
                "spawn_orc_troops_based_on_culture_effect",
                "horde_bloodshed_effect",
            }
        ),
        scripted_triggers=frozenset(),
    )


# ─── Env isolation ─────────────────────────────────────────────────────────────


@pytest.fixture
def clean_ck3_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Retire les variables d'environnement CK3_* pour isoler les tests qui
    touchent à config.py de la config utilisateur."""
    for key in ("CK3_LOGS_PATH", "CK3_ERROR_LOG_PATH", "CK3_RUN_PATH"):
        monkeypatch.delenv(key, raising=False)
    # Évite que os reste importé mais pas utilisé par les utilisateurs du fixture
    _ = os.environ
