#!/usr/bin/env python3
"""Linter pour les fichiers de localisation CK3 (.yml).

Valide chaque fichier contre les règles L01–L05 :
  L01 — BOM UTF-8 absent
  L02 — Header l_english: absent
  L03 — Format de clé invalide
  L04 — Placeholder "Blablabla" non remplacé
  L05 — Version de clé non nulle (:1, :2…)

Usage:
    python tools/lint_localization.py localization/english/
    python tools/lint_localization.py localization/english/wc_foo_l_english.yml
    python tools/lint_localization.py --rules
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))         # hansel-tools/linters/
sys.path.insert(0, str(Path(__file__).parent.parent))  # hansel-tools/
from rules import Severity
from _linter_runner import make_linter_main  # noqa: F401 — used in __main__ block

_UTF8_BOM = b"\xef\xbb\xbf"

# Correspond à :   key:0 "text"   ou   key:0 ""   (valeur vide autorisée)
_KEY_LINE = re.compile(
    r"^\s+([a-zA-Z_][a-zA-Z0-9_.]*):(\d+)\s+\"(.*)\"", re.MULTILINE
)

# Ligne non-vide et non-commentaire
_SIGNIFICANT_LINE = re.compile(r"^\s*[^#\s]")


@dataclass
class LocKey:
    """Une entrée de localisation extraite d'un fichier .yml."""

    key: str
    version: int
    value: str
    line: int  # numéro de ligne (1-based)


@dataclass
class LintViolation:
    """Une violation détectée dans un fichier de localisation."""

    rule_id: str
    file: str
    severity: Severity
    message: str
    line: int = 0


def check_bom(raw_bytes: bytes, file_name: str) -> list[LintViolation]:
    """L01 — vérifie la présence du BOM UTF-8."""
    if not raw_bytes.startswith(_UTF8_BOM):
        return [LintViolation(
            rule_id="L01",
            file=file_name,
            severity="ERROR",
            message="BOM UTF-8 absent (\\xef\\xbb\\xbf requis en début de fichier)",
            line=1,
        )]
    return []


def check_header(text: str, file_name: str) -> list[LintViolation]:
    """L02 — vérifie que la première ligne significative est 'l_english:'."""
    for i, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped != "l_english:":
            return [LintViolation(
                rule_id="L02",
                file=file_name,
                severity="ERROR",
                message=f"Header invalide : attendu 'l_english:', trouvé '{stripped}'",
                line=i,
            )]
        return []
    return [LintViolation(
        rule_id="L02",
        file=file_name,
        severity="ERROR",
        message="Header l_english: introuvable (fichier vide ou que des commentaires)",
        line=1,
    )]


def extract_loc_keys(text: str) -> list[LocKey]:
    """Extrait toutes les entrées clé:version "valeur" du texte."""
    keys: list[LocKey] = []
    for m in _KEY_LINE.finditer(text):
        line_no = text[: m.start()].count("\n") + 1
        keys.append(LocKey(
            key=m.group(1),
            version=int(m.group(2)),
            value=m.group(3),
            line=line_no,
        ))
    return keys


def check_key(key: LocKey, file_name: str) -> list[LintViolation]:
    """L04, L05 — valide une entrée de localisation individuelle."""
    violations: list[LintViolation] = []

    if key.version != 0:
        violations.append(LintViolation(
            rule_id="L05",
            file=file_name,
            severity="WARN",
            message=f"Version :{key.version} non nulle pour la clé '{key.key}' (doit être :0)",
            line=key.line,
        ))

    if "Blablabla" in key.value:
        violations.append(LintViolation(
            rule_id="L04",
            file=file_name,
            severity="WARN",
            message=f"Placeholder 'Blablabla' non remplacé dans '{key.key}'",
            line=key.line,
        ))

    return violations


def _check_malformed_lines(text: str, file_name: str) -> list[LintViolation]:
    """L03 — détecte les lignes qui ressemblent à des entrées mais ne parsent pas."""
    violations: list[LintViolation] = []
    # Ligne indentée, non-commentaire, non-vide, qui n'est pas le header et pas une valeur connue
    _INDENTED_ENTRY = re.compile(r"^\s+(\S.+)$")
    for i, line in enumerate(text.splitlines(), start=1):
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.strip() == "l_english:":
            continue
        m = _INDENTED_ENTRY.match(line)
        if not m:
            continue
        content = m.group(1)
        # Ligne avec ":" — probablement une entrée de localisation
        if ":" not in content:
            continue
        # Vérifier que cette ligne correspond bien au pattern clé
        if not _KEY_LINE.match(line):
            # Ignorer les lignes de continuation (valeur multiline sans guillemet)
            # Une vraie malformed line contient key:digit mais sans guillemets
            if re.match(r"^\s+[a-zA-Z_][a-zA-Z0-9_.]*:\d+\s*$", line):
                violations.append(LintViolation(
                    rule_id="L03",
                    file=file_name,
                    severity="WARN",
                    message=f"Entrée sans valeur : '{content.strip()}'",
                    line=i,
                ))
    return violations


def lint_file(path: Path) -> list[LintViolation]:
    """Lint un fichier .yml CK3 et retourne toutes les violations."""
    violations: list[LintViolation] = []
    file_name = path.name

    raw_bytes = path.read_bytes()
    violations.extend(check_bom(raw_bytes, file_name))

    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            text = raw_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            print(f"Erreur d'encodage dans {path}: {e}", file=sys.stderr)
            return violations

    violations.extend(check_header(text, file_name))

    keys = extract_loc_keys(text)
    known_key_names = {k.key for k in keys}
    for key in keys:
        violations.extend(check_key(key, file_name))

    violations.extend(_check_malformed_lines(text, file_name))

    return violations


if __name__ == "__main__":
    sys.exit(make_linter_main(
        lint_fn=lint_file,
        default_path=Path("localization/english/"),
        label="localization",
        glob_pattern="*.yml",
        rule_prefix="L",
    ))
