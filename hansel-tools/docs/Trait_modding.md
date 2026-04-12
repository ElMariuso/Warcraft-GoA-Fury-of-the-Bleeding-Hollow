# Trait Modding

> **Vue rapide** : Les traits sont définis dans `common/traits/` et modifient attributs, opinions, personnalité et comportement IA des personnages.

---

## Concept

Chaque fichier dans `common/traits/` déclare un ou plusieurs traits. Un trait possède une catégorie, des modifiers (attributs/opinions), et peut être incompatible avec d'autres traits via `opposites`.

## Structure

```jomini
blood_fury = {
    category = personality
    
    opposites = { calm content }
    
    modifiers = {
        monthly_prestige = 0.5
        martial = 2
        diplomacy = -1
        same_opinion = 10
    }
    
    ai_boldness = 30
    ai_energy = 20
    
    icon = "gfx/interface/icons/traits/blood_fury.dds"
}
```

## Champs disponibles

| Clé                        | Type  | Rôle                                                              |
| -------------------------- | ----- | ----------------------------------------------------------------- |
| `category`                 | enum  | Catégorie (personality, health, lifestyle, congenital, commander) |
| `opposites`                | list  | Traits automatiquement retirés si ce trait est ajouté             |
| `modifiers`                | block | Bloc de modifiers appliqués au personnage                         |
| `ai_boldness`, `ai_energy` | int   | Poids IA pour décisions                                           |
| `icon`                     | path  | Chemin vers icône (`gfx/`)                                        |
| `birth`                    | flag  | Trait assignable uniquement à la naissance                        |
| `flag = trait_is_pariah`   | flag  | Rend le personnage paria (excommunication mécanique)              |

## Scripting

Ajouter/retirer un trait via events ou effects :

```jomini
add_trait = blood_fury          # Ajoute, retire opposés automatiquement
remove_trait = blood_fury       # Retire
has_trait = blood_fury          # Condition (scope:character)
```

## Notes

- Un personnage ne peut pas avoir deux traits `opposites` — l'ajout retire l'opposé.
- `congenital` + `genetic_constraint` contrôlent la transmission héréditaire.
- Les traits `health` sont automatiquement retirés en fin de maladie.
