from src.match_sim import simulate_match
from src.league import LeagueTable
from src.schedule import round_robin
from src.schedule import round_robin_weeks

'''def run_season(teams):
    table = LeagueTable(teams)
    fixtures = round_robin(teams)

    for i in range(len(fixtures)): #num of teams
        for j in range(len(fixtures[0])): # num of weeks
            match = fixtures[j][i]
            result = simulate_match(match.home_team, match.away_team)
            table.update(match.home_team,match.away_team,result)
    ''for home, away in fixtures:
        result = simulate_match(home, away)
        table.update(home, away, result)''

    return table.table'''

class season:
    
    def __init__(self, teams):
        self.teams = teams
        self.week_num = 0
        self.fixtures_by_week = round_robin_weeks(teams)
        self.prev_result = []
    # running the entire season
    # why no self?
    def run_season(teams):
        table = LeagueTable(teams)
        fixtures = round_robin(teams)
        # flat list of all matches from teams var (passed from app.py)
        # fixtures[0] refers to MatchDay(Team A, Team B)

        for match in fixtures: # each match object in fixtures, 
                               # flat list, goes through each one
            result = simulate_match(match.home_team, match.away_team)
            #simualtes
            table.update(match.home_team, match.away_team, result)
            # updates according to simulated match result, and the scores
            # of the teams

        return table.table

    '''prints out each week output, but does entire season'''
    def run_season_entireWeeks(teams):
        table = LeagueTable(teams)
        fixtures_by_week = round_robin_weeks(teams)

        for week_num, week in enumerate(fixtures_by_week, start=1):
            # enumerate gives the index, and the item in each thing
            # that item refering to each week's match list
            print(f"Week {week_num}")
            for match in week:
                result = simulate_match(match.home_team.players, match.away_team.players)
                table.update(match.home_team, match.away_team, result)
            print(table.table)  # optional: print league table after each week

        return table.table


    def run_one_week(self, table):
        if self.week_num >= len(self.fixtures_by_week):
            return table  # or raise StopIteration

        week = self.fixtures_by_week[self.week_num]
        tot_match_one_week = []
        for match in week:
            result = simulate_match(match.home_team, match.away_team)
            table.update(match.home_team, match.away_team, result)
            tot_match_one_week.append(result)
            #self.prev_result.append(result) #storing MatchResult objs
            # ^above for keeping entire fixtures
        self.prev_result = tot_match_one_week #replacement, one week of match (reset)
        self.week_num += 1
        return table

        
