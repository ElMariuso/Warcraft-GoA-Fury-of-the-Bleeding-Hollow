#!/usr/bin/env python3
"""Watcher de dev unifié — surveille game.log et error.log en parallèle.

Filtre automatiquement les namespaces wc_* du mod.

Usage:
    python tools/dev_watch.py                        # filtre wc_ (tous namespaces mod)
    python tools/dev_watch.py --namespace bh         # wc_bleeding_hollow seulement
    python tools/dev_watch.py --namespace horde      # wc_horde_invasion seulement
    python tools/dev_watch.py --namespace all        # tout game.log
    python tools/dev_watch.py --errors-only          # ERROR+ seulement
    python tools/dev_watch.py --filter "kilrogg"     # regex custom sur game.log
    python tools/dev_watch.py --filter-errors "bh"  # regex custom sur error.log aussi
    python tools/dev_watch.py --event-trace          # résumé des events déclenchés
"""

import argparse
import contextlib
import re
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))         # hansel-tools/watchers/
sys.path.insert(0, str(Path(__file__).parent.parent))  # hansel-tools/

from config import CK3_ERROR_LOG, CK3_LOGS, SUBMOD_ROOT
from log_parser import LogLevel, LogRecord, parse_line, should_display
from log_viewer import LEVEL_COLORS
from ui import BOLD, CYAN, DIM, GREEN, RED, RESET, YELLOW, warn

# Raccourcis namespace → pattern regex
NAMESPACE_PATTERNS: dict[str | None, str | None] = {
    "bh": r"wc_bleeding_hollow",
    "horde": r"wc_horde_invasion",
    "all": None,
    None: r"wc_",  # défaut : tous les namespaces du mod
}

_lock = threading.Lock()
_event_counts: dict[str, int] = {}

# Regex pour détecter les events déclenchés dans game.log
# CK3 écrit : [HH:MM:SS][E][eventmanager.cpp:N]: Event #wc_ns.1234 has ...
#          ou : [HH:MM:SS][E][eventmanager.cpp:N]: Event 'wc_ns.1234' expected ...
_EVENT_RE = re.compile(
    r'\[(\d{2}:\d{2}:\d{2})\](?:\[[A-Z]\])?\[[^\]]+\]: Event [#\'\"]?(wc_[a-z_]+)\.(\d+)(.*)'
)


def _print_safe(line: str) -> None:
    with _lock:
        print(line, flush=True)


def _format_record(record: LogRecord) -> str:
    color = LEVEL_COLORS.get(record.level, RESET)
    return f"{color}[{record.timestamp}] {record.source}: {record.message}{RESET}"


def tail_game_log(
    pattern: re.Pattern[str] | None,
    level_min: LogLevel,
    event_trace: bool = False,
) -> None:
    """Thread : surveille game.log et affiche les lignes correspondant au filtre."""
    log_path = Path(CK3_LOGS)
    prefix = f"{CYAN}[GAME]{RESET}"
    trace_prefix = f"{BOLD}{CYAN}[EVT ]{RESET}"

    if not log_path.exists():
        warn(f"game.log non trouvé : {log_path}")
        return

    with open(log_path, encoding="utf-8", errors="ignore") as f:
        f.seek(0, 2)
        try:
            while True:
                line = f.readline()
                if line:
                    raw = line.rstrip()
                    if event_trace:
                        m = _EVENT_RE.match(raw)
                        if m:
                            ts, ns, event_id, msg = m.group(1), m.group(2), m.group(3), m.group(4)
                            # Filtre namespace si pattern actif
                            if pattern is None or pattern.search(ns) or pattern.search(raw):
                                key = f"{ns}.{event_id}"
                                with _lock:
                                    _event_counts[key] = _event_counts.get(key, 0) + 1
                                    count = _event_counts[key]
                                count_str = f"{DIM}×{count}{RESET}" if count > 1 else ""
                                _print_safe(
                                    f"{trace_prefix} {BOLD}{YELLOW}{ns}.{event_id}{RESET}"
                                    f" {DIM}[{ts}]{RESET} {count_str} {msg[:80]}"
                                )
                            continue
                    record = parse_line(raw)
                    if record and should_display(record, level_min, pattern):
                        _print_safe(f"{prefix} {_format_record(record)}")
                else:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            pass


def tail_error_log(
    pattern: re.Pattern[str] | None = None,
    save_path: Path | None = None,
) -> None:
    """Thread : surveille error.log et affiche tout (format Jomini variable).

    pattern : filtre optionnel propre à error.log (indépendant du filtre game.log).
    Par défaut (None), toutes les erreurs sont affichées.
    Si save_path est fourni, les lignes correspondant au pattern sont aussi
    écrites en texte brut dans ce fichier (sans ANSI).
    """
    log_path = Path(CK3_ERROR_LOG)
    prefix = f"{BOLD}{RED}[ERR!]{RESET}"

    if not log_path.exists():
        warn(f"error.log non trouvé : {log_path}")
        return

    with contextlib.ExitStack() as stack:
        save_file = (
            stack.enter_context(open(save_path, "w", encoding="utf-8"))
            if save_path
            else None
        )
        f = stack.enter_context(open(log_path, encoding="utf-8", errors="ignore"))
        f.seek(0, 2)
        try:
            while True:
                line = f.readline()
                if line.strip():
                    record = parse_line(line.rstrip())
                    if record:
                        plain = f"[{record.timestamp}] {record.source}: {record.message}"
                    else:
                        plain = line.rstrip()
                    # Filtre error.log indépendant — par défaut tout afficher
                    if not pattern or pattern.search(plain):
                        if record:
                            _print_safe(f"{prefix} {_format_record(record)}")
                        else:
                            _print_safe(f"{prefix} {RED}{line.rstrip()}{RESET}")
                        if save_file:
                            save_file.write(plain + "\n")
                            save_file.flush()
                else:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            pass


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Watcher de dev CK3 — game.log + error.log en parallèle"
    )
    parser.add_argument(
        "--namespace", "-n",
        choices=["bh", "horde", "all"],
        default=None,
        help="Filtre namespace : bh=wc_bleeding_hollow, horde=wc_horde_invasion, all=aucun filtre (défaut: wc_)",
    )
    parser.add_argument(
        "--filter", "-f",
        dest="custom_filter",
        type=str,
        help="Regex custom sur game.log (remplace --namespace)",
    )
    parser.add_argument(
        "--errors-only",
        action="store_true",
        help="game.log : afficher ERROR et CRITICAL seulement",
    )
    parser.add_argument(
        "--save-errors",
        action="store_true",
        help="Sauvegarder les ERR! du namespace dans error.log à la racine du projet",
    )
    parser.add_argument(
        "--filter-errors",
        dest="error_filter",
        type=str,
        default=None,
        help="Regex custom sur error.log (indépendant de --filter, défaut: tout afficher)",
    )
    parser.add_argument(
        "--event-trace",
        action="store_true",
        help="Afficher un résumé coloré des events wc_* déclenchés (namespace + ID + compteur)",
    )
    args = parser.parse_args()

    # Résoudre le pattern game.log
    if args.custom_filter:
        raw_pattern: str | None = args.custom_filter
    else:
        raw_pattern = NAMESPACE_PATTERNS[args.namespace]

    pattern = re.compile(raw_pattern) if raw_pattern else None
    # Filtre error.log — indépendant (None = tout afficher)
    error_pattern = re.compile(args.error_filter) if args.error_filter else None
    level_min = LogLevel.ERROR if args.errors_only else LogLevel.DEBUG

    # Chemin de sauvegarde des erreurs namespace
    save_path: Path | None = None
    if args.save_errors:
        save_path = SUBMOD_ROOT / "error.log"

    # Header
    filter_label = args.custom_filter or (
        f"namespace={args.namespace}" if args.namespace else "wc_* (défaut)"
    )
    print(f"{BOLD}=== CK3 Dev Watch ==={RESET}")
    game_mode = f"{BOLD}EVENT TRACE{RESET}" if args.event_trace else f"filtre: {filter_label}"
    print(f"  {CYAN}[GAME]{RESET}  {CK3_LOGS}  ({game_mode})")
    err_label = f"filtre: {error_pattern.pattern}" if error_pattern else "tout afficher"
    print(f"  {BOLD}{RED}[ERR!]{RESET}  {CK3_ERROR_LOG}  ({err_label})")
    if save_path:
        print(f"  {GREEN}[SAVE]{RESET}  erreurs namespace → {save_path}")
    print("  Ctrl+C pour quitter\n")

    t_game = threading.Thread(
        target=tail_game_log, args=(pattern, level_min, args.event_trace), daemon=True
    )
    t_error = threading.Thread(
        target=tail_error_log, args=(error_pattern, save_path), daemon=True
    )

    t_game.start()
    t_error.start()

    try:
        t_game.join()
        t_error.join()
    except KeyboardInterrupt:
        print()


if __name__ == "__main__":
    main()
