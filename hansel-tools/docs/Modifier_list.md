# Modifier list

> **Vue rapide** : Modificateurs CK3 les plus utiles pour le modding, classes par categorie + modificateurs custom de ce mod.

---

## Combat

| Modifier                                 | Scope     | Effet                          |
| ---------------------------------------- | --------- | ------------------------------ |
| `monthly_martial_lifestyle_xp_gain_mult` | character | Multiplicateur XP martial      |
| `knight_effectiveness_mult`              | character | Efficacite des chevaliers      |
| `pursuit_mult`                           | character | Bonus poursuite apres bataille |
| `siege_phase_time`                       | character | Duree de phase de siege        |
| `max_combat_roll`                        | character | Roll max en combat             |
| `advantage`                              | character | Avantage tactique en bataille  |
| `army_damage_mult`                       | character | Multiplicateur degats armee    |

## Economie

| Modifier                    | Scope     | Effet                      |
| --------------------------- | --------- | -------------------------- |
| `tax_mult`                  | county    | Multiplicateur de taxes    |
| `development_growth`        | county    | Croissance dev du comte    |
| `development_growth_factor` | county    | Facteur multiplicatif dev  |
| `build_speed`               | county    | Vitesse de construction    |
| `build_gold_cost`           | county    | Cout en or des batiments   |
| `levy_reinforcement_rate`   | county    | Taux de regen des levees   |
| `monthly_income`            | character | Revenu mensuel additionnel |

## Opinion et relations

| Modifier                    | Scope     | Effet                          |
| --------------------------- | --------- | ------------------------------ |
| `general_opinion`           | character | Opinion generale (+/-)         |
| `vassal_opinion`            | character | Opinion des vassaux            |
| `same_culture_opinion`      | character | Opinion meme culture           |
| `different_culture_opinion` | character | Opinion culture differente     |
| `same_faith_opinion`        | character | Opinion meme foi               |
| `attraction_opinion`        | character | Opinion d'attraction           |
| `monthly_prestige`          | character | Prestige mensuel               |
| `monthly_piety`             | character | Piete mensuelle                |
| `dread_gain_mult`           | character | Multiplicateur gain de terreur |

## Sante et stress

| Modifier                    | Scope     | Effet                       |
| --------------------------- | --------- | --------------------------- |
| `health`                    | character | Modification sante (+/-)    |
| `negate_health_penalty_add` | character | Annule penalites sante      |
| `stress_gain_mult`          | character | Multiplicateur gain stress  |
| `stress_loss_mult`          | character | Multiplicateur perte stress |
| `fertility`                 | character | Fertilite                   |

## Gouvernance

| Modifier                                   | Scope     | Effet                        |
| ------------------------------------------ | --------- | ---------------------------- |
| `domain_limit`                             | character | Limite de domaine            |
| `vassal_limit`                             | character | Limite de vassaux            |
| `tyranny_gain_mult`                        | character | Multiplicateur gain tyrannie |
| `short_reign_duration_mult`                | character | Duree penalite court regne   |
| `monthly_diplomacy_lifestyle_xp_gain_mult` | character | XP diplomatie                |

## Armee

| Modifier                  | Scope     | Effet                 |
| ------------------------- | --------- | --------------------- |
| `levy_size`               | county    | Taille des levees     |
| `garrison_size`           | county    | Taille de la garnison |
| `men_at_arms_maintenance` | character | Cout entretien MaA    |
| `men_at_arms_limit`       | character | Limite MaA            |
| `supply_duration`         | character | Duree des provisions  |

---

## Modificateurs custom — Fury of the Bleeding Hollow

| Modifier                                | Scope     | Effets                                                                   |
| --------------------------------------- | --------- | ------------------------------------------------------------------------ |
| `great_invader_modifier`                | character | Applique au story_owner Bleeding Hollow a la creation du story cycle     |
| `recently_sacked_by_the_horde_modifier` | county    | -0.5 levy regen, -0.5 dev growth, -0.2 tax — apres pillage Horde         |
| `brought_discipline_horde_modifier`     | county    | +0.1 dread gain, -10 general opinion, -0.1 levy size — discipline orcish |
| `horde_conqueror_modifier`              | character | +2 martial, +5 shamanism opinion, +10 doombringer — conquete reussie     |
| `path_to_glory_modifier`                | character | +0.5 monthly prestige — chemin de gloire                                 |

## Utilisation dans le script

```jomini
# Ajouter un modifier a un personnage
add_character_modifier = {
    modifier = great_invader_modifier
    years = 10
}

# Ajouter un modifier a un comte
scope:target_county = {
    add_county_modifier = {
        modifier = recently_sacked_by_the_horde_modifier
        years = 5
    }
}

# Modifier permanent (pas de duree)
add_character_modifier = {
    modifier = horde_conqueror_modifier
}
```
