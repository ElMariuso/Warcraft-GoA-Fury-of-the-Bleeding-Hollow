# Regiments Modding

> **Vue rapide** : Les Men-at-Arms (MaA) sont définis dans `common/men_at_arms_types/`. Chaque type spécifie stats, coûts, counters et terrain bonus.

---

## Définir un régiment

```jomini
example_maa = {
    type = skirmishers
    damage = 10
    toughness = 10
    pursuit = 10
    screen = 10
    stack = 100              # hommes par unité

    terrain_bonus = {
        forest = { damage = 3  screen = 3 }
    }
    counters = {
        heavy_infantry = 1
    }

    buy_cost = { gold = 150 }
    low_maintenance_cost = { gold = 1 }
    high_maintenance_cost = { gold = 5 }

    ai_quality = { value = culture_ai_weight_pikemen }
    icon = skirmishers       # nom du .dds sans extension
}
```

## Variables principales

| Variable                          | Description                                                |
| --------------------------------- | ---------------------------------------------------------- |
| `type`                            | Type d'unité (skirmishers, cavalry, heavy_infantry...)     |
| `can_recruit`                     | Trigger optionnel (scope character) pour recruter          |
| `damage/toughness/pursuit/screen` | Stats de combat                                            |
| `terrain_bonus`                   | Bonus par terrain (forest, mountains, etc.)                |
| `counters`                        | Types d'unités contrées                                    |
| `siege_tier`                      | Efficacité contre les forts                                |
| `fights_in_main_phase`            | `no` = n'agit qu'en phase poursuite (ex: engins de siège)  |
| `winter_bonus`                    | Bonus/malus par type d'hiver (normal_winter, harsh_winter) |

## Débloquer via Innovation

```jomini
unlock_maa = my_maa         # dans la définition d'innovation

# Ou bonus sur un type existant :
maa_upgrade = {
    type = cavalry
    damage = 0.1
    toughness = 0.1
}
```

## Débloquer via Tradition culturelle

Dans la tradition : `parameters = { unlock_my_maa = yes }`

Dans le MaA :

```jomini
can_recruit = {
    culture = { has_cultural_parameter = unlock_my_maa }
}
```

## Localisation

```yaml
my_maa:0 "My Men at Arms"
my_maa_flavor:0 "#F Description du régiment.#!"
```
