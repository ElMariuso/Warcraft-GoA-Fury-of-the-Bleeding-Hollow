# CK3 Effects — Quick Reference

> **Vue rapide** : Un effet modifie l'etat du jeu. Execute dans `immediate = { }`, `option = { }`, `effect = { }`, `after = { }`. Le scope courant determine la cible.

---

## Formes syntaxiques

```jomini
# Boolean — pas d'argument
release_from_prison = yes

# Simple — une valeur, un scope, ou une cle
add_gold = 1000
marry = scope:bride
add_trait = brave

# Complexe — bloc avec parametres
add_character_modifier = { modifier = key duration = 365 }
```

---

## Ressources

```jomini
add_gold = N               # character — ajoute or (negatif pour retirer)
remove_gold = N             # character — retire or
add_prestige = N            # character
add_piety = N               # character
add_stress = N              # character
add_dread = N               # character
```

## Traits

```jomini
add_trait = trait_key        # character — ajoute un trait
remove_trait = trait_key     # character — retire un trait
add_trait_force = trait_key  # character — ignore les regles de compatibilite
```

## Modificateurs

```jomini
# Character modifier — duration en jours (-1 = permanent)
add_character_modifier = {
    modifier = horde_conqueror_modifier
    duration = -1
}
remove_character_modifier = horde_conqueror_modifier

# Province modifier
add_province_modifier = {
    modifier = recently_sacked_by_the_horde_modifier
    duration = 3650
}
remove_province_modifier = recently_sacked_by_the_horde_modifier
```

## Scopes et variables

```jomini
# Sauvegarder un scope pour reference ulterieure
save_scope_as = kilrogg              # sauvegarde le scope courant

# Sauvegarder une valeur calculee
save_scope_value_as = {
    name = army_size
    value = max_military_strength
}

# Variables persistantes (sauvegardees dans la save)
set_variable = { name = invasion_stage value = 1 }
change_variable = { name = invasion_stage add = 1 }
remove_variable = invasion_stage
```

## Events

```jomini
# Declencher un event — immediat
trigger_event = { id = wc_horde_invasion.1001 }

# Avec delai fixe (jours)
trigger_event = { id = wc_bleeding_hollow_invasion.1000 days = 14 }

# Avec delai aleatoire (min max)
trigger_event = { id = wc_horde_invasion.2001 days = { 10 20 } }
```

## Story cycles

```jomini
# Creer un story cycle — le scope courant devient story_owner
create_story = story_horde_invasion

# Terminer le story cycle courant
end_story = yes

# Changer le proprietaire
make_story_owner = scope:new_owner
```

## Armees

```jomini
# Spawn de troupes
spawn_army = {
    men_at_arms = { type = light_infantry men = 500 }
    location = scope:loc
    origin = scope:loc
}

# Ou via scripted effect parametre
spawn_orc_troops_based_on_culture_effect = {
    OWNER = scope:kilrogg
    LOCATION = title:c_vekrishe.title_province
}
```

## Conversions culture/foi

```jomini
set_culture = culture:bleeding_hollow     # character ou province
set_faith = faith:shamanism               # character ou province
set_county_culture = culture:orcish       # county scope
set_county_faith = faith:shamanism        # county scope
```

## Mort et emprisonnement

```jomini
death = { death_reason = death_battle killer = scope:orgrim }
imprison = {
    target = scope:prisoner
    type = dungeon
}
release_from_prison = yes
```

## Opinions et relations

```jomini
add_opinion = { target = scope:kilrogg modifier = loyalty_modifier opinion = 20 }
reverse_add_opinion = { target = scope:blackhand modifier = angry_modifier opinion = -30 }
set_relation_rival = scope:target
set_relation_friend = scope:target
```

## Controle conditionnel

```jomini
if = { limit = { has_trait = brave } add_prestige = 100 }
else_if = { limit = { has_trait = craven } add_stress = 50 }
else = { add_prestige = 25 }
```

## Iterateurs (every/random/ordered)

```jomini
every_vassal = { add_opinion = { target = root modifier = fear opinion = -10 } }
random_vassal = { limit = { is_ai = yes } add_gold = 50 }
```

## show_as_tooltip

Previsualise un effet dans l'UI sans l'executer. Toujours doubler avec l'effet reel.

```jomini
option = {
    show_as_tooltip = { add_prestige = 500 }
    # L'effet reel dans le corps de l'option
    add_prestige = 500
}
```

## Exemple complet

```jomini
# Effet composite — sac d'un comte
horde_bloodshed_effect = {
    add_character_modifier = {
        modifier = horde_conqueror_modifier
        duration = -1
    }
    $TARGET$ = {
        set_culture = culture:orcish
        add_province_modifier = {
            modifier = recently_sacked_by_the_horde_modifier
            duration = 3650
        }
    }
}
```
