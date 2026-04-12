# Holdings Modding

> **Vue rapide** : Holdings et buildings definissent economie et troupes. `common/holdings/` et `common/buildings/`.

---

## Concept

Un holding type definit les batiments disponibles. Les buildings ajoutent levies, revenu, modificateurs. Types : `regular`, `special`, `duchy_capital`.

## Holding type

```jomini
# common/holdings/my_holding.txt
my_holding = {
    primary_building = my_building_01
    buildings = { my_church_01 my_castle_01 my_armoury_01 }
    flag = my_flag
    can_be_inherited = yes
}
```

Modificateurs auto-generes : `<type>_build_speed`, `<type>_build_gold_cost`, `<type>_holding_build_speed`, variantes `_piety_cost`/`_prestige_cost`.

## Building

```jomini
# common/buildings/my_buildings.txt
my_building_01 = {
    levy = 200
    max_garrison = 100
    construction_time = 720
    cost = { gold = 500 }
    type = regular                   # regular | special | duchy_capital
    next_building = my_building_02   # upgrade chain

    can_construct_potential = { }    # visible dans le menu ?
    can_construct = {                # constructible ?
        building_requirement_castle_city_church = { LEVEL = 01 }
    }

    province_modifier = { levy_reinforcement_rate = 0.01 }
    character_modifier = { monthly_prestige = 0.1 }
    county_modifier = { development_growth_factor = 0.1 }

    # Conditionnels (culture/faith/terrain/dynasty)
    province_culture_modifier = { parameter = culture_param }
    province_terrain_modifier = { terrain = mountains }
    county_dynasty_modifier = {
        county_holder_dynasty_perk = my_legacy_1
        monthly_income = 0.2
    }
    duchy_capital_county_modifier = { development_growth_factor = 0.1 }

    on_complete = { }
    ai_value = { base = 100 }
    flag = castle
}
```

## Ajouter un building via effect

```jomini
scope:county = { add_building = my_building_01 }
```

## Game concept et localization

```jomini
# common/game_concepts/
my_holding = {
    alias = { my mine }
    parent = holding_type
    texture = "gfx/interface/icons/my_holding_icon.dds"
}
```

```
my_holding:0 "My Holding"
my_building_01:0 "My Building"
my_building_01_desc:0 "Description."
```
