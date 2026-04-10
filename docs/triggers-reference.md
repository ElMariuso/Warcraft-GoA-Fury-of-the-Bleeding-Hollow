# Triggers Reference — CK3 Modding

> Reference for Warcraft-GoA: Fury of the Bleeding Hollow (CK3 1.18.4).
> Source: [Triggers_list - CK3 Wiki](https://ck3.paradoxwikis.com/Triggers_list)
>
> **Important:** This list may not be exhaustive or fully up-to-date. Run `script_docs` in the CK3
> console to export the authoritative list for your exact game version to `game/logs/`.

---

## Table of Contents

1. [Trigger Syntax](#trigger-syntax)
2. [Logic Operators](#logic-operators)
3. [Character Triggers](#character-triggers)
4. [Skill & Attribute Triggers](#skill--attribute-triggers)
5. [Trait Triggers](#trait-triggers)
6. [Relationship Triggers](#relationship-triggers)
7. [Title & Realm Triggers](#title--realm-triggers)
8. [War & Military Triggers](#war--military-triggers)
9. [Culture & Faith Triggers](#culture--faith-triggers)
10. [Province & Map Triggers](#province--map-triggers)
11. [Dynasty & House Triggers](#dynasty--house-triggers)
12. [Faction Triggers](#faction-triggers)
13. [Variable Triggers](#variable-triggers)
14. [Scope Existence Triggers](#scope-existence-triggers)
15. [Script Value Triggers](#script-value-triggers)

---

## Trigger Syntax

Triggers return `true` or `false`. They appear inside:

- `trigger = { }` blocks on events, decisions, interactions
- `limit = { }` blocks inside list-builders (`every_X`, `any_X`, etc.)
- `trigger_if = { limit = { } ... }` for conditional trigger evaluation

**Evaluation stops at the first false condition (early-out).**

```
trigger = {
    exists = primary_spouse            # Check existence first
    culture = primary_spouse.culture   # Only evaluated if spouse exists
}
```

### Value Comparisons

```
age >= 16
gold > 500
prestige <= 1000
martial = 12    # Exact match
```

### Scope Comparisons

```
primary_title = title:k_gurubashi    # Same title
liege = root                          # Same character
```

---

## Logic Operators

```
AND = { trigger_a trigger_b trigger_c }  # All must be true (implicit in any block)
OR  = { trigger_a trigger_b }            # At least one must be true
NOT = { trigger_a }                      # Negates
NOR = { trigger_a trigger_b }           # True only if all are false
NAND = { trigger_a trigger_b }          # False only if all are true
```

**Conditional trigger evaluation:**

```
trigger_if = {
    limit = { is_ai = no }
    # Triggers evaluated only for human players
    age >= 16
}
trigger_else_if = {
    limit = { has_trait = prodigy }
    age >= 14
}
trigger_else = {
    age >= 16
}
```

---

## Character Triggers

| Trigger                  | Value        | Description             |
| ------------------------ | ------------ | ----------------------- |
| `is_alive`               | `yes/no`     | Character alive         |
| `is_ai`                  | `yes/no`     | Controlled by AI        |
| `is_female`              | `yes/no`     | Character gender        |
| `is_male`                | `yes/no`     | Character gender        |
| `is_adult`               | `yes/no`     | Adult (≥16 by default)  |
| `is_minor`               | `yes/no`     | Child                   |
| `is_imprisoned`          | `yes/no`     | Currently imprisoned    |
| `is_incapable`           | `yes/no`     | Incapacitated           |
| `is_landless_adventurer` | `yes/no`     | Adventurer status       |
| `is_playable_character`  | `yes/no`     | Can be played           |
| `is_ruler`               | `yes/no`     | Controls a title        |
| `is_independent_ruler`   | `yes/no`     | No liege                |
| `is_vassal_of`           | `scope:char` | Is vassal of target     |
| `is_liege_of`            | `scope:char` | Is liege of target      |
| `is_at_war`              | `yes/no`     | Involved in any war     |
| `is_at_war_with`         | `scope:char` | At war with target      |
| `exists`                 | `yes/no`     | Scope exists (non-null) |
| `has_character_flag`     | `flag_name`  | Has character flag      |
| `has_variable`           | `var_name`   | Has variable set        |

---

## Skill & Attribute Triggers

| Trigger       | Value                         | Description           |
| ------------- | ----------------------------- | --------------------- |
| `age`         | `>= N`                        | Character age         |
| `diplomacy`   | `>= N`                        | Diplomacy skill       |
| `martial`     | `>= N`                        | Martial skill         |
| `stewardship` | `>= N`                        | Stewardship skill     |
| `intrigue`    | `>= N`                        | Intrigue skill        |
| `learning`    | `>= N`                        | Learning skill        |
| `prowess`     | `>= N`                        | Combat prowess        |
| `gold`        | `>= N`                        | Available gold        |
| `prestige`    | `>= N`                        | Prestige level        |
| `piety`       | `>= N`                        | Piety level           |
| `dread`       | `>= N`                        | Dread level (0-100)   |
| `fertility`   | `>= N`                        | Fertility (0-1 float) |
| `health`      | `>= N`                        | Health value          |
| `stress`      | `>= N`                        | Current stress        |
| `opinion`     | `{ who = target value >= N }` | Opinion of target     |

---

## Trait Triggers

| Trigger               | Value                   | Description             |
| --------------------- | ----------------------- | ----------------------- |
| `has_trait`           | `trait_key`             | Has specific trait      |
| `has_trait_with_flag` | `{ flag = trait_flag }` | Has any trait with flag |
| `num_of_traits`       | `>= N`                  | Trait count             |
| `is_genius`           | `yes/no`                | Genius education trait  |
| `is_ill`              | `yes/no`                | Has illness trait       |
| `is_pregnant`         | `yes/no`                | Currently pregnant      |

```
has_trait = brave
has_trait = craven
has_trait = ambitious
has_trait_with_flag = { flag = virtue }
has_trait_with_flag = { flag = sin }
```

---

## Relationship Triggers

| Trigger                   | Value                                | Description           |
| ------------------------- | ------------------------------------ | --------------------- |
| `has_relation_lover`      | `scope:char`                         | Lover relationship    |
| `has_relation_friend`     | `scope:char`                         | Friend relationship   |
| `has_relation_rival`      | `scope:char`                         | Rival relationship    |
| `has_relation_nemesis`    | `scope:char`                         | Nemesis relationship  |
| `has_hook`                | `{ target = scope:char type = ... }` | Hook over target      |
| `has_non_aggression_pact` | `scope:char`                         | NAP with target       |
| `is_spouse_of`            | `scope:char`                         | Married to target     |
| `is_concubine_of`         | `scope:char`                         | Concubine of target   |
| `is_parent_of`            | `scope:char`                         | Parent of target      |
| `is_child_of`             | `scope:char`                         | Child of target       |
| `is_sibling_of`           | `scope:char`                         | Sibling of target     |
| `any_spouse`              | trigger block                        | Has a spouse matching |
| `any_child`               | trigger block                        | Has a child matching  |
| `any_vassal`              | trigger block                        | Has a vassal matching |
| `any_ally`                | trigger block                        | Has an ally matching  |

```
any_vassal = {
    count >= 3
    has_trait = ambitious
}

any_spouse = {
    is_alive = yes
    culture = root.culture
}
```

---

## Title & Realm Triggers

| Trigger                | Value        | Description          |
| ---------------------- | ------------ | -------------------- |
| `completely_controls`  | `title:key`  | Fully controls title |
| `holds_landed_title`   | `title:key`  | Holds the title      |
| `has_primary_title`    | `title:key`  | Primary title is X   |
| `has_de_jure_claim_on` | `title:key`  | Has de jure claim    |
| `has_claim_on`         | `title:key`  | Has any claim        |
| `is_in_same_realm`     | `scope:char` | In same realm as     |
| `realm_size`           | `>= N`       | Realm county count   |
| `title_held_years`     | `>= N`       | Years holding title  |
| `is_titular_title`     | `yes/no`     | Title has no land    |

```
completely_controls = title:k_gurubashi
has_de_jure_claim_on = title:k_gurubashi
title:k_gurubashi = {
    exists = yes
    holder = { is_alive = yes }
}
```

---

## War & Military Triggers

| Trigger                  | Value                     | Description               |
| ------------------------ | ------------------------- | ------------------------- |
| `is_at_war`              | `yes/no`                  | In any war                |
| `is_at_war_with`         | `scope:char`              | At war with character     |
| `is_target_of_war`       | `yes/no`                  | Being attacked            |
| `days_of_continuous_war` | `>= N`                    | War duration in days      |
| `can_declare_war`        | `{ defender = X cb = Y }` | War declaration available |
| `can_join_faction`       | faction key               | Can join faction          |
| `any_targeting_faction`  | trigger block             | Targeted by faction       |
| `military_strength`      | `>= N`                    | Total military strength   |
| `num_of_soldiers`        | `>= N`                    | Current soldiers          |

---

## Culture & Faith Triggers

| Trigger                  | Value                                   | Description           |
| ------------------------ | --------------------------------------- | --------------------- |
| `culture`                | `scope:culture`                         | Exact culture match   |
| `culture`                | trigger block                           | Culture trigger block |
| `has_cultural_pillar`    | `heritage_X`                            | Heritage match        |
| `has_cultural_tradition` | `tradition_key`                         | Tradition present     |
| `has_innovation`         | `innovation_key`                        | Innovation unlocked   |
| `faith`                  | `scope:faith`                           | Exact faith match     |
| `faith`                  | trigger block                           | Faith trigger block   |
| `has_doctrine`           | `doctrine_key`                          | Faith doctrine        |
| `religion`               | trigger block                           | Religion group check  |
| `cultural_acceptance`    | `{ target = scope:culture value >= N }` | Cultural acceptance   |
| `same_culture`           | `scope:char`                            | Same culture as       |
| `same_faith`             | `scope:char`                            | Same faith as         |

```
culture = { has_cultural_pillar = heritage_orcish }
faith = { has_doctrine = tenet_warlike }
NOT = { same_culture = scope:zulgurub_holder }
```

---

## Province & Map Triggers

| Trigger               | Value                       | Description            |
| --------------------- | --------------------------- | ---------------------- |
| `location`            | trigger block               | Province trigger block |
| `geographical_region` | `region_key`                | In geographic region   |
| `county_control`      | `>= N`                      | Control level (0-100)  |
| `development_level`   | `>= N`                      | Development level      |
| `has_holding_type`    | `castle/city/temple/tribal` | Province holding type  |
| `has_building`        | `building_key`              | Building present       |

```
location = {
    geographical_region = world_eastern_kingdoms_azeroth_stranglethorn
}
```

---

## Dynasty & House Triggers

| Trigger                | Value           | Description             |
| ---------------------- | --------------- | ----------------------- |
| `dynasty`              | `scope:dynasty` | Specific dynasty        |
| `is_in_dynasty`        | `scope:char`    | Same dynasty as         |
| `dynasty_prestige`     | `>= N`          | Dynasty prestige level  |
| `has_dynasty_perk`     | `perk_key`      | Dynasty perk unlocked   |
| `has_dynasty_modifier` | `modifier_key`  | Dynasty modifier active |

---

## Faction Triggers

| Trigger                 | Value         | Description              |
| ----------------------- | ------------- | ------------------------ |
| `is_in_faction`         | `faction_key` | Member of faction        |
| `can_join_faction`      | `faction_key` | Eligible to join         |
| `faction_power`         | `>= N`        | Faction power level      |
| `any_targeting_faction` | trigger block | Faction targeting player |

---

## Variable Triggers

```
exists = var:my_variable               # Variable is set
var:my_variable >= 5                   # Numeric comparison
var:my_variable = 3                    # Exact match
```

---

## Scope Existence Triggers

Always check existence before accessing potentially null scopes:

```
exists = primary_spouse
exists = scope:my_saved_scope
exists = title:k_gurubashi.holder
```

---

## Script Value Triggers

Script values are named numeric expressions reusable across triggers:

```
# In common/script_values/
my_invasion_score = {
    value = 0
    add = { value = 10; if = { limit = { has_trait = brave } } }
    add = { value = 5; if = { limit = { martial >= 15 } } }
}

# In trigger:
my_invasion_score >= 10
```

---

## Count/Percent Modifiers on List Triggers

```
any_vassal = {
    count >= 3         # At least 3 vassals match
    has_trait = ambitious
}

any_vassal = {
    count = all        # All vassals must match
    has_trait = content
}

any_vassal = {
    percent >= 0.5     # At least 50% of vassals match
    has_trait = ambitious
}
```
