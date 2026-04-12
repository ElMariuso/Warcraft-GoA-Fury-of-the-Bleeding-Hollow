# Modding

> **Vue rapide** : Structure d'un mod CK3 — descriptor, dossiers, load order, content_source.

---

## descriptor.mod

Fichier racine du mod. Doit exister a la racine ET dans le dossier du mod.

```jomini
# descriptor.mod
version = "1.0"
tags = { "Total Conversion" "Gameplay" }
name = "Warcraft-GoA: Fury of the Bleeding Hollow"
supported_version = "1.18.*"
path = "mod/Warcraft-GoA-Fury-of-the-Bleeding-Hollow"
```

Champs :

- `name` — nom affiché dans le launcher
- `version` — version du mod (libre)
- `supported_version` — version CK3 cible, wildcard `*` autorisé
- `path` — chemin relatif depuis le dossier mods CK3
- `tags` — catégories pour le launcher / Steam Workshop

## Structure de dossiers

```
mod_root/
  descriptor.mod
  common/           # Definitions (traits, modifiers, scripted_effects, story_cycles)
  events/           # Event files (.txt), un namespace par fichier
  localization/     # Textes affichés, par langue (english/, french/...)
  gfx/              # Textures, icones, portraits
  gui/              # Layouts et widgets UI
  music/            # Musiques custom
  history/          # Characters, titles, provinces
```

Convention de namespace : prefixer tout avec `wc_` pour eviter les collisions.

## Load Order et replace_path

CK3 merge les fichiers de tous les mods actifs. Pour remplacer entierement un dossier vanilla :

```jomini
# descriptor.mod — remplace les events vanilla
replace_path = "events"
```

`replace_path` supprime tout le contenu vanilla du dossier specifie avant de charger le mod. A utiliser avec precaution — preferer l'overwrite fichier par fichier quand possible.

## content_source

Pour les sous-mods dependant d'un autre mod :

```jomini
# Sur chaque event visible par le joueur
content_source = dlc_GOA
```

Obligatoire sur tout event non-hidden dans un sous-mod. Sans ca, l'event ne se declenche pas si le mod parent n'est pas actif.

## Bonnes pratiques

- Un namespace = un fichier `.txt` dans `events/`
- Les scripted_effects dans `common/scripted_effects/` sont charges automatiquement
- Les story_cycles dans `common/story_cycles/` definissent le lifecycle (on_setup, on_end, on_owner_death)
- Toujours tester avec `make lint-all` puis `make tiger` avant de committer
