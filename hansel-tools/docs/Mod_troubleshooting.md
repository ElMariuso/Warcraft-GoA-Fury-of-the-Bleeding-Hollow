# Mod Troubleshooting

> **Vue rapide** : Debug CK3 via `-debug_mode`, console développeur, error.log, et hot-reload.

---

## Activer le mode debug

Ajouter `-debug_mode` aux options de lancement (Steam : clic droit → Propriétés → Options de lancement). Donne accès à la console (touche `` ` ``), à Errorhoof, et aux logs d'erreurs automatiques au démarrage.

## Console développeur

- Ouvrir avec `` ` `` (grave accent)
- Tester un event : `event namespace.id` (ex: `event diplomacy_foreign.1074`)
- Exécuter un effect : `add_gold = 999999`, `add_trait = lunatic_genetic`
- Générer les docs de référence : `script_docs` → dump dans `Documents/Paradox Interactive/Crusader Kings III/logs/`

## Fichiers de référence (via script_docs)

| Fichier             | Contenu                               |
| ------------------- | ------------------------------------- |
| `Effects.log`       | Tous les effects hardcodés            |
| `Triggers.log`      | Tous les triggers et scopes supportés |
| `Modifiers.log`     | Tous les modifiers par type           |
| `event_scopes.log`  | Types de scope valides                |
| `event_targets.log` | Tous les event targets                |

## Erreurs courantes de localisation

- **Encodage** : les fichiers .yml doivent être UTF-8 avec BOM (`utf8bom`)
- **Missing key** : clé mal orthographiée ou fichier non sauvegardé
- **Duplicate hash** : deux clés avec le même nom dans des fichiers différents

## Dynamic loc — erreurs fréquentes

- `[ROOT.GetSomething]` au lieu de `[ROOT.Char.GetSomething]`
- `[scope:name.GetFirstName]` au lieu de `[name.GetFirstName]` (pas de `scope:` en loc)
- Scope non sauvegardé car les triggers de l'event ne sont pas remplis (vérifier le ✔/✖ en haut à droite de l'event)

## Hot-loading

Permet de modifier des scripts **sans relancer le jeu**. Limites :

- Fermer l'event avant de hot-load si possible
- La loc existante se met à jour ; les **nouvelles** clés de loc ne se chargent pas
- Pour des changements importants, relancer le jeu pour éviter des états inconsistants

## Run scripts (automatisation)

Fichiers `.txt` dans `Documents/Paradox Interactive/Crusader Kings III/run/`. Exécutent des effects comme un bloc `immediate`. Lancer avec `run nom_du_script.txt` dans la console.

```jomini
# Exemple : donner des ressources au joueur
root = {
    add_prestige = 4000
    add_gold = 500
}
```
