# Lists

> **Vue rapide** : Les listes CK3 regroupent des scopes et s'itèrent via les list-builders `any_X`, `every_X`, `random_X`, `ordered_X`.

---

## Code lists (built-in)

Listes fournies par le code pour chaque scope. Exemple : `child` contient tous les enfants d'un personnage.

```jomini
every_child = {
    even_if_dead = yes       # paramètre de liste (pas un trigger)
    limit = { is_adult = yes }
    add_prestige = 100
}
```

Paramètres spéciaux : `even_if_dead` (inclut les morts), `type` (pour `every_relation`).

```jomini
every_relation = {
    type = friend
    type = lover
    limit = { <triggers> }
    <effects>
}
```

## Scripted lists

Définies dans `common/scripted_lists/`. Personnalisent une code list avec des conditions pré-appliquées.

```jomini
# Définition
adult_unlanded_child = {
    base = child
    conditions = {
        is_adult = yes
        is_landed_ruler = no
    }
}

# Utilisation — utilisable avec tous les list-builders
every_adult_unlanded_child = {
    limit = { <triggers> }
    <effects>
}
```

## Custom lists (temporaires)

Listes nommées arbitrairement, construites avec `add_to_list`. Disponibles dans la chaîne d'effects ininterrompue (comme un saved scope).

```jomini
add_to_list = my_targets     # ajoute le scope courant à la liste

every_in_list = {
    list = my_targets
    limit = { <triggers> }
    <effects>
}
```

## Variable lists (persistantes)

Stockées sur un scope spécifique, persistantes entre les chaînes d'effects (comme une variable).

```jomini
# Ajout
add_to_variable_list = {
    name = my_persistent_list
    target = character:10005
}

# Itération
every_in_list = {
    variable = my_persistent_list
    limit = { <triggers> }
    <effects>
}
```

Différence clé : `list = X` (temporaire, chaîne d'effects) vs `variable = X` (persistante, scope spécifique).
