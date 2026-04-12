# Title Modding

> **Vue rapide** : Les titres sont définis dans `common/landed_titles/` en hiérarchie imbriquée (empire > kingdom > duchy > county > barony). Chaque titre a une clé unique préfixée par son tier.

---

## Hiérarchie des tiers

| Préfixe | Tier    | Contient  |
| ------- | ------- | --------- |
| `e_`    | Empire  | Kingdoms  |
| `k_`    | Kingdom | Duchies   |
| `d_`    | Duchy   | Counties  |
| `c_`    | County  | Baronies  |
| `b_`    | Barony  | (holding) |

## Définition d'un titre

```jomini
e_horde = {
    color = { 180 30 30 }
    color2 = { 255 255 255 }
    capital = c_blackrock_spire

    landless = yes             # Pas de territoire de jure
    can_create = { always = no }

    k_blackrock_clan = {
        color = { 100 20 20 }
        capital = c_blackrock_spire

        d_hammerfall = {
            color = { 90 25 25 }
            capital = c_baymire

            c_baymire = {
                color = { 80 30 30 }
                b_baymire = { province = 4201 }
                b_northfold = { province = 4202 }
            }
        }
    }
}
```

## Champs principaux

| Champ                         | Type      | Description                           |
| ----------------------------- | --------- | ------------------------------------- |
| `color`                       | RGB       | Couleur sur la carte                  |
| `capital`                     | title key | Capitale de jure                      |
| `landless`                    | bool      | Titre sans territoire (titular)       |
| `can_create`                  | trigger   | Conditions pour créer le titre        |
| `can_be_named_after`          | trigger   | Peut renommer le titre                |
| `definite_form`               | bool      | Utilise "the" (localisation anglaise) |
| `ruler_uses_title_name`       | bool      | Le dirigeant utilise le nom du titre  |
| `destroy_if_invalid_heir`     | bool      | Détruit si pas d'héritier valide      |
| `no_automatic_claims`         | bool      | Pas de claims automatiques            |
| `de_jure_drift_disabled`      | bool      | Pas de drift de jure                  |
| `male_names` / `female_names` | list      | Noms culturels pour les holders       |
| `province`                    | int       | ID province (baronnies uniquement)    |

## De jure vs de facto

- **De jure** : hiérarchie dans le fichier — structure "légale"
- **De facto** : détenteur réel en jeu — change dynamiquement
- Drift de jure : ~100 ans pour aligner le légal sur le politique

## Titres landless (titular)

Titres sans territoire : `landless = yes`, souvent avec `can_create = { always = no }` et `destroy_if_invalid_heir = yes`.

## Règles clés

- La hiérarchie d'imbrication définit le de jure — un `d_` dans un `k_` est de jure vassal
- Chaque `b_` doit avoir un `province = <id>` unique correspondant à la carte
- `can_create = { always = no }` empêche la création manuelle — utile pour titres narratifs
- Localisation requise : `<title_key>` et `<title_key>_adj` dans les `.yml`
