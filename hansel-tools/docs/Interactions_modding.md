# Interactions Modding

> **Vue rapide** : Les character interactions sont définies dans `common/character_interactions/`. Elles attendent l'acceptation du destinataire puis appliquent des effects.

---

## Exemple minimal

```jomini
basic_interaction = {
    on_accept = {
        scope:actor = { add_gold = 100 }
        scope:recipient = { remove_short_term_gold = 100 }
    }
    auto_accept = { always = yes }   # acceptation automatique (utile pour tester)
}
```

## Scopes fournis par le code

- **scope:actor** — le personnage qui initie l'interaction
- **scope:recipient** — le destinataire

Toujours scoper vers un personnage avant d'appliquer les effects.

## Notes

- `on_accept` vs `on_send` : `on_send` ne génère pas de prévisualisation des effects
- Sans `category`, l'interaction apparaît dans "Uncategorized"
- Une interaction complète devrait avoir `category`, `icon`, et optionnellement `desc`
- Voir `_character_interactions.info` dans le dossier vanilla pour la référence complète
