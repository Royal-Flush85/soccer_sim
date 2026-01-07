# Proposal 1: calculate pos, shot, shotst from ratings,
#       Pros/cons: less specific, so player with high trait in 
#                  one attribute won't be inflated, good estimate,
#                  but less according to tactical roles and would
#                  have some differences if skewed traits
#
# Proposal 2: calculate pos, shot, shotst from attributes,
#       Pros/cons: more specific, but more time consuming, +
#                  things stated above
#
#
# 1/6/26: I should make formation decision-making, would possibly either add
#         a new variable for team_pos, decide how it will be decided


#player rating
POSITION_WEIGHTS = {
    "4-2-3-1": {
        "GK": {
            "blocking": 0.4, "technique": 0.3, "passing": 0.2, "positioning": 0.1
        },
        "CB": {
            "positioning": 0.1, "speed": 0.075,"physical": 0.3,"passing": 0.075,
            "shooting": 0.02,"control": 0.03,"defense": 0.4
        },
        "LB": {
            "positioning": 0.15,"speed": 0.2,"physical": 0.10,"passing": 0.2,
            "shooting": 0.05,"control": 0.15,"defense": 0.15
        },
        "RB": {
            "positioning": 0.15,"speed": 0.2,"physical": 0.10,"passing": 0.2,
            "shooting": 0.05, "control": 0.15, "defense": 0.15
        },
        "DM": {
            "positioning": 0.15, "speed": 0.05, "physical": 0.15,"passing": 0.225,
            "shooting": 0.05, "control": 0.225, "defense": 0.15
        },
        "CM": {
            "positioning": 0.15,"speed": 0.1, "physical": 0.1,"passing": 0.225,
            "shooting": 0.10,"control": 0.225,"defense": 0.10
        },
        "AM": {
            "positioning": 0.1,"speed": 0.1,"physical": 0.025,"passing": 0.30,
            "shooting": 0.175,"control": 0.275,"defense": 0.025
        },
        "LM": {
            "positioning": 0.125,"speed": 0.225,"physical": 0.05,"passing": 0.2,
            "shooting": 0.1,"control": 0.2,"defense": 0.1
        },
        "RM": {
            "positioning": 0.1,"speed": 0.25,"physical": 0.05,"passing": 0.2,
            "shooting": 0.1,"control": 0.2,"defense": 0.1
        },
        "CF": {
            "positioning": 0.15,"speed": 0.10,"physical": 0.1,"passing": 0.14,
            "shooting": 0.35,"control": 0.15,"defense": 0.01
        },
    },
    "4-3-3": {
        # addition to notes in the thing
        # counter attack, speed needed for wingers
        # midfield seeking balance
        "GK": {
            "blocking": 0.4, "technique": 0.3, "passing": 0.2, "positioning": 0.1
        },
        "CB": {
            "positioning": 0.1, "speed": 0.075,"physical": 0.3,"passing": 0.075,
            "shooting": 0.02,"control": 0.03,"defense": 0.4
        },
        "LB": { #will later depend on foot of player
            "positioning": 0.15,"speed": 0.2,"physical": 0.10,"passing": 0.2,
            "shooting": 0.05,"control": 0.15,"defense": 0.15
        },
        "RB": {
            "positioning": 0.15,"speed": 0.2,"physical": 0.10,"passing": 0.2,
            "shooting": 0.05, "control": 0.15, "defense": 0.15
        },
        "DM": {
            "positioning": 0.15, "speed": 0.05, "physical": 0.15,"passing": 0.225,
            "shooting": 0.05, "control": 0.225, "defense": 0.15
        },
        "CM": {
            "positioning": 0.2,"speed": 0.125, "physical": 0.075,"passing": 0.2,
            "shooting": 0.10,"control": 0.2,"defense": 0.10
        },
        "AM": { #similar to CM, but more specific to attacking
            "positioning": 0.175,"speed": 0.1,"physical": 0.05,"passing": 0.25,
            "shooting": 0.125,"control": 0.225,"defense": 0.075
        },
        "LW": {
            "positioning": 0.175,"speed": 0.275,"physical": 0.025,"passing": 0.15,
            "shooting": 0.2,"control": 0.15,"defense": 0.025
        },
        "RW": {
            "positioning": 0.175,"speed": 0.275,"physical": 0.025,"passing": 0.15,
            "shooting": 0.2,"control": 0.15,"defense": 0.025
        },
        "CF": {
            "positioning": 0.15,"speed": 0.10,"physical": 0.1,"passing": 0.14,
            "shooting": 0.35,"control": 0.15,"defense": 0.01
        },
    }

}

#

POSSESSION_WEIGHTS = {
    #access from weights = POSESSION_WEIGHTS[team.formation]
    # create player possession contribution in match_sim file
    # and multiplty that value with scale
    "4-2-3-1": { 
        "GK": 1, # once ready, I should make it so that certain attributes
        "LB": 7, # are important for a position in the formation 
        "CB": 15,
        "RB": 7,
        "CM": 15,
        "DM": 20,
        "AM": 5,
        "LM": 5,
        "RM": 5,
        #"LW": 0.03, #keep lw and rw until i fix formations
        #"RW": 0.03,
        "CF": 1
    },
    "4-3-3": { #less possession than 4-2-3-1
        "GK": 1,
        "LB": 7,
        "RB": 7,
        "CB": 15,
        "CM": 12.5,
        "DM": 20,
        "AM": 10,
        "LW": 2,
        "RW": 2,
        "CF": 1,
    }
}

DEF_POSSESSION_WEIGHTS = { #eventually
    "4-2-3-1": {
        "GK": 1, 
        "LB": 7, 
        "CB": 10,
        "RB": 7,
        "CM": 15,
        "DM": 15,
        "AM": 10,
        "LM": 7,
        "RM": 7,
        "CF": 5
    },
    "4-3-3": {
        "GK": 1,
        "LB": 7,
        "RB": 7,
        "CB": 10,
        "DM": 15,
        "CM": 15,
        "AM": 10,
        "LW": 5,
        "RW": 5,
        "CF": 5,
    }
}

SHOTS_WEIGHTS = { 
    # shots considering build up, like for 4231, it considers
    # dm cm cb (higher) for possession, lmrm, lbrb, am, cf for shots
    "4-2-3-1": { #access from weights = POSESSION_WEIGHTS[team.formation]
                 # create player possession contribution in match_sim file
                 # and multiplty that value with scale
        "GK": 0.01, # {home when attacking,opp when defending}
        "LB": 0.08,
        "CB": 0.02,
        "RB": 0.08,
        "CM": 0.15,
        "DM": 0.04,
        "AM": 0.25,
        "LM": 0.15,
        "RM": 0.15,
        "LW": 0.25, #keep lw and rw until i fix formations
        "RW": 0.25,
        "CF": 0.35
    }
}
DEF_SHOTS_WEIGHTS = {
    "4-2-3-1": { #my thought process is, once i add formation, the values
                 # are gonna be scalars that represent the importance of
                 # each attack + positions, which fits the ipad notes 
                 # regarding shots, possession, etc
        "GK": 0.1,
        "LB": 0.20,
        "CB": 0.30,
        "RB": 0.20,
        "CM": 0.15,
        "DM": 0.25,
        "AM": 0.05,
        "LM": 0.05,
        "RM": 0.05,
        "LW": 0.02, #keep lw and rw until i fix formations
        "RW": 0.02,
        "CF": 0.01
    }
}
SHOTST_WEIGHTS = {#access from weights = POSESSION_WEIGHTS[team.formation]
                 # create player possession contribution in match_sim file
                 # and multiplty that value with scale
    "4-2-3-1": {
        "GK": {"weight": 0.01, "attr": "passing"},
        "LB": {"weight": 0.07, "attr": "shooting"},
        "CB": {"weight": 0.03, "attr": "shooting"},
        "RB": {"weight": 0.07, "attr": "shooting"},
        "CM": {"weight": 0.10, "attr": "shooting"},
        "DM": {"weight": 0.04, "attr": "shooting"},
        "AM": {"weight": 0.25, "attr": "shooting"},
        "LM": {"weight": 0.10, "attr": "shooting"},
        "RM": {"weight": 0.10, "attr": "shooting"},
        "LW": {"weight": 0.20, "attr": "shooting"},
        "RW": {"weight": 0.20, "attr": "shooting"},
        "CF": {"weight": 0.40, "attr": "shooting"},
    }
}


DEF_SHOTST_WEIGHTS = {
    "4-2-3-1": {
        "LB": {"weight": 0.15,"first_def": "defense","second_def":"physical"},
        "CB": {"weight": 0.3,"first_def": "defense","second_def":"physical"},
        "RB": {"weight": 0.15,"first_def": "defense","second_def":"physical"},
        "CM": {"weight": 0.1,"first_def": "defense","second_def":"physical"},
        "DM": {"weight": 0.2,"first_def": "defense","second_def":"physical"},
        "AM": {"weight": 0.01,"first_def": "defense","second_def":"physical"},
        "LM": {"weight": 0.03,"first_def": "defense","second_def":"physical"},
        "RM": {"weight": 0.03,"first_def": "defense","second_def":"physical"},
        "LW": {"weight": 0.01,"first_def": "defense","second_def":"physical"},
        "RW": {"weight": 0.01,"first_def": "defense","second_def":"physical"},
        "CF": {"weight": 0.01,"first_def": "defense","second_def":"physical"},
    }
}

