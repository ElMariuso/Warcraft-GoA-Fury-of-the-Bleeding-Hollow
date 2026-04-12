# Weight Modifier

> **Vue rapide** : Modificateurs conditionnels appliqués séquentiellement sur une valeur de base. Utilisés dans `ai_will_do`, `random_list`, events, etc. Aussi appelés "syntaxe MTTH".

---

## Syntaxe de base

```jomini
base = 10
modifier = {
    add = 10           # total = 20
}
modifier = {
    factor = 2         # total = 40 (appliqué après le add)
}
```

Les modifiers s'appliquent **dans l'ordre de déclaration**. `add` et `factor` acceptent des nombres, script_values, ou saved scope values.

## Avec triggers conditionnels

```jomini
base = 10
modifier = {
    is_adult = yes
    add = 10           # +10 si adulte
}
modifier = {
    is_male = yes
    add = 20           # +20 si homme
}
# Homme adulte = 40, homme enfant = 30, femme adulte = 20, femme enfant = 10
```

Un modifier s'applique uniquement si **tous ses triggers** sont vrais.

## Scripted modifiers

Définis dans `common/scripted_modifiers/`. Remplacent un ensemble de modifiers réutilisé fréquemment.

### Forme simple

```jomini
# Définition
age_and_gender_modifier = {
    modifier = { is_adult = yes  add = 10 }
    modifier = { is_male = yes   add = 20 }
}

# Utilisation
base = 10
age_and_gender_modifier = yes
```

### Forme complexe (avec paramètres)

```jomini
# Définition — $PARAM$ = remplacement littéral de texte
rich_vassal_modifier = {
    modifier = {
        add = 10
        is_vassal_of = $TARGET$
        gold >= $VALUE$
    }
}

# Utilisation
base = 10
rich_vassal_modifier = { TARGET = title:k_france.holder  VALUE = 1000 }
```

Le remplacement est **textuel** : il se produit avant l'évaluation du modifier.
