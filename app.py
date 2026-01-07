import streamlit as st
import pandas as pd
import json
from src.models import Team
from src.season import season
from src.match_sim import calc_team_pow
from src.match_sim import calc_player_pow
from src.match_sim import team_pos_pwr
from src.match_sim import def_team_shotsT_pwr
from src.match_sim import team_shotsT_pwr
#from src.season import run_season_entireWeeks
#from src.season import run_one_week'''
from src.league import LeagueTable
from src.models import Player
from collections import defaultdict


#from models import Team
#from season import run_season'''
#from src.match_sim import simulate_match
#from src.schedule import round_robin'''

with open("data/demo/players.json", encoding="utf-8") as f:
    players_data = json.load(f)


with open("data/demo/team.json") as f:
    team_data = json.load(f)
players = [Player(**p) for p in players_data]

team_players_dict = defaultdict(list)

for player in players:
    team_players_dict[player.team_id].append(player)

teams = []

#team_lookup = {t["id"]: t for t in team_data}
#    teams = []

#for team_id, plist in team_players_dict.items():
#    teams.append(
#        Team(
#            id=team_id,
#            name=team_lookup[team_id]["name"],
#            players=plist
#       )
#    )
#

#to display team information, could be changed to define it when instantiating
for team_id, plist in team_players_dict.items(): # dictionary, so key access, not dot access
    spec_team = Team(id=team_id, name=team_data[team_id - 1]["name"], players = plist)
    spec_team.team_formation = team_data[team_id - 1]["team_formation"]
    for i in range(len(players)):
        players[i].rating = calc_player_pow(players[i], spec_team.team_formation)
    spec_team.team_power = calc_team_pow(plist, spec_team.team_formation)
    spec_team.team_con = team_pos_pwr(spec_team.players, spec_team.team_formation) #possession
    spec_team.team_def = def_team_shotsT_pwr(spec_team.players, spec_team.team_formation) #defense + physical
    spec_team.team_att = team_shotsT_pwr(spec_team.players, spec_team.team_formation) # shooting
    teams.append(spec_team)
    


#teams = [
#    Team("A", 80, 70, 75), # add players so Team(players), 
#    Team("B", 75, 72, 70), # and eventually whole team itself (coach too)
#    Team("C", 82, 65, 78), # then do probability and all based on stats
#    Team("D", 80, 80, 62)
#]

st.title("Soccer League Simulator")

#if st.button("Simulate Season"):
#    table = season.run_season_entireWeeks(teams)
#    df = pd.DataFrame.from_dict(table, orient="index")
#    df = df.sort_values(["pts", "gd", "gf"], ascending=False)
#    st.dataframe(df)
if "show_next" not in st.session_state:
    st.session_state.show_next = False

if "running" not in st.session_state:
    st.session_state.running = False


if st.button("start simulation") and not st.session_state.running:
    st.session_state.show_next = True


if st.session_state.show_next:


    
    # session_state used when previous state needs to be kept, progress keep
    # for this condition, new one is created if its the first time
    if "running" not in st.session_state:
        st.session_state.running = True

    if "season" not in st.session_state:
        st.session_state.season = season(teams)

    if "table" not in st.session_state:
        st.session_state.table = LeagueTable(teams)

    season = st.session_state.season
    if season.week_num != 0:
        st.write(f"### Week {season.week_num}")



    ### running one week
    ### investigate more on this
    #Problem: DataFrame in the condition of button,
    # because run_one_week() does not execute after rerunning
    #if st.session_state.running:
    #    if st.button("Run Week" + str(st.session_state.season.week_num + 1), key="run_week"): #inside so it disappears once it ends
    #        st.session_state.table = season.run_one_week(
    #            st.session_state.table
    #        )
    #    df = pd.DataFrame.from_dict(
    #        st.session_state.table.table, orient="index"
    #    ).sort_values(["pts", "gd", "gf"], ascending=False)
    #    # sort_values to make it a ranking
    #    st.dataframe(df)

    # button
    #if season.week_num < len(season.fixtures_by_week):
    #    if st.button(f"Run Week {season.week_num + 1}", key="run_week"):
    #        st.session_state.table = season.run_one_week(
    #            st.session_state.table
    #

    def run_week():
        season = st.session_state.season
        st.session_state.table = season.run_one_week(
            st.session_state.table
        )

    if "show_lineup" not in st.session_state:
        st.session_state.show_lineup = False

    if st.button("Show Team Lineup"):
        st.session_state.show_lineup = True

    if st.session_state.show_lineup:
        id = 0
        team_names = {team.name: team for team in teams}

        #choosing one team from the list
        selected_name = st.selectbox("Select a team", team_names.keys())
        spec_team = team_names[selected_name]

        st.subheader(spec_team.name)
        st.write("Team formation:", spec_team.team_formation)
        st.write("Team power:", spec_team.team_power)
        st.write("Team attack:", spec_team.team_att)
        st.write("Team control:", spec_team.team_con)
        st.write("Team defense:", spec_team.team_def)
        st.write(spec_team.players)

        

    st.button(
        f"Run Week {st.session_state.season.week_num + 1}",
        on_click=run_week,
        key="run_week"
    )



    # streamlit for showing results of the week
    if st.session_state.season.week_num != 0:
        if st.button("show results for week " + str(st.session_state.season.week_num)):
            result = st.session_state.season.prev_result
            week_idx = st.session_state.season.week_num - 1
            matches = st.session_state.season.fixtures_by_week[week_idx]
            df = pd.DataFrame(
                {
                    "Match": [(m.home_team.name + " vs " +  m.away_team.name) for m in matches],
                    "home": [m.home_goals for m in result],
                    "away": [m.away_goals for m in result],
                    "h shotsT": [m.home_shotsT for m in result],
                    "a shotsT": [m.away_shotsT for m in result],
                    "h shots": [m.home_shots for m in result],
                    "a shots": [m.away_shots for m in result],
                    "h pos": [m.home_possession for m in result],
                    "a pos": [m.away_possession for m in result]
                }
            )
            st.dataframe(df)


    # streamlit for fixture in upcoming week
    if st.session_state.season.week_num < (len(teams) - 1)* 2:
        if st.button("show fixture for week " + str(st.session_state.season.week_num + 1), key="fixture"):
            
            week_idx = st.session_state.season.week_num
            if week_idx < len(teams) * 2:  # len(teams) * 2
                matches = st.session_state.season.fixtures_by_week[week_idx]

                df = pd.DataFrame(
                    {
                        "home": [str(m.home_team.name) for m in matches],
                        "away": [str(m.away_team.name) for m in matches]
                    }
                )
                st.dataframe(df)


    # button for ending simulation
#    if st.button("End Simulation", key="end_sim"):
#       st.session_state.running = False
        # do ending

    # automatically end simulation if all matches are finished in fixtures
    if season.week_num >= len(teams) * 2 - 1:
        st.session_state.running = False
        st.warning("Season complete")
        # need to print final results below

    #reset button
    if st.button("Reset Simulation", key="reset_sim"):
        st.session_state.clear()
        st.rerun()


    # # ALWAYS render table
    df = (
        pd.DataFrame.from_dict(
            st.session_state.table.table, orient="index"
        )
        .sort_values(["pts", "gd", "gf"], ascending=False)
    )
    st.dataframe(df)

# bottom button needed for "soft reset"
#if st.button("Reset Simulation", key="reset_sim"):
#    teams = st.session_state.season.teams
#    st.session_state.season = Season(teams)
#    st.session_state.league = LeagueTable(teams)
#    st.rerun()


# not for streamlit
#if st.button("Simulate Season by weeks"):
#    running = True
#    table = LeagueTable(teams)
#    while running:
#        if st.button("run week" + str(season.week_num), 
#                        key=f"run_week_{season.week_num}"):
#            table = season.run_one_week(teams, table)
#            df = pd.DataFrame.from_dict(table, orient="index")
#            df = df.sort_values(["pts", "gd", "gf"], ascending=False)
#            st.dataframe(df)
#        if st.button("end simulation") or season.week_num >=38:
#            running = False'''''''''
        
