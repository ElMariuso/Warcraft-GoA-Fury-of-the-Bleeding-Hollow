# Outils de développement

Tous les scripts se lancent depuis la **racine du projet** avec `python tools/<script>.py`.

---

## Installation

```bash
pip install -r tools/requirements.txt
```

---

## Générer des stubs d'events

Crée les fichiers de départ `.txt` (events Jomini) et `.yml` (localisation) depuis un template YAML.

```bash
python tools/generate_events.py tools/templates/event_stub.yaml
```

**Résultat :**

```
✓ 2 event(s) générés
  → events/story_cycles/wc_bleeding_hollow_invasion_generated.txt
  → localization/english/wc_bleeding_hollow_invasion_l_english.yml
```

Les fichiers générés ont le suffixe `_generated` — renomme-les avant de les éditer définitivement.

**Créer un nouveau namespace :**

1. Copie `tools/templates/event_stub.yaml`
2. Change `namespace:` en `wc_<ta_feature>`
3. Ajoute tes events
4. Lance le script → édite les fichiers générés

---

## Surveiller les logs CK3 en temps réel

Affiche les nouvelles lignes de `game.log` au fil du jeu.

```bash
# Tout afficher
python tools/watch_logs.py

# Filtrer sur ton namespace uniquement
python tools/watch_logs.py --filter wc_bleeding_hollow

# Utiliser un chemin de log différent
python tools/watch_logs.py --log "C:/chemin/vers/game.log"
```

**Codes couleur :**

- Rouge → erreur
- Jaune → `debug_log` ou ligne `[wc_*]`
- Blanc → reste

Arrêt avec `Ctrl+C`.

---

## Injecter un script via la console CK3

Écrit un fichier dans `run/` pour l'exécuter depuis la console CK3 (`²`).

> ⚠️ La console désactive les achievements pour la save en cours.

```bash
# Commande inline
python tools/inject_run.py --inline "character:10005 = { add_prestige = 500 }"

# Nommer le fichier (par défaut : inject.txt)
python tools/inject_run.py --inline "character:10005 = { add_prestige = 500 }" --name test_kilrogg

# Depuis un fichier .txt existant
python tools/inject_run.py mon_script.txt --name debug_prestige
```

**Puis dans la console CK3 :**

```
run inject.txt
run test_kilrogg.txt
```

---

## Configuration des chemins

Les chemins CK3 (`game.log`, dossier `run/`) sont dans `tools/config.py`.

Pour les surcharger **sans toucher au code** (utile sur Linux/Wine ou avec un autre compte Windows) :

```bash
export CK3_LOGS_PATH="/home/user/.wine/.../game.log"
export CK3_RUN_PATH="/home/user/.wine/.../run"
```
