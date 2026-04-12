# Dynasties Modding

> **Vue rapide** : Les dynasties et maisons sont définies dans `common/dynasties/` (définitions) et `history/dynasties/` (legacy historique). Chaque personnage appartient à une dynasty via son ID.

---

## Dynasties vs Maisons

- **Dynasty** : lignée principale (ex: Doomhammer). Définie par un ID numérique
- **Dynasty House** : branche d'une dynasty (ex: une branche cadette). Rattachée via `dynasty`

## Définition d'une dynasty

```jomini
# common/dynasties/00_orcish_dynasties.txt
2001 = {
    name = "dyn_doomhammer"
    culture = "blackrock"

    # Optionnel
    motto = "dyn_doomhammer_motto"
    forced_coa_religiongroup = "shamanism_group"
}
```

## Définition d'une maison

```jomini
# common/dynasty_houses/00_orcish_houses.txt
dynasty_house_doomhammer_main = {
    name = "dyn_house_doomhammer"
    dynasty = 2001             # Rattachée à la dynasty Doomhammer
    motto = "dyn_house_doomhammer_motto"
}
```

## Lien avec les personnages

Dans `history/characters/`, le champ `dynasty` rattache un personnage :

```jomini
10050 = {
    name = "Orgrim"
    dynasty = 2001            # Dynasty Doomhammer
    culture = "blackrock"
    religion = "shamanism"
    583.1.1 = { birth = yes }
}
```

## Dynasty Legacies

Les legacies sont les bonus débloqués par la dynasty dans `common/dynasty_legacies/`.

```jomini
legacy_track_warfare = {
    legacy_warfare_1 = {
        # Coût en renown
        prestige_cost = { value = 1000 }
        # Bonus
        character_modifier = {
            knight_effectiveness_mult = 0.15
        }
    }
}
```

## Coat of Arms

Les blasons sont définis dans `common/coat_of_arms/coat_of_arms/` et liés par convention de nommage (même ID que la dynasty) ou via `coat_of_arms` dans la définition.

## Règles clés

- L'ID dynasty est un entier unique global — attention aux collisions entre mods
- Un personnage sans `dynasty` est lowborn (roturier)
- `culture` dans la dynasty = culture par défaut pour le blason, pas pour les membres
- Localisation requise : `dyn_<name>` et `dyn_<name>_prefix` dans les `.yml`
- Les maisons héritent du blason dynasty sauf override explicite
