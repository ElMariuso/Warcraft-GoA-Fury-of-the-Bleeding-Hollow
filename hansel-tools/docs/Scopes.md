# Scopes

> **Vue rapide** : un scope est l'entité courante sur laquelle s'exécutent les effets et triggers. Naviguer entre scopes = changer de contexte.

---

## Qu'est-ce qu'un scope

Le scope courant détermine **qui** est affecté par les effets et **quoi** est testé par les triggers. Types principaux : `character`, `landed_title`, `province`, `story`, `faith`, `culture`.

```jomini
# Dans un event, le scope par défaut est le personnage qui reçoit l'event
immediate = {
    add_gold = 100    # ajoute 100 or au personnage courant
}
```

## Naviguer les scopes

| Mot-clé     | Rôle                                              |
| ----------- | ------------------------------------------------- |
| `root`      | Scope initial du bloc (event owner, story owner…) |
| `prev`      | Scope précédent dans la pile (non chaînable)      |
| `this`      | Scope courant explicite (utile pour comparaisons) |
| `scope:nom` | Scope sauvegardé avec `save_scope_as`             |

```jomini
title:k_france = {
    holder = {
        prev = {
            # retour au scope title:k_france
        }
    }
}
```

## Sauvegarder un scope

```jomini
title:k_france.holder = {
    save_scope_as = roi_france
}
# Plus tard, n'importe où dans la chaîne d'effets :
scope:roi_france = {
    add_prestige = 500
}
```

Les saved scopes persistent dans les events/effects chaînés. Ils sont automatiquement libérés à la fin de la chaîne. `save_temporary_scope_as` expire à la fin du bloc courant.

## Naviguer vers un personnage lié

| Event target     | Depuis       | Vers                        |
| ---------------- | ------------ | --------------------------- |
| `liege`          | character    | Suzerain direct             |
| `heir`           | character    | Héritier primaire           |
| `primary_spouse` | character    | Conjoint principal          |
| `father/mother`  | character    | Parent                      |
| `story_owner`    | story        | Propriétaire du story cycle |
| `holder`         | landed_title | Détenteur du titre          |

## Naviguer vers un titre

```jomini
title:e_horde = { }                  # accès direct par clé
title:e_horde.holder = { }           # détenteur du titre (chaîné)
primary_title = { }                  # titre principal du personnage courant
```

## Itérateurs

Quand un scope a **plusieurs** relations (enfants, vassaux…), on utilise des itérateurs :

| Préfixe    | Type    | Usage                                         |
| ---------- | ------- | --------------------------------------------- |
| `every_`   | effect  | Tous les éléments                             |
| `random_`  | effect  | Un élément aléatoire (avec `weight`)          |
| `ordered_` | effect  | Trié par `order_by` (premier par défaut)      |
| `any_`     | trigger | Vrai si au moins un élément satisfait le test |

```jomini
every_vassal = {
    limit = { gold >= 100 }
    add_gold = -50
}

random_vassal = {
    weight = { base = 10 modifier = { add = 20 has_trait = brave } }
    save_scope_as = champion
}
```

## Exemple : navigation imbriquée

```jomini
# Depuis un event déclenché sur character scope
immediate = {
    save_scope_as = actor
    liege = {
        save_scope_as = suzerain
        every_vassal = {
            limit = { gold >= 100 }
            add_gold = -50
        }
    }
}
```

## Scope dans les story cycles

Le scope dans `on_setup` / `on_end` / `on_owner_death` est le story cycle lui-même. Utiliser `story_owner` pour accéder au propriétaire.

```jomini
on_setup = {
    story_owner = {
        save_scope_as = owner
        trigger_event = { id = wc_exemple.1000 days = 14 }
    }
}
```
