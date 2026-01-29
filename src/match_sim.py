import numpy as np
from src.models import MatchResult
from src.models import MatchResult2
from src.models import MinuteEvent
from src.weighting import (
    POSITION_WEIGHTS,
    POSSESSION_WEIGHTS,
    DEF_POSSESSION_WEIGHTS,
    SHOTS_WEIGHTS,
    SHOTS_WEIGHTS_BY_PLAYER,
    DEF_SHOTS_WEIGHTS,
    SHOTST_WEIGHTS,
    DEF_SHOTST_WEIGHTS,
)


HOME_ADVANTAGE = 1.03

'''def expected_goals(att, defn, home=False):
    # att is home attack, defn is away def, vice versa
    # goal number
    base = att / defn
    return base * HOME_ADVANTAGE if home else base

def simulate_goals(xg):
    # poisson distribution using numpy
    return np.random.poisson(xg) 

def simulate_match(home,away):
    # assigns vari as a matchresult class with stuff
    xg_home = expected_goals(home.attack,away.defense, home=True)
    xg_away = expected_goals(away.attack, home.defense)

    goals_home = simulate_goals(xg_home)
    goals_away = simulate_goals(xg_away)

    return MatchResult(goals_home, goals_away)
'''
def simulate_match(home_team, away_team): #list of players
    #shots, tshots, goals, possession
    home_players = home_team.players
    away_players = away_team.players
    home_possession = simulated_possession(expected_possession(
        team_pos(home_players, home_team.team_formation, 
        away_players,away_team.team_formation), 
        team_pos(away_players,away_team.team_formation, 
        home_players, home_team.team_formation),home=True))
    away_possession = 100 - home_possession

    exp_home_possession = expected_possession(
        team_pos(home_players, home_team.team_formation, 
        away_players,away_team.team_formation), 
        team_pos(away_players,away_team.team_formation,
        home_players, home_team.team_formation),home=True)
    exp_home_shots = exp_shots(home_players, away_players,
        home_possession,home_team.team_formation, away_team.team_formation, home=True)
    exp_away_shots = exp_shots(away_players, home_players, 
        away_possession, away_team.team_formation, home_team.team_formation)


    # for this, make simulated shots find which players score a goal (make that calculation every minute)
    # make player performance not random first, im making simulation work first, entertaining comes
    # based on such simulation
    home_shots = simulated_shots(exp_shots(home_players, away_players,
        home_possession,home_team.team_formation, away_team.team_formation, home=True))
    
    away_shots = simulated_shots(exp_shots(away_players, home_players, 
        away_possession, away_team.team_formation, home_team.team_formation))
    
    home_shotsT = simulated_shotsT(home_shots, expected_shotsT_ratio(home_players, 
        home_team.team_formation,away_players,away_team.team_formation))
    #could have combined expected + simulated shotsT method together
    away_shotsT = simulated_shotsT(away_shots, expected_shotsT_ratio(away_players, 
        away_team.team_formation, home_players, home_team.team_formation))
    home_goals = simulated_goals(exp_goals(home_shotsT, away_players[0], 
        home_players, home_team.team_formation), home_shotsT)
    away_goals = simulated_goals(exp_goals(away_shotsT, home_players[0], 
        away_players, away_team.team_formation), away_shotsT)
    
    return MatchResult(home_goals, away_goals, home_possession, away_possession,
        home_shots, away_shots, home_shotsT, away_shotsT, 
        exp_home_possession, exp_home_shots, exp_away_shots)

        #do player attributes

def simulate_match_2(home_team, away_team):
    home_players = home_team.players
    away_players = away_team.players
    home_possession = simulated_possession(expected_possession(
        team_pos(home_players, home_team.team_formation, 
        away_players,away_team.team_formation), 
        team_pos(away_players,away_team.team_formation, 
        home_players, home_team.team_formation),home=True))
    away_possession = 100 - home_possession

    exp_home_shots = exp_shots(home_players, away_players,
        home_possession,home_team.team_formation, away_team.team_formation, home=True)
    exp_away_shots = exp_shots(away_players, home_players, 
        away_possession, away_team.team_formation, home_team.team_formation)
    exp_home_possession = expected_possession(
        team_pos(home_players, home_team.team_formation, 
        away_players,away_team.team_formation), 
        team_pos(away_players,away_team.team_formation,
        home_players, home_team.team_formation),home=True)
    home_shots = 0
    home_shotsT = 0
    home_goals = 0
    away_shots = 0
    away_shotsT = 0
    away_goals = 0
    home_tot_events = []
    away_tot_events = []
    for minute in range(1, 90):
        events = simulate_all_by_minute(exp_home_shots, home_team, away_team, minute)
        away_event = simulate_all_by_minute(exp_away_shots, away_team, home_team, minute)
        home_tot_events.append(events) #events = all events in a minute
        away_tot_events.append(away_event)
        if len(events) != 0:
            home_shots+= len(events)
            for event in events:
                if event.on_target:
                    home_shotsT += 1
                    if event.goal:
                        home_goals += 1
            
        if len(away_event) != 0:
            away_shots += len(away_event)
            for event in away_event:
                if event.on_target:
                    away_shotsT += 1
                    if event.goal:
                        away_goals += 1
    
    return MatchResult2(home_goals, away_goals,home_possession, away_possession, 
        home_shots, away_shots, home_shotsT, away_shotsT, home_tot_events, 
        away_tot_events, exp_home_possession, exp_home_shots, exp_away_shots)


## POSSESSION CALCULATION ##
def team_pos_pwr(team_players, team_formation):
    weights = POSSESSION_WEIGHTS[team_formation]
    total = 0
    for player in team_players:
        total += player.rating * weights[player.position] 
        # change player.rating 
        # to specific method 
        # that calculates pos
        # based on attributes
    return total / 100 # from alteration of weighting.py

def team_pos(home_players, home_formation, away_players, away_formation):
    weights = POSSESSION_WEIGHTS[home_formation]
    def_weights = DEF_POSSESSION_WEIGHTS[away_formation]
    total = 0
    def_total = 0
    for player in home_players:
        total += player.rating * weights[player.position]
    for player in away_players:
        def_total += player.rating * def_weights[player.position]
    return total / def_total

def expected_possession(home_pwr, away_pwr, home=False):
    if home:
        home_pwr *= HOME_ADVANTAGE

    diff = home_pwr - away_pwr
    k = 5  # elo-style function tuning knob (higher = bigger impact), narrower curve

    # logistic function, clipped to reasonable bounds
    possession = 1 / (1 + np.exp(-k * diff))
    return np.clip(possession, 0.35, 0.65)


def simulated_possession(exp_pos, variance=0.025):
    # variance controls randomness (lower = more stable)
    alpha = exp_pos * (1 - variance) / variance
    beta = (1 - exp_pos) * (1 - variance) / variance

    return np.random.beta(alpha, beta) * 100 # percent conversion


## SHOTS CALCULATION ##
#team_formation needed since possession does not directly correlate with 
#shots, it also depends on formation
#
# for now, just use possession value and opponent defense for now
# in the future, id want to incorporate different cases for when 
# a specfic formattion encounters other type that impacts shots,
# possession, etc. if opp_defense is high, how would it react?
# more prone to counter-attack? etc
'''def exp_shots(home_players, away_players, possession, team_formation, opp_formation, home=False):
    pos_factor = 0.4 + 1.2 * (possession / 100)
    BASE_SHOTS = 10
    home_val = team_shots_pwr(home_players, team_formation)
    away_val = def_team_shots_pwr(away_players, opp_formation)
    exp_shots = BASE_SHOTS * pos_factor * home_val / away_val
    
    return exp_shots * HOME_ADVANTAGE if home else exp_shots'''
def exp_shots(home_players, away_players, possession,
              team_formation, opp_formation, home=False):
    BASE_SHOTS = 12
    possession_factor = 0.3 + 1.4 * (possession / 100)
    home_val = team_shots_pwr(home_players, team_formation)
    away_val = def_team_shots_pwr(away_players, opp_formation)
    # power_diff = (home_val - away_val)/100 #scale the difference
    # k = 1.2  # tuning knob for impact of power difference (1/e^diff)
    # strength_mult = 1 / (1 + np.exp(-k * power_diff))
    # higher k * power_diff indicates higher difference between teams
    power_diff = (home_val - away_val) * 0.0001
    k = 1 # sensitivity
    strength_mult = np.exp(k * power_diff)
    #possession_factor = possession/100
    exp_shots = BASE_SHOTS * possession_factor * strength_mult
    if home:
        exp_shots *= HOME_ADVANTAGE
    return exp_shots


def team_shots_pwr(home_players, team_formation):
    weights = SHOTS_WEIGHTS[team_formation]
    home_total = 0
    for player in home_players:
        home_total += player.rating * weights[player.position]
    return (home_total) # figure out the right val

def def_team_shots_pwr(away_players, opp_formation):
    away_total = 0
    def_weights = DEF_SHOTS_WEIGHTS[opp_formation]
    for player in away_players:
        away_total += player.rating * def_weights[player.position]
    return away_total

def simulated_shots(exp_shots):
    # r = dispersion (higher r → closer to Poisson), decides variance
    # # stable shots counts: higher r value
    # p = r / (r + exp_shots)
    # return np.random.negative_binomial(r, p)
    # return np.random.normal(loc=exp_shots, scale=exp_shots/2).round().astype(int)

    # create player score value based on exp_shots? -> for now
    #   - each player will have min or max value compare with simulated value 
    #   - this value will be based on summation of all prior players in the team
    #   - exp_shots / 90
    #   - also, mistake, just do it for goals first/only
    #   - in the future the full process goes like:
    #       - based on player value from plyr pos * plyr rating = plyr likeliness to
    #         create significant change (ignoring possession for now, cuz
    #         itll only matter when simulating minute by minute while displaying
    #         at the very least the shots/chances/goals created by each player)
    #       - then, based on that, calculate shots created by player (same calculation
    #         of likeliness) and then have shots on target calculated (player rate)
    #       - then goal, so essentially, all the methods created so far regarding
    #         shots, shotsT, goals, will be changed in the sense that they will
    #         take in value of player + minute and calculate (like filter, from
    #         a chance to shot to shotsT to goal), and i could also take in similar
    #         thing for defense as well.
    # later, simulate minute by minute, and see which player scores
    return np.random.poisson(exp_shots)
    # return np.random.binomial(exp_shots, p=1)



## SHOTST CALC ##
# def expected_shotsT(simulated_shots, home_players, home_formation, away_players, away_formation, home=False):
#     #avg is 30-45%
#     home_val = team_shotsT_pwr(home_players, home_formation)
#     away_val = def_team_shotsT_pwr(away_players, away_formation)
#     return simulated_shots * (home_val / away_val)
def expected_shotsT_ratio(home_players, home_formation, away_players, away_formation):
    home_val = team_shotsT_pwr(home_players, home_formation)
    away_val = def_team_shotsT_pwr(away_players, away_formation)
    return home_val / away_val

def team_shotsT_pwr(home_players, home_formation):
    weights = SHOTST_WEIGHTS[home_formation]
    home_val = 0
    for player in home_players:
        attr = weights[player.position]["attr"]
        home_val += getattr(player, attr, 0) * weights[player.position]["weight"]
    return home_val
def def_team_shotsT_pwr(away_players, away_formation):
    def_weights = DEF_SHOTST_WEIGHTS[away_formation]
    away_val = 0
    for player in away_players:
        pos = player.position
        if pos in def_weights:
            first_attr = def_weights[pos]["first_def"] #defense
            second_attr = def_weights[pos]["second_def"] #physical

            first_val = getattr(player, first_attr)
            second_val = getattr(player, second_attr)
            away_val += (def_weights[pos]["weight"] *
                (first_val + second_val))
    return away_val

# def simulated_shotsT(exp_shotsT, simulated_shots):
#     sim_shotsT = np.random.poisson(exp_shotsT)
#     returnVal = max(0, min(simulated_shots,sim_shotsT))
#     return returnVal
def simulated_shotsT(simulated_shots, ratio):
    return max(0, min(np.random.binomial(simulated_shots, ratio), simulated_shots))

## GOALS calc##
def exp_goals(simulated_shotsT, away_keeper, home_players, home_formation): 
    #eventually put algorithm for formation
    # when i research more about it
    total = away_keeper.blocking * 200 # scale from weighting.py total being around 110
    shooter_pwr = team_shotsT_pwr(home_players, home_formation)
    return simulated_shotsT * (shooter_pwr)/(total + shooter_pwr)

# def simulated_goals(exp_goals, simulated_shotsT):
#     sim_goals = np.random.poisson(exp_goals)
#     return max(0, min(sim_goals, simulated_shotsT))
def simulated_goals(exp_goals, simulated_shotsT, r=13):
    # r = dispersion (higher r → closer to Poisson), decides variance
    # stable shots counts: higher r value
    # g = r / (r + exp_goals)
    # sim_goals = np.random.negative_binomial(r, g)
    return max(0, min(np.random.binomial(exp_goals, p=1), simulated_shotsT))






## SIMULATION with player data ##

# method that has probability distribution over players
def build_player_shot_weights(players, formation):
    pos_weights = SHOTS_WEIGHTS_BY_PLAYER[formation] # make it so that striker is also high?
    weights = []
    for p in players:
        w = p.rating * pos_weights[p.position]
        weights.append(w)
    total = sum(weights)
    probs = [w / total for w in weights] 
    return probs
# in simulate_match(), for minute in 1 ... 90, simulate_minute()
def simulate_all_by_minute(exp_shots, home_team, away_team, minute):
    # probability of a shot in this minute
    p_shot = exp_shots / 90.0

    player_probs = build_player_shot_weights(home_team.players, home_team.team_formation)
    events = []

    # Bernoulli trial: does a shot happen this minute?
    if np.random.rand() < p_shot:
        # choose shooter based on player_probs
        shooter = np.random.choice(home_team.players, p=player_probs)
        event = MinuteEvent(minute, shooter)
        # on target
        event.on_target = simulate_shotsT_minute(shooter, home_team, away_team)
        # goal
        # TODO: replace away_team.players[0] with actual goalie reference
        if event.on_target:
            event.goal = goal_prob(shooter, home_team.team_formation, away_team.players[0])
        
        events.append(event)

    return events
 # list of shots per minute with player and minute info
# shots is more like a team thing, so exp_shots (that used team value was reused)
# shots on target is more like player shooting thing, so we create a new one
#    -defense is reused cuz its kinda team thing
def shotsT_prob(shooter, home_formation, away_players, away_formation):
    # att = (getattr(shooter, SHOTST_WEIGHTS[home_formation][shooter.position]["attr"])
    #     * SHOTST_WEIGHTS[home_formation][shooter.position]["weight"]) #do the weights
    att = (getattr(shooter, SHOTST_WEIGHTS[home_formation][shooter.position]["attr"])
        * SHOTS_WEIGHTS_BY_PLAYER[home_formation][shooter.position])
    df = def_team_shotsT_pwr(away_players, away_formation) / 20 #next 17-20
    diff = (att - df) * 0.1
    prob = 1/ (1+np.exp(-diff))
    return np.clip(prob, 0.05, 0.50) # min 5% chance, max 50% chance
def simulate_shotsT_minute(shooter, home_team, away_team):
    p = shotsT_prob(shooter, home_team.team_formation, away_team.players, away_team.team_formation)
    return np.random.rand() < p
def goal_prob(shooter, home_formation, away_keeper):
    att = getattr(shooter, SHOTST_WEIGHTS[home_formation][shooter.position]["attr"])
    df = away_keeper.blocking * 0.8 + away_keeper.technique * 0.3
    diff = (att - df) * 0.04 #turning knob
    prob = 1 / (1 + np.exp(-diff))
    fin_prob =  np.clip(prob, 0.03, 0.85) # min
    return fin_prob > np.random.rand()


def calc_team_pow(home_players, home_formation): 
    total = 0
    for player in home_players:
        total += calc_player_pow(player, home_formation)
    return total / 11


# player power for reference #
def calc_player_pow(player, team_formation):
    weights = POSITION_WEIGHTS[team_formation][player.position]
    return sum(
        getattr(player, attr) * weight
        for attr, weight in weights.items() # .items() makes (key, value)
                                            # so attr gets key, weight gets weight
    )








### standard w/out specific positions ###
'''def calc_team_pow(home_players):
    homeVal = 0
    for players in home_players:
        # players have shooting, passing, def, phy, spd, con
        # in the future i can implement things like passing is strong against
        # this value, passing / physical = some val to be part of sum
        if players.position == "GK":
            homeVal += players.passing * 0.01
        else:
            value = (players.passing * 0.5 + players.control * 0.3 + players.physical * 0.25
            + players.speed * 0.75 + players.shooting * 0.1 + players.positioning * 0.5)/2.4
            if players.position == "DF":
                homeVal += value * 0.1
            elif players.position == "MF":
                homeVal += value * 0.5
            else:
                homeVal += value * 0.39

    return homeVal/3.2

def exp_shots(home_players, away_players, home=False):
    ## SHOTS: depend most on fw + mf (39:50:10:1)
    # home: passing(mid:0.5), control (mid-low:0.3), physical (mid-low:0.25)
    #       speed (mid-high:0.75), shoooting (low:0.1)  tot:2
    # away: depend most on df,mf,fw,gk (50:45:4:1) (w/ defense (high:0.9), physical (mid-high: 0.7), 
    #       technique (low:0.1) tot:1.7
    #
    # same -> 10
    # +10 -> 18
    # +5 -> 14
    # -10 -> 2
    # -5 -> 6
    homeVal = 0
    awayVal = 0
    for players in home_players:
        # players have shooting, passing, def, phy, spd, con
        # in the future i can implement things like passing is strong against
        # this value, passing / physical = some val to be part of sum
        if players.position == "GK":
            homeVal += players.passing * 0.01
        else:
            value = (players.passing * 0.5 + players.control * 0.3 + players.physical * 0.25
            + players.speed * 0.75 + players.shooting * 0.1 + players.positioning * 0.5)/2.4
            if players.position == "DF":
                homeVal += value * 0.1
            elif players.position == "MF":
                homeVal += value * 0.5
            else:
                homeVal += value * 0.39
    for players in away_players:
        if players.position == "GK":
            awayVal += players.technique * 0.01
        else:
            value = (players.defense * 0.9 + players.physical * 0.7 
                        + players.positioning *0.5)/2.1
            if players.position == "DF":
                awayVal += value * 0.5
            elif players.position == "MF":
                awayVal += value * 0.45
            else:
                awayVal += value * 0.04
    
    #final calculation based on formula above
    # 3.2 and 3.88 are to be changed from when i get formation class
    finalVal = homeVal/(3.2) - awayVal/(3.88)
    
    if finalVal >= 10:
        return (18 * HOME_ADVANTAGE) if home else 18
    elif finalVal >= 0:
        return finalVal*0.8 + 10 * HOME_ADVANTAGE if home else finalVal * 0.8 + 10
    elif finalVal >= -10:
        return (10 - finalVal*0.8) * HOME_ADVANTAGE if home else 10 - finalVal*0.8
    else:
        return 2

def simulated_shots(exp_shots):
    return np.random.poisson(exp_shots) # where it turns to int

def expected_shotsT(simulated_exp_shots, home_players, away_players, home=False):
    # home: fw, mf (50,40,9,1), shooting (high), positioning (mid), physical (low), passing (low), con (low)
    # away: gk, df, (1, 65, 30, 4), defense (high), physical (midlow)
    # 0 -> 30%
    # 10 -> 50%
    # -10 -> 10%
    homeVal = 0
    awayVal = 0
    for players in home_players:
        if players.position != "GK":
            value = (players.passing * 0.1 + players.control * 0.1 + players.physical * 0.1
                + players.shooting * 0.9 + players.positioning * 0.5)/1.7
            if players.position == "DF":
                homeVal += value * 0.09
            elif players.position == "MF":
                homeVal += value * 0.4
            else:
                homeVal += value * 0.5

    for players in away_players:
        if players.position != "GK":
            value = (players.defense * 0.9 + players.physical * 0.25)
            if players.position == "DF":
                awayVal += value * 0.65
            elif players.position == "MF":
                awayVal += value * 0.3
            else:
                awayVal += value * 0.04
    finalVal = homeVal/2.96 - awayVal/3.88
    if finalVal > 10:
        return simulated_exp_shots * 0.5 * HOME_ADVANTAGE if home else simulated_exp_shots * 0.5
    elif finalVal >= -10:
        return simulated_exp_shots * (30 + finalVal * 2) * HOME_ADVANTAGE if home else simulated_exp_shots * (30 + finalVal * 2)
    else:
        return simulated_exp_shots * 0.1 * HOME_ADVANTAGE if home else simulated_exp_shots * 0.1

def simulated_shotsT(exp_shotsT, simulated_shots):
    sim_shotsT = np.random.poisson(exp_shotsT)
    if sim_shotsT > simulated_shots:
        return simulated_shots
    else:
        return sim_shotsT

    #return np.random.poisson(exp_shotsT) # where it turns to int

def exp_pos_helper(home_players, away_players):
    homeVal = 0
    awayVal = 0
    for players in home_players:
        if players.position == "GK":
            homeVal += (players.passing + players.technique)/2 * 0.1
        else:
            value = (players.control * 0.75 + players.positioning * 0.75 + players.passing * 0.75
            + players.speed * 0.25 + players.physical * 0.5)/3
            if players.position == "DF":
                homeVal += value * 0.4
            elif players.position == "MF":
                homeVal += value * 0.45
            else:
                homeVal += value * 0.05
    for players in away_players:
        if players.position == "GK":
            awayVal += players.technique * 0.00
        else:
            value = (players.speed * 0.75 + players.physical * 0.75
                        + players.positioning *0.75 + players.defense * 0.25)/2.5
            if players.position == "DF":
                awayVal += value * 0.2
            elif players.position == "MF":
                awayVal += value * 0.4
            else:
                awayVal += value * 0.4

    return homeVal/(3.5) - awayVal/(3.2)

def expected_posession(home_players, away_players, home=False):
    #right now, just do as the formula, but later, I want
    #to have it so that it posessession causes higher goals, higher goals 
    # for opponents if they have high speed, higher shots, etc
    # home: depends on control(mid-h), positioning(mid-h), passing(mid-h), physical(mid), speed(mid-l),
    #     gk,df (10,40,45,5)
    # away: speed (mid-high), physical (mid-high), positioning (mid-high), defense (mid-l)
    #     gk, df (0, 20,40,40)
    # dif of 10 -> 90
    # dif of 5 -> 70
    # dif of 0 -> 50
    # home
    fin_val = exp_pos_helper(home_players, away_players) 
    - exp_pos_helper(away_players, home_players)

    if fin_val >= 20:
        return 90
    elif fin_val >= -20:
        return 50 + fin_val * 2 * HOME_ADVANTAGE if home else 50 + fin_val * 4
    else:
        return 10

def simulated_posession(exp_pos):
    val = np.random.poisson(exp_pos)
    if val >=100:
        return 100
    if val <=0:
        return 0
    return np.random.poisson(exp_pos)
 

def exp_goals(home_players,away_GK, shotsT, home=False):
    #
    # GOALS:
    #home: shooting (high) just one (50, 40, 10,0)
    #away: blocking (high) just one (0,0,0,100)
    #
    # 0 dif = 35%
    # 5 dif = 45% goalie lower
    # -5 dif = 25%
    # 12.5 dif or more = 60%
    # -12.5 dif or less = 10%
    homeVal = 0
    for players in home_players:
        # players have shooting, passing, def, phy, spd, con
        if players.position != "GK":
            value = players.shooting
            if players.position == "DF":
                homeVal += value * 0.1
            elif players.position == "MF":
                homeVal += value * 0.4
            else:
                homeVal += value * 0.5
    homeVal = homeVal/2.5
    finalVal = homeVal - away_GK.blocking
    if finalVal <= -12.5: #goalie higher
        return 0.1 * shotsT * HOME_ADVANTAGE if home else 0.4*shotsT
    elif finalVal <= 12.5:
        return 0.35 - 2 * finalVal * HOME_ADVANTAGE * shotsT if home else 0.65 + 2 * finalVal
    else:
        return 0.6 * shotsT * HOME_ADVANTAGE if home else 0.9*shotsT


def simulated_goals(exp_goals, simulated_shotsT):
    if exp_goals <= 0:
        return 0
    sim_goals = np.random.poisson(exp_goals)
    if sim_goals >= simulated_shotsT:
        return simulated_shotsT
    else:
        return sim_goals'''
