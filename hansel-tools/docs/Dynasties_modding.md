# Dynasties Modding

> **Vue rapide** : Les dynasties (`common/dynasties/`) regroupent des houses (`common/dynasty_houses/`). Chaque personnage appartient à une house qui appartient à une dynasty.

---

## Concept

CK3 sépare dynasties (lignages principaux) et houses (branches cadettes). Un personnage appartient toujours à une house, jamais directement à une dynasty. Les houses hériten de la dynasty parente mais peuvent avoir leur propre héraldique et préfixe.

## Dynasty

Fichier : `common/dynasties/<id>.txt`

```jomini
2100 = {
    name = "dynn_bleeding_hollow"
    culture = "bleeding_hollow"
    coat_of_arms = {
        template = "plain"
        color1 = "red"
        color2 = "black"
    }
}
```

| Clé            | Type    | Rôle                          |
| -------------- | ------- | ----------------------------- |
| `name`         | clé loc | Affichage dans l'UI           |
| `culture`      | culture | Culture par défaut            |
| `coat_of_arms` | bloc    | Armoiries : template + colors |

## Dynasty House

Fichier : `common/dynasty_houses/<key>.txt`

```jomini
house_bleeding_hollow = {
    name = "dynn_bleeding_hollow_house"
    dynasty = 2100
    prefix = "house_prefix_bleeding_hollow"
    coat_of_arms = {
        template = "plain"
        color1 = "dark_red"
    }
}
```

| Clé            | Type    | Rôle                            |
| -------------- | ------- | ------------------------------- |
| `name`         | clé loc | Nom de la maison                |
| `dynasty`      | ID      | ID dynasty parent               |
| `prefix`       | clé loc | Préfixe ("House", "Clan", etc.) |
| `coat_of_arms` | bloc    | Armoiries propres à la house    |

## Scripting et history

```jomini
dynasty = dynasty:2100                        # Accès par ID
house = house:house_bleeding_hollow           # Accès par clé
character:10005 = { set_house = house:house_bleeding_hollow }
```

History : `history/characters/<id>.txt` référence `dynasty = <id>`. `history/dynasties/<id>.txt` permet `set_dynasty_head`, `set_name` par bloc daté.

## Notes

- L'ID dynasty est numérique ; l'ID house est une clé texte.
- L'armoiries utilise des templates dans `gfx/coat_of_arms/`.
- Changer la house via script : `set_house`, `become_house_leader`.
