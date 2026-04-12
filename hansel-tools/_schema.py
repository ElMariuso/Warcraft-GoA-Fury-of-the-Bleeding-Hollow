"""Typed schema for the CK3 event generator YAML format.

parse_spec(data) validates a yaml.safe_load() dict and returns an EventFileSpec.
Raises ValueError with a precise message on any validation error — never KeyError.
"""

from __future__ import annotations

from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationError,
    field_validator,
    model_validator,
)

AI_VALUE_TRAITS: frozenset[str] = frozenset({
    "ai_boldness",
    "ai_compassion",
    "ai_greed",
    "ai_energy",
    "ai_honor",
    "ai_rationality",
    "ai_sociability",
    "ai_vengefulness",
    "ai_zeal",
})


class AiChanceMod(BaseModel):
    """A single ai_chance modifier block."""

    model_config = ConfigDict(frozen=True)

    condition: str
    add: int | None = None
    factor: float | None = None


class AiValueMod(BaseModel):
    """ai_value_modifier block — personality trait weights (9 traits max)."""

    model_config = ConfigDict(frozen=True)

    values: tuple[tuple[str, float], ...]

    @field_validator("values", mode="before")
    @classmethod
    def _validate_values(cls, v: Any) -> Any:
        if isinstance(v, dict):
            result: list[tuple[str, float]] = []
            for trait, value in v.items():
                if trait not in AI_VALUE_TRAITS:
                    raise ValueError(
                        f"ai_value_modifier has unknown trait '{trait}' "
                        f"(valid: {', '.join(sorted(AI_VALUE_TRAITS))})"
                    )
                if isinstance(value, bool) or not isinstance(value, (int, float)):
                    raise ValueError(
                        f"ai_value_modifier['{trait}'] must be a number, "
                        f"got {type(value).__name__}"
                    )
                result.append((trait, float(value)))
            return tuple(result)
        return v


class StressImpact(BaseModel):
    """stress_impact entry — trait and level."""

    model_config = ConfigDict(frozen=True)

    trait: str
    level: str


class OptionSpec(BaseModel):
    """A single event option."""

    model_config = ConfigDict(frozen=True)

    key: str
    label: str
    ai_chance_base: int = 100
    ai_chance_mods: tuple[AiChanceMod, ...] = ()
    ai_value_mod: AiValueMod | None = None
    effects: tuple[str, ...] = ()
    trigger: str | None = None
    show_as_unavailable: str | None = None
    show_as_tooltip: str | None = None
    custom_tooltip: str | None = None
    stress_impact: tuple[StressImpact, ...] = ()
    flavor: str = ""
    fallback: bool = False

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError(f"option must be a dict, got {type(data).__name__}")
        data = dict(data)

        key = data.get("key")
        if not key:
            raise ValueError("option field 'key' is required")
        if not isinstance(key, str):
            raise ValueError(
                f"option field 'key' must be str, got {type(key).__name__}"
            )

        label = data.get("label")
        if not label:
            raise ValueError(
                f"option (key={key}) field 'label' is required"
            )
        if not isinstance(label, str):
            raise ValueError(
                f"option (key={key}) field 'label' must be str, got {type(label).__name__}"
            )

        # Backward-compat ai_chance: int → ai_chance_base, dict → base + modifiers + avm
        if "ai_chance" in data:
            ai_chance = data.pop("ai_chance")
            if isinstance(ai_chance, bool) or not isinstance(ai_chance, (int, dict)):
                raise ValueError(
                    f"option (key={key}) field 'ai_chance' must be int or dict, "
                    f"got {type(ai_chance).__name__}"
                )
            if isinstance(ai_chance, int):
                data["ai_chance_base"] = ai_chance
            else:
                base = ai_chance.get("base")
                if base is not None:
                    if isinstance(base, bool) or not isinstance(base, int):
                        raise ValueError(
                            f"option (key={key}) field 'ai_chance.base' must be int, "
                            f"got {type(base).__name__}"
                        )
                    data["ai_chance_base"] = base

                mods_list = ai_chance.get("modifiers", [])
                if not isinstance(mods_list, list):
                    raise ValueError(
                        f"option (key={key}) field 'ai_chance.modifiers' must be a list"
                    )
                data["ai_chance_mods"] = mods_list

                avm_data = ai_chance.get("ai_value_modifier")
                if avm_data is not None:
                    if not isinstance(avm_data, dict):
                        raise ValueError(
                            f"option (key={key}) field 'ai_value_modifier' must be a dict"
                        )
                    data["ai_value_mod"] = {"values": avm_data}

        # Normalize effects: list/tuple of str or single-key dicts → list of str
        if "effects" in data:
            effects_raw = data["effects"]
            if isinstance(effects_raw, tuple):
                effects_raw = list(effects_raw)
                data["effects"] = effects_raw
            if not isinstance(effects_raw, list):
                raise ValueError(
                    f"option (key={key}) field 'effects' must be a list"
                )
            normalized_effects: list[str] = []
            for idx, item in enumerate(effects_raw):
                if isinstance(item, str):
                    normalized_effects.append(item)
                elif isinstance(item, dict):
                    for eff_name, eff_val in item.items():
                        normalized_effects.append(f"{eff_name} = {eff_val}")
                else:
                    raise ValueError(
                        f"option (key={key}) effect [{idx}] must be str or dict"
                    )
            data["effects"] = normalized_effects

        # Normalize stress_impact: list/tuple of dict or (trait, level) pairs → list of dict
        if "stress_impact" in data:
            si_raw = data["stress_impact"]
            if isinstance(si_raw, tuple):
                si_raw = list(si_raw)
                data["stress_impact"] = si_raw
            if not isinstance(si_raw, list):
                raise ValueError(
                    f"option (key={key}) field 'stress_impact' must be a list"
                )
            normalized_si: list[dict[str, str]] = []
            for idx, item in enumerate(si_raw):
                if isinstance(item, dict):
                    trait = item.get("trait")
                    level = item.get("level")
                    if not trait or not isinstance(trait, str):
                        raise ValueError(
                            f"option (key={key}) stress_impact [{idx}] field 'trait' "
                            f"must be a non-empty str"
                        )
                    if not level or not isinstance(level, str):
                        raise ValueError(
                            f"option (key={key}) stress_impact [{idx}] field 'level' "
                            f"must be a non-empty str"
                        )
                    normalized_si.append({"trait": trait, "level": level})
                elif isinstance(item, tuple) and len(item) == 2:
                    normalized_si.append(
                        {"trait": str(item[0]), "level": str(item[1])}
                    )
                elif hasattr(item, "trait") and hasattr(item, "level"):
                    # Already a StressImpact instance — pass through as dict
                    normalized_si.append({"trait": item.trait, "level": item.level})
                else:
                    raise ValueError(
                        f"option (key={key}) stress_impact [{idx}] must be a dict or tuple"
                    )
            data["stress_impact"] = normalized_si

        return data


class DescVariant(BaseModel):
    """A desc_variants entry."""

    model_config = ConfigDict(frozen=True)

    trigger: str
    key: str | None = None


class PortraitSpec(BaseModel):
    """A portrait (left, right, lower_right, lower_left)."""

    model_config = ConfigDict(frozen=True)

    character: str = "root"
    animation: str = "idle"


class MtthMod(BaseModel):
    """A single modifier in mean_time_to_happen.modifiers."""

    model_config = ConfigDict(frozen=True)

    condition: str
    add: int | None = None
    factor: float | None = None


class MtthSpec(BaseModel):
    """mean_time_to_happen block."""

    model_config = ConfigDict(frozen=True)

    months: int
    modifiers: tuple[MtthMod, ...] = ()


class EventSpec(BaseModel):
    """A single event definition."""

    model_config = ConfigDict(frozen=True)

    id: int
    title: str
    desc: str
    options: tuple[OptionSpec, ...]
    type: str = "character_event"
    hidden: bool = False
    scope: str | None = None
    background: str | None = None
    trigger: tuple[str, ...] = ()
    immediate: tuple[str, ...] = ()
    after: tuple[str, ...] = ()
    mean_time_to_happen: MtthSpec | None = None
    desc_variants: tuple[DescVariant, ...] = ()
    title_variants: tuple[DescVariant, ...] = ()
    left_portrait: PortraitSpec | None = None
    right_portrait: PortraitSpec | None = None
    lower_right_portrait: PortraitSpec | None = None
    lower_left_portrait: PortraitSpec | None = None
    window: str | None = None
    cooldown_years: int | None = None

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError(f"event must be a dict, got {type(data).__name__}")
        data = dict(data)

        event_id = data.get("id")
        if event_id is None:
            raise ValueError("event field 'id' is required")
        if isinstance(event_id, bool) or not isinstance(event_id, int):
            raise ValueError(
                f"event field 'id' must be int, got {type(event_id).__name__}"
            )

        if not data.get("title"):
            raise ValueError(
                f"event (id={event_id}) field 'title' is required"
            )
        if not data.get("desc"):
            raise ValueError(
                f"event (id={event_id}) field 'desc' is required"
            )

        options_list = data.get("options")
        if options_list is None:
            raise ValueError(
                f"event (id={event_id}) field 'options' is required"
            )
        if isinstance(options_list, tuple):
            data["options"] = list(options_list)
            options_list = data["options"]
        if not isinstance(options_list, list):
            raise ValueError(
                f"event (id={event_id}) field 'options' must be a list, "
                f"got {type(options_list).__name__}"
            )
        if not options_list:
            raise ValueError(
                f"event (id={event_id}) must have at least one option"
            )

        # Backward-compat mean_time_to_happen: int → {"months": int}
        if "mean_time_to_happen" in data:
            mtth = data["mean_time_to_happen"]
            if mtth is None:
                pass
            elif isinstance(mtth, bool):
                raise ValueError(
                    f"event (id={event_id}) field 'mean_time_to_happen' "
                    f"must be int, dict, or null, got bool"
                )
            elif isinstance(mtth, int):
                data["mean_time_to_happen"] = {"months": mtth}
            elif hasattr(mtth, "months"):
                # Already an MtthSpec instance — pass through as dict
                data["mean_time_to_happen"] = mtth.model_dump()
            elif not isinstance(mtth, dict):
                raise ValueError(
                    f"event (id={event_id}) field 'mean_time_to_happen' "
                    f"must be int, dict, or null, got {type(mtth).__name__}"
                )

        return data


class EventFileSpec(BaseModel):
    """Top-level event file specification."""

    model_config = ConfigDict(frozen=True)

    namespace: str
    theme: str = "default"
    content_source: str = "dlc_GOA"
    events: tuple[EventSpec, ...] = ()

    @model_validator(mode="before")
    @classmethod
    def _normalize(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            raise ValueError("spec must be a dict")
        data = dict(data)
        if not data.get("namespace"):
            raise ValueError("field 'namespace' is required")
        return data


def parse_spec(data: dict[str, object]) -> EventFileSpec:
    """Parse a yaml.safe_load() dict into EventFileSpec.

    Raises ValueError (never KeyError) on any validation error.
    Backwards compatible: old ai_chance as int → ai_chance_base.
    """
    try:
        return EventFileSpec.model_validate(data)
    except ValidationError as e:
        raise ValueError(str(e)) from e
