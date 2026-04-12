# CK3 Localization

> **Vue rapide** : Les textes affichés en jeu sont dans des fichiers `.yml` encodés UTF-8 avec BOM, un par langue. Chaque clé suit le format `key:0 "texte"`.

---

## Format de fichier

- Extension : `.yml`
- Encoding : **UTF-8 avec BOM** (obligatoire, sinon le fichier est ignoré silencieusement)
- Première ligne : déclaration de langue (`l_english:`, `l_french:`, etc.)
- Une clé par ligne, indentation par espace (pas de tab)

```yml
l_english:
  wc_horde_invasion.1001.title:0 "The Dark Portal Opens"
  wc_horde_invasion.1001.desc:0 "A rift tears through the sky..."
  wc_horde_invasion.1001.a:0 "Rally the clans!"
  wc_horde_invasion.1001.a_flavor:0 "The Horde marches as one."
```

---

## Syntaxe des clés

```
namespace.event_id.champ:version "texte"
```

| Champ      | Usage                              |
| ---------- | ---------------------------------- |
| `.title`   | Titre de l'event                   |
| `.desc`    | Description principale             |
| `.a`       | Texte de l'option A                |
| `.b`       | Texte de l'option B                |
| `_flavor`  | Texte d'ambiance (italique en jeu) |
| `_tooltip` | Infobulle au survol                |

Le suffixe `:0` est la version. Toujours utiliser `:0` (version de base).

---

## Variables & Scopes

Insérer des valeurs dynamiques avec `$VARIABLE$` ou `[scope.GetMethod]` :

```yml
battle_won:0 "$WINNER$ has defeated $LOSER$ at [battle.GetLocation.GetName]!"
```

| Syntaxe                        | Source                                      |
| ------------------------------ | ------------------------------------------- |
| `$VAR$`                        | Passé via `send_interface_message` ou event |
| `[Character.GetName]`          | Méthode sur le scope courant                |
| `[ROOT.Char.GetFirstName]`     | Scope explicite                             |
| `[GetPlayer.GetFaith.GetName]` | Chainage de scopes                          |

---

## Icones & Formatage

```yml
key:0 "[icon|trait_brave] You are [b]brave[/b] and [i]fearless[/i]."
```

| Code            | Rendu                 |
| --------------- | --------------------- |
| `[b]...[/b]`    | **Gras**              |
| `[i]...[/i]`    | _Italique_            |
| `[icon          | X]`                   |
| `#bold ...\n`   | Gras (syntaxe legacy) |
| `#italic ...\n` | Italique (legacy)     |
| `\\n`           | Retour à la ligne     |

---

## Fichier complet — exemple minimal

```yml
l_english:
 # Event: Dark Portal Opens
 wc_horde_invasion.0001.title:0 "The Dark Portal"
 wc_horde_invasion.0001.desc:0 "A swirling vortex of fel energy tears open..."
 wc_horde_invasion.0001.a:0 "For the Horde!"
 wc_horde_invasion.0001.a_flavor:0 "The clans unite under one banner."

 # Modifier
 great_invader_modifier:0 "Great Invader"
 great_invader_modifier_desc:0 "This warlord leads a terrifying invasion force."
```

---

## Erreurs courantes

- **Fichier ignoré** : encoding pas UTF-8 BOM, ou `l_english:` manquant.
- **Texte vide en jeu** : clé mal orthographiée (pas d'erreur dans le log).
- **Copy-paste** : clé `.title` / `.desc` pointe vers le mauvais event ID — vérifier après duplication.
- **`"Blablabla"`** : placeholder de texte non écrit — remplacer avant release.

---

## Rechargement

```bash
# Console CK3 — recharger sans relancer le jeu
reload localization
```
