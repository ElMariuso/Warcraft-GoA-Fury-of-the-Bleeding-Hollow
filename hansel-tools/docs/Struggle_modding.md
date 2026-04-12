# Struggle Modding

> **Vue rapide** : Systemes regionaux multi-phases avec catalyseurs. Definis dans `common/struggles/`.

---

## Concept

Une lutte couvre une region, des cultures/fois impliquees, et progresse via des catalyseurs entre phases. Chaque phase applique des modificateurs et peut mener a des decisions de fin.

## Setup de base

```jomini
# common/struggles/my_struggle.txt
my_struggle = {
    cultures = { persian kurdish bedouin }
    faiths = { ashari mazdayasna }
    regions = { world_persian_empire }
    involvement_prerequisite_percentage = 0.8  # % des comtes requis pour devenir implique

    on_start = { trigger_event = my_struggle.0001 }
    on_join = { add_trait = my_struggle_supporter }  # Root = personnage qui rejoint

    start_phase = my_phase_1

    phase_list = {
        my_phase_1 = {
            duration = { points = 500 }
            future_phases = {
                my_phase_2 = {
                    catalysts = {
                        catalyst_war_declared = major_struggle_catalyst_gain
                        catalyst_peace_treaty = minor_struggle_catalyst_gain
                    }
                }
            }
            war_effects = {
                name = WAR_EFFECTS_NAME
                common_parameters = { invasion_conquest_war_cannot_be_declared = yes }
                involved_character_modifier = { men_at_arms_recruitment_cost = -0.5 }
            }
            ending_decisions = { my_struggle_ending_decision }
        }
        my_phase_2 = {
            duration = { points = 1000 }
            future_phases = { my_phase_1 = { catalysts = { ... } } }
        }
    }
}
```

## Lancer la lutte

```jomini
# common/on_action/game_start.txt ou scripted_effect
on_game_start = {
    start_struggle = {
        struggle_type = my_struggle
        start_phase = my_phase_1
    }
}
```

## Catalyseurs

Definis dans `common/struggles/catalysts/`. References dans `future_phases.catalysts` avec un gain : `major/medium/minor/minimal_struggle_catalyst_gain`.

```jomini
catalyst_war_declared = {
    trigger = { is_at_war = yes }
}
```

## Phase effects

4 blocs possibles : `war_effects`, `culture_effects`, `faith_effects`, `other_effects`. Chacun contient :

- `involved_character_modifier` -- cultures/fois impliquees
- `interloper_character_modifier` -- non-impliques dans la region
- `uninvolved_character_modifier` -- hors region
- `common_parameters` -- parametres globaux

## GFX

- Backgrounds : `gfx/interface/illustrations/struggle_backgrounds/<phase>_bg.dds`
- Icons de phase : `gui/texticons.gui` + `common/game_concepts/`
