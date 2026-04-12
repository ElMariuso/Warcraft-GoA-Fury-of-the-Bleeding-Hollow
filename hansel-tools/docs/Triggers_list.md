# Triggers List — CK3 Modding Reference

> **Vue rapide** : Index compact des triggers CK3 les plus utilisés en modding. Source : `script_docs` console command → `triggers.log`. Liste non exhaustive.

---

## Etat du personnage

| Nom                    | Scope     | Description                       |
| ---------------------- | --------- | --------------------------------- |
| `is_ai`                | character | yes/no — est contrôlé par l'IA    |
| `is_alive`             | character | yes/no — est vivant               |
| `is_adult`             | character | yes/no — est adulte               |
| `is_female`            | character | yes/no — est une femme            |
| `is_male`              | character | yes/no — est un homme             |
| `is_landed`            | character | yes/no — possède un titre         |
| `is_ruler`             | character | yes/no — est un dirigeant         |
| `is_independent_ruler` | character | yes/no — dirigeant indépendant    |
| `is_at_war`            | character | yes/no — est en guerre            |
| `is_at_war_with`       | character | `is_at_war_with = scope:enemy`    |
| `is_imprisoned`        | character | yes/no — est emprisonné           |
| `is_imprisoned_by`     | character | `is_imprisoned_by = scope:jailer` |
| `is_married`           | character | yes/no                            |
| `is_betrothed`         | character | yes/no                            |

## Comparaisons numériques

| Nom                       | Scope     | Opérateurs                                |
| ------------------------- | --------- | ----------------------------------------- |
| `age`                     | character | `age >= 16` — <, <=, =, !=, >, >=         |
| `gold`                    | character | Quantité d'or                             |
| `prestige`                | character | Prestige courant                          |
| `piety`                   | character | Piété courante                            |
| `stress`                  | character | Niveau de stress                          |
| `dread`                   | character | Niveau de terreur                         |
| `opinion`                 | character | `opinion = { target = X value >= 50 }`    |
| `diplomacy`               | character | Skill diplomatie                          |
| `martial`                 | character | Skill martial                             |
| `stewardship`             | character | Skill intendance                          |
| `intrigue`                | character | Skill intrigue                            |
| `learning`                | character | Skill savoir                              |
| `prowess`                 | character | Skill prouesse                            |
| `domain_size`             | character | Nombre de domaines détenus                |
| `realm_size`              | character | Taille du royaume                         |
| `sub_realm_size`          | character | Taille du sous-royaume                    |
| `dynasty_prestige`        | dynasty   | Prestige dynastique                       |
| `highest_held_title_tier` | character | `highest_held_title_tier >= tier_kingdom` |

## Traits, Modifs, Culture, Faith

| Nom                      | Scope       | Description                             |
| ------------------------ | ----------- | --------------------------------------- |
| `has_trait`              | character   | `has_trait = brave`                     |
| `has_character_modifier` | character   | `has_character_modifier = modifier_key` |
| `has_culture`            | char/county | `has_culture = culture:blackrock`       |
| `has_faith`              | char/county | `has_faith = faith:shamanism`           |
| `has_religion`           | char/faith  | `has_religion = religion:key`           |
| `has_government`         | character   | `has_government = tribal_government`    |
| `has_dynasty`            | character   | `has_dynasty = dynasty:2001`            |
| `has_dynasty_modifier`   | dynasty     | Vérifie un modif de dynastie            |
| `has_dynasty_perk`       | dynasty     | Vérifie un perk dynastique              |
| `has_county_modifier`    | county      | Vérifie un modif de comté               |
| `has_province_modifier`  | province    | Vérifie un modif de province            |
| `has_nickname`           | character   | `has_nickname = nick_the_bold`          |

## Titres & Vassalité

| Nom                                | Scope     | Description                      |
| ---------------------------------- | --------- | -------------------------------- |
| `has_claim_on`                     | character | `has_claim_on = title:k_england` |
| `holds_title`                      | character | `holds_title = title:e_horde`    |
| `has_realm_law`                    | character | `has_realm_law = law_key`        |
| `target_is_liege_or_above`         | character | Le target est liège ou au-dessus |
| `target_is_de_jure_liege_or_above` | character | Idem de jure                     |
| `government_has_flag`              | character | `government_has_flag = flag_key` |

## Flags, Variables, Hooks

| Nom                                 | Scope     | Description                                           |
| ----------------------------------- | --------- | ----------------------------------------------------- |
| `has_character_flag`                | character | `has_character_flag = flag_name`                      |
| `has_variable`                      | any       | `has_variable = var_name`                             |
| `has_global_variable`               | none      | `has_global_variable = var_name`                      |
| `has_hook`                          | character | `has_hook = { target = scope:char type = hook_type }` |
| `has_perk`                          | character | `has_perk = perk_key`                                 |
| `has_secret_relation_lover`         | character | Relations secrètes (variantes : friend, rival, etc.)  |
| `has_relation_friend`               | character | `has_relation_friend = scope:char`                    |
| `is_target_in_variable_list`        | any       | Target est dans une liste nommée                      |
| `is_target_in_global_variable_list` | any       | Idem pour liste globale                               |

## Scope & Existence

| Nom                  | Scope | Description                                 |
| -------------------- | ----- | ------------------------------------------- |
| `exists`             | any   | `exists = scope:my_scope` — le scope existe |
| `always`             | any   | `always = yes/no` — true/false constant     |
| `custom_description` | any   | Tooltip custom pour un bloc de triggers     |

## Opérateurs logiques

| Nom               | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| `AND`             | Toutes les conditions doivent être vraies (implicite dans un bloc) |
| `OR`              | Au moins une condition vraie                                       |
| `NOT`             | Négation                                                           |
| `NOR`             | Aucune condition vraie                                             |
| `NAND`            | Au moins une condition fausse                                      |
| `trigger_if`      | `trigger_if = { limit = { X } Y }` — Y évalué seulement si X vrai  |
| `trigger_else_if` | Branche alternative conditionnelle                                 |
| `trigger_else`    | Fallback                                                           |

## Itérateurs (any_)

Chaque itérateur teste si au moins `count` éléments matchent : `any_X = { count >= 3 <triggers> }`.

| Nom                       | Scope     | Cible                               |
| ------------------------- | --------- | ----------------------------------- |
| `any_vassal`              | character | character — vassaux directs         |
| `any_vassal_or_below`     | character | character — vassaux récursifs       |
| `any_child`               | character | character — enfants                 |
| `any_sibling`             | character | character — frères/soeurs           |
| `any_spouse`              | character | character — épouses                 |
| `any_courtier`            | character | character — courtisans              |
| `any_held_title`          | character | title — titres détenus              |
| `any_realm_county`        | character | title — comtés du royaume           |
| `any_realm_province`      | character | province — provinces                |
| `any_sub_realm_county`    | character | title — sous-royaume récursif       |
| `any_ally`                | character | character — alliés                  |
| `any_war_enemy`           | character | character — ennemis en guerre       |
| `any_close_family_member` | character | character — famille proche          |
| `any_dynasty_member`      | dynasty   | character — membres de dynastie     |
| `any_claim`               | character | title — claims détenus              |
| `any_heir`                | character | character — héritiers               |
| `any_army`                | character | army — armées                       |
| `any_de_jure_county`      | title     | title — comtés de jure              |
| `any_county`              | none      | title — tous les comtés du jeu      |
| `any_county_in_region`    | none      | title — `{ region = region_key }`   |
| `any_living_character`    | none      | character — tous les vivants (LENT) |
| `any_player`              | none      | character — tous les joueurs        |
