# Religions Modding

> **Vue rapide** : Hierarchie famille > religion > foi. Definies dans `common/religion/religions/` avec doctrines, tenets, et sites saints.

---

## Concept

religion_family > religion > faith. Les niveaux inferieurs overrident les superieurs. Les faiths sont ce que les personnages pratiquent.

## Religion family

```jomini
# common/religion/religion_families/my_family.txt
rf_my_family = {
    is_pagan = no
    graphical_faith = "catholic_gfx"
    piety_icon_group = christian
    doctrine_background_icon = core_tenet_banner_christian.dds
    hostility_doctrine = my_hostility_doctrine
}
```

## Religion

```jomini
# common/religion/religions/my_religion.txt
my_religion = {
    family = rf_my_family
    pagan_roots = yes

    # Doctrines (appliquees a toutes les fois)
    doctrine = doctrine_spiritual_head
    doctrine = doctrine_gender_male_dominated
    doctrine = doctrine_concubines
    doctrine = doctrine_homosexuality_shunned
    doctrine = doctrine_clerical_function_taxation

    traits = {
        virtues = { brave generous }
        sins = { craven greedy }
    }

    holy_order_names = {
        { name = "holy_order_my_warriors" coat_of_arms = "ho_coa_1" }
    }
    holy_order_maa = { huscarl }

    localization = {
        HighGodName = my_high_god
        HouseOfWorship = my_temple
        # 60+ cles : DevilName, PriestMale, ReligiousText, etc.
    }

    faiths = { my_faith = { ... } }
}
```

## Faith

```jomini
faiths = {
    my_faith = {
        color = { 0.2 0.2 0.9 }
        icon = my_faith_icon
        holy_site = jerusalem
        holy_site = rome
        doctrine = tenet_warmonger
        doctrine = tenet_ancestor_worship
        religious_head = d_my_papacy   # optionnel
    }
}
```

## Holy sites

```jomini
# common/religion/holy_sites/my_sites.txt
my_holy_site = {
    county = c_jerusalem
    barony = b_jerusalem            # optionnel
    character_modifier = { monthly_piety_gain_mult = 0.2 }
    flag = jerusalem_conversion_bonus
}
```

## Localization et GFX

Cles obligatoires : `<name>`, `<name>_adj`, `<name>_adherent`, `<name>_adherent_plural`, `<name>_desc`.
Bloc `localization = { ... }` dans la religion : 60+ cles (HighGodName, DevilName, PriestMale, HouseOfWorship, etc.).
Icone de foi : `gfx/interface/icons/faith/<icon_name>.dds` (100x100).

## Conversion via script

```jomini
set_character_faith = faith:my_faith
create_faith = { parent = faith:my_faith  template = "reformed"  doctrine = tenet_armed_pilgrimages }
```
