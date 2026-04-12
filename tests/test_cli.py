"""tests/test_cli.py — Tests pour hansel-tools/cli.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent
CLI = str(PROJECT_ROOT / "hansel-tools" / "cli.py")


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    """Lance le CLI depuis le project root et capture la sortie."""
    return subprocess.run(
        [sys.executable, CLI, *args],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        text=True,
    )


class TestCliSearch:
    def test_cli_search_returns_results(self) -> None:
        """search story_cycle → exit 0 + output non-vide."""
        result = run_cli("search", "story_cycle")
        assert result.returncode == 0
        assert result.stdout.strip() != ""

    def test_cli_search_no_match(self) -> None:
        """search xyzabc123 → exit 0 + message 'Aucun résultat'."""
        result = run_cli("search", "xyzabc123notexist")
        assert result.returncode == 0
        assert "Aucun résultat" in result.stdout


    def test_cmd_search_highlight_tokens_present(self) -> None:
        """Les tokens de la requête apparaissent dans l'output (sans couleur)."""
        proc = run_cli("search", "story_cycle", "--no-color", "--max", "5")
        assert proc.returncode == 0
        # Sans couleur, story_cycle doit apparaître tel quel dans les excerpts
        assert "story_cycle" in proc.stdout.lower() or "story cycle" in proc.stdout.lower()

    def test_cmd_search_section_names_truncated(self) -> None:
        """Les noms de section § sont tronqués à 70 chars max."""
        proc = run_cli("search", "character", "--no-color", "--max", "30")
        assert proc.returncode == 0
        for line in proc.stdout.splitlines():
            if line.strip().startswith("§"):
                section_text = line.strip()[2:].strip()  # après "§ "
                assert len(section_text) <= 71, f"Section trop longue: {section_text!r}"


class TestCliTiger:
    def test_tiger_missing_binary_exits_nonzero(self) -> None:
        """tiger avec PATH vide → exit 1 + message stderr mentionnant ck3-tiger."""
        import os

        env = {**os.environ, "PATH": ""}
        result = subprocess.run(
            [sys.executable, CLI, "tiger"],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            env=env,
        )
        assert result.returncode == 1
        assert "ck3-tiger" in result.stderr
