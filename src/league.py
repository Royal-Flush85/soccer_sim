class LeagueTable:
    #create variable
    week_num = 0

    def addweek(self):
        week_num = week_num + 1

    # teams will have to have all the teams
    def __init__(self, teams):
        self.table = {
            #below, it is like dictionary for team.name, maybe look into 
            # how to create better visual output
            team.name: {
                "pts": 0,
                "gd": 0,
                "gf": 0,
                "ga": 0,
                "W": 0,
                "T": 0,
                "L": 0
            } for team in teams
        }
    
    def update(self, home, away, result):
        t1 = self.table[home.name]
        t2 = self.table[away.name]

        t1["gf"] += result.home_goals
        t1["ga"] += result.away_goals
        t2["gf"] += result.away_goals
        t2["ga"] += result.home_goals

        t1["gd"] = t1["gf"] - t1["ga"]
        t2["gd"] = t2["gf"] - t2["ga"]

        if result.home_goals > result.away_goals:
            t1["pts"] += 3
            t1["W"] += 1
            t2["L"] += 1
        elif result.home_goals < result.away_goals:
            t2["pts"] += 3
            t2["W"] += 1
            t1["L"] += 1
        else: 
            t1["pts"] += 1
            t2["pts"] += 1
            t1["T"] += 1
            t2["T"] += 1


