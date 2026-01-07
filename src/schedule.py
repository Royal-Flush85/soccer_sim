from src.models import MatchDay
import numpy as np

'''def round_robin(teams):
    rows, cols = 2*len(teams), len(teams)
    schedule = np.empty((rows, cols), dtype=object)
    for i in range(cols):
        for j in range(rows):
            if i != j:
                if j < len(teams):
                    schedule[j][i] = MatchDay(teams[i], teams[j])
                else:
                    schedule[j][i] = MatchDay(teams[j - cols], teams[i])
            ''schedule.append((teams[i], teams[j]))
            schedule.append((teams[j], teams[i])) ''        
    return schedule #use 2d array'''
'''scheduel of an entire thing, 
scheudle is a flat list, so it does not incorporate weeks'''
def round_robin(teams):
    schedule = []
    for i in range(len(teams)):
        for j in range(len(teams)):
            if i != j:
                schedule.append(MatchDay(teams[i], teams[j]))
    return schedule


''' returns a list of weeks, each week is a list of MatchDay
objects, simple round-robin scheduling ( each team plays once per week)

the passed schedule is list of list (list that has list as each index)
so if there are 20 teams, theres gonna be 10 MatchDay object in each list index

bottom version botsu because first team was always home team
'''
def round_robin_weeks(teams):
    n = len(teams)
    schedule = []

    for week in range(n-1): #(num of each teams matches)
        week_matches = [] #start of list of list
        for i in range(n//2): 
            t1 = teams[i]
            t2 = teams[n - 1 - i]

            if week % 2 == 0:
                home, away = t1, t2
            else:
                home, away = t2, t1
            
            week_matches.append(MatchDay(home, away)) #at the end, week_matches 
                                                      #has all MatchDay obj for week
        # rotate based on circle method, 
        # keep first term, and put last term after that
        # then the rest
        # eventually make randomized fixtures
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]

        schedule.append(week_matches)

    schedule = opposite_side(schedule)
    return schedule

def opposite_side(schedule):
    return_schedule = []

    for week in schedule:
        return_week = []
        for match in week:
            return_week.append(MatchDay(match.away_team, match.home_team))
        return_schedule.append(return_week) # appending return_schedule so
                                            # it wont have infinite loop
    return schedule + return_schedule 

    '''i = 0
    for matchWeek in schedule:
        weekAdd = []
        for match in matchWeek:
            weekAdd.append(MatchDay(matchWeek[i].away_team), matchWeek[i].home_team)
            i = i + 1
        schedule.append(weekAdd)'''

'''def round_robin_weeks(teams):
    num_teams = len(teams)
    ''if num_teams % 2 != 0: #no need to be used
        teams.append(None)''
    n = len(teams)
    schedule = []
    for week in range(n-1): #(num of each teams matches)
        week_matches = [] #start of list of list
        for i in range(n//2): # floor division
            home = teams[i]
            away = teams[n - 1 - i]
            # set match from other side
            if home is not None and away is not None:
                week_matches.append(MatchDay(home, away))
        # rotate based on circle method, 
        # keep first term, and put last term after that
        # then the rest
        # eventually make randomized fixtures
        teams = [teams[0]] + [teams[-1]] + teams[1:-1]
        schedule.append(week_matches)
    return schedule'''

