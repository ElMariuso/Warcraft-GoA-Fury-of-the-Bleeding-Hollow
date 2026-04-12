# CK3 Modifier List — Référence compacte

> **Vue rapide** : Les modifiers sont des bonus/malus numériques attachés à un personnage, un titre ou une province. Ils s'appliquent via `add_character_modifier` ou `add_county_modifier`.

---

## Syntaxe

```jomini
# Définition (common/modifiers/)
great_invader_modifier = {
    icon = martial
    martial = 3
    monthly_prestige = 0.5
    general_opinion = -10
}

# Application (event/effect)
add_character_modifier = {
    modifier = great_invader_modifier
    years = 10    # ou "days = N", ou rien pour permanent
}
```

---

## Combat

| Modifier                       | Scope     | Effet principal                     |
| ------------------------------ | --------- | ----------------------------------- |
| `martial`                      | character | Compétence martiale                 |
| `prowess`                      | character | Prouesse personnelle                |
| `knight_effectiveness_mult`    | character | Multiplicateur efficacité chevalier |
| `men_at_arms_maintenance`      | character | Coût d'entretien des troupes        |
| `men_at_arms_limit`            | character | Limite de régiments                 |
| `levy_size`                    | county    | Taille des levées                   |
| `levy_reinforcement_rate`      | county    | Vitesse de reconstitution           |
| `garrison_size`                | county    | Taille de la garnison               |
| `advantage`                    | character | Avantage tactique en combat         |
| `max_combat_roll`              | character | Roll max en combat                  |
| `enemy_hard_casualty_modifier` | character | Pertes infligées à l'ennemi         |

---

## Economie

| Modifier                    | Scope     | Effet principal              |
| --------------------------- | --------- | ---------------------------- |
| `tax_mult`                  | county    | Multiplicateur de taxes      |
| `monthly_income`            | character | Revenu mensuel               |
| `domain_limit`              | character | Limite de domaine            |
| `build_speed`               | county    | Vitesse de construction      |
| `build_gold_cost`           | county    | Coût de construction         |
| `development_growth`        | county    | Croissance du développement  |
| `development_growth_factor` | county    | Facteur de croissance (mult) |
| `holding_build_gold_cost`   | county    | Coût de construction holding |

## Opinion

| Modifier                  | Scope     | Effet principal                 |
| ------------------------- | --------- | ------------------------------- |
| `general_opinion`         | character | Opinion de tous les personnages |
| `vassal_opinion`          | character | Opinion des vassaux             |
| `liege_opinion`           | character | Opinion envers le suzerain      |
| `clergy_opinion`          | character | Opinion du clergé               |
| `same_faith_opinion`      | character | Opinion de la meme foi          |
| `different_faith_opinion` | character | Opinion des autres fois         |
| `attraction_opinion`      | character | Opinion par attraction          |
| `dynasty_opinion`         | character | Opinion de la dynastie          |

---

## Sante & Fertilite

| Modifier                    | Scope     | Effet principal                |
| --------------------------- | --------- | ------------------------------ |
| `health`                    | character | Points de santé                |
| `negate_health_penalty_add` | character | Annule malus de santé          |
| `fertility`                 | character | Fertilité                      |
| `life_expectancy`           | character | Espérance de vie               |
| `stress_gain_mult`          | character | Multiplicateur gain de stress  |
| `stress_loss_mult`          | character | Multiplicateur perte de stress |

---

## Gouvernance

| Modifier                    | Scope     | Effet principal                 |
| --------------------------- | --------- | ------------------------------- |
| `diplomacy`                 | character | Compétence diplomatique         |
| `stewardship`               | character | Compétence intendance           |
| `intrigue`                  | character | Compétence intrigue             |
| `learning`                  | character | Compétence savoir               |
| `monthly_prestige`          | character | Prestige mensuel                |
| `monthly_piety`             | character | Piété mensuelle                 |
| `monthly_dynasty_prestige`  | character | Renommée dynastique mensuelle   |
| `dread_baseline_add`        | character | Terreur de base                 |
| `dread_gain_mult`           | character | Multiplicateur gain de terreur  |
| `dread_loss_mult`           | character | Multiplicateur perte de terreur |
| `tyranny_gain_mult`         | character | Multiplicateur gain de tyrannie |
| `short_reign_duration_mult` | character | Durée malus "règne court"       |

---

## Province

| Modifier                        | Scope  | Effet principal                  |
| ------------------------------- | ------ | -------------------------------- |
| `supply_limit`                  | county | Limite d'approvisionnement       |
| `supply_limit_mult`             | county | Multiplicateur approvisionnement |
| `fort_level`                    | county | Niveau de fortification          |
| `county_opinion_add`            | county | Opinion du comté                 |
| `travel_danger`                 | county | Danger de voyage                 |
| `monthly_county_control_change` | county | Vitesse de gain de controle      |

| `scheme_power` | character | Puissance de complot |
| `scheme_secrecy` | character | Discrétion de complot |
| `hostile_scheme_power_mult` | character | Mult. puissance complots hostiles |
| `enemy_hostile_scheme_success_chance_add` | character | Resistance aux complots |
