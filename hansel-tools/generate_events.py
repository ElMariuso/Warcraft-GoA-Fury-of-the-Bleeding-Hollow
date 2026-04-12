#!/usr/bin/env python3
"""
CK3 Event Generator — renders Jomini event definitions from YAML templates.

Uses _schema.py for typed parsing, generates strict Jomini syntax with proper
indentation, BOM-encoded localization, and correct event block ordering.
"""

import sys
from pathlib import Path

# sys.path.insert pattern for running from project root
sys.path.insert(0, str(Path(__file__).parent))

import yaml
from _schema import (
    EventFileSpec,
    EventSpec,
    OptionSpec,
    DescVariant,
    PortraitSpec,
    MtthSpec,
    parse_spec,
)


# ============================================================================
# Pure render functions (no I/O)
# ============================================================================


def render_ai_chance(opt: OptionSpec) -> str:
    """Render ai_chance block for an option (unindented; caller adds indentation).

    Returns Jomini-formatted ai_chance block with internal nesting.
    """
    lines: list[str] = []
    lines.append("ai_chance = {")

    # base
    lines.append(f"    base = {opt.ai_chance_base}")

    # modifiers
    for mod in opt.ai_chance_mods:
        lines.append(f"    modifier = {{ {mod.condition}")
        if mod.add is not None:
            lines.append(f"        add = {mod.add}")
        if mod.factor is not None:
            lines.append(f"        factor = {mod.factor}")
        lines.append("    }")

    # ai_value_modifier
    if opt.ai_value_mod is not None:
        lines.append("    ai_value_modifier = {")
        for trait, value in opt.ai_value_mod.values:
            lines.append(f"        {trait} = {value}")
        lines.append("    }")

    lines.append("}")
    return "\n".join(lines)


def render_option(opt: OptionSpec, ns: str, eid: int) -> tuple[str, list[tuple[str, str]]]:
    """Render a single option block and return (jomini_text, localization_entries).

    Jomini block is indented 1 level (4 spaces from event root).
    Loc entries: (key, value) tuples for label, flavor, custom_tooltip.
    """
    loc_entries: list[tuple[str, str]] = []
    lines: list[str] = []

    lines.append("option = {")

    # name (required)
    loc_key_base = f"{ns}.{eid}.{opt.key}"
    lines.append(f"    name = {loc_key_base}")
    loc_entries.append((loc_key_base, opt.label))

    # trigger (optional)
    if opt.trigger is not None:
        lines.append(f"    trigger = {{ {opt.trigger} }}")

    # show_as_unavailable (optional)
    if opt.show_as_unavailable is not None:
        lines.append(f"    show_as_unavailable = {{ {opt.show_as_unavailable} }}")

    # show_as_tooltip (optional)
    if opt.show_as_tooltip is not None:
        lines.append(f"    show_as_tooltip = {{ {opt.show_as_tooltip} }}")

    # custom_tooltip (optional)
    if opt.custom_tooltip is not None:
        lines.append(f"    custom_tooltip = {opt.custom_tooltip}")

    # effects (option body)
    for effect in opt.effects:
        lines.append(f"    {effect}")

    # stress_impact (optional)
    if opt.stress_impact:
        for si in opt.stress_impact:
            lines.append(f"    stress_impact = {{ {si.trait} = {si.level} }}")

    # ai_chance
    ai_chance_text = render_ai_chance(opt)
    # Indent ai_chance block (4 spaces = 1 level inside option)
    for ac_line in ai_chance_text.split("\n"):
        lines.append(f"    {ac_line}")

    # fallback (optional)
    if opt.fallback:
        lines.append("    fallback = yes")

    lines.append("}")

    # Flavor localization (if present)
    if opt.flavor:
        flavor_key = f"{loc_key_base}_flavor"
        loc_entries.append((flavor_key, opt.flavor))

    return "\n".join(f"    {line}" for line in lines), loc_entries


def render_after(lines: tuple[str, ...]) -> str:
    """Render after block. Return empty string if no lines."""
    if not lines:
        return ""
    after_lines = ["after = {"]
    for line in lines:
        after_lines.append(f"    {line}")
    after_lines.append("}")
    return "\n".join(f"    {line}" for line in after_lines)


def render_mtth(spec: MtthSpec) -> str:
    """Render mean_time_to_happen block (indented 1 level = 4 spaces)."""
    lines: list[str] = []
    lines.append("mean_time_to_happen = {")
    lines.append(f"    months = {spec.months}")

    for mod in spec.modifiers:
        lines.append(f"    modifier = {{ {mod.condition}")
        if mod.add is not None:
            lines.append(f"        add = {mod.add}")
        if mod.factor is not None:
            lines.append(f"        factor = {mod.factor}")
        lines.append("    }")

    lines.append("}")
    return "\n".join(f"    {line}" for line in lines)


def render_portrait(p: PortraitSpec, side: str) -> str:
    """Render a portrait block (left_portrait, right_portrait, lower_right_portrait)."""
    return f"    {side}_portrait = {{ character = {p.character}  animation = {p.animation} }}"


def render_desc_or_title_variants(
    variants: tuple[DescVariant, ...],
    ns: str,
    eid: int,
    base_key_suffix: str,  # ".desc" or ".title"
) -> str:
    """Render desc_variants or title_variants as first_valid block.

    base_key_suffix: ".desc" or ".title" — used for auto-generated variant keys.
    Returns empty string if no variants.
    """
    if not variants:
        return ""

    lines: list[str] = []
    lines.append(f"{base_key_suffix[1:]} = {{")  # "desc" or "title"
    lines.append("    first_valid = {")

    for variant in variants:
        lines.append("        triggered_desc = {")
        lines.append(f"            trigger = {{ {variant.trigger} }}")
        # Auto-generate key if not provided
        if variant.key is None:
            # e.g., "wc_foo.1000.desc_0" or similar
            variant_key = f"{ns}.{eid}{base_key_suffix}_variant_{variants.index(variant)}"
        else:
            variant_key = variant.key
        lines.append(f"            {base_key_suffix[1:]} = {variant_key}")
        lines.append("        }")

    # Fallback to base key
    base_key = f"{ns}.{eid}{base_key_suffix}"
    lines.append(f"        {base_key_suffix[1:]} = {base_key}")

    lines.append("    }")
    lines.append("}")

    return "\n".join(f"    {line}" for line in lines)


def render_event(
    spec: EventSpec,
    ns: str,
    content_source: str,
    theme: str,
) -> tuple[str, list[tuple[str, str]]]:
    """Render a complete event block with canonical ordering.

    Returns (jomini_text, loc_entries).

    Canonical order:
    1. type, scope, hidden, content_source
    2. title / title_variants
    3. desc / desc_variants
    4. theme, background
    5. portraits (left, right, lower_right)
    6. cooldown, trigger, mean_time_to_happen
    7. immediate
    8. options
    9. after
    """
    loc_entries: list[tuple[str, str]] = []
    event_id = spec.id
    event_key = f"{ns}.{event_id}"

    lines: list[str] = []
    lines.append(f"{event_key} = {{")

    # 1. Metadata
    lines.append(f"    type = {spec.type}")
    if spec.window is not None:
        lines.append(f"    window = {spec.window}")
    if spec.scope is not None:
        lines.append(f"    scope = {spec.scope}")
    if spec.hidden:
        lines.append("    hidden = yes")
    if not spec.hidden:
        lines.append(f"    content_source = {content_source}")

    # 2. Title (or title_variants)
    if spec.title_variants:
        title_block = render_desc_or_title_variants(spec.title_variants, ns, event_id, ".title")
        lines.append(title_block)
    else:
        title_key = f"{event_key}.title"
        lines.append(f"    title = {title_key}")
        loc_entries.append((title_key, spec.title))

    # 3. Desc (or desc_variants)
    if spec.desc_variants:
        desc_block = render_desc_or_title_variants(spec.desc_variants, ns, event_id, ".desc")
        lines.append(desc_block)
    else:
        desc_key = f"{event_key}.desc"
        lines.append(f"    desc = {desc_key}")
        loc_entries.append((desc_key, spec.desc))

    # 4. Theme and background
    if theme != "default":
        lines.append(f"    theme = {theme}")
    if spec.background is not None:
        lines.append(f"    override_background = {{ reference = {spec.background} }}")

    # 5. Portraits
    if spec.left_portrait is not None:
        lines.append(render_portrait(spec.left_portrait, "left"))
    if spec.right_portrait is not None:
        lines.append(render_portrait(spec.right_portrait, "right"))
    if spec.lower_right_portrait is not None:
        lines.append(render_portrait(spec.lower_right_portrait, "lower_right"))
    if spec.lower_left_portrait is not None:
        lines.append(render_portrait(spec.lower_left_portrait, "lower_left"))

    # 6. Cooldown, trigger, mean_time_to_happen
    if spec.cooldown_years is not None:
        lines.append(f"    cooldown = {{ years = {spec.cooldown_years} }}")

    if spec.trigger:
        trigger_lines: list[str] = ["    trigger = {"]
        for trig in spec.trigger:
            trigger_lines.append(f"        {trig}")
        trigger_lines.append("    }")
        lines.extend(trigger_lines)

    if spec.mean_time_to_happen is not None:
        mtth_block = render_mtth(spec.mean_time_to_happen)
        lines.append(mtth_block)

    # 7. Immediate
    if spec.immediate:
        imm_lines: list[str] = ["    immediate = {"]
        for imm in spec.immediate:
            imm_lines.append(f"        {imm}")
        imm_lines.append("    }")
        lines.extend(imm_lines)

    # 8. Options
    for opt in spec.options:
        opt_text, opt_locs = render_option(opt, ns, event_id)
        lines.append(opt_text)
        loc_entries.extend(opt_locs)

    # 9. After
    if spec.after:
        after_block = render_after(spec.after)
        lines.append(after_block)

    lines.append("}")

    return "\n".join(lines), loc_entries


def render_all_events(
    file_spec: EventFileSpec,
) -> tuple[str, list[tuple[str, str]]]:
    """Render all events in a file spec. Return (full_txt_content, all_loc_entries)."""
    txt_lines: list[str] = []
    all_loc_entries: list[tuple[str, str]] = []

    # Namespace declaration
    txt_lines.append(f"namespace = {file_spec.namespace}")
    txt_lines.append("")

    # Render each event
    for event in file_spec.events:
        event_text, event_locs = render_event(event, file_spec.namespace, file_spec.content_source, file_spec.theme)
        txt_lines.append(event_text)
        txt_lines.append("")
        all_loc_entries.extend(event_locs)

    return "\n".join(txt_lines), all_loc_entries


def render_loc_yml(ns: str, entries: list[tuple[str, str]]) -> str:
    """Render localization .yml file content (with UTF-8 BOM header).

    Returns: BOM + l_english: header + key:0 "value" lines.
    """
    lines: list[str] = []
    lines.append("l_english:")

    for key, value in entries:
        # Escape quotes in value
        escaped_value = value.replace('"', '\\"')
        lines.append(f" {key}:0 \"{escaped_value}\"")

    # BOM prefix + content
    bom = "\ufeff"  # UTF-8 BOM as Python string (will encode correctly)
    return bom + "\n".join(lines)


def main(template_path: str) -> None:
    """Load YAML template, parse, render, and write output files.

    Input:  tools/templates/event_foo.yaml
    Output: event_foo_generated.txt
            event_foo_generated_l_english.yml
    """
    template_file = Path(template_path)
    if not template_file.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    # Load and parse YAML
    yaml_content = template_file.read_text(encoding="utf-8")
    yaml_data = yaml.safe_load(yaml_content)

    try:
        file_spec = parse_spec(yaml_data)
    except ValueError as e:
        raise ValueError(f"YAML validation error: {e}") from e

    # Render events
    txt_content, loc_entries = render_all_events(file_spec)

    # Generate output filenames — écriture dans les dossiers cibles du mod
    project_root = Path(__file__).parent.parent  # hansel-tools/../
    stem = template_file.stem
    txt_dir = project_root / "events" / "story_cycles"
    yml_dir = project_root / "localization" / "english"
    txt_file = txt_dir / f"{stem}_generated.txt"
    yml_file = yml_dir / f"{stem}_generated_l_english.yml"

    # Write .txt file
    txt_file.write_text(txt_content, encoding="utf-8")
    print(f"✓ Generated: {txt_file.relative_to(project_root)}")

    # Write .yml file (with BOM)
    yml_content = render_loc_yml(file_spec.namespace, loc_entries)
    yml_file.write_bytes(yml_content.encode("utf-8"))
    print(f"✓ Generated: {yml_file.relative_to(project_root)}")

    # Summary
    print("\nSummary:")
    print(f"  Namespace: {file_spec.namespace}")
    print(f"  Events: {len(file_spec.events)}")
    print(f"  Localization keys: {len(loc_entries)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/generate_events.py <template.yaml>")
        print("Example: python tools/generate_events.py tools/templates/event_stub.yaml")
        sys.exit(1)

    try:
        main(sys.argv[1])
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
