from src.match_sim import simulate_match
from src.match_sim import simulate_match_2
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
    
    class PlayerGoal:
        def __init__(self, player):
            self.player_name = player.name
            self.player_id = player.id
            self.goals = 0

        def add_goal(self):
            self.goals += 1

    def __init__(self, teams):
        self.teams = teams
        self.week_num = 0
        self.fixtures_by_week = round_robin_weeks(teams)
        self.prev_result = []#普通の結果
        self.player_Goals = {}
        for team in teams:
            for player in team.players:
                self.player_Goals[player.id] = (self.PlayerGoal(player))


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
    def run_season_entireWeeks(self, table):
        for week in range(len(self.fixtures_by_week)):
            actual_week = week + self.week_num
            if actual_week < len(self.fixtures_by_week):
                week_fixtures = self.fixtures_by_week[actual_week]
                tot_match_one_week = []

                for match in week_fixtures:
                    result = simulate_match(match.home_team, match.away_team)
                    table.update(match.home_team, match.away_team, result)
                    tot_match_one_week.append(result)
                    

                self.prev_result = tot_match_one_week
            else:
                self.week_num = actual_week
                break
        return table

    def run_season_entireWeeks_player(self, table):
        for week in range(len(self.fixtures_by_week)):
            actual_week = week + self.week_num
            if actual_week < len(self.fixtures_by_week):
                week_fixtures = self.fixtures_by_week[actual_week]
                tot_match_one_week = []

                for match in week_fixtures:
                    result = simulate_match_2(match.home_team, match.away_team)
                    table.update(match.home_team, match.away_team, result)
                    tot_match_one_week.append(result)
                    self.track_player_goals(result)

                self.prev_result = tot_match_one_week
            else:
                self.week_num = actual_week
                break
        return table


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

    def track_player_goals(self, result):
        for event in result.home_tot_events:
            if len(event) != 0 and event[0].goal:
                self.player_Goals[event[0].shooter.id].add_goal()

        for event in result.away_tot_events:
            if len(event) != 0 and event[0].goal:
                self.player_Goals[event[0].shooter.id].add_goal()

    def run_one_week_player(self, table):
        if self.week_num >= len(self.fixtures_by_week):
            return table  # or raise StopIteration

        week = self.fixtures_by_week[self.week_num]
        tot_match_one_week = []
        for match in week:
            result = simulate_match_2(match.home_team, match.away_team) # returns MatchResult2 object
            table.update(match.home_team, match.away_team, result)
            tot_match_one_week.append(result)
            self.track_player_goals(result)
            #self.prev_result.append(result) #storing MatchResult objs
            # ^above for keeping entire fixtures
        self.prev_result = tot_match_one_week #replacement, one week of match (reset)
        self.week_num += 1
        return table
    




        
