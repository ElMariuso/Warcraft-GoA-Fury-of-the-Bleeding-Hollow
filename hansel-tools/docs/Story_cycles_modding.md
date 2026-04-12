# Story Cycles

> **Vue rapide** : un story cycle est un gestionnaire d'events persistant qui fire des events periodiquement et stocke des variables entre les sessions, meme apres la mort du proprietaire.

---

## Structure de base

Defini dans `common/story_cycles/`, fichier `.txt`. Trois hooks principaux + des `effect_group` optionnels.

```jomini
story_nom = {
    on_setup = { }        # a la creation du story cycle
    on_end = { }          # quand end_story = yes est appele
    on_owner_death = { }  # quand le story_owner meurt (encore vivant a ce moment)

    effect_group = {
        days = 30         # pulse repetitif (aussi: months, years)
        trigger = { }
        triggered_effect = {
            trigger = { }
            effect = { }
        }
    }
}
```

## Creer un story cycle

Depuis n'importe quel effet (event, decision, on_action) :

```jomini
# Dans un bloc immediate ou effect
create_story = story_exemple
```

Le personnage executant l'effet devient le `story_owner`.

## Story owner

Dans tous les blocs du story cycle, `story_owner` reference le proprietaire :

```jomini
on_setup = {
    story_owner = {
        save_scope_as = owner
        trigger_event = { id = wc_exemple.1000 days = 14 }
    }
}
```

Sans `story_owner = { }`, les effets s'appliquent au scope du story lui-meme.

## Terminer un story cycle

```jomini
end_story = yes
```

Appelle automatiquement le bloc `on_end`. Peut etre utilise dans n'importe quel contexte script.

## Transfert de propriete

Dans `on_owner_death`, transferer le story a un heritier au lieu de le terminer :

```jomini
on_owner_death = {
    make_story_owner = story_owner.primary_heir
}
```

## Effect groups (pulses)

Pulses repetitifs avec intervalle fixe ou aleatoire. Supporte `first_valid` pour choisir parmi plusieurs effets.

```jomini
effect_group = {
    days = { 30 60 }   # intervalle aleatoire entre 30 et 60 jours
    chance = 50         # 50% de chance que le pulse fire (1-100)
    first_valid = {
        triggered_effect = {
            trigger = { story_owner = { has_trait = brave } }
            effect = { story_owner = { add_prestige = 100 } }
        }
        triggered_effect = {
            effect = { story_owner = { add_prestige = 50 } }
        }
    }
}
```

## Exemple complet

```jomini
# common/story_cycles/story_exemple.txt
story_exemple = {
    on_setup = {
        story_owner = {
            save_scope_as = owner
            add_character_modifier = great_invader_modifier
            trigger_event = { id = wc_exemple.1000 days = 14 }
        }
    }

    on_end = {
        story_owner = {
            remove_character_modifier = great_invader_modifier
        }
    }

    on_owner_death = {
        story_owner = {
            primary_heir = {
                if = {
                    limit = { has_cultural_pillar = heritage_orcish }
                    make_story_owner = this
                }
                else = { end_story = yes }
            }
        }
    }

    effect_group = {
        months = 6
        triggered_effect = {
            trigger = { story_owner = { is_at_war = yes } }
            effect = {
                story_owner = {
                    trigger_event = { id = wc_exemple.2001 }
                }
            }
        }
    }
}
```
