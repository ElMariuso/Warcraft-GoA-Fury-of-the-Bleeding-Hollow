"""Tests for tools/log_viewer.py."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "hansel-tools"))
sys.path.insert(0, str(Path(__file__).parent.parent / "hansel-tools" / "watchers"))

from log_viewer import LogLevel, LogRecord, parse_line, should_display


def test_parse_line_error() -> None:
    """Error logs should be classified as ERROR level."""
    line = "[15:32:11][error.cpp:217]: Script error in file 'events/foo.txt' on line 42"
    record = parse_line(line)
    assert record is not None
    assert record.timestamp == "15:32:11"
    assert record.source == "error.cpp:217"
    assert record.level == LogLevel.ERROR


def test_parse_line_wc_namespace() -> None:
    """Namespace messages should be classified as INFO."""
    line = "[15:32:11][pdx_log.cpp:82]: [wc_bleeding_hollow_invasion] kilrogg found"
    record = parse_line(line)
    assert record is not None
    assert "wc_bleeding_hollow_invasion" in record.message
    assert record.level == LogLevel.INFO


def test_parse_line_unknown_format() -> None:
    """Lines without CK3 format should return None."""
    assert parse_line("This line has no CK3 log format") is None
    assert parse_line("") is None


def test_level_filter_blocks_lower() -> None:
    """Messages below minimum level should be filtered out."""
    record = LogRecord(
        timestamp="00:00:00",
        level=LogLevel.INFO,
        source="foo",
        message="bar",
        raw=""
    )
    assert not should_display(record, LogLevel.WARN, None)


def test_level_filter_passes_equal() -> None:
    """Messages at minimum level should pass."""
    record = LogRecord(
        timestamp="00:00:00",
        level=LogLevel.WARN,
        source="foo",
        message="bar",
        raw=""
    )
    assert should_display(record, LogLevel.WARN, None)


def test_regex_filter_matches_source() -> None:
    """Regex filter should match source."""
    record = LogRecord(
        timestamp="00:00:00",
        level=LogLevel.INFO,
        source="wc_bleeding_hollow_invasion",
        message="test",
        raw=""
    )
    pattern = re.compile(r"wc_bleeding")
    assert should_display(record, LogLevel.DEBUG, pattern)


def test_regex_filter_no_match() -> None:
    """Regex filter should reject non-matching records."""
    record = LogRecord(
        timestamp="00:00:00",
        level=LogLevel.INFO,
        source="pdx_log.cpp",
        message="unrelated",
        raw=""
    )
    pattern = re.compile(r"wc_horde")
    assert not should_display(record, LogLevel.DEBUG, pattern)


def test_parse_line_warn() -> None:
    """Warning logs should be classified as WARN level."""
    line = "[10:00:00][pdx_log.cpp:10]: Warning: missing localisation key"
    record = parse_line(line)
    assert record is not None
    assert record.level == LogLevel.WARN


def test_parse_line_debug() -> None:
    """Debug logs should be classified as DEBUG level."""
    line = "[09:15:30][pdx_log.cpp:100]: Debug event triggered"
    record = parse_line(line)
    assert record is not None
    assert record.level == LogLevel.DEBUG


def test_level_filter_passes_higher() -> None:
    """Messages above minimum level should pass."""
    record = LogRecord(
        timestamp="00:00:00",
        level=LogLevel.CRITICAL,
        source="foo",
        message="bar",
        raw=""
    )
    assert should_display(record, LogLevel.WARN, None)


def test_regex_filter_matches_message() -> None:
    """Regex filter should match message."""
    record = LogRecord(
        timestamp="00:00:00",
        level=LogLevel.INFO,
        source="pdx_log.cpp",
        message="[wc_horde_invasion] attack started",
        raw=""
    )
    pattern = re.compile(r"wc_horde")
    assert should_display(record, LogLevel.DEBUG, pattern)
