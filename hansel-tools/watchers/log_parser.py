"""Parsing primitives for CK3 game.log lines.

Extracted from log_viewer.py so that other watchers (dev_watch, future tools)
can share the same structured representation without pulling in terminal
rendering dependencies.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import IntEnum


class LogLevel(IntEnum):
    """Enumeration of log severity levels."""

    DEBUG = 0
    INFO = 1
    WARN = 2
    ERROR = 3
    CRITICAL = 4


@dataclass
class LogRecord:
    """A parsed log record from CK3 game.log."""

    timestamp: str
    level: LogLevel
    source: str  # ex: "error.cpp:217" ou "[wc_bleeding_hollow_invasion]"
    message: str
    raw: str


# Pattern regex CK3 game.log — format réel : [HH:MM:SS][LEVEL][source]: msg
# Le groupe [LEVEL] (ex: [E], [I], [W]) est optionnel pour compatibilité
_LINE_RE = re.compile(r"\[(\d{2}:\d{2}:\d{2})\](?:\[[A-Z]\])?\[([^\]]+)\]: (.+)")


def parse_line(line: str) -> LogRecord | None:
    """Parse a CK3 log line into a structured LogRecord, or None if no match."""
    m = _LINE_RE.match(line.rstrip())
    if not m:
        return None
    timestamp, source, message = m.group(1), m.group(2), m.group(3)
    level = _classify_level(source, message)
    return LogRecord(
        timestamp=timestamp,
        level=level,
        source=source,
        message=message,
        raw=line.rstrip(),
    )


def _classify_level(source: str, message: str) -> LogLevel:
    """Infer LogLevel from source/message content."""
    combined = (source + " " + message).lower()
    if "error" in combined or "script error" in combined or "invalid" in combined:
        return LogLevel.ERROR
    if "warning" in combined or "warn" in combined:
        return LogLevel.WARN
    if "debug" in combined:
        return LogLevel.DEBUG
    return LogLevel.INFO


def should_display(
    record: LogRecord,
    level_min: LogLevel,
    pattern: re.Pattern[str] | None,
) -> bool:
    """Return True if the record passes level and filter criteria."""
    if record.level < level_min:
        return False
    if pattern is not None:
        return bool(pattern.search(record.source) or pattern.search(record.message))
    return True
