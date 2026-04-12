# Localization

> **Vue rapide** : Fichiers `.yml` UTF-8 BOM qui fournissent tout le texte visible au joueur — events, tooltips, UI.

---

## Format de base

Fichier : `localization/english/wc_feature_l_english.yml`

Regles strictes :

- Encodage **UTF-8 avec BOM** (byte order mark) — sans BOM, CK3 ignore le fichier silencieusement
- Premiere ligne : `l_english:` (ou `l_french:`, `l_german:`, etc.)
- Indentation : 1 espace avant chaque cle
- Format cle : `namespace.id.champ:0 "texte"`
- Le suffixe `:0` est obligatoire (numero de version)

## Exemple complet

```jomini
l_english:
 wc_bleeding_hollow_invasion.1000.title:0 "The Bleeding Hollow Arrives"
 wc_bleeding_hollow_invasion.1000.desc:0 "Kilrogg Deadeye leads his clan through the jungles of Stranglethorn, the eye of the Dead searing visions of conquest into his mind."
 wc_bleeding_hollow_invasion.1000.a:0 "March forward!"
 wc_bleeding_hollow_invasion.1000.a.tt:0 "The Bleeding Hollow will claim these lands."
 wc_bleeding_hollow_invasion.1000.b:0 "Send scouts first."
 wc_bleeding_hollow_invasion.1000.b.tt:0 "Caution may serve us better than brute force."
 wc_bleeding_hollow_invasion.1000.flavor:0 "[i]The jungle trembles.[/i]"
```

## Variables et getters

Inserer des valeurs dynamiques dans le texte :

```jomini
# Variable passee par le script
 key:0 "You gain $GOLD_AMOUNT$ gold."

# Getter — appel sur un scope
 key:0 "[ROOT.Char.GetFirstName] conquers [target_county.GetName]."

# Getter avec Custom
 key:0 "[ROOT.Char.Custom('GetClanTitle')]"
```

Variables courantes : `$GOLD$`, `$PRESTIGE$`, `$PIETY$`, `$STRESS$`.

## Codes de formatage

```jomini
# Gras et italique
 key:0 "[b]Bold text[/b] and [i]italic text[/i]"

# Icones inline
 key:0 "@gold_icon! 500 gold gained"
 key:0 "@prestige_icon! +100"

# Nouvelle ligne
 key:0 "Line one\nLine two"

# Couleur (reference game color)
 key:0 "#high This is highlighted.#!"
```

## Conventions du projet

- Nommage fichier : `wc_<feature>_l_english.yml`
- Cles structurees : `wc_<namespace>.<event_id>.<champ>`
- Champs standard : `title`, `desc`, `a`, `b`, `c` (options), `tt` (tooltip), `flavor`
- Placeholder `"Blablabla"` = texte non ecrit, a remplacer avant release
- `first_valid` dans les events → cles suffixees par personnage pour le flavour text

## Erreurs frequentes

- Fichier sans BOM → CK3 l'ignore sans erreur dans le log
- Oubli du `:0` → cle non reconnue
- Guillemets non fermes → corrompt toutes les cles suivantes
- Copier-coller d'event sans changer les cles loc → mauvais texte affiche, aucune erreur log
