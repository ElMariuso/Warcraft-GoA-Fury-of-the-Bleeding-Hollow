# Console commands

> **Vue rapide** : Commandes debug CK3 essentielles pour tester un mod — ouvrir la console avec `~` ou `` ` ``.

---

## Events et personnages

```jomini
# Declencher un event sur le joueur actif
event wc_horde_invasion.1001

# Declencher un event sur un personnage specifique
event wc_bleeding_hollow_invasion.1000 10005

# Afficher les IDs de personnage dans les tooltips
charinfo 1

# Jouer comme un autre personnage
play 10005
```

## Mode observation et IA

```jomini
# Mode spectateur — l'IA joue tout
observe

# Revenir en mode joueur
play <char_id>

# L'IA accepte toutes les propositions
yesmen
```

## Ressources

```jomini
# Ajouter des ressources au joueur actif
add_gold 1000
add_prestige 500
add_piety 500

# Debloquer toutes les technologies
discover_technologies all
```

## Culture et religion

```jomini
# Changer la culture d'un personnage
set_culture culture:bleeding_hollow

# Changer la foi
set_faith faith:shamanism
```

## Date et temps

```jomini
# Changer la date du jeu
set_date 583.1.1
```

## Rechargement a chaud

```jomini
# Recharger sans relancer le jeu
reload localization
reload events
reload gui
```

Limitation : les `common/` (scripted_effects, story_cycles, modifiers) ne sont PAS rechargeables a chaud. Il faut relancer le jeu.

## Logs et debug

```jomini
# Ouvrir le log d'erreurs in-game
error_log

# Vider le log d'erreurs
clear_error_log

# Explorateur de donnees live (scopes, variables, flags)
ingame_explorer
```

## Commandes utiles pour ce mod

```jomini
# Tester l'invasion du Bleeding Hollow
event wc_bleeding_hollow_invasion.0001 10005
charinfo 1

# Tester l'invasion Horde depuis le debut
set_date 582.12.1
event wc_horde_invasion.0001

# Verifier les scopes actifs
ingame_explorer
```
