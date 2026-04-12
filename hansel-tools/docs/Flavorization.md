# Flavorization

> **Vue rapide** : Le système de flavorization dans `common/flavorization/` affiche des titres culturels/genrés sur les personnages (ex: "Warchief" au lieu de "Emperor") sans modifier les titres réels.

---

## Concept

Les flavorizations adaptent le nom d'un titre selon la culture, la religion ou le genre du détenteur. Le moteur évalue les entrées par priorité (`priority`) et applique la première qui matche. Cela permet des variantes culturelles sans dupliquer les titres.

## Structure

```jomini
orc_warchief_male = {
    type = character          # Flavorise le personnage
    gender = male             # ou female
    tier = empire             # Rang de titre ciblé
    priority = 150            # Plus haut = évalué en premier

    trigger = {
        culture = { has_cultural_pillar = heritage_orcish }
        highest_held_title_tier = tier_empire
    }

    name = {
        key = "flavor_warchief"  # Clé de localisation
    }
}
```

## Clés/blocs disponibles

| Clé        | Type   | Rôle                                                         |
| ---------- | ------ | ------------------------------------------------------------ |
| `type`     | string | `character` ou `title` — ce qui est flavorisé                |
| `gender`   | string | `male`, `female`, ou omis (les deux)                         |
| `tier`     | string | `empire`, `kingdom`, `duchy`, `county` — filtre par rang     |
| `priority` | int    | Plus élevé = évalué en premier (fallbacks génériques en bas) |
| `trigger`  | block  | Conditions pour appliquer cette flavorization                |
| `name`     | block  | `key = "clé_loc"` — le titre affiché                         |
| `prefix`   | block  | Optionnel : préfixe "the", "of the"                          |

## Localisation associée

```
flavor_warchief:0 "Warchief"
flavor_chieftain:0 "Chieftain"
```

## Notes

- Les flavorizations ne modifient pas le titre réel — affichage uniquement.
- La règle la plus spécifique (priorité haute + trigger restrictif) gagne toujours.
- Tester avec `script_docs` en jeu : génère `event_scopes.log` pour vérifier quels scopes match.
