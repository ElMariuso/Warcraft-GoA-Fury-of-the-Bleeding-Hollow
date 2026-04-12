# Effects List — CK3 Modding Reference

> **Vue rapide** : Index compact des effets CK3 les plus utilisés en modding, groupés par catégorie. Source : `script_docs` console command → `effects.log`. Liste non exhaustive — certains effets post-launch manquent.

---

## Ressources (Gold, Prestige, Piety, Stress, Dread)

| Nom                       | Scope     | Description                              |
| ------------------------- | --------- | ---------------------------------------- |
| `add_gold`                | character | Ajoute/retire de l'or                    |
| `add_prestige`            | character | Ajoute du prestige                       |
| `add_prestige_experience` | character | Ajoute de l'XP prestige (monte le level) |
| `add_piety`               | character | Ajoute de la piété                       |
| `add_piety_experience`    | character | Ajoute de l'XP piété                     |
| `add_stress`              | character | Ajoute/retire du stress                  |
| `add_dread`               | character | Ajoute/retire de la terreur              |
| `add_tyranny`             | character | Ajoute de la tyrannie                    |
| `add_legitimacy`          | character | Ajoute de la légitimité                  |
| `add_dynasty_prestige`    | dynasty   | Ajoute du prestige dynastique            |

## Traits

| Nom                       | Scope     | Description                               |
| ------------------------- | --------- | ----------------------------------------- |
| `add_trait`               | character | `add_trait = brave` — ajoute un trait     |
| `remove_trait`            | character | `remove_trait = craven` — retire un trait |
| `add_trait_force_tooltip` | character | Ajoute un trait avec tooltip forcé        |

## Modificateurs

| Nom                         | Scope         | Description                                                      |
| --------------------------- | ------------- | ---------------------------------------------------------------- |
| `add_character_modifier`    | character     | `{ modifier = name years = 10 }` — modif temporaire ou permanent |
| `remove_character_modifier` | character     | Retire un modificateur character                                 |
| `add_county_modifier`       | county/title  | Ajoute un modif de comté                                         |
| `remove_county_modifier`    | county/title  | Retire un modif de comté                                         |
| `add_province_modifier`     | province      | Ajoute un modif de province                                      |
| `remove_province_modifier`  | province      | Retire un modif de province                                      |
| `add_dynasty_modifier`      | dynasty       | Ajoute un modif de dynastie                                      |
| `add_house_modifier`        | dynasty house | Ajoute un modif de maison                                        |

## Scopes & Variables

| Nom                       | Scope     | Description                                                    |
| ------------------------- | --------- | -------------------------------------------------------------- |
| `save_scope_as`           | any       | `save_scope_as = my_name` — sauvegarde le scope courant        |
| `save_temporary_scope_as` | any       | Idem mais temporaire (disparaît après le bloc)                 |
| `set_variable`            | any       | `{ name = var_name value = 5 }` — crée/écrase une variable     |
| `change_variable`         | any       | `{ name = var_name add = 1 }` — modifie une variable existante |
| `remove_variable`         | any       | Supprime une variable                                          |
| `set_global_variable`     | none      | Variable globale persistante                                   |
| `change_global_variable`  | none      | Modifie une variable globale                                   |
| `add_to_list`             | any       | Ajoute le scope courant à une liste nommée                     |
| `remove_from_list`        | any       | Retire de la liste                                             |
| `add_character_flag`      | character | Flag booléen (optionnel : `{ flag = name years = 5 }`)         |
| `remove_character_flag`   | character | Retire un flag                                                 |

## Evenements & Story Cycles

| Nom                | Scope     | Description                                                   |
| ------------------ | --------- | ------------------------------------------------------------- |
| `trigger_event`    | character | `trigger_event = ns.0001` ou `{ id = ns.0001 days = 30 }`     |
| `create_story`     | character | `create_story = { type = story_name }` — lance un story cycle |
| `end_story`        | story     | Met fin au story cycle                                        |
| `make_story_owner` | story     | Change le propriétaire du story cycle                         |

## Personnages

| Nom                      | Scope     | Description                                                       |
| ------------------------ | --------- | ----------------------------------------------------------------- |
| `death`                  | character | `{ death_reason = death_battle killer = scope:enemy }`            |
| `imprison`               | character | `{ target = scope:prisoner type = dungeon }`                      |
| `release_from_prison`    | character | Libère un prisonnier                                              |
| `banish`                 | character | Bannit le personnage de la cour                                   |
| `create_character`       | none      | `{ name = "X" culture = Y faith = Z ... }`                        |
| `add_courtier`           | character | Ajoute un courtisan à la cour                                     |
| `marry`                  | character | `marry = scope:spouse`                                            |
| `divorce`                | character | `divorce = scope:spouse`                                          |
| `add_hook`               | character | `{ type = favor_hook target = scope:char }`                       |
| `remove_hook`            | character | Retire un hook                                                    |
| `set_relation_friend`    | character | `set_relation_friend = scope:char` (idem pour rival, lover, etc.) |
| `remove_relation_friend` | character | Retire la relation                                                |
| `add_opinion`            | character | `{ target = scope:char modifier = opinion_key }`                  |
| `reverse_add_opinion`    | character | Ajoute opinion inversée (target → scope)                          |
| `change_first_name`      | character | Change le prénom                                                  |
| `set_nickname`           | character | Ajoute un surnom                                                  |
| `add_secret`             | character | Crée un secret                                                    |
| `add_perk`               | character | Ajoute un perk de lifestyle                                       |

## Titres & Claims

| Nom                              | Scope     | Description                          |
| -------------------------------- | --------- | ------------------------------------ |
| `usurp_title`                    | character | `usurp_title = title:k_england`      |
| `destroy_title`                  | title     | Détruit le titre                     |
| `create_title_and_vassal_change` | character | Crée un titre et transfert vassal    |
| `give_title`                     | character | Transfert de titre                   |
| `add_pressed_claim`              | character | Ajoute un claim pressé               |
| `add_unpressed_claim`            | character | Ajoute un claim non pressé           |
| `remove_claim`                   | character | Retire un claim                      |
| `set_de_jure_liege`              | title     | Change le liège de jure              |
| `add_realm_law`                  | character | Ajoute/change une loi du royaume     |
| `set_owner`                      | artifact  | Change le propriétaire d'un artefact |

## Culture & Religion

| Nom                          | Scope            | Description                         |
| ---------------------------- | ---------------- | ----------------------------------- |
| `set_culture`                | character/county | Change la culture                   |
| `set_faith`                  | character/county | Change la foi                       |
| `change_cultural_acceptance` | culture          | `{ target = culture:X value = 10 }` |
| `add_doctrine`               | faith            | Ajoute une doctrine                 |
| `add_innovation`             | culture          | Ajoute une innovation               |

## Armée & Guerre

| Nom                 | Scope     | Description                                                     |
| ------------------- | --------- | --------------------------------------------------------------- |
| `spawn_army`        | character | `{ men_at_arms = { type = X men = 500 } location = scope:loc }` |
| `start_war`         | character | `{ cb = cb_type target = scope:enemy }`                         |
| `end_war`           | war       | `end_war = attacker/defender/white_peace`                       |
| `create_alliance`   | character | `{ target = scope:ally }`                                       |
| `dissolve_alliance` | character | Dissout l'alliance                                              |

## Flow Control (effets spéciaux)

| Nom                      | Scope     | Description                                    |
| ------------------------ | --------- | ---------------------------------------------- |
| `if`                     | any       | `if = { limit = { <triggers> } <effects> }`    |
| `else_if`                | any       | Branche alternative                            |
| `else`                   | any       | Fallback                                       |
| `hidden_effect`          | any       | Exécute sans tooltip                           |
| `show_as_tooltip`        | any       | Affiche un tooltip sans exécuter               |
| `custom_tooltip`         | any       | Texte custom dans le tooltip                   |
| `random`                 | any       | `random = { chance = 50 <effects> }`           |
| `random_list`            | any       | Liste pondérée `{ 10 = { ... } 90 = { ... } }` |
| `send_interface_message` | character | Notification UI au joueur                      |

## Itérateurs (every_, random_, ordered_)

Chaque itérateur existe en 3 variantes : `every_X`, `random_X`, `ordered_X`.

| Base                            | Scope     | Cible                               |
| ------------------------------- | --------- | ----------------------------------- |
| `_vassal`                       | character | character — tous les vassaux        |
| `_courtier`                     | character | character — tous les courtisans     |
| `_child`                        | character | character — tous les enfants        |
| `_spouse`                       | character | character — toutes les épouses      |
| `_held_title`                   | character | title — tous les titres détenus     |
| `_realm_county`                 | character | title — tous les comtés du royaume  |
| `_realm_province`               | character | province — toutes les provinces     |
| `_sub_realm_county`             | character | title — sous-royaume récursif       |
| `_dynasty_member`               | dynasty   | character — membres de dynastie     |
| `_de_jure_county`               | title     | title — comtés de jure              |
| `_direct_de_facto_vassal_title` | title     | title — titres vassaux de facto     |
| `_neighboring_county`           | county    | title — comtés voisins              |
| `_war_attacker`                 | war       | character — attaquants              |
| `_war_defender`                 | war       | character — défenseurs              |
| `_faction_member`               | faction   | character — membres de faction      |
| `_living_character`             | none      | character — tous les vivants (LENT) |
| `_player`                       | none      | character — tous les joueurs        |

Syntaxe : `every_X = { limit = { <triggers> } <effects> }`
Ordered ajoute : `order_by`, `position`, `min`, `max`.
Random ajoute : `weight = { mtth }`.
