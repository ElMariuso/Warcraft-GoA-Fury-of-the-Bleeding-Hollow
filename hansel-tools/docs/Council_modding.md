# Council Modding

> **Vue rapide** : Positions de conseil dans `common/council_positions/`, tâches dans `common/council_tasks/`. Au moins 1 tâche par position sinon crash.

---

## Structure d'une position

```jomini
my_councillor = {
    skill = diplomacy                # compétence principale (tri dans la liste)

    # Comportement
    auto_fill = no                   # remplissage auto (yes/no/{triggers})
    inherit = no                     # hérité par l'héritier principal
    can_fire = yes                   # peut être renvoyé
    can_reassign = yes               # peut être réassigné
    can_change_once = no             # assignable une fois, puis verrouillé
    special_council_position = no    # cumulable avec position régulière (ex: spouse)
    max_amount = 1                   # nombre max de positions (0 = infini)

    # Nom (loc key ou triggered loc)
    name = my_councillor_name
    # Définir aussi my_councillor_name_possessive sauf si special_council_position = yes

    # Modifiers
    modifier = { }                   # appliqué au conseiller (scale = script_value)
    council_owner_modifier = { }     # appliqué au liège

    # Triggers (scope: council owner sauf valid_character = scope character)
    valid_position = { }             # position disponible pour ce conseil ?
    valid_character = { }            # personnage éligible ?

    # Effects (scope: le personnage)
    on_get_position = { }
    on_lose_position = { }
    on_fired_from_position = { }

    use_for_scheme_power = no
    use_for_scheme_resistance = no
    portrait_animation = personality_rational
}
```

## Notes

- Les nouvelles positions n'apparaissent que dans les **nouvelles parties**
- Le court physician n'est **pas** dans `council_positions/` (géré séparément)
- Jusqu'à 5 blocs `modifier`/`council_owner_modifier` avec des `scale` différents
