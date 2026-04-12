"""tests/test_schema.py — Tests for _schema.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "hansel-tools"))

import pytest

from _schema import (
    parse_spec,
    EventFileSpec,
)


def test_minimal_valid_spec():
    """Parse minimal valid spec with only required fields."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test Event",
                "desc": "Test description",
                "options": [
                    {
                        "key": "a",
                        "label": "Option A",
                    }
                ],
            }
        ],
    }

    spec = parse_spec(data)

    assert isinstance(spec, EventFileSpec)
    assert spec.namespace == "wc_test"
    assert spec.theme == "default"
    assert spec.content_source == "dlc_GOA"
    assert len(spec.events) == 1

    event = spec.events[0]
    assert event.id == 1000
    assert event.title == "Test Event"
    assert event.desc == "Test description"
    assert len(event.options) == 1
    assert event.options[0].key == "a"
    assert event.options[0].label == "Option A"
    assert event.options[0].ai_chance_base == 100


def test_full_spec_all_fields():
    """Parse spec with all optional fields included."""
    data = {
        "namespace": "wc_full_test",
        "theme": "martial",
        "content_source": "dlc_custom",
        "events": [
            {
                "id": 1001,
                "title": "Full Event",
                "desc": "Full description",
                "type": "letter_event",
                "hidden": False,
                "scope": "character",
                "background": "wc_background_test",
                "cooldown_years": 5,
                "trigger": [
                    "has_trait = ambitious",
                    "is_alive = yes",
                ],
                "immediate": [
                    "save_scope_as = test_scope",
                ],
                "after": [
                    "add_prestige = 100",
                ],
                "mean_time_to_happen": {
                    "months": 12,
                    "modifiers": [
                        {"condition": "is_at_war = yes", "factor": 0.5},
                        {"condition": "has_trait = ambitious", "add": 3},
                    ],
                },
                "left_portrait": {
                    "character": "root",
                    "animation": "personality_bold",
                },
                "right_portrait": {
                    "character": "scope:other_char",
                    "animation": "idle",
                },
                "desc_variants": [
                    {"trigger": "has_trait = ambitious", "key": "wc_full_test.1001.desc_ambitious"},
                    {"trigger": "always = yes", "key": None},
                ],
                "title_variants": [
                    {"trigger": "is_female = yes", "key": "wc_full_test.1001.title_female"},
                ],
                "options": [
                    {
                        "key": "a",
                        "label": "Complex Option",
                        "ai_chance": {
                            "base": 200,
                            "modifiers": [
                                {"condition": "has_trait = ambitious", "add": 50},
                                {"condition": "is_at_war = yes", "factor": 2.0},
                            ],
                            "ai_value_modifier": {
                                "ai_boldness": 0.8,
                                "ai_compassion": -0.5,
                            },
                        },
                        "flavor": "Test flavor text",
                        "trigger": "has_trait = brave",
                        "effects": [
                            "add_prestige = large_prestige_gain",
                            "add_stress = -10",
                        ],
                        "show_as_tooltip": "add_prestige = large_prestige_gain",
                        "show_as_unavailable": "is_imprisoned = yes",
                        "custom_tooltip": "custom_tt",
                        "stress_impact": [
                            {"trait": "shy", "level": "minor"},
                            {"trait": "paranoid", "level": "major"},
                        ],
                    }
                ],
            }
        ],
    }

    spec = parse_spec(data)

    assert spec.namespace == "wc_full_test"
    assert spec.theme == "martial"
    assert spec.content_source == "dlc_custom"

    event = spec.events[0]
    assert event.id == 1001
    assert event.type == "letter_event"
    assert event.hidden is False
    assert event.scope == "character"
    assert event.background == "wc_background_test"
    assert event.cooldown_years == 5
    assert event.trigger == ("has_trait = ambitious", "is_alive = yes")
    assert event.immediate == ("save_scope_as = test_scope",)
    assert event.after == ("add_prestige = 100",)

    # Check MTTH
    assert event.mean_time_to_happen is not None
    assert event.mean_time_to_happen.months == 12
    assert len(event.mean_time_to_happen.modifiers) == 2
    assert event.mean_time_to_happen.modifiers[0].condition == "is_at_war = yes"
    assert event.mean_time_to_happen.modifiers[0].factor == 0.5
    assert event.mean_time_to_happen.modifiers[1].add == 3

    # Check portraits
    assert event.left_portrait is not None
    assert event.left_portrait.character == "root"
    assert event.left_portrait.animation == "personality_bold"
    assert event.right_portrait is not None
    assert event.right_portrait.character == "scope:other_char"

    # Check variants
    assert len(event.desc_variants) == 2
    assert event.desc_variants[0].key == "wc_full_test.1001.desc_ambitious"
    assert event.desc_variants[1].key is None
    assert len(event.title_variants) == 1
    assert event.title_variants[0].key == "wc_full_test.1001.title_female"

    # Check option
    option = event.options[0]
    assert option.key == "a"
    assert option.label == "Complex Option"
    assert option.ai_chance_base == 200
    assert len(option.ai_chance_mods) == 2
    assert option.ai_chance_mods[0].condition == "has_trait = ambitious"
    assert option.ai_chance_mods[0].add == 50
    assert option.ai_chance_mods[1].factor == 2.0
    assert option.ai_value_mod is not None
    assert len(option.ai_value_mod.values) == 2
    assert option.flavor == "Test flavor text"
    assert option.trigger == "has_trait = brave"
    assert option.show_as_tooltip == "add_prestige = large_prestige_gain"
    assert option.show_as_unavailable == "is_imprisoned = yes"
    assert option.custom_tooltip == "custom_tt"
    assert len(option.stress_impact) == 2
    assert option.stress_impact[0].trait == "shy"
    assert option.stress_impact[0].level == "minor"


def test_missing_namespace_raises():
    """Missing namespace should raise ValueError."""
    data = {
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
            }
        ],
    }

    with pytest.raises(ValueError, match="namespace.*required"):
        parse_spec(data)


def test_missing_option_key_raises():
    """Option without key should raise ValueError."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [
                    {
                        "label": "No Key",
                    }
                ],
            }
        ],
    }

    with pytest.raises(ValueError, match="key.*required"):
        parse_spec(data)


def test_old_ai_chance_int_format():
    """Backwards compatible: ai_chance as int becomes ai_chance_base."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [
                    {
                        "key": "a",
                        "label": "Option A",
                        "ai_chance": 75,
                    }
                ],
            }
        ],
    }

    spec = parse_spec(data)
    option = spec.events[0].options[0]

    assert option.ai_chance_base == 75
    assert len(option.ai_chance_mods) == 0


def test_new_ai_chance_dict_format():
    """Parse ai_chance as dict with base and modifiers."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [
                    {
                        "key": "a",
                        "label": "Option A",
                        "ai_chance": {
                            "base": 150,
                            "modifiers": [
                                {"condition": "has_trait = ambitious", "add": 30},
                                {"condition": "is_at_war = yes", "factor": 1.5},
                            ],
                        },
                    }
                ],
            }
        ],
    }

    spec = parse_spec(data)
    option = spec.events[0].options[0]

    assert option.ai_chance_base == 150
    assert len(option.ai_chance_mods) == 2
    assert option.ai_chance_mods[0].condition == "has_trait = ambitious"
    assert option.ai_chance_mods[0].add == 30
    assert option.ai_chance_mods[1].condition == "is_at_war = yes"
    assert option.ai_chance_mods[1].factor == 1.5


def test_invalid_ai_value_trait_raises():
    """Unknown trait in ai_value_modifier should raise ValueError."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [
                    {
                        "key": "a",
                        "label": "Option A",
                        "ai_chance": {
                            "base": 100,
                            "ai_value_modifier": {
                                "ai_boldness": 0.5,
                                "ai_invalid_trait": 0.3,
                            },
                        },
                    }
                ],
            }
        ],
    }

    with pytest.raises(ValueError, match="unknown trait.*ai_invalid_trait"):
        parse_spec(data)


def test_after_field_parsed():
    """after field: list of strings parsed to tuple."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
                "after": [
                    "add_prestige = 100",
                    "add_stress = -10",
                ],
            }
        ],
    }

    spec = parse_spec(data)
    event = spec.events[0]

    assert event.after == ("add_prestige = 100", "add_stress = -10")


def test_mtth_with_modifiers():
    """mean_time_to_happen with condition factors."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
                "mean_time_to_happen": {
                    "months": 24,
                    "modifiers": [
                        {"condition": "is_at_war = yes", "factor": 0.5},
                        {"condition": "has_opinion = { target = scope:other modifier = sympathetic }", "factor": 2.0},
                    ],
                },
            }
        ],
    }

    spec = parse_spec(data)
    event = spec.events[0]

    assert event.mean_time_to_happen is not None
    assert event.mean_time_to_happen.months == 24
    assert len(event.mean_time_to_happen.modifiers) == 2
    assert event.mean_time_to_happen.modifiers[0].condition == "is_at_war = yes"
    assert event.mean_time_to_happen.modifiers[0].factor == 0.5
    assert event.mean_time_to_happen.modifiers[1].factor == 2.0


def test_mtth_as_int():
    """mean_time_to_happen as simple int (just months)."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
                "mean_time_to_happen": 18,
            }
        ],
    }

    spec = parse_spec(data)
    event = spec.events[0]

    assert event.mean_time_to_happen is not None
    assert event.mean_time_to_happen.months == 18
    assert len(event.mean_time_to_happen.modifiers) == 0


def test_multiple_events():
    """Parse spec with multiple events."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "First",
                "desc": "First desc",
                "options": [{"key": "a", "label": "A"}],
            },
            {
                "id": 2000,
                "title": "Second",
                "desc": "Second desc",
                "options": [{"key": "a", "label": "A"}],
            },
        ],
    }

    spec = parse_spec(data)

    assert len(spec.events) == 2
    assert spec.events[0].id == 1000
    assert spec.events[1].id == 2000


def test_portrait_with_defaults():
    """Portrait with default character and animation."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
                "left_portrait": {"animation": "thinking"},
            }
        ],
    }

    spec = parse_spec(data)
    portrait = spec.events[0].left_portrait

    assert portrait is not None
    assert portrait.character == "root"
    assert portrait.animation == "thinking"


def test_stress_impact_as_dicts():
    """Parse stress_impact with dict format."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [
                    {
                        "key": "a",
                        "label": "A",
                        "stress_impact": [
                            {"trait": "shy", "level": "minor"},
                            {"trait": "brave", "level": "major"},
                        ],
                    }
                ],
            }
        ],
    }

    spec = parse_spec(data)
    option = spec.events[0].options[0]

    assert len(option.stress_impact) == 2
    assert option.stress_impact[0].trait == "shy"
    assert option.stress_impact[0].level == "minor"
    assert option.stress_impact[1].trait == "brave"
    assert option.stress_impact[1].level == "major"


def test_effects_as_mixed_list():
    """Parse effects as list with strings and dicts."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [
                    {
                        "key": "a",
                        "label": "A",
                        "effects": [
                            "add_stress = -10",
                            {"add_prestige": "medium_prestige_gain"},
                        ],
                    }
                ],
            }
        ],
    }

    spec = parse_spec(data)
    option = spec.events[0].options[0]

    assert len(option.effects) == 2
    assert "add_stress = -10" in option.effects
    assert "add_prestige = medium_prestige_gain" in option.effects


def test_desc_variant_with_auto_key():
    """desc_variant with key=None (auto-generate)."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
                "desc_variants": [
                    {"trigger": "always = yes"},
                ],
            }
        ],
    }

    spec = parse_spec(data)
    variant = spec.events[0].desc_variants[0]

    assert variant.trigger == "always = yes"
    assert variant.key is None


def test_invalid_ai_chance_type_raises():
    """ai_chance with invalid type should raise ValueError."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [
                    {
                        "key": "a",
                        "label": "A",
                        "ai_chance": "invalid",
                    }
                ],
            }
        ],
    }

    with pytest.raises(ValueError, match="ai_chance.*must be int or dict"):
        parse_spec(data)


def test_missing_event_title_raises():
    """Event without title should raise ValueError."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
            }
        ],
    }

    with pytest.raises(ValueError, match="title.*required"):
        parse_spec(data)


def test_missing_event_desc_raises():
    """Event without desc should raise ValueError."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "options": [{"key": "a", "label": "A"}],
            }
        ],
    }

    with pytest.raises(ValueError, match="desc.*required"):
        parse_spec(data)


def test_empty_options_list_raises():
    """Event with empty options list should raise ValueError."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [],
            }
        ],
    }

    with pytest.raises(ValueError, match="at least one option"):
        parse_spec(data)


def test_missing_option_label_raises():
    """Option without label should raise ValueError."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [
                    {
                        "key": "a",
                    }
                ],
            }
        ],
    }

    with pytest.raises(ValueError, match="label.*required"):
        parse_spec(data)


def test_fallback_flag():
    """fallback flag on option."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [
                    {
                        "key": "a",
                        "label": "A",
                        "fallback": True,
                    }
                ],
            }
        ],
    }

    spec = parse_spec(data)
    option = spec.events[0].options[0]

    assert option.fallback is True


def test_parse_event_window():
    """window parsé depuis YAML."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
                "window": "fullscreen_event",
            }
        ],
    }

    spec = parse_spec(data)
    event = spec.events[0]

    assert event.window == "fullscreen_event"


def test_parse_event_window_absent():
    """Sans window dans YAML → EventSpec.window is None."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
            }
        ],
    }

    spec = parse_spec(data)
    event = spec.events[0]

    assert event.window is None


def test_parse_event_lower_left_portrait():
    """lower_left_portrait parsé depuis YAML."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Test",
                "desc": "Test",
                "options": [{"key": "a", "label": "A"}],
                "lower_left_portrait": {
                    "character": "scope:warchief",
                    "animation": "anger",
                },
            }
        ],
    }

    spec = parse_spec(data)
    portrait = spec.events[0].lower_left_portrait

    assert portrait is not None
    assert portrait.character == "scope:warchief"
    assert portrait.animation == "anger"


def test_hidden_event():
    """Parse hidden event."""
    data = {
        "namespace": "wc_test",
        "events": [
            {
                "id": 1000,
                "title": "Hidden Event",
                "desc": "Not shown to player",
                "hidden": True,
                "options": [{"key": "a", "label": "A"}],
            }
        ],
    }

    spec = parse_spec(data)
    event = spec.events[0]

    assert event.hidden is True
