# Scopes List

> **Vue rapide** : Un scope est le contexte d'exécution dans lequel les triggers et effects opèrent. Chaque scope a un type (character, title, province...) qui détermine les opérations disponibles.

---

## Scopes principaux

| Scope          | Accès depuis                            | Utilité principale                 |
| -------------- | --------------------------------------- | ---------------------------------- |
| `character`    | `root`, `character:<id>`, scope saves   | Stats, traits, relations, opinion  |
| `landed_title` | `title:<key>`, `primary_title`          | Hiérarchie, holder, de jure        |
| `province`     | `title:b_<key>`, `capital_province`     | Terrain, buildings, culture locale |
| `county`       | `title:c_<key>`, `capital_county`       | Développement, contrôle, opinion   |
| `faith`        | `faith`, `root.faith`                   | Doctrines, ferveur, holy sites     |
| `culture`      | `culture`, `root.culture`               | Traditions, innovations, heritage  |
| `dynasty`      | `dynasty`, `root.dynasty`               | Prestige, legacies, members        |
| `house`        | `house`, `root.house`                   | Branche dynasty, head              |
| `story_cycle`  | `story_owner.story`                     | Story events, data                 |
| `army`         | `army` (in combat triggers)             | Troupes, commander                 |
| `war`          | `primary_war`                           | Attacker, defender, war score      |
| `struggle`     | `struggle:<key>`                        | Phases, involvement                |
| `scheme`       | `scheme` (in scheme triggers)           | Target, type, progress             |
| `combat_side`  | dans combat triggers                    | Attacker/defender side             |
| `secret`       | `secret` (in secret triggers)           | Type, owner, knowers               |
| `artifact`     | `artifact` (in artifact triggers)       | Type, quality, owner               |
| `inspiration`  | `inspiration` (in inspiration triggers) | Type, progress, sponsor            |

## Navigation entre scopes

```jomini
# Depuis un character → ses scopes liés
root = {                          # Character scope
    primary_title = { ... }       # → landed_title
    faith = { ... }               # → faith
    culture = { ... }             # → culture
    dynasty = { ... }             # → dynasty
    capital_province = { ... }    # → province
    liege = { ... }               # → character (liege)
    primary_heir = { ... }        # → character
    primary_war = { ... }         # → war
}
```

## Accès directs (global scopes)

```jomini
character:10005 = { ... }         # Character par ID
title:e_horde = { ... }           # Titre par clé
faith:shamanism = { ... }         # Foi par clé
culture:blackrock = { ... }       # Culture par clé
struggle:struggle_key = { ... }   # Struggle par clé
```

## Scope sauvegardé

```jomini
save_scope_as = kilrogg            # Sauvegarde le scope courant
scope:kilrogg = { ... }            # Accès ultérieur dans le même event
```

## Listes de scopes (every/any/random)

```jomini
# Itération sur des listes
every_vassal = { add_opinion = { target = root modifier = grateful } }
any_vassal = { prowess >= 15 }     # Trigger : au moins un vassal
random_vassal = {
    limit = { prowess >= 10 }
    weight = { base = 1 modifier = { add = 5 trigger = { martial >= 15 } } }
    save_scope_as = champion
}
```

## Listes communes par scope

| Scope source   | Listes disponibles                                                              |
| -------------- | ------------------------------------------------------------------------------- |
| `character`    | `vassal`, `courtier`, `knight`, `child`, `sibling`, `spouse`, `claim`, `secret` |
| `landed_title` | `in_de_jure_hierarchy`, `county`, `directly_owned_barony`                       |
| `faith`        | `holy_site`, `faith_character`                                                  |
| `culture`      | `culture_character`, `parent_culture`                                           |
| `war`          | `war_attacker`, `war_defender`, `war_participant`                               |

## Triggers de type (vérifier le scope courant)

```jomini
is_landed = yes                    # Character possède un titre
is_alive = yes                     # Character vivant
tier = tier_kingdom                # Title est de tier kingdom
has_holder = yes                   # Title a un détenteur
```

## Règles clés

- Erreur fréquente : utiliser un effect/trigger character dans un scope title (ou inverse)
- `root` = le scope initial de l'event (généralement le personnage qui le reçoit)
- `prev` = le scope parent dans un bloc imbriqué — fragile, préférer `save_scope_as`
- `this` = le scope courant (rarement nécessaire explicitement)
- Les scopes invalides provoquent des erreurs dans `error.log` au runtime
