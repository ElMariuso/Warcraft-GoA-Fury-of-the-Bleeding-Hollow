# Culture Modding

> **Vue rapide** : Cultures = noms, ethnicites, heritages. Structure : culture_group > culture. `common/culture/cultures/`.

---

## Concept

Chaque culture appartient a un culture_group. Definit noms, patronymes, couleur carte, heritage, modificateurs. Traditions et innovations sont separees.

## Culture group

```jomini
# common/culture/cultures/my_group.txt
my_culture_group = {
    graphical_cultures = { my_coa_gfx my_building_gfx my_clothing_gfx my_unit_gfx }
    mercenary_names = {
        { name = "mercenary_my_company" coat_of_arms = "mc_my_coa" }
    }
    my_culture = { ... }   # cultures definies a l'interieur
}
```

## Culture

```jomini
my_culture = {
    color = { 0.1 0.75 0.1 }
    heritage = heritage_north_germanic
    character_modifier = { diplomacy = 1 }

    male_names = {
        10 = { Erik Olaf Sven }     # poids 10 = courant
        1 = { Ragnar Bjorn }        # poids 1 = rare
    }
    female_names = { Astrid Freya Ingrid }

    dynasty_names = {
        { dynnp_von dynn_Pommern }  # prefixe + nom
        dynn_Fournier               # nom seul
    }
    dynasty_of_location_prefix = "dynnp_von"

    # Heritage de noms (somme <= 100 par groupe)
    pat_grf_name_chance = 50
    mat_grf_name_chance = 5
    father_name_chance = 10
    pat_grm_name_chance = 10
    mat_grm_name_chance = 50
    mother_name_chance = 5

    patronym_suffix_male = "dynnpat_suf_son"
    patronym_suffix_female = "dynnpat_suf_sdaughter"
    always_use_patronym = yes

    ethnicities = { 10 = german  10 = caucasian }

    dynasty_title_names = no
    founder_named_dynasties = no
    dynasty_name_first = no      # style asiatique
}
```

## Modifier via event

```jomini
scope:culture = { add_culture_tradition = tradition_warrior_culture }
set_character_culture = culture:my_culture
set_county_culture = culture:my_culture
change_cultural_acceptance = { target = culture:french  value = 25  desc = reason }
```

## Convention d'ID

- Culture group : minuscules, espaces -> `_`, suffixe `_group`
- Culture : minuscules, supprimer les diacritiques
