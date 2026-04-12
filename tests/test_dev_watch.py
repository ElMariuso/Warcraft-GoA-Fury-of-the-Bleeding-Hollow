"""Tests pour tools/dev_watch.py."""

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hansel-tools"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hansel-tools", "watchers"))

from dev_watch import NAMESPACE_PATTERNS, _format_record, tail_error_log
from log_viewer import LogLevel, LogRecord


def _make_record(level: LogLevel, message: str = "test") -> LogRecord:
    return LogRecord(
        timestamp="12:00:00",
        level=level,
        source="test.cpp:1",
        message=message,
        raw=f"[12:00:00][test.cpp:1]: {message}",
    )


def test_format_record_error_contains_red():
    """ERROR doit utiliser la couleur rouge."""
    record = _make_record(LogLevel.ERROR, "script error")
    result = _format_record(record)
    assert "\033[31m" in result  # RED
    assert "script error" in result


def test_format_record_debug_contains_dim():
    """DEBUG doit utiliser DIM."""
    record = _make_record(LogLevel.DEBUG, "debug trace")
    result = _format_record(record)
    assert "\033[2m" in result  # DIM


def test_format_record_warn_contains_yellow():
    """WARN doit utiliser jaune."""
    record = _make_record(LogLevel.WARN, "deprecated")
    result = _format_record(record)
    assert "\033[33m" in result  # YELLOW


def test_namespace_pattern_bh():
    """--namespace bh doit filtrer wc_bleeding_hollow."""
    raw = NAMESPACE_PATTERNS["bh"]
    assert raw is not None
    pattern = re.compile(raw)
    assert pattern.search("wc_bleeding_hollow_invasion")
    assert not pattern.search("wc_horde_invasion")


def test_namespace_pattern_horde():
    """--namespace horde doit filtrer wc_horde_invasion."""
    raw = NAMESPACE_PATTERNS["horde"]
    assert raw is not None
    pattern = re.compile(raw)
    assert pattern.search("wc_horde_invasion")
    assert not pattern.search("wc_bleeding_hollow")


def test_namespace_pattern_all_is_none():
    """--namespace all = pas de filtre."""
    assert NAMESPACE_PATTERNS["all"] is None


def test_namespace_pattern_default_matches_all_wc():
    """Défaut (None) doit matcher tous les namespaces wc_."""
    raw = NAMESPACE_PATTERNS[None]
    assert raw is not None
    pattern = re.compile(raw)
    assert pattern.search("wc_bleeding_hollow_invasion")
    assert pattern.search("wc_horde_invasion")
    assert not pattern.search("pdx_log.cpp")


def test_save_errors_writes_matching_lines(tmp_path):
    """--save-errors écrit les lignes namespace dans le fichier, pas les autres."""
    import threading
    import time
    from unittest.mock import patch

    fake_ck3_log = tmp_path / "error.log"
    fake_ck3_log.write_text("", encoding="utf-8")  # fichier vide pour que le thread démarre

    save_file = tmp_path / "error.log.out"
    pattern = re.compile(r"wc_bleeding_hollow")

    with patch("dev_watch.CK3_ERROR_LOG", fake_ck3_log):
        t = threading.Thread(
            target=tail_error_log,
            kwargs={"pattern": pattern, "save_path": save_file},
            daemon=True,
        )
        t.start()
        time.sleep(0.15)  # laisser le thread se positionner en fin de fichier

        # Écrire les lignes après que le thread surveille
        with open(fake_ck3_log, "a", encoding="utf-8") as f:
            f.write("[10:00:00][error.cpp:1]: [wc_bleeding_hollow_invasion] bad scope\n")
            f.write("[10:00:01][error.cpp:2]: some unrelated CK3 error\n")
            f.write("[10:00:02][error.cpp:3]: [wc_horde_invasion] missing effect\n")

        time.sleep(0.3)  # laisser le thread lire et écrire

    lines = save_file.read_text(encoding="utf-8").splitlines() if save_file.exists() else []
    assert any("wc_bleeding_hollow_invasion" in l for l in lines), "ligne BH attendue"
    assert not any("unrelated" in l for l in lines), "ligne non-namespace ne doit pas être sauvée"
    assert not any("wc_horde_invasion" in l for l in lines), "horde ne doit pas être sauvée avec filtre BH"
