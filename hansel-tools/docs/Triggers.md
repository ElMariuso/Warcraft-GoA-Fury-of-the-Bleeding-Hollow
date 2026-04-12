# CK3 Triggers — Quick Reference

> **Vue rapide** : Un trigger est une condition qui retourne true/false dans un scope donné. Utilisé dans `trigger = { }`, `limit = { }`, `is_shown = { }`.

---

## Logique

Combinaison de triggers. Par defaut, un bloc trigger est un AND implicite.

```jomini
AND = { <triggers> }    # toutes vraies (implicite dans un bloc)
OR = { <triggers> }     # au moins une vraie
NOT = { <trigger> }     # inverse une condition
NOR = { <triggers> }    # aucune vraie
NAND = { <triggers> }   # pas toutes vraies
```

## Identite / Scope

```jomini
exists = scope:nom             # scope sauvegarde existe — any scope
is_ai = yes                    # est un AI — character
is_alive = yes                 # est vivant — character
is_landed = yes                # possede un titre — character
is_ruler = yes                 # est dirigeant — character
is_independent_ruler = yes     # pas de suzerain — character
```

## Comparaisons numeriques

Operateurs : `=`, `>=`, `<=`, `>`, `<`. Acceptent valeurs, scopes, variables.

```jomini
age >= 16                      # character
gold >= 200                    # character
prestige >= 500                # character
piety >= 100                   # character
opinion = { who = scope:target value >= 20 }  # character
```

## Traits et modificateurs

```jomini
has_trait = brave                           # character
has_character_modifier = path_to_glory_modifier  # character
has_culture = culture:bleeding_hollow       # character/province
has_faith = faith:shamanism                 # character/province
has_heritage = heritage:heritage_orcish     # culture
```

## Titres et vassaux

```jomini
is_holder_of = title:k_bleeding_hollow_clan  # character
has_title = title:e_horde                    # character (any in realm)
liege = { has_trait = ambitious }             # scope sur le suzerain — character
vassal_of = scope:kilrogg                    # est vassal de — character
any_vassal = { has_trait = brave }           # au moins un vassal satisfait — character
any_held_title = { tier = tier_kingdom }     # character
```

## Story cycles

```jomini
has_story = story_horde_invasion   # a ce story cycle actif — character
is_story_owner = yes               # est proprietaire du story — character
```

## Iterateurs (any/every/random)

Retournent true si au moins un element satisfait les triggers (any_), ou appliquent a tous (every_).

```jomini
any_vassal = { <triggers> }        # au moins un vassal
any_realm_province = { <triggers> }
any_held_title = { <triggers> }
any_courtier = { <triggers> }
```

## trigger_if / trigger_else

Evaluation conditionnelle dans un bloc trigger.

```jomini
trigger_if = {
    limit = { is_ai = yes }
    gold >= 100
}
trigger_else = {
    gold >= 500
}
```

## Exemple complet

```jomini
# Trigger compose — vassal riche et courageux
trigger = {
    is_landed = yes
    gold >= 200
    has_trait = brave
    NOT = { has_character_modifier = path_to_glory_modifier }
    any_vassal = {
        opinion = { who = root value >= 0 }
    }
}
```
