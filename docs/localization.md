# Localization Reference — CK3 Modding

> Reference for Warcraft-GoA: Fury of the Bleeding Hollow (CK3 1.18.4).
> Source: [Localization - CK3 Wiki](https://ck3.paradoxwikis.com/Localization)

---

## Table of Contents

1. [File Format](#file-format)
2. [Key Conventions](#key-conventions)
3. [Formatting Codes](#formatting-codes)
4. [Dynamic Content](#dynamic-content)
5. [Icons](#icons)
6. [Number Formatting](#number-formatting)
7. [Game Concepts](#game-concepts)
8. [Traits & Titles](#traits--titles)
9. [Mod Override Pattern](#mod-override-pattern)
10. [Common Mistakes](#common-mistakes)

---

## File Format

**Location:** `localization/english/`

**File requirements:**

- Extension: `.yml`
- Encoding: **UTF-8 with BOM** (CK3 silently ignores files without BOM)
- First line: `l_english:` (lowercase L, not number 1)
- Naming: must contain `l_english` in the filename

```yaml
l_english:
  key_name:0 "Text content"
  another_key:0 "More text"
```

**Verify BOM with:**

```bash
file localization/english/wc_bleeding_hollow_invasion_l_english.yml
# Should show: UTF-8 Unicode (with BOM) text
```

---

## Key Conventions

**Format:** `key:0 "text"` — the `:0` version suffix is mandatory in this mod.

**Key naming mirrors event IDs:**

```yaml
wc_bleeding_hollow_invasion.1000.title:0 "Invasion of Stranglethorn"
wc_bleeding_hollow_invasion.1000.desc:0 "Kilrogg Deadeye leads his clan south..."
wc_bleeding_hollow_invasion.1000.a:0 "Lok'tar Ogar!"
wc_bleeding_hollow_invasion.1000.a_flavor:0 "The Bleeding Hollow march to war."
```

**Standard keys per event:**

| Key                     | Purpose                    |
| ----------------------- | -------------------------- |
| `namespace.id.title`    | Event window title bar     |
| `namespace.id.desc`     | Main body text             |
| `namespace.id.a`        | First option button label  |
| `namespace.id.a_flavor` | First option tooltip text  |
| `namespace.id.b`        | Second option button label |
| `namespace.id.b_flavor` | Second option tooltip      |

**Placeholder text:** `"Blablabla"` marks unwritten localization. Search before shipping:

```bash
grep -r "Blablabla" localization/
```

---

## Formatting Codes

Pattern: `#<code> text#!`

**A space is required between the code and the text.**

```yaml
key:0 "#bold Kilrogg Deadeye#! leads the charge."
key:0 "#P +200 Prestige#! gained from the victory."
key:0 "#N Your army is routed.#!"
```

### Color / Emphasis Codes

| Code       | Effect                    | Usage                  |
| ---------- | ------------------------- | ---------------------- |
| `#bold`    | Bold text                 | Names, important terms |
| `#italic`  | Italic text               | Flavor, quotes         |
| `#P`       | Green (positive)          | Gains, bonuses         |
| `#N`       | Red (negative)            | Losses, penalties      |
| `#T`       | Large bold title          | Section headers        |
| `#E`       | Light blue (game concept) | Game terms             |
| `#warning` | Red italic                | Warnings, dangers      |
| `#high`    | Gold/yellow highlight     | Special emphasis       |

### Combining Codes

Use semicolons:

```yaml
key:0 "#high;bold Lok'tar Ogar!#!"
```

### Line Breaks

```yaml
key:0 "First paragraph.\n\nSecond paragraph."
key:0 "Line one.\nLine two."
```

Avoid spaces immediately before or after `\n`.

---

## Dynamic Content

### Character Name Functions

Scope-based dynamic text. `ROOT` refers to the event's root character:

```yaml
key:0 "[ROOT.Char.GetFirstName] leads the charge."
key:0 "[ROOT.Char.GetFirstNameNicknamed]"
key:0 "[ROOT.Char.GetFullName]"
key:0 "[ROOT.Char.GetTitledFirstName]"     # "Warlord Kilrogg"
key:0 "[ROOT.Char.GetLadyLord]"           # "Lord" or "Lady"
key:0 "[ROOT.Char.GetSheHe]"              # "He" or "She"
key:0 "[ROOT.Char.GetHerHis]"             # "His" or "Her"
key:0 "[ROOT.Char.GetHerHim]"             # "Him" or "Her"
```

### Accessing Saved Scopes

```yaml
# scope:kilrogg
key:0 "[kilrogg.Char.GetFirstName] watches from the ridge."

# scope:zulgurub_holder
key:0 "The troll [zulgurub_holder.Char.GetTitledFirstName] prepares his defenses."
```

### Localization Key Re-use

Embed another localization key:

```yaml
key:0 "The cry of [$wc_bleeding_hollow_invasion.battlecry$] echoes."
```

### Case Modifiers

Append to function calls:

```yaml
[ROOT.Char.GetFirstName|U]    # Uppercase first letter
[ROOT.Char.GetFirstName|L]    # Lowercase first letter
```

### Escaped Characters

```yaml
key:0 "He said \"Lok'tar Ogar!\"" # Literal quote marks
```

---

## Icons

Pattern: `@icon_name!`

```yaml
key:0 "Costs @gold_icon! 500 gold."
key:0 "Gain @prestige_icon! prestige."
key:0 "@warning_icon! This action cannot be undone."
```

**Common icons:**

| Icon        | Code                 |
| ----------- | -------------------- |
| Gold        | `@gold_icon!`        |
| Prestige    | `@prestige_icon!`    |
| Piety       | `@piety_icon!`       |
| Dread       | `@dread_icon!`       |
| Renown      | `@renown_icon!`      |
| Warning     | `@warning_icon!`     |
| Martial     | `@martial_icon!`     |
| Diplomacy   | `@diplomacy_icon!`   |
| Intrigue    | `@intrigue_icon!`    |
| Stewardship | `@stewardship_icon!` |
| Learning    | `@learning_icon!`    |

> Full icon list: run `script_docs` in-game console, check exported `game/logs/`.

---

## Number Formatting

Append format modifiers to numeric variables:

| Modifier       | Effect                                                 | Example                |
| -------------- | ------------------------------------------------------ | ---------------------- |
| `\|0`          | 0 decimal places                                       | `500`                  |
| `\|1`          | 1 decimal place                                        | `500.0`                |
| `\|2`          | 2 decimal places                                       | `500.00`               |
| `\|=`          | Show sign, 2 decimals                                  | `+500.00` or `-500.00` |
| `\|k` or `\|K` | Thousands format                                       | `1.20K`                |
| `\|%`          | Percentage                                             | `20.00%`               |
| `\|+`          | Color by modifier (green if positive, red if negative) | —                      |

```yaml
key:0 "Gained [ROOT.Char.GetGold|0] @gold_icon! gold."
key:0 "#P [ROOT.Char.GetPrestige|k] Prestige#!"
```

---

## Game Concepts

Link to in-game concept tooltips:

```yaml
key:0 "[concept_prestige|E] is key to expansion."
key:0 "[concept_prestige|El]" # Lowercase first letter
```

The `|E` suffix renders the text as a clickable game concept link (light blue).

---

## Traits & Titles

### Trait Names

```yaml
key:0 "The [GetTrait('brave').GetName(Character.Self)] warrior stood firm."
```

### Title Names

```yaml
key:0 "The ruler of [GetTitleByKey('k_gurubashi').GetName] called for aid."
```

---

## Mod Override Pattern

To override a single localization entry from another mod without replacing the entire file, use the `replace/` subdirectory:

```
localization/replace/english/my_overrides_l_english.yml
```

The `replace/` prefix takes precedence over regular localization files when multiple mods modify the same key.

---

## Common Mistakes

| Mistake                                             | Result                        | Fix                                          |
| --------------------------------------------------- | ----------------------------- | -------------------------------------------- |
| Missing UTF-8 BOM                                   | CK3 silently ignores the file | Save with BOM in editor; use `.editorconfig` |
| Wrong header (`l_English:` instead of `l_english:`) | File ignored                  | Always lowercase                             |
| Missing `:0` suffix                                 | Key may not load              | `key:0 "text"` format always                 |
| `#bold text#` without `!`                           | Renders literally             | Always close with `#!`                       |
| Space missing after code (`#boldtext#!`)            | Renders literally             | `#bold text#!`                               |
| Relative path in filename                           | May not load                  | Include `l_english` in filename              |

---

## Complete Example

```yaml
l_english:
 wc_bleeding_hollow_invasion.1000.title:0 "#T Invasion of Stranglethorn#!"
 wc_bleeding_hollow_invasion.1000.desc:0 "#bold [ROOT.Char.GetTitledFirstName]#! surveys the jungle ahead. The #bold Bleeding Hollow#! clan has marched south from the #bold Dark Portal#!.\n\nThe troll kingdom of #bold Zul'Gurub#! stands between the Horde and dominion over #bold Stranglethorn#!. Today, that changes."
 wc_bleeding_hollow_invasion.1000.a:0 "Lok'tar Ogar!"
 wc_bleeding_hollow_invasion.1000.a_flavor:0 "@prestige_icon! The Bleeding Hollow march to war. Victory will bring #P great renown#! to the clan."
```
