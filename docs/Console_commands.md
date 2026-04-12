# CK3 Console Commands — Debug & Test

> **Vue rapide** : La console CK3 (touche `~` ou `'`) permet de déclencher des events, manipuler des personnages et recharger des fichiers sans relancer le jeu.

---

## Events

```bash
event <namespace.id>                    # déclenche pour le joueur
event <namespace.id> <character_id>     # déclenche pour un personnage spécifique
# Exemples
event wc_horde_invasion.1001
event wc_bleeding_hollow_invasion.1000 10005
```

---

## Infos personnage

| Commande    | Effet                                                    |
| ----------- | -------------------------------------------------------- |
| `charinfo`  | Toggle infos détaillées sur les personnages (ID, traits) |
| `observe`   | Mode spectateur — ne joue aucun personnage               |
| `play <id>` | Reprendre le controle d'un personnage                    |

---

## Manipulation IA

| Commande | Effet                                          |
| -------- | ---------------------------------------------- |
| `yesmen` | L'IA accepte toutes les propositions du joueur |
| `nomen`  | L'IA refuse toutes les propositions            |
| `ai`     | Toggle l'IA on/off pour tous les personnages   |

---

## Ressources

```bash
add_gold <N>                # ajoute N or
add_prestige <N>            # ajoute N prestige
add_piety <N>               # ajoute N piété
add_dread <N>               # ajoute N terreur
add_stress <N>              # ajoute N stress
```

---

## Technologie & Culture

```bash
discover_technologies all              # débloque toutes les innovations
discover_innovation <innovation_key>   # débloque une innovation spécifique
```

---

## Temps & Date

```bash
set_date <YYYY.MM.DD>      # change la date du jeu
speed <1-5>                 # vitesse de jeu (5 = max)
pause                       # toggle pause
```

---

## Rechargement à chaud

```bash
reload events               # recharge tous les fichiers events
reload localization          # recharge tous les fichiers de localisation
reload gui                   # recharge les fichiers GUI
```

Permet de tester des modifications sans relancer CK3 (sauf `common/` qui nécessite un redémarrage).

---

## Guerre & Personnages

```bash
add_claim <title> <char_id>         # ajoute un claim
kill <char_id>                      # tue un personnage
effect <script>                     # exécute un effet scripté inline
```

---

## Divers

| Commande        | Effet                                       |
| --------------- | ------------------------------------------- |
| `error_log`     | Ouvre error.log dans l'éditeur par défaut   |
| `trigger_debug` | Affiche les triggers d'un event dans le GUI |
| `clear`         | Efface la console                           |
