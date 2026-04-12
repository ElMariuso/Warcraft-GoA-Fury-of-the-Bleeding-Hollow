# Characters Modding

> **Vue rapide** : Personnages definis dans `history/characters/` avec ID unique, attributs, traits, date blocks. Reference via `character:<id>`.

---

## Concept

Un personnage historique a un ID numerique unique, un nom, dynastie, culture, foi, traits, et des date blocks pour naissance/mort/mariages. Le jeu genere aleatoirement ce qui n'est pas specifie.

## Definition de base

```jomini
# history/characters/my_characters.txt
999001 = {
    name = "Henri"
    female = yes                    # optionnel, defaut = male
    dynasty = 2100001               # ou dynasty_house = house_id
    culture = french
    religion = catholic
    dna = my_custom_dna_entry       # optionnel, ref common/dna_data/

    # Attributs (base 0-100, aleatoire si omis)
    martial = 14
    diplomacy = 23
    intrigue = 10
    stewardship = 21
    learning = 8
    prowess = 5

    trait = diligent
    trait = education_learning_4
    disallow_random_traits = yes

    father = 999003
    mother = 999004
    sexuality = heterosexual        # heterosexual/homosexual/bisexual/asexual
    health = 5
    fertility = 0.8

    846.7.29 = { birth = yes }
    920.5.25 = { death = yes }
}
```

## Date blocks avances

```jomini
870.1.1 = {
    add_spouse = 999010
    give_nickname = nick_the_bold
    trait = scarred_2
    employer = 999020                # deplace a la cour
    give_council_position = councillor_marshal  # marshal/spymaster/chancellor/court_chaplain/steward
    effect = { add_character_flag = special_flag }
}
890.3.15 = { remove_spouse = 999010 }
```

## Reference dans les scripts

```jomini
character:999001 = {
    if = { limit = { is_alive = yes } }
    trigger_event = my_event.0001
}
character:10005 = { save_scope_as = kilrogg }
```

## Creer un personnage via effet

```jomini
create_character = {
    name = "Arthas"
    culture = culture:lordaeron
    faith = faith:light
    dynasty = dynasty:menethil
    age = 25
    trait = ambitious
    save_scope_as = new_char
}
```

## Apparence (DNA modifiers)

Definir dans `gfx/portraits/portrait_modifiers/`. Appliquer via `add_character_flag = { flag = my_modifier }` :

```jomini
my_modifier = {
    usage = game
    priority = 50
    my_modifier = {
        dna_modifiers = {
            accessory = { mode = add  gene = headgear  template = western_imperial  value = 1.0 }
        }
        weight = { base = 0  modifier = { add = 100  has_character_flag = my_modifier } }
    }
}
```
