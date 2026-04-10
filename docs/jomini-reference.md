# Jomini Scripting Reference — CK3 Modding

> Reference for Warcraft-GoA: Fury of the Bleeding Hollow (CK3 1.18.4).
> Sources: [Event modding](https://ck3.paradoxwikis.com/Event_modding), [Scopes](https://ck3.paradoxwikis.com/Scopes), [Scripted effects](https://ck3.paradoxwikis.com/Scripted_effects), [On_actions](https://ck3.paradoxwikis.com/On_actions)

---

## Table of Contents

1. [Syntax Basics](#syntax-basics)
2. [Event Structure](#event-structure)
3. [Scopes](#scopes)
4. [Triggers](#triggers)
5. [Effects](#effects)
6. [Scripted Effects](#scripted-effects)
7. [On_Actions](#on_actions)
8. [Story Cycles](#story-cycles)
9. [Variables](#variables)
10. [Debug](#debug)

---

## Syntax Basics

Jomini uses a key-value syntax with nested blocks:

```
key = value
key = { block }
key = { key = value key2 = value2 }
```

**Conventions used in this project:**

- Tabs for indentation (not spaces)
- One key-value per line
- Opening `{` on the same line as the key
- Namespace prefix `wc_` on all identifiers

**Comments:**

```
# This is a comment
```

**Operators:**

```
=    # equals / assignment
!=   # not equals
>    # greater than
>=   # greater than or equal
<    # less than
<=   # less than or equal
```

---

## Event Structure

### Namespace

Every event file declares a namespace at the top:

```
namespace = wc_bleeding_hollow_invasion
```

Event IDs combine namespace + number:

```
wc_bleeding_hollow_invasion.1000 = { ... }
```

Maximum 9999 IDs per namespace.

### ID Conventions (this mod)

| Range     | Purpose                                    |
| --------- | ------------------------------------------ |
| 0001–0009 | Hidden setup/trigger events (no UI)        |
| 1000–1099 | Base narrative events (intro, major beats) |
| 1500–1599 | Named character introduction events        |
| 2000–2999 | Ongoing/mid-story events                   |
| 9000–9999 | Location/conquest events                   |

### Event Block — All Fields

```
namespace.1000 = {
    type = character_event          # character_event | letter_event | duel_event | none | empty
    content_source = dlc_GOA        # Required on all player-visible events in this mod
    title = namespace.1000.title    # Localization key
    desc = namespace.1000.desc      # Localization key (or first_valid / random_valid block)
    theme = bleeding_hollow         # Visual/audio theme
    override_background = { reference = wc_background_stranglethorn }

    # Portrait slots
    left_portrait = {
        character = root
        animation = personality_bold
    }
    right_portrait = {
        character = scope:target
        animation = idle
        triggered_animation = {
            trigger = { has_trait = brave }
            animation = personality_bold
        }
    }
    lower_left_portrait = scope:third_character
    lower_center_portrait = scope:fourth
    lower_right_portrait = scope:fifth

    trigger = {
        # Conditions that must be true for the event to fire
    }

    immediate = {
        # Effects executed before the UI renders
        # Use for: save_scope_as, show_as_tooltip, setup logic
    }

    option = {
        name = namespace.1000.a     # Localization key for button text
        flavor = namespace.1000.a_flavor  # Tooltip text
        trigger = { ... }           # Option availability condition
        show_as_unavailable = { ... }  # Shows grayed out if true

        # Effects
        add_prestige = medium_prestige_gain
        trigger_event = namespace.1001

        ai_chance = {
            base = 100              # ALWAYS include on every option
            modifier = {
                add = 50
                has_trait = bold
            }
            ai_value_modifier = {
                ai_boldness = 0.5
            }
        }
    }

    after = {
        # Cleanup effects executed after any option is selected
    }
}
```

### `first_valid` Descriptions

Use for character-specific flavor text. Most specific trigger first, generic fallback last:

```
desc = {
    first_valid = {
        triggered_desc = {
            trigger = { has_trait = brave }
            desc = namespace.1000.desc_brave
        }
        triggered_desc = {
            trigger = { is_female = yes }
            desc = namespace.1000.desc_female
        }
        desc = namespace.1000.desc   # fallback — always last
    }
}
```

### `random_valid` Descriptions

For random flavor text:

```
desc = {
    random_valid = {
        desc = namespace.1000.desc_a
        desc = namespace.1000.desc_b
        triggered_desc = {
            trigger = { has_trait = greedy }
            desc = namespace.1000.desc_greedy
        }
    }
}
```

### Triggering Events

```
trigger_event = namespace.1001                # Fires on root character
trigger_event = { id = namespace.1001 days = 7 }  # With delay

# On another character:
scope:target = { trigger_event = namespace.1001 }

# With delay on another character:
scope:target = {
    trigger_event = { id = namespace.1001 days = 30 }
}
```

### `show_as_tooltip`

Previews effects in the event UI without executing them. Always pair with the real effect:

```
immediate = {
    show_as_tooltip = {
        declare_war_on_zulgurub_effect = yes
    }
}

option = {
    name = namespace.1000.a
    declare_war_on_zulgurub_effect = yes  # The real execution
}
```

---

## Scopes

### Scope Types

| Type          | Description                                     |
| ------------- | ----------------------------------------------- |
| **character** | A character (player, NPC, historical)           |
| **title**     | A landed title (county, duchy, kingdom, empire) |
| **province**  | A province (map location)                       |
| **culture**   | A culture object                                |
| **faith**     | A religion / faith object                       |
| **dynasty**   | A dynasty object                                |
| **war**       | An active war                                   |
| **faction**   | A faction object                                |
| **story**     | A story cycle instance                          |
| **artifact**  | An artifact object                              |

### Accessing Scopes

**By database key:**

```
title:k_gurubashi = { ... }      # Title by key
character:10005 = { ... }         # Character by ID (historical only)
faith:orcish_shamanism = { ... }  # Faith by key
```

**By relationship:**

```
root                              # The event's scope owner
title:k_gurubashi.holder = { ... }  # Chained access
liege = { ... }
primary_spouse = { ... }
```

**Saved scopes:**

```
save_scope_as = my_scope         # Save current scope as a named pointer
scope:my_scope = { ... }         # Access saved scope

save_temporary_scope_as = temp   # Temporary — expires at block end
```

**Key rule:** Save important scopes in `immediate` before they're needed in `option` blocks.

```
# CORRECT
immediate = {
    title:k_gurubashi.holder = { save_scope_as = zulgurub_holder }
}
option = {
    name = namespace.1000.a
    scope:zulgurub_holder = { add_prestige = 100 }  # Works
}

# BUG — scope not saved, runtime crash
option = {
    name = namespace.1000.a
    title:k_gurubashi.holder = { add_prestige = 100 }  # May fail in certain contexts
    scope:zulgurub_holder = { add_prestige = 100 }     # CRASH if not saved first
}
```

### Special Scope Keywords

| Keyword      | Meaning                                             |
| ------------ | --------------------------------------------------- |
| `root`       | The primary scope of the current event/effect block |
| `this`       | Current scope in a context switch                   |
| `prev`       | Previous scope (one level up in a nested switch)    |
| `scope:name` | Named saved scope                                   |

### List-Builders

| Builder     | Behavior                                |
| ----------- | --------------------------------------- |
| `every_X`   | Executes effects for ALL matching items |
| `any_X`     | Trigger: true if at least one matches   |
| `random_X`  | Executes for ONE randomly selected item |
| `ordered_X` | Executes for items sorted by `order_by` |

```
every_vassal = {
    limit = {
        has_trait = ambitious
    }
    add_opinion = {
        target = root
        modifier = opinion_ambitious_vassal
        days = 365
    }
}

any_vassal = {
    count >= 3
    has_trait = ambitious
}

random_vassal = {
    limit = { has_trait = brave }
    weight = { base = 10 }
    add_prestige = 50
}

ordered_vassal = {
    order_by = military_strength
    position = 1   # The strongest vassal
    save_scope_as = best_general
}
```

---

## Triggers

Triggers are boolean conditions. Evaluation stops at the first false (early-out principle).

### Logic Operators

```
AND = { trigger_a trigger_b }   # All must be true (implicit inside blocks)
OR = { trigger_a trigger_b }    # At least one must be true
NOT = { trigger_a }             # Negates
NOR = { trigger_a trigger_b }   # True only if all are false
NAND = { trigger_a trigger_b }  # False only if all are true
```

### Conditional Trigger Structures

```
trigger_if = {
    limit = { is_ai = no }
    age >= 30
}
trigger_else_if = {
    limit = { age < 20 }
    has_trait = prodigy
}
trigger_else = {
    age >= 20
}
```

### Common Character Triggers

```
age >= 16
age < 30
is_ai = yes / no
is_alive = yes
is_female = yes / no
is_imprisoned = yes
is_at_war = yes
has_trait = brave
has_trait_with_flag = { flag = virtue }
has_character_flag = my_flag
has_hook = { target = scope:target type = favor }
has_relation_lover = scope:other
is_vassal_of = scope:liege
culture = { has_cultural_pillar = heritage_orcish }
faith = { has_doctrine = tenet_warlike }
gold >= 500
prestige >= 1000
```

### Title Triggers

```
title:k_gurubashi = {
    exists = yes
    holder = { is_alive = yes }
}
completely_controls = title:k_gurubashi
has_de_jure_claim_on = title:k_gurubashi
```

### Performance Notes

- Avoid `any_living_character` or `every_living_character` in pulse-based on_actions (O(n) over all characters)
- Wiki marks slow triggers with "VERY SLOW" warnings
- Use `exists = scope:target` before accessing potentially null scopes

---

## Effects

### Syntax Forms

**Boolean form:**

```
release_from_prison = yes
```

**Simple form:**

```
add_gold = 500
add_prestige = medium_prestige_gain
```

**Complex form:**

```
add_opinion = {
    target = scope:target
    modifier = opinion_fear
    days = 365
}
```

### Flow Control Effects

```
if = {
    limit = { has_trait = brave }
    add_prestige = 100
}
else_if = {
    limit = { has_trait = craven }
    add_prestige = -50
}
else = {
    add_prestige = 25
}

while = {
    limit = { gold < 0 }
    add_gold = 50
}  # Max 1000 iterations

random_list = {
    50 = { add_prestige = 100 }
    25 = {
        modifier = { add = 25; has_trait = lucky }
        add_prestige = 200
    }
    25 = { add_prestige = 50 }
}

switch = {
    trigger = has_trait
    brave = { add_prestige = 100 }
    craven = { add_prestige = -100 }
    fallback = { add_prestige = 0 }
}
```

### Common Character Effects

```
add_gold = 500
add_prestige = medium_prestige_gain
add_piety = small_piety_gain
add_trait = brave
remove_trait = craven
set_character_flag = { flag = my_flag days = 365 }
remove_character_flag = my_flag
imprison = { target = scope:prisoner type = dungeon }
release_from_prison = yes
kill_character = { killer = root }
```

### War Effects

```
start_war = {
    cb = mongol_invasion_war
    target = scope:defender
    target_title = title:k_gurubashi
}
add_character_flag = {
    flag = free_mongol_cb
    days = 14
}
end_war = { war = scope:active_war outcome = white_peace }
```

### Story Cycle Effects

```
create_story = story_bleeding_hollow_invasion  # Creates story, sets story owner to root
end_story = yes                                 # Ends current story (must be in story context)
```

---

## Scripted Effects

Scripted effects are parameterized macros that reduce code duplication.

**Definition** (`common/scripted_effects/`):

```
my_scripted_effect = {
    scope:$TARGET$ = {
        add_prestige = $AMOUNT$
    }
    if = {
        limit = { exists = scope:other_target }
        scope:other_target = {
            add_opinion = {
                target = scope:$TARGET$
                modifier = opinion_impressed
                days = 365
            }
        }
    }
}
```

**Invocation:**

```
my_scripted_effect = {
    TARGET = kilrogg
    AMOUNT = 200
}
```

**Simple invocation (no parameters):**

```
declare_war_on_zulgurub_effect = yes
```

**Rules:**

- Parameter names are UPPERCASE by convention (`$PARAM$`)
- Parameters are text-replaced before execution (not dynamic scoping)
- Can be used inside events, decisions, interactions, other scripted effects
- `show_as_tooltip` wraps the effect call to preview it without executing

---

## On_Actions

On_actions are hooks that fire events/effects in response to game events.

**File location:** `common/on_action/*.txt`

**Append safely (without overwriting):**

```
on_birth_child = {
    on_actions = { my_custom_on_action }
}

my_custom_on_action = {
    trigger = {
        culture = { has_cultural_pillar = heritage_orcish }
    }
    effect = {
        trigger_event = wc_my_event.1000
    }
}
```

**Common on_action hooks:**

| Hook                           | Scope         | When                   |
| ------------------------------ | ------------- | ---------------------- |
| `on_birth_child`               | newborn child | On birth               |
| `on_16th_birthday`             | character     | 16th birthday          |
| `on_game_start_after_lobby`    | player        | After character select |
| `random_yearly_playable_pulse` | player        | ~1x/year per player    |
| `quarterly_playable_pulse`     | player        | Every ~3 months        |
| `monthly_playable_pulse`       | player        | Every month            |
| `on_war_started`               | attacker      | War declaration        |
| `on_war_ended_victory`         | winner        | War end (victory)      |
| `on_war_ended_defeat`          | loser         | War end (defeat)       |
| `on_title_gain`                | character     | Title acquired         |
| `on_death`                     | character     | On death               |

**Performance rules:**

- Never use `every_living_character` inside pulse on_actions
- Prefer `quarterly_playable_pulse` over `monthly` for rare events
- Use `trigger` blocks to filter before executing effects

---

## Story Cycles

Story cycles manage multi-event chains with a persistent owner.

**Definition** (`common/story_cycles/`):

```
story_my_story = {
    on_setup = {
        # Effects executed when story is created
        set_bleeding_hollow_characters_effect = yes
        trigger_event = { id = wc_my.1000 days = 14 }
    }

    on_end = {
        # Effects when story ends (end_story called)
    }

    on_owner_death = {
        # Choices when the story owner dies
        if = {
            limit = {
                scope:story_owner = {
                    any_heir = {
                        culture = { has_cultural_pillar = heritage_orcish }
                    }
                }
            }
            # Transfer story to primary heir
            scope:story_owner = {
                primary_heir = { make_story_owner = yes }
            }
        }
        else = {
            end_story = yes  # End story if no valid heir
        }
    }
}
```

**Creating a story:**

```
# In an event's immediate or option block:
root = {
    create_story = story_my_story
    save_scope_as = story_owner
}
```

**Story owner scope:**

- `story_owner` is available within story cycle `on_setup`/`on_end`/`on_owner_death` blocks
- In events fired BY the story, `story_owner` must be saved manually:

```
immediate = {
    story_owner = { save_scope_as = story_owner }
}
```

---

## Variables

Variables store numeric values on scopes.

```
# Set
set_variable = { name = invasion_phase value = 1 }

# Change
change_variable = { name = invasion_phase add = 1 }
change_variable = { name = invasion_phase subtract = 1 }

# Check (in triggers)
var:invasion_phase >= 2
exists = var:invasion_phase

# Remove
remove_variable = invasion_phase
```

Variables persist on the scope they're set on (character, title, etc.).

---

## Debug

### Console Commands

```
event wc_bleeding_hollow_invasion.0001    # Fire event on selected character
discover_interaction <name>               # Unlock interaction
script_docs                               # Export valid triggers/effects list to logs/
```

### `debug_log`

```
immediate = {
    debug_log = "Bleeding Hollow invasion started!"
    debug_log_date = yes
}
```

Output appears in `game.log` (watch with `python tools/watch_logs.py`).

### Launch Flags

```
ck3.exe -debug_mode    # Dev tooltips, Ctrl+click character switch
ck3.exe -develop       # Hot-reload scripts without restart (partial)
```

### Error Log

```
%APPDATA%\Paradox Interactive\Crusader Kings III\logs\error.log
```

Syntax errors appear at game launch. Scope errors appear during gameplay. Watch with:

```bash
python tools/watch_logs.py --filter wc_bleeding_hollow
```
