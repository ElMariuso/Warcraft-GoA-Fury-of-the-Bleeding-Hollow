# Event Modding

> **Vue rapide** : les events sont des blocs narratifs scriptes dans `events/` (fichiers `.txt`). Ils ne se declenchent jamais seuls — toujours fires par un on_action, story cycle, decision ou autre effet.

---

## Structure minimale

```jomini
namespace = wc_exemple

wc_exemple.1001 = {
    type = character_event
    title = wc_exemple.1001.title
    desc = wc_exemple.1001.desc
    option = { name = wc_exemple.1001.a }
}
```

Namespace declare en debut de fichier. IDs de 1 a 9999 max par namespace.

## Types d'events

| Type               | Root scope | Usage                                 |
| ------------------ | ---------- | ------------------------------------- |
| `character_event`  | Personnage | Le plus courant, affiche portraits    |
| `letter_event`     | Personnage | Format lettre avec `sender = scope:X` |
| `fullscreen_event` | Personnage | Plein ecran (cinematiques)            |
| `hidden = yes`     | Variable   | Pas d'UI, maintenance en background   |

## Champs importants

**`immediate`** — execute avant l'affichage. Sauvegarder scopes et appliquer effets inconditionnels.

**`trigger`** — condition pour que l'event fire. Evaluee AVANT `immediate` (pas d'acces aux scopes crees dedans).

**`after`** — execute apres le choix d'une option. Nettoyage de variables.

**`content_source = dlc_GOA`** — obligatoire sur tout event visible (non-hidden) dans les mods GoA.

```jomini
immediate = {
    save_scope_as = owner
    character:10005 = { save_scope_as = kilrogg }
}
trigger = { is_ai = no }
```

## Options et ai_chance

Chaque option a un `name` (loc key), des effets, et un `ai_chance` obligatoire dans GoA.

```jomini
option = {
    name = wc_exemple.1001.a
    trigger = { has_trait = brave }        # option conditionnelle
    add_prestige = 200
    ai_chance = {
        base = 60
        ai_value_modifier = { ai_boldness = 0.5 }
    }
}
option = {
    name = wc_exemple.1001.b
    ai_chance = { base = 0 }              # non-canon : IA ne choisit jamais
}
```

Flags : `trait = brave` (icone), `add_internal_flag = dangerous` (rouge), `exclusive = yes` (seule si valide).

**`show_as_tooltip`** — previsualise un effet dans l'UI sans l'executer. Toujours pairer avec l'effet reel :

```jomini
show_as_tooltip = { add_prestige = 200 }  # preview seulement
add_prestige = 200                         # execution reelle
```

## first_valid (descriptions conditionnelles)

Affiche la premiere description dont le trigger est vrai. Fallback sans trigger en dernier.

```jomini
desc = {
    first_valid = {
        triggered_desc = {
            trigger = { scope:owner = { has_trait = brave } }
            desc = wc_exemple.1001.desc_brave
        }
        desc = wc_exemple.1001.desc
    }
}
```

Fonctionne aussi pour `title` et `flavor`.

## Declencher un event

```jomini
trigger_event = { id = wc_exemple.1002 days = 30 }   # avec delai
trigger_event = wc_exemple.1002                        # immediat
trigger_event = { on_action = my_on_action }           # via on_action
```

## Exemple complet

```jomini
namespace = wc_exemple

wc_exemple.1001 = {
    type = character_event
    content_source = dlc_GOA
    title = wc_exemple.1001.title
    desc = {
        first_valid = {
            triggered_desc = {
                trigger = { scope:owner = { has_trait = brave } }
                desc = wc_exemple.1001.desc_brave
            }
            desc = wc_exemple.1001.desc
        }
    }
    theme = war
    left_portrait = { character = root animation = anger }
    immediate = {
        save_scope_as = owner
        add_character_modifier = { modifier = path_to_glory_modifier }
    }
    trigger = { is_ai = no }
    option = {
        name = wc_exemple.1001.a
        trigger_event = { id = wc_exemple.1002 days = 30 }
        ai_chance = { base = 60 }
    }
    option = {
        name = wc_exemple.1001.b
        add_prestige = 100
        ai_chance = { base = 40 ai_value_modifier = { ai_greed = 0.5 } }
    }
}
```
