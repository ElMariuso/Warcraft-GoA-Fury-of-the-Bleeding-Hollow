"""
Unit tests for generate_events.py render functions.

Tests cover: ai_chance, options, after, mtth, portraits, and full event rendering.
All tests use inline fixtures; no conftest.
"""

import sys
from pathlib import Path

# sys.path.insert pattern for running from tests/
sys.path.insert(0, str(Path(__file__).parent.parent / "hansel-tools"))

from _schema import (
    AiChanceMod,
    AiValueMod,
    EventFileSpec,
    EventSpec,
    MtthMod,
    MtthSpec,
    OptionSpec,
    PortraitSpec,
    StressImpact,
)
from generate_events import (
    render_ai_chance,
    render_after,
    render_event,
    render_mtth,
    render_option,
    render_portrait,
)


# ============================================================================
# Tests: render_ai_chance
# ============================================================================


def test_render_ai_chance_base_only() -> None:
    """ai_chance with base value only."""
    opt = OptionSpec(key="a", label="Test", ai_chance_base=50)
    result = render_ai_chance(opt)
    assert "base = 50" in result
    assert "ai_chance = {" in result
    assert "modifier = {" not in result


def test_render_ai_chance_with_modifiers() -> None:
    """ai_chance with base + multiple modifiers."""
    mod1 = AiChanceMod(condition="has_trait = ambitious", add=100)
    mod2 = AiChanceMod(condition="is_at_war = yes", factor=0.5)

    opt = OptionSpec(
        key="b",
        label="Test",
        ai_chance_base=100,
        ai_chance_mods=(mod1, mod2),
    )
    result = render_ai_chance(opt)
    assert "base = 100" in result
    assert "has_trait = ambitious" in result
    assert "add = 100" in result
    assert "is_at_war = yes" in result
    assert "factor = 0.5" in result


def test_render_ai_chance_with_ai_value_modifier() -> None:
    """ai_chance with ai_value_modifier (personality weights)."""
    avm = AiValueMod(values=(("ai_boldness", 2.0), ("ai_honor", -1.0)))
    opt = OptionSpec(
        key="c",
        label="Test",
        ai_chance_base=100,
        ai_value_mod=avm,
    )
    result = render_ai_chance(opt)
    assert "ai_value_modifier = {" in result
    assert "ai_boldness = 2.0" in result
    assert "ai_honor = -1.0" in result


def test_render_ai_chance_complex() -> None:
    """ai_chance with all components."""
    mod = AiChanceMod(condition="has_trait = brave", add=200)
    avm = AiValueMod(values=(("ai_boldness", 1.5),))
    opt = OptionSpec(
        key="d",
        label="Test",
        ai_chance_base=100,
        ai_chance_mods=(mod,),
        ai_value_mod=avm,
    )
    result = render_ai_chance(opt)
    assert "base = 100" in result
    assert "has_trait = brave" in result
    assert "add = 200" in result
    assert "ai_boldness = 1.5" in result


# ============================================================================
# Tests: render_option
# ============================================================================


def test_render_option_minimal() -> None:
    """Minimal option with just key and label."""
    opt = OptionSpec(key="a", label="Accept")
    txt, locs = render_option(opt, "wc_test", 1000)

    assert "option = {" in txt
    assert "name = wc_test.1000.a" in txt
    assert "fallback = yes" not in txt

    # Localization
    assert ("wc_test.1000.a", "Accept") in locs


def test_render_option_with_trigger() -> None:
    """Option with trigger condition."""
    opt = OptionSpec(
        key="b",
        label="For brave only",
        trigger="has_trait = brave",
    )
    txt, locs = render_option(opt, "wc_test", 1000)

    assert "trigger = { has_trait = brave }" in txt


def test_render_option_with_show_as() -> None:
    """Option with show_as_unavailable and show_as_tooltip."""
    opt = OptionSpec(
        key="c",
        label="Risky choice",
        show_as_unavailable="is_at_war = no",
        show_as_tooltip="add_prestige = 500",
    )
    txt, locs = render_option(opt, "wc_test", 1000)

    assert "show_as_unavailable = { is_at_war = no }" in txt
    assert "show_as_tooltip = { add_prestige = 500 }" in txt


def test_render_option_with_custom_tooltip() -> None:
    """Option with custom_tooltip."""
    opt = OptionSpec(
        key="d",
        label="Special",
        custom_tooltip="wc_test.1000.d_tip",
    )
    txt, locs = render_option(opt, "wc_test", 1000)

    assert "custom_tooltip = wc_test.1000.d_tip" in txt


def test_render_option_with_stress_impact() -> None:
    """Option with stress_impact."""
    si1 = StressImpact(trait="coward", level="medium_stress_impact_gain")
    si2 = StressImpact(trait="brave", level="minor_stress_impact_loss")

    opt = OptionSpec(
        key="e",
        label="Courageous act",
        stress_impact=(si1, si2),
    )
    txt, locs = render_option(opt, "wc_test", 1000)

    assert "stress_impact = { coward = medium_stress_impact_gain }" in txt
    assert "stress_impact = { brave = minor_stress_impact_loss }" in txt


def test_render_option_with_flavor() -> None:
    """Option with flavor text."""
    opt = OptionSpec(
        key="f",
        label="Go forward",
        flavor="Into the fray!",
    )
    txt, locs = render_option(opt, "wc_test", 1000)

    assert ("wc_test.1000.f_flavor", "Into the fray!") in locs


def test_render_option_fallback() -> None:
    """Option with fallback flag."""
    opt = OptionSpec(
        key="g",
        label="Default",
        fallback=True,
    )
    txt, locs = render_option(opt, "wc_test", 1000)

    assert "fallback = yes" in txt


def test_render_option_with_effects() -> None:
    """Option with multiple effects."""
    opt = OptionSpec(
        key="h",
        label="Grant reward",
        effects=("add_prestige = 100", "add_gold = 50"),
    )
    txt, locs = render_option(opt, "wc_test", 1000)

    assert "add_prestige = 100" in txt
    assert "add_gold = 50" in txt


# ============================================================================
# Tests: render_after
# ============================================================================


def test_render_after_empty() -> None:
    """render_after with no lines."""
    result = render_after(())
    assert result == ""


def test_render_after_single_line() -> None:
    """render_after with one line."""
    result = render_after(("trigger_event = { id = wc_test.1001 }",))

    assert "after = {" in result
    assert "trigger_event = { id = wc_test.1001 }" in result


def test_render_after_multiple_lines() -> None:
    """render_after with multiple lines."""
    lines = (
        "trigger_event = { id = wc_test.1001  days = 3 }",
        "add_prestige = 100",
    )
    result = render_after(lines)

    assert "after = {" in result
    assert "trigger_event = { id = wc_test.1001  days = 3 }" in result
    assert "add_prestige = 100" in result


# ============================================================================
# Tests: render_mtth
# ============================================================================


def test_render_mtth_no_modifiers() -> None:
    """Mean time to happen without modifiers."""
    spec = MtthSpec(months=24)
    result = render_mtth(spec)

    assert "mean_time_to_happen = {" in result
    assert "months = 24" in result
    assert "modifier = {" not in result


def test_render_mtth_with_modifiers() -> None:
    """Mean time to happen with modifiers."""
    mod1 = MtthMod(condition="has_trait = ambitious", factor=0.5)
    mod2 = MtthMod(condition="is_at_war = yes", add=12)

    spec = MtthSpec(months=24, modifiers=(mod1, mod2))
    result = render_mtth(spec)

    assert "months = 24" in result
    assert "has_trait = ambitious" in result
    assert "factor = 0.5" in result
    assert "is_at_war = yes" in result
    assert "add = 12" in result


# ============================================================================
# Tests: render_portrait
# ============================================================================


def test_render_portrait_default() -> None:
    """Portrait with default character and animation."""
    p = PortraitSpec()
    result = render_portrait(p, "left")

    assert "left_portrait = { character = root  animation = idle }" in result


def test_render_portrait_custom() -> None:
    """Portrait with custom character and animation."""
    p = PortraitSpec(character="scope:kilrogg", animation="personality_bold")
    result = render_portrait(p, "right")

    assert "right_portrait = { character = scope:kilrogg  animation = personality_bold }" in result


# ============================================================================
# Tests: render_event (integration)
# ============================================================================


def test_render_event_minimal() -> None:
    """Minimal event with required fields only."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1000,
        title="Test Event",
        desc="A test event.",
        options=(opt,),
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    # Event structure
    assert "wc_test.1000 = {" in txt
    assert "type = character_event" in txt
    assert "hidden = yes" not in txt
    assert "content_source = dlc_GOA" in txt

    # Localization
    assert ("wc_test.1000.title", "Test Event") in locs
    assert ("wc_test.1000.desc", "A test event.") in locs


def test_render_event_hidden() -> None:
    """Hidden event (no content_source)."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=2000,
        title="Hidden",
        desc="Secret",
        options=(opt,),
        hidden=True,
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "hidden = yes" in txt
    # content_source should NOT appear for hidden events
    assert "content_source = dlc_GOA" not in txt


def test_render_event_with_scope() -> None:
    """Event with explicit scope."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1001,
        title="Scoped",
        desc="Has scope.",
        options=(opt,),
        scope="none",
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "scope = none" in txt


def test_render_event_with_background() -> None:
    """Event with background override."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1002,
        title="Scenic",
        desc="Has background.",
        options=(opt,),
        background="wc_background_stranglethorn",
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "override_background = { reference = wc_background_stranglethorn }" in txt


def test_render_event_with_portraits() -> None:
    """Event with all three portrait sides."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1003,
        title="Scenic",
        desc="Multiple portraits.",
        options=(opt,),
        left_portrait=PortraitSpec(character="root", animation="idle"),
        right_portrait=PortraitSpec(character="scope:other", animation="thinking"),
        lower_right_portrait=PortraitSpec(character="root", animation="happy"),
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "left_portrait = {" in txt
    assert "right_portrait = {" in txt
    assert "lower_right_portrait = {" in txt


def test_render_event_with_cooldown() -> None:
    """Event with cooldown."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1004,
        title="Rare",
        desc="Has cooldown.",
        options=(opt,),
        cooldown_years=2,
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "cooldown = { years = 2 }" in txt


def test_render_event_with_trigger() -> None:
    """Event with trigger conditions."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1005,
        title="Conditional",
        desc="Needs conditions.",
        options=(opt,),
        trigger=("has_title = k_bleeding_hollow_clan", "is_at_war = yes"),
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "trigger = {" in txt
    assert "has_title = k_bleeding_hollow_clan" in txt
    assert "is_at_war = yes" in txt


def test_render_event_with_immediate() -> None:
    """Event with immediate block."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1006,
        title="Setup",
        desc="Has immediate effects.",
        options=(opt,),
        immediate=("add_prestige = 100", "create_story = story_test"),
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "immediate = {" in txt
    assert "add_prestige = 100" in txt
    assert "create_story = story_test" in txt


def test_render_event_with_mtth() -> None:
    """Event with mean_time_to_happen."""
    opt = OptionSpec(key="a", label="OK")
    mtth = MtthSpec(months=24, modifiers=(MtthMod(condition="is_at_war = yes", factor=0.5),))
    event = EventSpec(
        id=2001,
        title="Random",
        desc="Happens randomly.",
        options=(opt,),
        mean_time_to_happen=mtth,
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "mean_time_to_happen = {" in txt
    assert "months = 24" in txt


def test_render_event_with_after() -> None:
    """Event with after block."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1007,
        title="Chain",
        desc="Triggers next event.",
        options=(opt,),
        after=("trigger_event = { id = wc_test.1008  days = 5 }",),
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "after = {" in txt
    assert "trigger_event = { id = wc_test.1008  days = 5 }" in txt


def test_render_event_with_theme() -> None:
    """Event with non-default theme."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1008,
        title="Epic",
        desc="Epic battle.",
        options=(opt,),
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "martial")

    assert "theme = martial" in txt


def test_render_event_canonical_order() -> None:
    """Verify canonical field ordering."""
    mod = AiChanceMod(condition="has_trait = brave", add=100)
    opt1 = OptionSpec(key="a", label="Go", ai_chance_mods=(mod,))
    opt2 = OptionSpec(key="b", label="Wait", fallback=True)

    mtth = MtthSpec(months=12)
    event = EventSpec(
        id=3000,
        title="Complex",
        desc="Full event.",
        type="character_event",
        hidden=False,
        scope="none",
        background="wc_bg",
        trigger=("has_title = k_test",),
        immediate=("add_prestige = 50",),
        after=("trigger_event = { id = wc_test.3001 }",),
        mean_time_to_happen=mtth,
        options=(opt1, opt2),
        left_portrait=PortraitSpec(character="root", animation="idle"),
        cooldown_years=1,
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    # Find positions of key sections
    pos_type = txt.find("type = character_event")
    pos_scope = txt.find("scope = none")
    pos_title = txt.find("title = wc_test.3000.title")
    pos_bg = txt.find("override_background")
    pos_portrait = txt.find("left_portrait")
    pos_cooldown = txt.find("cooldown")
    pos_trigger = txt.find("trigger = {")
    pos_mtth = txt.find("mean_time_to_happen")
    pos_immediate = txt.find("immediate = {")
    pos_option = txt.find("option = {")
    pos_after = txt.find("after = {")

    # Verify ordering (each position should be greater than previous)
    assert pos_type < pos_scope < pos_title < pos_bg < pos_portrait
    assert pos_portrait < pos_cooldown < pos_trigger < pos_mtth
    assert pos_mtth < pos_immediate < pos_option < pos_after


# ============================================================================
# Tests: integration with _schema
# ============================================================================


def test_render_event_window_fullscreen() -> None:
    """window: fullscreen_event → window = fullscreen_event dans l'output."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1000,
        title="Test",
        desc="Test desc.",
        options=(opt,),
        window="fullscreen_event",
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "window = fullscreen_event" in txt


def test_render_event_window_absent_by_default() -> None:
    """Sans window, pas de ligne window dans l'output."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1000,
        title="Test",
        desc="Test desc.",
        options=(opt,),
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "window" not in txt


def test_render_event_lower_left_portrait() -> None:
    """lower_left_portrait rendu correctement."""
    opt = OptionSpec(key="a", label="OK")
    event = EventSpec(
        id=1000,
        title="Test",
        desc="Test desc.",
        options=(opt,),
        lower_left_portrait=PortraitSpec(character="scope:warchief", animation="anger"),
    )

    txt, locs = render_event(event, "wc_test", "dlc_GOA", "default")

    assert "lower_left_portrait = { character = scope:warchief  animation = anger }" in txt


def test_render_full_file_spec() -> None:
    """Full integration: parse_spec + render."""
    opt1 = OptionSpec(key="a", label="Yes")
    opt2 = OptionSpec(key="b", label="No", fallback=True)

    event1 = EventSpec(
        id=1000,
        title="First event",
        desc="First description.",
        options=(opt1, opt2),
    )

    event2 = EventSpec(
        id=2000,
        title="Second event",
        desc="Second description.",
        options=(opt1,),
        mean_time_to_happen=MtthSpec(months=12),
    )

    file_spec = EventFileSpec(
        namespace="wc_test_full",
        theme="default",
        content_source="dlc_GOA",
        events=(event1, event2),
    )

    # Render
    txt_lines = []
    txt_lines.append(f"namespace = {file_spec.namespace}")
    txt_lines.append("")

    for event in file_spec.events:
        event_txt, _ = render_event(event, file_spec.namespace, file_spec.content_source, file_spec.theme)
        txt_lines.append(event_txt)
        txt_lines.append("")

    full_txt = "\n".join(txt_lines)

    assert "namespace = wc_test_full" in full_txt
    assert "wc_test_full.1000 = {" in full_txt
    assert "wc_test_full.2000 = {" in full_txt
