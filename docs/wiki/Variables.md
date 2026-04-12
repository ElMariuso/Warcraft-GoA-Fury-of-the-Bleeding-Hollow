# Variables

> **Vue rapide** : CK3 offre trois mécanismes de stockage de données : variables (persistantes, typées), flags (booléens simples) et scopes sauvegardés (références temporaires). Chacun a une portée et une durée de vie différente.

---

## Variables

Stockent une valeur numérique sur un scope. Persistent dans la sauvegarde.

```jomini
# Définir / modifier
set_variable = { name = invasion_progress value = 0 }
change_variable = { name = invasion_progress add = 1 }
change_variable = { name = invasion_progress multiply = 2 }

# Lire (dans un trigger ou un calcul)
var:invasion_progress >= 5

# Supprimer
remove_variable = invasion_progress
```

## Variables globales

Même syntaxe, portée globale (pas attachée à un scope spécifique).

```jomini
set_global_variable = { name = horde_war_started value = yes }

# Lire
global_var:horde_war_started = yes

# Supprimer
remove_global_variable = horde_war_started
```

## Variables avec durée

```jomini
set_variable = {
    name = recently_invaded
    value = yes
    days = 365               # Auto-supprimée après 365 jours
}
```

## Flags

Booléens simples — plus légers que les variables. Pas de valeur, juste présent/absent.

```jomini
# Définir
add_character_flag = horde_member
add_title_flag = was_conquered

# Vérifier
has_character_flag = horde_member

# Avec durée
add_character_flag = {
    flag = recent_battle
    days = 30
}

# Supprimer
remove_character_flag = horde_member
```

## Scopes sauvegardés

Références temporaires à un objet. Durée = le bloc d'exécution courant (event, effect).

```jomini
immediate = {
    character:10005 = { save_scope_as = kilrogg }
}
# Utilisation dans le même event
option = {
    scope:kilrogg = { add_prestige = 100 }
}
```

Les scopes sauvegardés avec `save_temporary_scope_as` ne survivent pas au bloc courant. `save_scope_as` persiste dans l'event entier.

## Comparaison

| Mécanisme        | Valeur    | Persistance | Portée  | Accès            |
| ---------------- | --------- | ----------- | ------- | ---------------- |
| Variable         | numérique | sauvegarde  | scope   | `var:nom`        |
| Variable globale | numérique | sauvegarde  | globale | `global_var:nom` |
| Flag             | booléen   | sauvegarde  | scope   | `has_*_flag`     |
| Scope sauvegardé | référence | event       | locale  | `scope:nom`      |

## Règles clés

- `set_variable` écrase la valeur existante — pas besoin de `remove` avant
- Les flags sont plus performants que les variables pour des booléens
- `var:nom` dans un trigger compare la valeur — `has_variable = nom` teste l'existence
- Les variables sur un scope détruit (personnage mort) sont perdues
