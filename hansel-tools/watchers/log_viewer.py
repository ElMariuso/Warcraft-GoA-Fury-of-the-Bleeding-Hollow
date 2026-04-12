#!/usr/bin/env python3
"""Real-time CK3 game.log viewer with structured parsing."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))  # hansel-tools/
sys.path.insert(0, str(Path(__file__).parent))         # hansel-tools/watchers/

import argparse
import re
import time

from config import CK3_LOGS
from log_parser import LogLevel, LogRecord, parse_line, should_display
from ui import BOLD, CYAN, DIM, RED, RESET, YELLOW, error as ui_error

__all__ = [
    "LEVEL_COLORS",
    "LogLevel",
    "LogRecord",
    "parse_line",
    "should_display",
    "display_record",
    "watch",
    "main",
]

# ANSI color mapping for log levels
LEVEL_COLORS = {
    LogLevel.DEBUG: DIM,
    LogLevel.INFO: CYAN,
    LogLevel.WARN: YELLOW,
    LogLevel.ERROR: RED,
    LogLevel.CRITICAL: BOLD + RED,
}


def display_record(record: LogRecord, use_color: bool) -> None:
    """Print a log record with appropriate formatting."""
    if not use_color:
        print(f"[{record.timestamp}] [{record.level.name}] {record.source}: {record.message}")
        return

    color = LEVEL_COLORS.get(record.level, RESET)
    print(f"{color}[{record.timestamp}] [{record.level.name}] {record.source}: {record.message}{RESET}")


def watch(
    log_path: Path,
    level_min: LogLevel,
    pattern: re.Pattern[str] | None,
    from_start: bool,
    use_color: bool,
) -> None:
    """Tail log_path in real-time, printing matching records."""
    try:
        with open(log_path, encoding="utf-8", errors="replace") as f:
            if not from_start:
                f.seek(0, 2)  # Seek to end
            try:
                while True:
                    line = f.readline()
                    if line:
                        record = parse_line(line)
                        if record and should_display(record, level_min, pattern):
                            display_record(record, use_color)
                    else:
                        time.sleep(0.1)
            except KeyboardInterrupt:
                print("\nArrêté.")
    except FileNotFoundError:
        ui_error(f"Log file not found: {log_path}")
        sys.exit(1)


def main() -> None:
    """Entry point for the log viewer CLI."""
    parser = argparse.ArgumentParser(description="Real-time CK3 log viewer")
    parser.add_argument(
        "--log",
        type=Path,
        default=CK3_LOGS,
        help="Path to game.log"
    )
    parser.add_argument(
        "--filter",
        "-f",
        dest="filter",
        default=None,
        help="Regex filter on source or message"
    )
    parser.add_argument(
        "--level",
        "-l",
        default="DEBUG",
        choices=[level_enum.name for level_enum in LogLevel],
        help="Minimum log level"
    )
    parser.add_argument(
        "--errors-only",
        action="store_true",
        help="Shorthand for --level ERROR"
    )
    parser.add_argument(
        "--from-start",
        action="store_true",
        help="Read from file start instead of tail"
    )
    args = parser.parse_args()

    level_min = LogLevel.ERROR if args.errors_only else LogLevel[args.level]
    pattern = re.compile(args.filter) if args.filter else None
    use_color = sys.stdout.isatty()

    watch(args.log, level_min, pattern, args.from_start, use_color)


if __name__ == "__main__":
    main()
