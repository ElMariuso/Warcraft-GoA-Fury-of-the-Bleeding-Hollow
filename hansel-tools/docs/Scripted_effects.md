# Scripted Effects

> **Vue rapide** : Macros réutilisables définies dans `common/scripted_effects/`. Réduisent la duplication de code et acceptent des paramètres `$PARAM$`.

---

## Concept

Un scripted effect encapsule un bloc d'effects dans une fonction nommée, avec des paramètres passés par remplacement textuel.

## Exemple

```jomini
# Définition (common/scripted_effects/)
mana_power_increase = {
    if = {
        limit = { NOT = { exists = var:magic_power } }
        set_variable = { name = magic_power  value = 0 }
    }
    change_variable = { name = magic_power  add = $MAGIC_POWER$ }
}

# Invocation
mana_power_increase = { MAGIC_POWER = 5 }
```

## Points clés

- Les paramètres `$PARAM$` sont du **remplacement textuel** — on peut passer des nombres, scopes, ou chaînes
- Passer une chaîne permet de créer des effects dynamiques (différents modifiers/effects selon le paramètre)
- Les paramètres sont en MAJUSCULES par convention
