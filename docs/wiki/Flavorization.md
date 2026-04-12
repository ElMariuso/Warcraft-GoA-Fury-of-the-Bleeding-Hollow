# Flavorization

> **Vue rapide** : Le système de flavorization dans `common/flavorization/` remplace les titres génériques (King, Duke...) par des variantes culturelles ou religieuses (Warchief, Chieftain...). Chaque règle cible un tier, un genre et des conditions.

---

## Concept

Quand le jeu affiche un titre de noblesse, il cherche dans les règles de flavorization la première qui matche les conditions du personnage. Si aucune ne matche, le titre générique est utilisé.

## Structure d'une règle

```jomini
# common/flavorization/wc_orcish_flavors.txt
warchief_flavor = {
    type = character        # character | title
    gender = male
    special = holder         # holder | queen_consort | heir | ...
    tier = empire

    # Conditions de matching
    top_liege = {
        culture = { has_cultural_parameter = heritage_orcish }
    }

    # Clé de localisation utilisée
    name = {
        first_valid = {
            triggered_desc = {
                trigger = { culture = culture:blackrock }
                desc = "flavor_warchief_blackrock"
            }
            desc = "flavor_warchief"
        }
    }
}
```

## Champs principaux

| Champ      | Valeurs                                          | Description                               |
| ---------- | ------------------------------------------------ | ----------------------------------------- |
| `type`     | `character`, `title`                             | Cible un personnage ou un titre           |
| `gender`   | `male`, `female`                                 | Genre du porteur                          |
| `special`  | `holder`, `queen_consort`, `heir`, `regent`      | Rôle du personnage                        |
| `tier`     | `empire`, `kingdom`, `duchy`, `county`, `barony` | Tier du titre                             |
| `priority` | int                                              | Plus élevé = testé en premier (défaut: 0) |

## Conditions et variantes

Le bloc accepte des triggers standards (culture, government, religion) pour filtrer. Localisation : `flavor_<key>:0 "Titre"` dans les `.yml`. Pour les variantes féminines, créer une règle séparée avec `gender = female`.

## Règles clés

- `priority` contrôle l'ordre d'évaluation — la première règle qui matche gagne
- Sans `priority`, l'ordre dépend du chargement des fichiers (imprévisible entre mods)
- `first_valid` permet des variantes contextuelles dans une même règle
- Une règle sans conditions valides = titre générique affiché (pas d'erreur)
- Les flavorizations s'appliquent aussi aux `GetTitleAs*` dans la localisation
