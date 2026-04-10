# Effects Reference — CK3 Modding

> Reference for Warcraft-GoA: Fury of the Bleeding Hollow (CK3 1.18.4).
> Source: [Effects_list - CK3 Wiki](https://ck3.paradoxwikis.com/Effects_list)
>
> **Important:** This list may not be exhaustive or fully up-to-date. Run `script_docs` in the CK3
> console to export the authoritative list for your exact game version to `game/logs/`.

---

## Table of Contents

1. [Effect Syntax](#effect-syntax)
2. [Flow Control Effects](#flow-control-effects)
3. [Character Effects](#character-effects)
4. [Gold & Budget Effects](#gold--budget-effects)
5. [Prestige & Piety Effects](#prestige--piety-effects)
6. [Trait Effects](#trait-effects)
7. [Relationship Effects](#relationship-effects)
8. [Memory Effects](#memory-effects)
9. [Title Effects](#title-effects)
10. [War Effects](#war-effects)
11. [Province Effects](#province-effects)
12. [Culture Effects](#culture-effects)
13. [Faith Effects](#faith-effects)
14. [Dynasty Effects](#dynasty-effects)
15. [Faction Effects](#faction-effects)
16. [Artifact Effects](#artifact-effects)
17. [Story Cycle Effects](#story-cycle-effects)
18. [Scope & Variable Effects](#scope--variable-effects)
19. [Event Trigger Effects](#event-trigger-effects)
20. [Script Values](#script-values)

---

## Effect Syntax

Effects modify game state. They appear inside:

- `immediate = { }` blocks on events
- `option = { }` blocks on events
- `after = { }` blocks on events
- `on_actions`, decisions, interactions, scripted effects

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

### Named Script Values

CK3 provides named script values for common amounts. Prefer these over raw numbers for maintainability:

| Name                   | Approximate Value |
| ---------------------- | ----------------- |
| `minor_prestige_gain`  | ~25               |
| `small_prestige_gain`  | ~50               |
| `medium_prestige_gain` | ~150              |
| `major_prestige_gain`  | ~300              |
| `minor_piety_gain`     | ~25               |
| `small_piety_gain`     | ~50               |
| `medium_piety_gain`    | ~150              |
| `major_piety_gain`     | ~300              |

---

## Flow Control Effects

### if / else_if / else

```
if = {
    limit = { has_trait = brave }
    add_prestige = 200
}
else_if = {
    limit = { has_trait = craven }
    add_prestige = -100
}
else = {
    add_prestige = 50
}
```

### while

```
while = {
    limit = { gold < 0 }
    add_gold = 100
}
# Max 1000 iterations — always ensure a termination condition
```

### random

```
random = {
    chance = 25    # 25% chance
    add_prestige = 500
}
```

### random_list

```
random_list = {
    50 = { add_prestige = 100 }
    30 = {
        modifier = {
            add = 20
            has_trait = lucky
        }
        add_prestige = 300
    }
    20 = { add_prestige = -50 }
}
```

### switch

```
switch = {
    trigger = has_trait
    brave  = { add_prestige = 200 }
    craven = { add_prestige = -100 }
    bold   = { add_prestige = 150 }
    fallback = { add_prestige = 50 }
}
```

---

## Character Effects

| Effect                      | Syntax                                   | Description                   |
| --------------------------- | ---------------------------------------- | ----------------------------- |
| `kill_character`            | `{ killer = scope:char }`                | Kill character                |
| `imprison`                  | `{ target = scope:char type = dungeon }` | Imprison character            |
| `release_from_prison`       | `= yes`                                  | Release from prison           |
| `set_character_flag`        | `{ flag = name days = N }`               | Set flag (timed or permanent) |
| `remove_character_flag`     | `= flag_name`                            | Remove flag                   |
| `add_character_modifier`    | `{ modifier = name months = N }`         | Add character modifier        |
| `remove_character_modifier` | `= modifier_name`                        | Remove modifier               |
| `set_focus`                 | `= focus_key`                            | Set character focus           |
| `set_stress`                | `= N`                                    | Set stress directly           |
| `add_stress`                | `= N`                                    | Add/subtract stress           |
| `set_health`                | `= N`                                    | Set health directly           |
| `change_age`                | `= N`                                    | Change character age          |
| `add_education_trait`       | `= trait_key`                            | Add education level           |
| `become_independent`        | `= yes`                                  | Break free from liege         |
| `set_primary_title_to`      | `= title:key`                            | Change primary title          |

### Prison Types

```
imprison = {
    target = scope:prisoner
    type = dungeon       # dungeon | house_arrest | oubliette
}
```

---

## Gold & Budget Effects

| Effect                | Syntax                                 | Description                          |
| --------------------- | -------------------------------------- | ------------------------------------ |
| `add_gold`            | `= N`                                  | Add gold (use negative for subtract) |
| `add_long_term_gold`  | `= N`                                  | Add to long-term budget              |
| `add_short_term_gold` | `= N`                                  | Add to short-term budget             |
| `add_war_chest_gold`  | `= N`                                  | Add to war chest                     |
| `pay_reserved_gold`   | `{ target = scope:char gold = N }`     | Transfer gold between characters     |
| `move_budget_gold`    | `{ from = long_term to = short_term }` | Move between budgets                 |

---

## Prestige & Piety Effects

| Effect         | Syntax               | Description        |
| -------------- | -------------------- | ------------------ |
| `add_prestige` | `= N` or named value | Add prestige       |
| `add_piety`    | `= N` or named value | Add piety          |
| `add_dread`    | `= N`                | Add dread (0-100)  |
| `add_claim`    | `= title:key`        | Add claim on title |
| `remove_claim` | `= title:key`        | Remove claim       |

---

## Trait Effects

| Effect                  | Syntax                   | Description           |
| ----------------------- | ------------------------ | --------------------- |
| `add_trait`             | `= trait_key`            | Add trait             |
| `remove_trait`          | `= trait_key`            | Remove trait          |
| `add_trait_xp`          | `{ trait = key xp = N }` | Add XP to a trait     |
| `add_personality_trait` | `= trait_key`            | Add personality trait |

```
add_trait = brave
remove_trait = craven
add_trait_xp = { trait = hunter xp = 100 }
```

---

## Relationship Effects

| Effect                   | Syntax                                            | Description             |
| ------------------------ | ------------------------------------------------- | ----------------------- |
| `add_opinion`            | `{ target = scope:char modifier = key days = N }` | Add opinion modifier    |
| `remove_opinion`         | `{ target = scope:char modifier = key }`          | Remove opinion modifier |
| `set_relation_lover`     | `= scope:char`                                    | Set lover relation      |
| `set_relation_friend`    | `= scope:char`                                    | Set friend relation     |
| `set_relation_rival`     | `= scope:char`                                    | Set rival relation      |
| `set_relation_nemesis`   | `= scope:char`                                    | Set nemesis relation    |
| `remove_relation_friend` | `= scope:char`                                    | Remove friend relation  |
| `add_hook`               | `{ target = scope:char type = favor }`            | Add hook over character |
| `use_hook`               | `{ target = scope:char type = favor }`            | Consume hook            |

---

## Memory Effects

| Effect                     | Syntax                                  | Description    |
| -------------------------- | --------------------------------------- | -------------- |
| `create_character_memory`  | `{ type = key participants = { ... } }` | Create memory  |
| `destroy_character_memory` | `= memory_scope`                        | Destroy memory |

```
create_character_memory = {
    type = memory_battle_won
    participants = {
        enemy = scope:enemy_commander
    }
}
```

---

## Title Effects

| Effect                     | Syntax                                         | Description               |
| -------------------------- | ---------------------------------------------- | ------------------------- |
| `grant_title`              | `{ title = title:key recipient = scope:char }` | Grant title               |
| `revoke_title`             | `= title:key`                                  | Revoke title              |
| `change_development_level` | `= N`                                          | Change county development |
| `set_capital_county`       | `= title:key`                                  | Set capital               |
| `set_de_jure_liege_title`  | `{ title = title:key liege = title:key }`      | Change feudal hierarchy   |
| `clear_title_laws`         | `= yes`                                        | Remove all title laws     |
| `add_title_law`            | `= law_key`                                    | Add law to title          |

---

## War Effects

| Effect               | Syntax                                                      | Description                 |
| -------------------- | ----------------------------------------------------------- | --------------------------- |
| `start_war`          | `{ cb = key target = scope:char target_title = title:key }` | Declare war                 |
| `end_war`            | `{ war = scope:war outcome = white_peace }`                 | End war                     |
| `add_attacker`       | `= scope:char`                                              | Add attacker to current war |
| `add_defender`       | `= scope:char`                                              | Add defender to current war |
| `add_character_flag` | `{ flag = free_mongol_cb days = 14 }`                       | Temporary flag for CB       |
| `set_casus_belli`    | complex                                                     | Set war justification       |

```
add_character_flag = {
    flag = free_mongol_cb
    days = 14
}
start_war = {
    cb = mongol_invasion_war
    target = scope:defender
    target_title = title:k_gurubashi
}
```

### War Outcomes (for `end_war`)

```
white_peace    # No result
enforced       # Attacker wins, demands enforced
victory        # Attacker wins
defeat         # Attacker loses
```

---

## Province Effects

| Effect                     | Syntax                          | Description                |
| -------------------------- | ------------------------------- | -------------------------- |
| `add_building`             | `= building_key`                | Construct building         |
| `remove_building`          | `= building_key`                | Remove building            |
| `add_province_modifier`    | `{ modifier = key months = N }` | Add province modifier      |
| `remove_province_modifier` | `= modifier_key`                | Remove province modifier   |
| `refill_garrison`          | `= yes`                         | Restore defensive garrison |
| `begin_create_holding`     | `= holding_type`                | Start building a holding   |
| `change_county_control`    | `= N`                           | Modify control level       |

---

## Culture Effects

| Effect                       | Syntax                                 | Description         |
| ---------------------------- | -------------------------------------- | ------------------- |
| `add_culture_tradition`      | `= tradition_key`                      | Add tradition       |
| `remove_culture_tradition`   | `= tradition_key`                      | Remove tradition    |
| `add_innovation`             | `= innovation_key`                     | Unlock innovation   |
| `change_cultural_acceptance` | `{ target = scope:culture value = N }` | Modify acceptance   |
| `set_culture_name`           | complex                                | Custom culture name |

---

## Faith Effects

| Effect                 | Syntax                          | Description             |
| ---------------------- | ------------------------------- | ----------------------- |
| `activate_holy_site`   | `= title:key`                   | Enable holy site        |
| `add_doctrine`         | `= doctrine_key`                | Add doctrine            |
| `remove_doctrine`      | `= doctrine_key`                | Remove doctrine         |
| `change_fervor`        | `= N`                           | Modify religious fervor |
| `start_great_holy_war` | complex                         | Initiate great holy war |
| `add_faith_modifier`   | `{ modifier = key months = N }` | Add faith modifier      |

---

## Dynasty Effects

| Effect                       | Syntax                          | Description                 |
| ---------------------------- | ------------------------------- | --------------------------- |
| `add_dynasty_modifier`       | `{ modifier = key months = N }` | Add dynasty-wide modifier   |
| `remove_dynasty_modifier`    | `= modifier_key`                | Remove modifier             |
| `add_dynasty_perk`           | `= perk_key`                    | Unlock dynasty perk         |
| `add_dynasty_prestige`       | `= N`                           | Add dynasty prestige        |
| `add_dynasty_prestige_level` | `= N`                           | Add prestige level directly |

---

## Faction Effects

| Effect                   | Syntax  | Description                 |
| ------------------------ | ------- | --------------------------- |
| `add_faction_discontent` | `= N`   | Increase faction discontent |
| `destroy_faction`        | `= yes` | Remove faction entirely     |
| `faction_start_war`      | `= yes` | Trigger faction war         |

---

## Artifact Effects

| Effect                    | Syntax                                            | Description                |
| ------------------------- | ------------------------------------------------- | -------------------------- |
| `equip_artifact_to_owner` | `= scope:artifact`                                | Equip artifact             |
| `reforge_artifact`        | complex                                           | Restore/modify artifact    |
| `set_artifact_name`       | `= key`                                           | Custom name                |
| `set_artifact_rarity`     | `= common/masterwork/famed/illustrious/legendary` | Set rarity                 |
| `add_artifact_modifier`   | complex                                           | Apply modifier to artifact |
| `destroy_artifact`        | `= scope:artifact`                                | Destroy artifact           |

---

## Story Cycle Effects

| Effect             | Syntax        | Description                                |
| ------------------ | ------------- | ------------------------------------------ |
| `create_story`     | `= story_key` | Create story cycle, set root as owner      |
| `end_story`        | `= yes`       | End current story (must be in story scope) |
| `make_story_owner` | `= yes`       | Transfer story ownership to current scope  |

```
# Create story (fires on_setup)
root = {
    create_story = story_bleeding_hollow_invasion
    save_scope_as = story_owner
}

# End story
end_story = yes

# Transfer on death
scope:story_owner = {
    primary_heir = { make_story_owner = yes }
}
```

---

## Scope & Variable Effects

### Saving Scopes

```
save_scope_as = my_scope              # Permanent through effect chain
save_temporary_scope_as = temp_scope  # Expires at block end
```

### Variables

```
set_variable = { name = phase value = 1 }
change_variable = { name = phase add = 1 }
change_variable = { name = phase subtract = 1 }
multiply_variable = { name = phase value = 2 }
remove_variable = phase
```

Variables are saved on the scope they're set on (character, title, etc.).

### List Operations

```
add_to_list = { name = my_list }      # Add current scope to named list
remove_from_list = { name = my_list } # Remove current scope from list
clear_list = my_list                  # Empty the list

every_in_list = {
    list = my_list
    limit = { has_trait = brave }
    add_prestige = 100
}
```

---

## Event Trigger Effects

```
trigger_event = namespace.1001
trigger_event = { id = namespace.1001 days = 7 }

# On another character:
scope:target = { trigger_event = namespace.1001 }

# With delay:
scope:target = {
    trigger_event = { id = namespace.1001 days = 30 }
}
```

---

## Script Values

Named numeric expressions defined in `common/script_values/`. Used wherever a number is expected:

```
# Definition
my_score = {
    value = 0
    add = 100
    if = {
        limit = { has_trait = brave }
        add = 50
    }
    multiply = 1.5
}

# Usage
add_prestige = my_score
if = {
    limit = { my_score >= 100 }
    add_gold = 500
}
```

**Math operations in script values:**

- `add = N`
- `subtract = N`
- `multiply = N`
- `divide = N`
- `min = N` (floor)
- `max = N` (ceiling)
- `round = yes`
- `abs = yes`
