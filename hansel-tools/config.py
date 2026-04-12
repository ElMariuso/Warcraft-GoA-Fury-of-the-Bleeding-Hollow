"""Chemins centraux du projet.

Surcharges possibles via variables d'environnement :
    CK3_LOGS_PATH       — chemin complet vers game.log
    CK3_ERROR_LOG_PATH  — chemin complet vers error.log
    CK3_RUN_PATH        — chemin complet vers le dossier run/

Exemples :
    Linux  : pas de variable nécessaire, chemin détecté automatiquement
    Windows: pas de variable nécessaire si tu es l'utilisateur par défaut
    Custom : export CK3_LOGS_PATH="/chemin/vers/game.log"
"""

import os
import platform
from pathlib import Path

# Racine du submod
SUBMOD_ROOT = Path(__file__).parent.parent

# Mod parent (Warcraft-Guardians-of-Azeroth-2)
PARENT_MOD_ROOT = SUBMOD_ROOT.parent / "Warcraft-Guardians-of-Azeroth-2"

# Dossiers cibles du submod
EVENTS_DIR = SUBMOD_ROOT / "events" / "story_cycles"
LOC_DIR = SUBMOD_ROOT / "localization" / "english"

# Chemins CK3 — détection automatique selon l'OS
_PLATFORM = platform.system()
if _PLATFORM == "Windows":
    _CK3_DOCS_DEFAULT = (
        Path.home() / "OneDrive/Documents/Paradox Interactive/Crusader Kings III"
    )
elif _PLATFORM == "Darwin":
    _CK3_DOCS_DEFAULT = (
        Path.home() / "Library/Application Support/Paradox Interactive/Crusader Kings III"
    )
else:  # Linux
    _CK3_DOCS_DEFAULT = (
        Path.home() / ".local/share/Paradox Interactive/Crusader Kings III"
    )

CK3_LOGS: Path = (
    Path(os.environ["CK3_LOGS_PATH"])
    if "CK3_LOGS_PATH" in os.environ
    else _CK3_DOCS_DEFAULT / "logs" / "game.log"
)

CK3_ERROR_LOG: Path = (
    Path(os.environ["CK3_ERROR_LOG_PATH"])
    if "CK3_ERROR_LOG_PATH" in os.environ
    else _CK3_DOCS_DEFAULT / "logs" / "error.log"
)

CK3_RUN: Path = (
    Path(os.environ["CK3_RUN_PATH"])
    if "CK3_RUN_PATH" in os.environ
    else _CK3_DOCS_DEFAULT / "run"
)
