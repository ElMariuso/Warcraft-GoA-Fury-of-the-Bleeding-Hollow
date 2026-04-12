# Scopes List

> **Vue rapide** : Les scopes sont des pointeurs vers les objets du jeu (caractères, titres, provinces). Chaque script navigue entre scopes pour accéder aux données et appliquer des effets.

---

## Concept

Un scope détermine la cible d'un trigger ou d'un effect. Le scope initial (`root`) est défini par le contexte (event owner, story owner). On navigue vers d'autres scopes via des accesseurs (`liege`, `capital_province`) ou des itérateurs (`every_vassal`).

## Scopes principaux

| Scope       | Accès            | Description                        |
| ----------- | ---------------- | ---------------------------------- |
| `character` | `character:<id>` | Personnage — scope le plus courant |
| `title`     | `title:<key>`    | Titre (landed ou titular)          |
| `province`  | `province:<id>`  | Province/baronnie sur la carte     |
| `faith`     | `faith:<key>`    | Religion/foi                       |
| `culture`   | `culture:<key>`  | Culture                            |
| `dynasty`   | `dynasty:<id>`   | Dynastie                           |
| `house`     | `house:<key>`    | Maison dynastique                  |

## Navigations courantes (depuis character)

```jomini
liege                    # Suzerain direct
top_liege                # Suzerain de plus haut rang
heir                     # Héritier principal
primary_title            # Titre principal
capital_province         # Province capitale
faith / culture / dynasty / house
```

## Depuis title

```jomini
title:k_bleeding_hollow_clan.holder   # Détenteur actuel
de_jure_liege                         # Titre suzerain de jure
capital_county                        # Comté capitale
```

## Itérateurs

| Pattern                    | Type    | Description                   |
| -------------------------- | ------- | ----------------------------- |
| `every_vassal { }`         | Effect  | Tous les vassaux du scope     |
| `every_held_title { }`     | Effect  | Tous les titres détenus       |
| `every_realm_province { }` | Effect  | Toutes les provinces du realm |
| `any_vassal { }`           | Trigger | Au moins un vassal match      |
| `random_vassal { }`        | Effect  | Un vassal aléatoire           |

## Scopes spéciaux

| Scope         | Usage                                      |
| ------------- | ------------------------------------------ |
| `root`        | Scope initial (event owner)                |
| `prev`        | Scope précédent dans la chaîne             |
| `this`        | Scope courant (implicite)                  |
| `story_owner` | Propriétaire du story cycle                |
| `scope:nom`   | Scope sauvegardé via `save_scope_as = nom` |

## Sauvegarde

```jomini
character:10005 = { save_scope_as = kilrogg }
title:e_horde = { save_scope_as = horde_empire }
scope:kilrogg = { add_prestige = 500 }
```

## Notes

- `scope:` est temporaire (durée du bloc).
- `every_*` exécute sur chaque match ; `any_*` teste l'existence.
- `random_*` + `limit = { }` pour filtrer avant sélection aléatoire.
