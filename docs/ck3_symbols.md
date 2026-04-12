# CK3 Symbols — Warcraft GoA: Fury of the Bleeding Hollow

Source of truth for character IDs, title keys, modifiers, and scripted effects.
Extracted from GoA2 (`history/characters/`, `common/landed_titles/`). Update when parent mod changes.

---

## Characters

`character:<id>` — save to scope in `immediate` with `save_scope_as = <name>`.

| ID      | Nom               | Culture/Clan     | Scope convention | Mort     | Notes                               |
| ------- | ----------------- | ---------------- | ---------------- | -------- | ----------------------------------- |
| `10000` | Blackhand         | blackrock        | `blackhand`      | 586.2.1  | Warchief → tué par Orgrim           |
| `10002` | Dal'rend          | blackrock        | —                | —        | Fils de Blackhand                   |
| `10004` | Griselda          | blackrock        | —                | exécutée | Fille de Blackhand                  |
| `10005` | Kilrogg Deadeye   | bleeding_hollow  | `kilrogg`        | 591.6.18 | Protagoniste du sous-mod            |
| `10014` | Ner'zhul          | shadowmoon       | —                | —        | Chef Shadowmoon                     |
| `10015` | Gul'dan           | shadowmoon       | `guldan`         | —        | Shadow Council, dynasty 2350        |
| `10016` | Nagaz             | shadowmoon       | —                | —        | Shadow Council warlock              |
| `10017` | Teron'gor         | shadowmoon       | —                | —        | Shadow Council                      |
| `10018` | Fel'dan           | shadowmoon       | —                | —        | Shadow Council                      |
| `10019` | Durotan           | frostwolf        | `durotan`        | 585.1.1  | Assassiné par Gul'dan, dynasty 2200 |
| `10020` | Draka             | frostwolf        | —                | décédée  | Épouse de Durotan                   |
| `10021` | Go'el (Thrall)    | frostwolf        | —                | —        | Fils de Durotan                     |
| `10050` | Orgrim Doomhammer | blackrock        | `orgrim`         | 601.11.1 | dynasty 2001                        |
| `52000` | Cho'gall          | twilights_hammer | `chogall`        | 611.2.19 | Ogre, dynasty 2050                  |

---

## Titres (GoA2)

`title:<key>` — accès direct ; `<key>.holder` pour le détenteur actuel.

| Clé                       | Type    | Capital / Région             |
| ------------------------- | ------- | ---------------------------- |
| `e_horde`                 | empire  | Titular (pas de capitale)    |
| `e_dark_horde`            | empire  | `c_blackrock_spire`          |
| `e_horde_of_draenor`      | empire  | `c_dark_portal` (Fel Horde)  |
| `k_bleeding_hollow_clan`  | kingdom | `c_dead_ravine`              |
| `k_blackrock_clan`        | kingdom | `c_blackrock_spire`          |
| `k_frostwolf_clan`        | kingdom | `c_alterac_valley`           |
| `k_shadowmoon_clan`       | kingdom | `c_dark_portal`              |
| `k_warsong_clan`          | kingdom | `c_blackrock_spire`          |
| `k_gurubashi`             | kingdom | Titular (sous `e_gurubashi`) |
| `k_shattered_hand_clan`   | kingdom | `c_deihsei`                  |
| `d_cape_of_stranglethorn` | duchy   | Stranglethorn Vale           |
| `d_bonechewer_clan`       | duchy   | `c_dark_portal`              |
| `d_dragonmaw_clan`        | duchy   | `c_grim_batol`               |
| `d_twilights_hammer_clan` | duchy   | `c_obsidian_hills`           |
| `d_stormreaver_clan`      | duchy   | `c_dark_portal`              |
| `d_thunderlord_clan`      | duchy   | `c_dark_portal`              |
| `d_hammerfall`            | duchy   | `c_baymire`                  |

---

## Modificateurs actifs dans ce mod

| Clé                                     | Type      | Effets                                               |
| --------------------------------------- | --------- | ---------------------------------------------------- |
| `great_invader_modifier`                | character | Appliqué au story_owner du Bleeding Hollow           |
| `recently_sacked_by_the_horde_modifier` | province  | -0.5 levy regen, -0.5 dev growth, -0.2 tax           |
| `brought_discipline_horde_modifier`     | province  | +0.1 dread gain, -10 general opinion, -0.1 levy size |
| `horde_conqueror_modifier`              | character | +2 martial, +5 shamanism opinion, +10 doombringer    |
| `path_to_glory_modifier`                | character | +0.5 monthly prestige                                |

---

## Scripted Effects

| Nom                                        | Params          | Rôle                                                    |
| ------------------------------------------ | --------------- | ------------------------------------------------------- |
| `set_bleeding_hollow_characters_effect`    | —               | Save character:10005 → scope:kilrogg                    |
| `try_to_set_bleeding_hollow_story_owner`   | —               | Vérifie heritage_orcish → make_story_owner ou end_story |
| `spawn_orc_troops_based_on_culture_effect` | OWNER, LOCATION | Spawn troupes orcs, culture-gated, cooldown 18 mois     |
| `horde_bloodshed_effect`                   | TARGET          | Pillage + conversion culture/faith permanente           |
| `sack_county_effect`                       | TARGET          | Sac d'un comté                                          |
| `try_to_transfer_story_effect`             | OWNER           | Transfert story ownership → héritier                    |

---

## Comtés

### Stranglethorn Vale — cible de l'invasion Bleeding Hollow

Hiérarchie : `e_gurubashi` → `k_booty_bay` → `d_cape_of_stranglethorn`

| Comté          | Baronnies principales          | Notes             |
| -------------- | ------------------------------ | ----------------- |
| `c_vekrishe`   | b_vekrishe, b_puhlar, b_mentea | Capitale du duché |
| `c_fikinnun`   | b_fikinnun, b_yalme            | Région est        |
| `c_hardwrench` | b_hardwrench, b_othu           | Région ouest      |
| `c_nekmani`    | b_nekmani, b_okahzia           | Région sud        |

### Capitales de clans orcs (comtés de référence)

Les titres de clans sont `landless = yes` — ces comtés sont leurs holdings de référence.

| Comté               | Clan(s) associé(s)                                                                    |
| ------------------- | ------------------------------------------------------------------------------------- |
| `c_dead_ravine`     | `k_bleeding_hollow_clan`                                                              |
| `c_blackrock_spire` | `k_blackrock_clan`, `k_warsong_clan`, `d_burning_blade_clan`, `d_laughing_skull_clan` |
| `c_alterac_valley`  | `k_frostwolf_clan`                                                                    |
| `c_dark_portal`     | `k_shadowmoon_clan`, `d_bonechewer_clan`                                              |
| `c_deihsei`         | `k_shattered_hand_clan`                                                               |
| `c_grim_batol`      | `d_dragonmaw_clan`                                                                    |
| `c_obsidian_hills`  | `d_twilights_hammer_clan`                                                             |
| `c_baymire`         | `d_hammerfall`                                                                        |

---

## Namespaces & Plages d'ID

| Namespace                     | Fichier                                              | Plages ID                                          |
| ----------------------------- | ---------------------------------------------------- | -------------------------------------------------- |
| `wc_horde_invasion`           | `wc_story_cycle_horde_invasion_events.txt`           | 0001–0009 setup · 1001–1008 arc · 1500–1599 intros |
| `wc_bleeding_hollow_invasion` | `wc_story_cycle_bleeding_hollow_invasion_events.txt` | 0001 setup · 1000–1xxx narrative                   |
