# Trait Modding

> **Vue rapide** : Les traits sont définis dans `common/traits/` et modifient les stats, l'IA et les interactions des personnages. Chaque trait a une catégorie, des modifiers optionnels et peut avoir des opposés.

---

## Structure d'un trait

```jomini
brave = {
    category = personality    # personality | skill | health | fame | lifestyle | ...

    # Modifiers appliqués au porteur
    martial = 2
    prowess = 3
    monthly_prestige = 0.5
    attraction_opinion = 10

    # Traits incompatibles
    opposites = {
        craven
    }

    # Comportement IA
    ai_boldness = 25          # Prise de risque
    ai_compassion = -10
    ai_energy = 15

    # Affichage
    index = 5                 # Position dans la liste des traits
    birth = 5                 # % chance d'apparition à la naissance (congenital)
    random_creation = 10      # % chance sur personnages générés
    genetic = yes             # Héréditaire
    good = yes                # Classé positif (couleur verte)

    # Coût si trait sélectionnable (ruler designer)
    ruler_designer_cost = 50

    # Compatibilité
    can_have = {
        is_adult = yes
    }
}
```

## Catégories principales

| Catégorie     | Usage                             | Exemples                  |
| ------------- | --------------------------------- | ------------------------- |
| `personality` | Tempérament, affect l'IA          | brave, craven, greedy     |
| `skill`       | Bonus de compétences              | brilliant_strategist      |
| `health`      | État physique                     | wounded, ill, maimed      |
| `lifestyle`   | Acquis via perks                  | scholar, strategist       |
| `fame`        | Réputation                        | famous_champion           |
| `congenital`  | Héréditaire, avec `genetic = yes` | genius, beautiful, albino |

## Traits congenitaux

Traits avec `genetic = yes` se transmettent aux enfants. Champs : `birth` (% naissance), `inherit_chance` (% si 1 parent), `both_parents_chance` (% si 2 parents).

## Niveaux de traits

Paliers liés via `next_level` / `previous_level` (ex: `wounded_1` → `wounded_2`).

## Règles clés

- `opposites` : le jeu retire automatiquement l'ancien si on ajoute l'opposé
- `can_have` : trigger block — si faux, le trait ne peut pas être ajouté
- `ai_*` : affectent les décisions IA (mariage, guerre, complots)
- Un trait sans `category` provoque une erreur silencieuse au chargement
- Localisation requise : `trait_<key>`, `trait_<key>_desc` dans les fichiers `.yml`
