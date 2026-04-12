# Defines

> **Vue rapide** : Les fichiers `common/defines/` permettent de surcharger les constantes numériques du moteur CK3 (seuils, durées, multiplicateurs). Un mod charge ses propres defines qui écrasent les valeurs vanilla.

---

## Concept

Le jeu charge d'abord les defines vanilla, puis les defines des mods dans l'ordre de priorité. Seules les valeurs explicitement redéfinies sont écrasées — le reste garde les valeurs par défaut.

## Structure

```jomini
# common/defines/my_mod_defines.txt
NCharacter = {
    MAX_PROWESS = 100                  # Défaut vanilla : 100
    ACCOLADE_GLORY_GAIN_MULT = 1.5
}

NMilitary = {
    LEVY_REINFORCEMENT_RATE = 0.05     # Taux de regen des levées
    MAX_COMBAT_ROLL = 12               # Dé de combat max
}

NTitle = {
    DE_JURE_DRIFT_YEARS = 100          # Années pour drift de jure
}
```

## Catégories principales

| Namespace    | Domaine                                |
| ------------ | -------------------------------------- |
| `NCharacter` | Stats, âge, fertilité, éducation       |
| `NMilitary`  | Combat, levées, MaA, sièges            |
| `NTitle`     | Drift, création, destruction de titres |
| `NReligion`  | Ferveur, conversion, reformation       |
| `NEconomy`   | Or, développement, bâtiments           |
| `NDiplomacy` | Opinion, alliances, hooks              |
| `NIntrigue`  | Complots, secrets, stress              |
| `NProvince`  | Contrôle, supply, attrition            |
| `NGame`      | Dates, vitesse, sauvegarde             |

## Exemple : modifier le seuil de tyrannie

```jomini
# common/defines/wc_defines.txt
NCharacter = {
    TYRANNY_GAIN_REVOKE_TITLE = 20     # Vanilla : 20 — augmenter pour plus de punition
    TYRANNY_LOSS_PER_MONTH = 0.5       # Vanilla : ~0.33
}
```

## Règles clés

- Un seul `NCategory = { ... }` par catégorie par fichier — si dupliqué, le dernier gagne
- Les defines ne supportent que des valeurs numériques (int ou float)
- Pas de triggers ni conditions — ce sont des constantes pures
- Pour trouver les defines vanilla : `game/common/defines/00_defines.txt`
- Les defines sont chargés une fois au lancement — pas de hot-reload
