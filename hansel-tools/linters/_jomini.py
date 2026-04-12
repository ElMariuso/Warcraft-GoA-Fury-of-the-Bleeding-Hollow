"""Shared Jomini parsing primitives.

Used by lint_events.py, lint_effects.py, and generate_events.py.
No circular imports: this module imports stdlib only.
"""
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Block:
    """A top-level Jomini block extracted from a .txt file."""

    id: str          # e.g. "wc_horde_invasion.1004" or "spawn_orc_troops_based_on_culture_effect"
    raw: str         # raw content between braces (not including the header line)
    line_start: int  # 1-based line number of the header in the source file


# ─── Compiled regex constants (extracted from lint_events.py / lint_effects.py) ──

CHAR_REF: re.Pattern[str] = re.compile(r"\bcharacter:(\d+)\b")
"""Match: character:12345"""

TITLE_REF: re.Pattern[str] = re.compile(r"\btitle:([a-zA-Z]\w*)\b")
"""Match: title:e_horde"""

EFFECT_CALL: re.Pattern[str] = re.compile(r"\b(\w+_effect)\s*=\s*(?:yes|\{)")
"""Match: scripted_effect = yes or scripted_effect = { ... }"""

MODIFIER_NAME: re.Pattern[str] = re.compile(
    r"(?:has_\w+_modifier|remove_\w+_modifier)\s*=\s*(\w+)"
    r"|(?<!\w)modifier\s*=\s*(\w+_modifier)\b"
)
"""Match: has_X_modifier = name, remove_Y_modifier = name, or modifier = name_modifier"""

EVENT_HEADER: re.Pattern[str] = re.compile(r"^(\w+\.\d+)\s*=\s*\{", re.MULTILINE)
"""Match: event ID with dot (e.g. wc_horde_invasion.1004 = {)"""

EFFECT_HEADER: re.Pattern[str] = re.compile(r"^([a-z]\w+)\s*=\s*\{", re.MULTILINE)
"""Match: scripted effect header (lowercase start, e.g. spawn_orc_troops_based_on_culture_effect = {)"""

CK3_BUILTIN_EFFECTS: frozenset[str] = frozenset({
    "hidden_effect",
    "random_effect",
    "custom_tooltip_effect",
})
"""CK3 built-in keywords that look like effects but are not scripted_effects."""


def extract_blocks(text: str, header_re: re.Pattern[str]) -> list[Block]:
    """Extract all top-level Jomini blocks matching header_re.

    Uses a brace-depth state machine identical to the duplicated
    extract_event_blocks() / extract_effect_blocks() functions.

    Args:
        text: Full file content.
        header_re: Compiled regex with group(1) = block ID or name.

    Returns:
        List of Block objects with id, raw content, and 1-based line numbers.
    """
    blocks: list[Block] = []

    for match in header_re.finditer(text):
        block_id = match.group(1)
        start_pos = match.end()  # position after opening '{'
        line_start = text[:match.start()].count("\n") + 1

        # Brace-depth state machine: find closing '}'
        depth = 1
        i = start_pos
        while i < len(text) and depth > 0:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1

        raw = text[start_pos : i - 1]
        blocks.append(Block(id=block_id, raw=raw, line_start=line_start))

    return blocks
