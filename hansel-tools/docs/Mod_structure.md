# Mod Structure

> **Vue rapide** : Un mod CK3 = un fichier `.mod` + un dossier mod, dans le répertoire utilisateur.

---

## Emplacement

- Windows : `%USERPROFILE%\Documents\Paradox Interactive\Crusader Kings III\mod`
- Linux : `~/.local/share/Paradox Interactive/Crusader Kings III/mod`

## Composants requis

Chaque mod nécessite (même nom, extensions différentes) :

1. **`monmod.mod`** — métadonnées, à côté du dossier (requis pour que le launcher détecte le mod)
2. **`monmod/`** — dossier contenant les fichiers du mod
3. **`monmod/descriptor.mod`** — copie du .mod sans la clé `path`

## Fichier .mod — syntaxe

```jomini
version="0.0.1"
tags={
    "Culture"
    "Decisions"
}
name="My Mod"
supported_version="1.18.*"    # wildcards acceptés
path="mod/my_mod"             # relatif au dossier utilisateur CK3
```

Clés principales : `name` (requis), `version` (requis), `supported_version` (requis sauf descriptor.mod), `path` (requis sauf descriptor.mod), `tags`, `picture`, `replace_path`, `remote_file_id`.

## Structure du dossier mod

| Dossier             | Contenu                  |
| ------------------- | ------------------------ |
| `events/`           | Événements               |
| `common/decisions/` | Décisions                |
| `common/defines/`   | Defines                  |
| `common/traits/`    | Traits                   |
| `localization/`     | Fichiers de localisation |
| `gfx/`              | Assets graphiques        |
| `music/`            | Musique                  |

La structure reproduit celle de `game/` dans l'installation CK3. Seuls les fichiers placés au bon chemin sont chargés.

## Créer via le launcher

Launcher → All Installed Mods → Upload Mod → Create a Mod. Remplir nom, version, répertoire, au moins un tag. Le launcher génère automatiquement les 3 fichiers.

## Tips

- `replace_path` empêche le chargement des fichiers vanilla pour un chemin donné
- Recharger les mods dans le launcher : Manage all mods → Reload installed mods
- Noms de fichiers/dossiers sensibles à la casse sur Linux/Mac
