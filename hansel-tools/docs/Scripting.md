# Scripting

> **Vue rapide** : le langage Jomini structure tout le contenu CK3 avec la syntaxe `key = value` / `key = { bloc }`. Scripts dans `common/` et `events/`.

---

## Structure d'un fichier .txt

- Encoding UTF-8 (pas de BOM requis — le BOM est réservé aux `.yml` de localisation)
- Un fichier event = un namespace déclaré en haut
- Commentaires avec `#`

```jomini
namespace = wc_mon_mod

wc_mon_mod.1000 = {
    type = character_event
    # ...
}
```

## Variables

```jomini
# Créer / écraser
set_variable = { name = compteur value = 10 }

# Lire (préfixe var:)
add_gold = var:compteur

# Modifier
change_variable = { name = compteur add = 5 }

# Supprimer
remove_variable = compteur
```

| Type    | Set                   | Accès         | Portée                       |
| ------- | --------------------- | ------------- | ---------------------------- |
| Normal  | `set_variable`        | `var:`        | Stockée sur le scope courant |
| Globale | `set_global_variable` | `global_var:` | Accessible partout           |
| Locale  | `set_local_variable`  | `local_var:`  | Durée d'exécution du script  |

## Conditions (if / else)

```jomini
if = {
    limit = { is_ai = no }
    add_gold = 100
}
else_if = {
    limit = { gold < 50 }
    add_gold = 25
}
else = {
    add_prestige = 10
}
```

`limit` agit comme un AND implicite — plusieurs triggers s'y combinent directement.

## Opérateurs logiques

`AND`, `OR`, `NOT`, `NOR`, `NAND` — imbriquables. Blocs trigger = AND par défaut.

## Descriptions conditionnelles (first_valid)

```jomini
desc = {
    first_valid = {
        triggered_desc = {
            trigger = { this = character:10005 }
            desc = wc_event.1000.desc_kilrogg
        }
        desc = wc_event.1000.desc_generic
    }
}
```

## Tooltips et UX

| Bloc              | Rôle                                          |
| ----------------- | --------------------------------------------- |
| `show_as_tooltip` | Montre l'effet dans l'UI **sans l'exécuter**  |
| `hidden_effect`   | Exécute l'effet **invisible** dans l'UI       |
| `custom_tooltip`  | Affiche une clé de localisation comme tooltip |

```jomini
option = {
    name = wc_event.1000.a
    show_as_tooltip = { add_gold = 100 }    # preview
    add_gold = 100                          # exécution réelle
}
```

## Délais et déclencheurs

```jomini
# Délai fixe
trigger_event = { id = wc_event.1001 days = 14 }

# Délai aléatoire (entre 10 et 30 jours)
trigger_event = { id = wc_event.1002 days = { 10 30 } }
```

## Scripted effects (templates réutilisables)

Définis dans `common/scripted_effects/`, paramétrisés avec `$PARAM$` :

```jomini
# Définition
spawn_troops_effect = {
    $OWNER$ = {
        spawn_army = { levies = 500 location = $LOCATION$ }
    }
}

# Appel
spawn_troops_effect = {
    OWNER = scope:kilrogg
    LOCATION = scope:target_county
}
```

Les scripted triggers fonctionnent de la même manière dans `common/scripted_triggers/`.

## Poids AI

Toujours inclure `ai_chance` sur chaque option. `base = 0` pour les options non-canon.

```jomini
option = {
    name = wc_event.1001.a
    ai_chance = { base = 60  modifier = { add = 40  has_trait = brave } }
}
```

## Switch et while

```jomini
# Switch — remplace des chaînes de else_if sur le même trigger
switch = {
    trigger = has_culture
    culture:blackrock = { add_gold = 100 }
    culture:frostwolf = { add_prestige = 50 }
}

# While — boucle (max 1000 itérations, pas de break)
while = { count = 5  add_gold = 100 }
```
