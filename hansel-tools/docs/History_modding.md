# History Modding

> **Vue rapide** : Les fichiers `history/` définissent l'état initial du monde — personnages, titres, provinces. Le moteur applique les entrées chronologiquement au chargement.

---

## Concept

Le dossier `game/history/` contient des sous-dossiers : `characters/`, `titles/`, `provinces/`. Chaque fichier décrit un objet (personnage, titre, province) et ses changements datés. Le moteur applique les blocs `YYYY.MM.DD = { ... }` dans l'ordre chronologique.

## Characters

Fichier : `history/characters/<id>.txt` ou fichier groupé.

```jomini
# Définition d'un personnage orc
10005 = {
    name = "Kilrogg"
    dynasty = 2100
    religion = "shamanism"
    culture = "bleeding_hollow"
    trait = "brave"
    father = 10006
    birth = 583.1.1
    death = 591.6.18
}
```

**Blocs datés** : `birth`, `death`, `set_culture`, `set_faith`, `add_trait`, `remove_trait`, `give_title`, `add_spouse`, `effect`.

## Titles

Fichier : `history/titles/<title_key>.txt`. Définit le détenteur historique d'une couronne/duché.

```jomini
k_bleeding_hollow_clan = {
    583.1.1 = {
        holder = 10005
        government = "tribal_government"
    }
}
```

**Blocs datés courants** : `holder`, `capital`, `set_government`, `add_law`, `effect`.

## Provinces

Fichier : `history/provinces/<id>.txt`. Culture, religion, bâtiments initiaux.

```jomini
4200 = {
    culture = "bleeding_hollow"
    religion = "shamanism"
    holding = tribal_holding
    830.1.1 = {
        culture = "gurubashi"
        religion = "loa_worship"
    }
}
```

## Notes

- Entrées sans date s'appliquent au démarrage (date de bookmark).
- Format date strict : `YYYY.MM.DD` (année.mois.jour, 1-indexé).
- Le moteur applique cumul jusqu'à la date du bookmark actif.
- Vérifier les IDs des caractères dans `ck3_symbols.md` avant référence.
