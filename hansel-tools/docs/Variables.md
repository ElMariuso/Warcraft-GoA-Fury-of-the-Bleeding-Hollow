# Variables

> **Vue rapide** : CK3 offre trois mécanismes de stockage : variables (valeur numérique persistante), flags (booléens), et scopes sauvegardés (référence temporaire à un objet).

---

## Types de variables

| Type       | Setter                | Getter           | Persistance      |
| ---------- | --------------------- | ---------------- | ---------------- |
| Locale     | `set_variable`        | `var:nom`        | Jusqu'à `remove` |
| Globale    | `set_global_variable` | `global_var:nom` | Durée de la save |
| Scope-list | `set_local_variable`  | `local_var:nom`  | Bloc courant     |

## Opérations sur variables

```jomini
# Créer / assigner
set_variable = { name = invasion_progress value = 0 }

# Modifier
change_variable = { name = invasion_progress add = 1 }
change_variable = { name = invasion_progress multiply = 2 }

# Tester
trigger_if = {
    limit = { var:invasion_progress >= 5 }
    # ...
}

# Supprimer
remove_variable = invasion_progress
```

Opérations : `add`, `subtract`, `multiply`, `divide`.

## Flags (booléens)

```jomini
# Poser un flag
set_character_flag = bleeding_hollow_arrived

# Tester
has_character_flag = bleeding_hollow_arrived

# Avec expiration (cooldown)
set_character_flag = {
    flag = recently_invaded
    days = 365
}

# Retirer
remove_character_flag = bleeding_hollow_arrived
```

Types : `character_flag`, `title_flag`, `dynasty_flag`, `global_flag`.

## Scopes sauvegardés

Références temporaires valides dans le bloc courant.

```jomini
immediate = {
    character:10005 = { save_scope_as = kilrogg }
}
# Utilisable dans le même event :
scope:kilrogg = { add_prestige = 100 }
```

## Script values

Constantes réutilisables en top du fichier `.txt`.

```jomini
@my_prestige_cost = 500
@my_modifier_duration = 365

trigger_if = {
    limit = { prestige >= @my_prestige_cost }
    # ...
}
```

## Résumé

| Mécanisme    | Type      | Persistance      | Usage                         |
| ------------ | --------- | ---------------- | ----------------------------- |
| `variable`   | Nombre    | Jusqu'à `remove` | Compteurs, progression        |
| `flag`       | Booléen   | Jusqu'à `remove` | État oui/non, cooldowns       |
| `scope`      | Référence | Bloc courant     | Passer des objets entre blocs |
| `global_var` | Nombre    | Save entière     | État global du mod            |
