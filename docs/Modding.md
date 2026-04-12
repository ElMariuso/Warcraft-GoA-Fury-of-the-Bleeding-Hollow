# CK3 Modding — Structure & Conventions

> **Vue rapide** : Un mod CK3 est un dossier contenant un `descriptor.mod` et des sous-dossiers miroir de `game/`. Le moteur fusionne les fichiers du mod avec la base via le load order.

---

## descriptor.mod

Fichier racine obligatoire. Déclare le mod au launcher.

```jomini
name = "My Mod"
version = "1.0"
tags = { "Total Conversion" "Gameplay" }
supported_version = "1.18.*"
path = "mod/my_mod"
```

---

## Arborescence standard

```
my_mod/
  descriptor.mod
  common/           # Définitions statiques (traits, cultures, religions, modifiers...)
    scripted_effects/
    scripted_triggers/
    story_cycles/
    modifiers/
    on_action/
  events/           # Fichiers d'events (.txt)
  history/           # Characters, titles, provinces à une date donnée
    characters/
    titles/
    provinces/
  localization/     # Textes affichés (.yml, UTF-8 BOM)
    english/
    french/
  gfx/              # Assets graphiques (portraits, blasons, icônes)
  gui/              # Layouts UI (.gui)
```

---

## Load Order & Override

- Les fichiers du mod **remplacent** ceux du jeu de base au même chemin relatif.
- Pour ajouter sans remplacer : utiliser un nom de fichier différent dans le même dossier.
- `replace_path = "common/traits"` dans `descriptor.mod` supprime tout le dossier vanilla avant de charger le mod.

---

## Namespaces

Chaque fichier d'event déclare un namespace unique en première ligne :

```jomini
namespace = wc_horde_invasion
```

Les IDs d'events sont préfixés par ce namespace : `wc_horde_invasion.1001`.

---

## content_source

Pour les sous-mods / DLC, marquer les events visibles :

```jomini
# Requis sur tout event non-hidden d'un sous-mod
content_source = dlc_GOA
```

Sans ce champ, l'event n'apparaît pas si le DLC/mod parent est absent.

---

## Validation

Aucun compilateur. Le moteur CK3 interprète les `.txt` et `.yml` au lancement.

```bash
# Log d'erreurs (Windows)
%APPDATA%\Paradox Interactive\Crusader Kings III\logs\error.log

# Recharger sans relancer
reload events        # console CK3
reload localization  # console CK3
```

Erreurs de syntaxe = log au lancement. Erreurs de logique = observation en jeu.

---

## Bonnes pratiques

- Préfixer tous les identifiants avec un namespace court (`wc_`, `agot_`) pour éviter les collisions.
- Un namespace = un fichier d'events. Tester avec `error.log` ouvert.
- Utiliser `content_source` sur tout event joueur dans un sous-mod.
