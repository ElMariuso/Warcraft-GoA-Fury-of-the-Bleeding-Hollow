# History Modding

> **Vue rapide** : Les fichiers `history/` définissent l'état du monde au lancement — personnages, titres, provinces. Chaque entrée est datée et appliquée chronologiquement par le moteur.

---

## Répertoires

| Dossier               | Contenu                                         |
| --------------------- | ----------------------------------------------- |
| `history/characters/` | Définition et événements de vie des personnages |
| `history/titles/`     | Détenteurs de titres par date                   |
| `history/provinces/`  | Culture, religion, buildings des baronnies      |
| `history/wars/`       | Guerres actives au démarrage                    |

## Characters

Chaque personnage est un bloc `<id> = { ... }` avec des entrées datées pour les changements de vie.

```jomini
10005 = {
    name = "Kilrogg"
    dynasty = 2100
    religion = "shamanism"
    culture = "bleeding_hollow"
    father = 10006
    martial = 8
    prowess = 6
    trait = "brave"
    trait = "scarred"

    # Entrées datées — appliquées quand le jeu atteint cette date
    583.1.1 = { birth = yes }
    586.2.1 = { add_trait = "one_eyed" }
    591.6.18 = { death = yes }
}
```

Les effets disponibles dans les blocs datés : `birth`, `death`, `add_trait`, `remove_trait`, `add_spouse`, `employer`, `effect = { ... }`.

## Titles

Attribue les détenteurs de titres par date. Le fichier correspond au titre (`e_horde.txt`).

```jomini
e_horde = {
    583.1.1 = {
        holder = 10000  # Blackhand
        government = "tribal_government"
    }
    586.2.1 = {
        holder = 10050  # Orgrim Doomhammer
    }
}
```

## Provinces

Définit l'état initial de chaque baronnie (holding). Le fichier est nommé par ID province.

```jomini
# history/provinces/4200.txt
culture = "gurubashi"
religion = "loa_worship"
holding = castle_holding
buildings = { curtain_wall_01 barracks_01 }

583.1.1 = { culture = "bleeding_hollow" religion = "shamanism" }
```

## Règles clés

- Les entrées datées s'appliquent dans l'ordre chronologique au chargement
- Un personnage sans `birth = yes` dans une entrée datée n'existe pas en jeu
- `death = yes` sans date précise = mort à la date de la dernière entrée
- Les traits ajoutés dans history ne déclenchent pas les `on_gain` effects
- Les fichiers history sont chargés avant les events — pas d'accès aux scopes dynamiques
