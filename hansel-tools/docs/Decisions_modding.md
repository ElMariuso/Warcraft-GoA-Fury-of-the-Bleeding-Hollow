# Decisions Modding

> **Vue rapide** : Les decisions sont des actions optionnelles pour les rulers. Definies dans `common/decisions/`. Chaque decision a des conditions de visibilite, de validite, un cout et un effet.

---

## Concept

Une decision apparait dans l'onglet Decisions si `is_shown` est vrai. Le joueur peut la prendre si `is_valid` est vrai et le cout est paye. L'IA utilise `ai_check_interval` + `ai_potential` + `ai_will_do` pour decider.

## Structure complete

```jomini
# common/decisions/my_decisions.txt
@my_prestige_cost = 500    # variable reusable

my_decision = {
    picture = { reference = "gfx/interface/illustrations/decisions/decision_smith.dds" }
    desc = my_decision_desc
    selection_tooltip = my_decision_tooltip

    # Quand la decision apparait
    is_shown = {
        is_ruler = yes
        has_royal_court = yes
    }

    # Conditions pour la prendre (tooltip = echecs seulement)
    is_valid_showing_failures_only = {
        is_available_adult = yes
        is_at_war = no
    }

    # Conditions pour la prendre (tooltip complet)
    is_valid = {
        piety_level >= 3
    }

    # Cout en gold/piety/prestige (accepte des script_values)
    cost = {
        gold = 100
        prestige = @my_prestige_cost
    }

    # Effet de la decision
    effect = {
        add_character_modifier = {
            modifier = my_modifier
        }
        trigger_event = my_event.0001
    }

    # Cooldown apres utilisation
    cooldown = { years = 5 }

    # IA
    ai_check_interval = 60      # mois entre chaque check (0 = jamais)
    ai_potential = { always = yes }
    ai_will_do = { base = 100 }

    # Optionnels
    sort_order = 10              # plus haut = plus haut dans la liste
    should_create_alert = { gold >= 50 }
    confirm_click_sound = "event:/SFX/UI/decision_confirm"
}
```

## Cles/blocs disponibles

| Cle                              | Type    | Role                                         |
| -------------------------------- | ------- | -------------------------------------------- |
| `is_shown`                       | trigger | Conditions de visibilite                     |
| `is_valid`                       | trigger | Conditions de validite (tooltip complet)     |
| `is_valid_showing_failures_only` | trigger | Validite (tooltip echecs seulement)          |
| `cost`                           | block   | gold, piety, prestige                        |
| `minimum_cost`                   | block   | Montant requis sans deduction                |
| `effect`                         | block   | Effets executes                              |
| `ai_check_interval`              | int     | Mois entre checks IA (0 = jamais)            |
| `ai_goal`                        | bool    | L'IA budgetise (ignore ai_check_interval)    |
| `ai_potential`                   | trigger | L'IA considere-t-elle ?                      |
| `ai_will_do`                     | block   | % de chance que l'IA la prenne               |
| `cooldown`                       | block   | `{ years = N }` / `{ months = N }`           |
| `widget`                         | block   | GUI custom dans `gui/decision_view_widgets/` |

## Localization

4 cles par decision :

```
l_english:
 my_decision:0 "Decision Name"
 my_decision_desc:0 "Description shown when opened"
 my_decision_tooltip:0 "Tooltip on hover"
 my_decision_confirm:0 "Confirm button text"
```

Overridable via `title`, `desc`, `selection_tooltip`, `confirm_text`. Console : `effect remove_decision_cooldown = my_decision`.
