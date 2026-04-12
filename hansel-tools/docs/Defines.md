# Defines

> **Vue rapide** : Les defines sont des constantes globales statiques dans `common/defines/` qui surchargent les comportements internes du moteur (armées, schèmes, opinions, etc.).

---

## Concept

Les defines modifient les paramètres du moteur CK3 avant le jeu. Elles s'appliquent globalement à toute la partie et ne peuvent pas être changées dynamiquement via script.

## Syntaxe

Fichier : `common/defines/<mod_name>.txt`

```jomini
NDefines.NCharacter.OPINION_DECAY_PER_MONTH = 2
NDefines.NBuilding.CONSTRUCTION_SPEED_MULT = 1.5
NDefines.NMilitary.MAX_COMBAT_WIDTH = 30
NDefines.NMilitary.LEVY_REINFORCEMENT_RATE = 0.05
NDefines.NScheme.BASE_SUCCESS_CHANCE = 5
```

Format : `NDefines.NSection.CONSTANT = value`

## Sections courantes

| Section      | Exemples de constantes                               |
| ------------ | ---------------------------------------------------- |
| `NCharacter` | `OPINION_DECAY_PER_MONTH`, `MAX_STRESS`, `MAX_AGE`   |
| `NTitle`     | `TITLE_TIER_CHANGE_AMBITION_COST`, `CLAIM_DURATION`  |
| `NBuilding`  | `CONSTRUCTION_SPEED_MULT`, `HOLDING_SLOTS`           |
| `NMilitary`  | `MAX_COMBAT_WIDTH`, `LEVY_REINFORCEMENT_RATE`        |
| `NScheme`    | `BASE_SUCCESS_CHANCE`, `SCHEME_POWER_PER_AGENT`      |
| `NDiplomacy` | `ALLIANCE_OPINION_THRESHOLD`, `VASSAL_OPINION_LIMIT` |

## Bonnes pratiques

- Un seul fichier define par mod suffit — toutes les sections y cohabitent.
- Les defines s'appliquent globalement : impossible de cibler un personnage ou région.
- À utiliser avec prudence — les effets se propagent à tout le jeu.
- Pour la liste complète : voir `common/defines/00_defines.txt` dans CK3 vanilla.
