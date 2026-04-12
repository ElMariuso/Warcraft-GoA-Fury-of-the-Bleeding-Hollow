#!/usr/bin/env python3
"""
Écrit un script Jomini dans le dossier run/ de CK3 pour injection via la console.

⚠️  Utiliser la console CK3 désactive les achievements pour la save en cours.

Usage:
    python tools/inject_run.py <script.txt>
    python tools/inject_run.py --inline "character:10005 = { add_prestige = 500 }"
    python tools/inject_run.py --inline "character:10005 = { add_prestige = 500 }" --name debug_prestige
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config import CK3_RUN
from ui import CYAN, GREEN, RED, RESET, warn


def write_run_script(content: str, name: str) -> None:
    if not CK3_RUN.exists():
        print(f"{RED}Dossier run/ introuvable :{RESET} {CK3_RUN}")
        print("Vérifie le chemin dans tools/config.py ou la variable CK3_RUN_PATH.")
        sys.exit(1)

    out = CK3_RUN / f"{name}.txt"
    out.write_text(content, encoding="utf-8")

    warn("⚠️  La console CK3 désactive les achievements pour cette save.\n")
    print(f"{GREEN}Script écrit :{RESET} {out}")
    print()
    print("  Dans la console CK3 (²) :")
    print(f"  {CYAN}run {name}.txt{RESET}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Injecte un script Jomini via run/ de CK3")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("script", nargs="?", metavar="FILE", help="Fichier .txt Jomini à injecter")
    group.add_argument("--inline", "-i", metavar="CODE", help="Script Jomini inline (chaîne)")
    parser.add_argument(
        "--name",
        "-n",
        metavar="NAME",
        default="inject",
        help="Nom du fichier dans run/ (sans .txt, défaut: inject)",
    )
    args = parser.parse_args()

    if args.inline:
        content = args.inline
    else:
        src = Path(args.script)
        if not src.exists():
            print(f"{RED}Fichier introuvable :{RESET} {args.script}", file=sys.stderr)
            sys.exit(1)
        content = src.read_text(encoding="utf-8")

    write_run_script(content, args.name)


if __name__ == "__main__":
    main()
