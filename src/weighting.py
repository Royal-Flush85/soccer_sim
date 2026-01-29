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
            "positioning": 0.125,"speed": 0.225,"physical": 0.05,"passing": 0.2,
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
            "positioning": 0.2,"speed": 0.15, "physical": 0.05,"passing": 0.2,
            "shooting": 0.10,"control": 0.2,"defense": 0.10
        },
        "AM": { # similar to CM, but more specific to attacking
            "positioning": 0.15,"speed": 0.1,"physical": 0.05,"passing": 0.25,
            "shooting": 0.125,"control": 0.25,"defense": 0.075
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
        }
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
            "positioning": 0.2,"speed": 0.15, "physical": 0.05,"passing": 0.2,
            "shooting": 0.10,"control": 0.2,"defense": 0.10
        },
        "AM": { # similar to CM, but more specific to attacking
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
        }
    }, 
    "5-2-3": {
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
            "positioning": 0.15,"speed": 0.25,"physical": 0.10,"passing": 0.2,
            "shooting": 0.05,"control": 0.15,"defense": 0.10
        },
        "RB": {
            "positioning": 0.15,"speed": 0.25,"physical": 0.10,"passing": 0.2,
            "shooting": 0.05, "control": 0.15, "defense": 0.10
        },
        "DM": {
            "positioning": 0.15, "speed": 0.125, "physical": 0.1,"passing": 0.2,
            "shooting": 0.05, "control": 0.25, "defense": 0.125
        },
        "CM": {
            "positioning": 0.2,"speed": 0.15, "physical": 0.075,"passing": 0.225,
            "shooting": 0.10,"control": 0.25,"defense": 0.10
        },
        "AM": { 
            "positioning": 0.175,"speed": 0.175,"physical": 0.025,"passing": 0.25,
            "shooting": 0.125,"control": 0.225,"defense": 0.1
        },
        "LW": {
            "positioning": 0.175,"speed": 0.275,"physical": 0.025,"passing": 0.125,
            "shooting": 0.2,"control": 0.15,"defense": 0.05
        },
        "RW": {
            "positioning": 0.175,"speed": 0.275,"physical": 0.025,"passing": 0.125,
            "shooting": 0.2,"control": 0.15,"defense": 0.05
        },
        "CF": {
            "positioning": 0.15,"speed": 0.2,"physical": 0.1,"passing": 0.1,
            "shooting": 0.3,"control": 0.1,"defense": 0.05
        }
    }, 
    "5-3-2": {
        # addition to notes in the thing
        # counter attack, speed needed for wingers
        # midfield seeking balance
        "GK": {
            "blocking": 0.4, "technique": 0.3, "passing": 0.2, "positioning": 0.1
        },
        "CB": {
            "positioning": 0.1, "speed": 0.075,"physical": 0.25,"passing": 0.125,
            "shooting": 0.02,"control": 0.03,"defense": 0.4
        },
        "LB": { #will later depend on foot of player
            "positioning": 0.15,"speed": 0.225,"physical": 0.05,"passing": 0.275,
            "shooting": 0.025,"control": 0.125,"defense": 0.15
        },
        "RB": {
            "positioning": 0.15,"speed": 0.225,"physical": 0.05,"passing": 0.275,
            "shooting": 0.025, "control": 0.125, "defense": 0.15
        },
        "DM": {
            "positioning": 0.15, "speed": 0.05, "physical": 0.125,"passing": 0.225,
            "shooting": 0.05, "control": 0.225, "defense": 0.175
        },
        "CM": {
            "positioning": 0.125, "speed": 0.125, "physical": 0.075,"passing": 0.275,
            "shooting": 0.10, "control": 0.2, "defense": 0.10
        },
        "AM": { # similar to CM, but more specific to attacking
            "positioning": 0.125,"speed": 0.125,"physical": 0.05,"passing": 0.275,
            "shooting": 0.125,"control": 0.225,"defense": 0.075
        },
        "CF": {
            "positioning": 0.1,"speed": 0.175,"physical": 0.1,"passing": 0.1,
            "shooting": 0.40,"control": 0.1,"defense": 0.025
        }
    }


}

#

POSSESSION_WEIGHTS = {
    #access from weights = POSESSION_WEIGHTS[team.formation]
    # create player possession contribution in match_sim file
    # and multiplty that value with scale
    "4-2-3-1": { 
        "GK": 1, # once ready, I should make it so that certain attributes
        "LB": 10, # are important for a position in the formation 
        "CB": 12.5,
        "RB": 10,
        "CM": 17,
        "DM": 19,
        "AM": 6,
        "LM": 6,
        "RM": 6,
        #"LW": 0.03, #keep lw and rw until i fix formations
        #"RW": 0.03,
        "CF": 1
    },
    "4-3-3": { # less possession than 4-2-3-1
        "GK": 1,
        "LB": 9,
        "RB": 9,
        "CB": 12.5,
        "CM": 16,
        "DM": 21,
        "AM": 13,
        "LW": 2,
        "RW": 2,
        "CF": 1,
    },
    "5-2-3": { # less possession than 4-2-3-1
        "GK": 1,
        "LB": 6,
        "RB": 6,
        "CB": 12.5,
        "CM": 20,
        "DM": 17.5,
        "AM": 10,
        "LW": 2.5,
        "RW": 2.5,
        "CF": 1,
    },
    "5-3-2": { # depends on fighting style
        "GK": 1,
        "LB": 7,
        "RB": 7,
        "CB": 12.5,
        "CM": 12.5,
        "DM": 17.5,
        "AM": 10,
        "CF": 2,
    },
}

DEF_POSSESSION_WEIGHTS = { #eventually
    "4-2-3-1": {
        "GK": 1, 
        "LB": 9, 
        "CB": 10,
        "RB": 9,
        "CM": 14,
        "DM": 17.5,
        "AM": 10,
        "LM": 7,
        "RM": 7,
        "CF": 5
    },
    "4-3-3": {
        "GK": 1,
        "LB": 9,
        "RB": 9,
        "CB": 10,
        "DM": 15,
        "CM": 12.5,
        "AM": 10,
        "LW": 5,
        "RW": 5,
        "CF": 5,
    }, 
    "5-2-3": { # still should be low since this formation is weak in possession
        "GK": 1,
        "LB": 6,
        "RB": 6,
        "CB": 10,
        "CM": 10,
        "DM": 12.5,
        "AM": 5,
        "LW": 4,
        "RW": 4,
        "CF": 3,
    },
    "5-3-2": { 
        "GK": 1,
        "LB": 6,
        "RB": 6,
        "CB": 10,
        "CM": 10,
        "DM": 15,
        "AM": 7.5,
        "LW": 4,
        "RW": 4,
        "CF": 3,
    }
}

SHOTS_WEIGHTS = { 
    # shots considering build up, like for 4231, it considers
    # dm cm cb (higher) for possession, lmrm, lbrb, am, cf for shots
    "4-2-3-1": { #access from weights = POSESSION_WEIGHTS[team.formation]
                 # create player possession contribution in match_sim file
                 # and multiplty that value with scale
        "GK": 1, # {home when attacking,opp when defending}
        "LB": 9,
        "CB": 5,
        "RB": 9,
        "CM": 15,
        "DM": 11,
        "AM": 23,
        "LM": 21,
        "RM": 21,
        "CF": 17
    }, #more shots for 4-3-3? since possession is high for 4-2-3-1
    "4-3-3": {
        "GK": 1,
        "LB": 8,
        "CB": 5,
        "RB": 8,
        "DM": 10,
        "CM": 15,
        "AM": 17.5,
        "LW": 22.5,
        "RW": 22.5,
        "CF": 18
    },
    "5-2-3": { # higher percent shots compared to lack of possession
        "GK": 1,
        "LB": 10,
        "RB": 10,
        "CB": 5,
        "CM": 15,
        "DM": 12.5,
        "AM": 17.5,
        "LW": 20,
        "RW": 20,
        "CF": 20,
    },
    "5-3-2": { # still should be low since this formation is weak in possession
        "GK": 1,
        "LB": 10,
        "RB": 10,
        "CB": 5,
        "CM": 15,
        "DM": 10,
        "AM": 20,
        "CF": 20,
    }

}
DEF_SHOTS_WEIGHTS = {
    "4-2-3-1": { # my thought process is, once i add formation, the values
                 # are gonna be scalars that represent the importance of
                 # each attack + positions, which fits the ipad notes 
                 # regarding shots, possession, etc
        "GK": 5,
        "LB": 12.5,
        "CB": 22.5,
        "RB": 12.5,
        "CM": 12.5,
        "DM": 17,
        "AM": 7.5,
        "LM": 10,
        "RM": 10,
        "CF": 3
    },
    "4-3-3": { #my thought process is, once i add formation, the values
                 # are gonna be scalars that represent the importance of
                 # each attack + positions, which fits the ipad notes 
                 # regarding shots, possession, etc
        "GK": 5,
        "LB": 13.5,
        "CB": 22.5,
        "RB": 13.5,
        "CM": 12.5,
        "DM": 17,
        "AM": 12.5,
        "LW": 5,
        "RW": 5,
        "CF": 3
    },
    "5-2-3": { # higher cuz possession disadvantage
        "GK": 1,
        "LB": 12.5,#10,
        "RB": 12.5,#10,
        "CB": 22.5,#20,
        "CM": 15,#12.5,
        "DM": 17.5,#15,
        "AM": 10,#7.5,
        "LW": 7,#5,
        "RW": 7,#5,
        "CF": 5#3,
    },
    "5-3-2": { # still should be low since this formation is weak in possession
        "GK": 1,
        "LB": 12.5,#10,
        "RB": 12.5,#10,
        "CB": 25,#20,
        "CM": 15, #10,
        "DM": 20,#17.5,
        "AM": 12.5,#7.5
        "CF": 5#3,
    }
    
}

SHOTST_WEIGHTS = {#access from weights = POSESSION_WEIGHTS[team.formation]
                 # create player possession contribution in match_sim file
                 # and multiplty that value with scale
    "4-2-3-1": {
        "GK": {"weight": 1, "attr": "passing"},
        "LB": {"weight": 7, "attr": "shooting"},
        "CB": {"weight": 3, "attr": "shooting"},
        "RB": {"weight": 7, "attr": "shooting"},
        "CM": {"weight": 10, "attr": "shooting"},
        "DM": {"weight": 4, "attr": "shooting"},
        "AM": {"weight": 25, "attr": "shooting"},
        "LM": {"weight": 17.5, "attr": "shooting"},
        "RM": {"weight": 17.5, "attr": "shooting"},
        "CF": {"weight": 32.5, "attr": "shooting"},
    },
    "4-3-3": {
        "GK": {"weight": 1, "attr": "passing"},
        "LB": {"weight": 6, "attr": "shooting"},
        "CB": {"weight": 3, "attr": "shooting"},
        "RB": {"weight": 6, "attr": "shooting"},
        "CM": {"weight": 12, "attr": "shooting"},
        "DM": {"weight": 4, "attr": "shooting"},
        "AM": {"weight": 17.5, "attr": "shooting"},
        "LW": {"weight": 29, "attr": "shooting"},
        "RW": {"weight": 29, "attr": "shooting"},
        "CF": {"weight": 35, "attr": "shooting"}
    },
    "5-2-3": { #relatively high, sicne theres higher value in counter-attack
        "GK": {"weight": 1, "attr": "passing"},
        "LB": {"weight": 10, "attr": "shooting"},
        "CB": {"weight": 3, "attr": "shooting"},
        "RB": {"weight": 10, "attr": "shooting"},
        "CM": {"weight": 15, "attr": "shooting"},
        "DM": {"weight": 12.5, "attr": "shooting"},
        "AM": {"weight": 17.5, "attr": "shooting"},
        "LW": {"weight": 30, "attr": "shooting"},
        "RW": {"weight": 30, "attr": "shooting"},
        "CF": {"weight": 32.5, "attr": "shooting"}
    },
    "5-3-2": { 
        "GK": {"weight": 1, "attr": "passing"},
        "LB": {"weight": 10, "attr": "shooting"},
        "CB": {"weight": 3, "attr": "shooting"},
        "RB": {"weight": 10, "attr": "shooting"},
        "CM": {"weight": 15, "attr": "shooting"},
        "DM": {"weight": 12.5, "attr": "shooting"},
        "AM": {"weight": 17.5, "attr": "shooting"},
        "CF": {"weight": 40, "attr": "shooting"}
    }
}


DEF_SHOTST_WEIGHTS = {
    "4-2-3-1": {
        "LB": {"weight": 13,"first_def": "defense","second_def":"physical"},
        "CB": {"weight": 30,"first_def": "defense","second_def":"physical"},
        "RB": {"weight": 13,"first_def": "defense","second_def":"physical"},
        "CM": {"weight": 13,"first_def": "defense","second_def":"physical"},
        "DM": {"weight": 19,"first_def": "defense","second_def":"physical"},
        "AM": {"weight": 3,"first_def": "defense","second_def":"physical"},
        "LM": {"weight": 5,"first_def": "defense","second_def":"physical"},
        "RM": {"weight": 5,"first_def": "defense","second_def":"physical"},
        "CF": {"weight": 1,"first_def": "defense","second_def":"physical"},
    },
    "4-3-3": {
        "LB": {"weight": 14,"first_def": "defense","second_def":"physical"},
        "CB": {"weight": 30,"first_def": "defense","second_def":"physical"},
        "RB": {"weight": 14,"first_def": "defense","second_def":"physical"},
        "CM": {"weight": 12,"first_def": "defense","second_def":"physical"},
        "DM": {"weight": 20,"first_def": "defense","second_def":"physical"},
        "AM": {"weight": 7,"first_def": "defense","second_def":"physical"},
        "LW": {"weight": 2,"first_def": "defense","second_def":"physical"},
        "RW": {"weight": 2,"first_def": "defense","second_def":"physical"},
        "CF": {"weight": 1,"first_def": "defense","second_def":"physical"},
    },
    "5-2-3": {
        "LB": {"weight": 11,"first_def": "defense","second_def":"physical"},
        "CB": {"weight": 30,"first_def": "defense","second_def":"physical"},
        "RB": {"weight": 11,"first_def": "defense","second_def":"physical"},
        "CM": {"weight": 12.5,"first_def": "defense","second_def":"physical"},
        "DM": {"weight": 15,"first_def": "defense","second_def":"physical"},
        "AM": {"weight": 10,"first_def": "defense","second_def":"physical"},
        "LW": {"weight": 5,"first_def": "defense","second_def":"physical"},
        "RW": {"weight": 5,"first_def": "defense","second_def":"physical"},
        "CF": {"weight": 4,"first_def": "defense","second_def":"physical"},
    },
    "5-3-2": {
        "LB": {"weight": 11,"first_def": "defense","second_def":"physical"},
        "CB": {"weight": 30,"first_def": "defense","second_def":"physical"},
        "RB": {"weight": 11,"first_def": "defense","second_def":"physical"},
        "CM": {"weight": 12.5,"first_def": "defense","second_def":"physical"},
        "DM": {"weight": 20,"first_def": "defense","second_def":"physical"},
        "AM": {"weight": 10,"first_def": "defense","second_def":"physical"},
        "CF": {"weight": 5,"first_def": "defense","second_def":"physical"},
    }
}


SHOTS_WEIGHTS_BY_PLAYER = { 
    # shots considering build up, like for 4231, it considers
    # dm cm cb (higher) for possession, lmrm, lbrb, am, cf for shots
    "4-2-3-1": { #access from weights = POSESSION_WEIGHTS[team.formation]
                 # create player possession contribution in match_sim file
                 # and multiplty that value with scale
        "GK": 1, # {home when attacking,opp when defending}
        "LB": 14,
        "CB": 15,
        "RB": 14,
        "CM": 16,
        "DM": 16,
        "AM": 19.5,
        "LM": 19,
        "RM": 19,
        "CF": 20
    }, #more shots for 4-3-3? since possession is high for 4-2-3-1
    "4-3-3": {
        "GK": 1,
        "LB": 13.5,
        "CB": 15,
        "RB": 13.5,
        "DM": 15.5,
        "CM": 16.5,
        "AM": 18.5,
        "LW": 19.5,
        "RW": 19.5,
        "CF": 20
    },
    "5-2-3": { # higher percent shots compared to lack of possession
        "GK": 1,
        "LB": 14.5,
        "RB": 14.5,
        "CB": 15,
        "CM": 17,
        "DM": 16,
        "AM": 18,
        "LW": 20,
        "RW": 20,
        "CF": 20,
    },
    "5-3-2": { # still should be low since this formation is weak in possession
        "GK": 1,
        "LB": 14.5,
        "RB": 14.5,
        "CB": 15,
        "CM": 17,
        "DM": 16,
        "AM": 19,
        "CF": 20,
    }

}
