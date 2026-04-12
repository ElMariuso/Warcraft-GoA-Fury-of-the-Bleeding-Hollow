# Governments Modding

> **Vue rapide** : Les gouvernements sont définis dans `common/governments/00_government_types.txt`. Ils déterminent les holdings, contrats vassaux, et comportement IA.

---

## Structure

```jomini
feudal_government = {
    create_cadet_branches = yes
    rulers_should_have_dynasty = yes
    dynasty_named_realms = yes
    council = yes                               # conseil disponible (défaut: yes)
    regiments_prestige_as_gold = no             # MaA payés en prestige ? (défaut: no)
    fallback = 1

    primary_holding = castle_holding            # holding principal
    valid_holdings = { city_holding }           # holdings utilisables sans pénalité
    required_county_holdings = { castle_holding city_holding church_holding }

    vassal_contract = {
        feudal_government_taxes
        feudal_government_levies
        special_contract
        religious_rights
        fortification_rights
        coinage_rights
        succession_rights
        war_declaration_rights
        council_rights
        title_revocation_rights
    }

    ai = {
        use_lifestyle = yes
        imprison = yes
        start_murders = yes
        arrange_marriage = yes
        use_goals = yes
        use_decisions = yes
        use_scripted_guis = yes
        perform_religious_reformation = yes
    }

    color = hsv{ 0.67 1.00 0.78 }
}
```

## Notes

- `primary_holding` : type de holding considéré principal par ce gouvernement
- `valid_holdings` : holdings additionnels sans pénalité
- Le bloc `ai` permet de désactiver des comportements IA spécifiques (tous activés par défaut)
- Voir `_governments.info` dans le dossier vanilla pour la référence complète
