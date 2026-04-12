#!/usr/bin/env python3
"""Accumulation d'erreurs CK3 — set persistant, sans doublons.

Lit stdin ligne par ligne, filtre via --pattern, et n'ajoute dans le
fichier de sortie que les lignes jamais vues (set cumulatif).

Usage:
    make dev-bh 2>&1 | python tools/error_accumulator.py [--out logs/errors-bh.log] [--pattern REGEX]
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))  # hansel-tools/

from ui import BOLD, DIM, GREEN, RED, RESET


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        default="logs/errors-bh.log",
        help="Fichier de sortie (défaut: logs/errors-bh.log)",
    )
    parser.add_argument(
        "--pattern",
        default=r"wc_bleeding_hollow|wc_horde_invasion|Fury|Bleeding",
        help="Regex de filtre sur les lignes entrantes",
    )
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    pattern = re.compile(args.pattern, re.IGNORECASE)

    # Charger le set des erreurs déjà connues
    seen: set[str] = set()
    if out_path.exists():
        seen = set(out_path.read_text(encoding="utf-8").splitlines())

    new_count = 0
    print(
        f"{DIM}→ Accumulation dans {out_path}  "
        f"({len(seen)} erreurs existantes){RESET}",
        file=sys.stderr,
    )

    try:
        with out_path.open("a", encoding="utf-8") as fh:
            for raw_line in sys.stdin:
                line = raw_line.rstrip()
                if not line:
                    continue
                if not pattern.search(line):
                    continue
                if line in seen:
                    # Déjà connu — afficher en gris pour feedback visuel
                    print(f"{DIM}{line}{RESET}")
                    continue
                seen.add(line)
                fh.write(line + "\n")
                fh.flush()
                new_count += 1
                print(f"{RED}[NEW]{RESET} {line}")
    except KeyboardInterrupt:
        pass
    finally:
        print(
            f"\n{BOLD}{GREEN}+{new_count} nouvelle(s) erreur(s){RESET} "
            f"— total : {len(seen)} dans {out_path}",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
