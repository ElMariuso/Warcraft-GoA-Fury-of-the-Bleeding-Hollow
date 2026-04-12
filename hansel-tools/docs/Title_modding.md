# Title Modding

> **Vue rapide** : Les titres sont définis dans `common/landed_titles/` avec une hiérarchie imbriquée empire > kingdom > duchy > county > barony. Les titres `landless` servent de titulaires sans terre (clans, organisations).

---

## Concept

CK3 utilise une hiérarchie de titres imbriqués. Chaque niveau est défini par son préfixe : `e_` (empire), `k_` (kingdom), `d_` (duchy), `c_` (county), `b_` (barony). Les titres enfants sont imbriqués dans leur parent.

## Structure hiérarchique

```jomini
e_horde = {
    color = { 150 30 30 }
    landless = yes
    capital = c_blackrock_spire

    k_bleeding_hollow_clan = {
        color = { 100 50 20 }
        landless = yes
        capital = c_dead_ravine

        d_cape_of_stranglethorn = {
            capital = c_vekrishe

            c_vekrishe = {
                b_vekrishe = { province = 4200 }
                b_puhlar = { province = 4201 }
            }
        }
    }
}
```

## Clés principales

| Clé                          | Type   | Rôle                                               |
| ---------------------------- | ------ | -------------------------------------------------- |
| `color`, `color2`            | RGB    | Couleur sur la carte                               |
| `capital`                    | titre  | Siège de référence (comté/baronnie)                |
| `landless`                   | yes/no | Titre sans holdings ni levies                      |
| `de_jure_liege`              | titre  | Suzerain de jure (si imbrication implicite)        |
| `holder_enforce_same_faith`  | yes    | Titre forcément tenu par même foi que le souverain |
| `can_be_named_after_dynasty` | yes    | Peut être renommé par dynasty                      |
| `definite_form`              | yes    | Affichage : "the Kingdom of..."                    |

## Titres landless (clans, organisations)

Un titre `landless = yes` ne génère pas de levies ni revenus, mais peut être détenu et utilisé comme titre honorifique. Utile pour les clans orcs, factions, ou ordres religieux.

## Noms culturels

```jomini
k_bleeding_hollow_clan = {
    landless = yes
    capital = c_dead_ravine

    cultural_names = {
        bleeding_hollow = "Clan Creux Sanglant"
        human = "Clan du Creux Sanglant"
    }
}
```

## Notes

- Les baronies nécessitent un `province = <id>` pour le lien carte.
- La hiérarchie imbriquée rend `de_jure_liege` implicite.
- Un titre sans `landless` génère automatiquement levies et revenus basés sur ses holdings.
