import streamlit as st
import pandas as pd
import json
from src.models import Team
from src.season import season
from src.match_sim import calc_team_pow
from src.match_sim import calc_player_pow
from src.match_sim import team_pos_pwr
from src.match_sim import def_team_shotsT_pwr
from src.match_sim import def_team_shots_pwr
from src.match_sim import team_shots_pwr
from src.match_sim import team_shotsT_pwr 
# from src.season import run_season_entireWeeks
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
    for player in plist:
        player.rating = calc_player_pow(player, spec_team.team_formation)
    spec_team.team_power = calc_team_pow(plist, spec_team.team_formation)
    spec_team.team_con = team_pos_pwr(spec_team.players, spec_team.team_formation) #possession
    spec_team.team_def = (def_team_shotsT_pwr(spec_team.players, spec_team.team_formation) +
        def_team_shots_pwr(spec_team.players, spec_team.team_formation))/ 200 #defense + physical
    spec_team.team_att = (team_shots_pwr(spec_team.players, spec_team.team_formation) +
        team_shotsT_pwr(spec_team.players, spec_team.team_formation))/ 200 # shooting
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
    #    if st.button("Run Week" + str(st.session_state.season.week_num + 1), key="run_week"): 
    # #inside so it disappears once it ends
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
        st.session_state.timeline = False
    def run_week_player():
        season = st.session_state.season
        st.session_state.table = season.run_one_week_player(st.session_state.table)
    def run_week_and_show_timeline():
        run_week_player()
        st.session_state.timeline = True

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

    if "run season" not in st.session_state:
        st.session_state.run_season = False
        
    if st.button("Simulate Entire Season"):
        st.session_state.run_season = True
    if st.session_state.run_season:
        table = season.run_season_entireWeeks(st.session_state.table)
        # df = pd.DataFrame.from_dict(table.table, orient="index")
        # df = df.sort_values(["pts", "gd", "gf"], ascending=False)
        # st.dataframe(df)
        st.session_state.run_season = False
    
    if "run season2" not in st.session_state:
        st.session_state.run_season2 = False
        
    if st.button("Simulate Entire Season (player)") and season.week_num <= 37:
        st.session_state.run_season2 = True
    if st.session_state.run_season2:
        table = season.run_season_entireWeeks_player(st.session_state.table)
        # df = pd.DataFrame.from_dict(table.table, orient="index")
        # df = df.sort_values(["pts", "gd", "gf"], ascending=False)
        # st.dataframe(df)
        st.session_state.run_season2 = False
        
    if "show_rating" not in st.session_state:
        st.session_state.show_rating = False
    if st.button("show team rating ranking"):
        st.session_state.show_rating = True

    if st.session_state.show_rating:
        table1 = {
            "team": [team.name for team in teams],
            "power": [team.team_power for team in teams],
            "att": [team.team_att for team in teams],
            "con": [team.team_con for team in teams],
            "def": [team.team_def / 2 for team in teams],
            "total": [team.team_power + team.team_att + team.team_con + (team.team_def/2) for team in teams]
        }
        df = pd.DataFrame(table1)
        print("Columns in df:", df.columns)
        
        # Sort by power and att
        df = df.sort_values(["total", "power", "att"], ascending=False)
        
        # Show in Streamlit
        st.dataframe(df)
        

    st.button(
        f"Run Week {st.session_state.season.week_num + 1}",
        on_click=run_week,
        key="run_week"
    )
    
    if "timeline" not in st.session_state:
        st.session_state.timeline = False
    st.button(
        f"Run Week {st.session_state.season.week_num + 1} (player)",
        on_click=run_week_and_show_timeline,
        key="run_week_player",
    )
    

    if "show_week_results" not in st.session_state:
        st.session_state.show_week_results = False


    # streamlit for showing results of the week
    if st.session_state.season.week_num != 0:
        # if st.button("show results for week " + str(st.session_state.season.week_num)):
        #     result = st.session_state.season.prev_result
        #     week_idx = st.session_state.season.week_num - 1
        #     matches = st.session_state.season.fixtures_by_week[week_idx]
        #     df = pd.DataFrame(
        #         {
        #             "Match": [(m.home_team.name + " vs " +  m.away_team.name) for m in matches],
        #             "home": [m.home_goals for m in result],
        #             "away": [m.away_goals for m in result],
        #             "h shotsT": [m.home_shotsT for m in result],
        #             "a shotsT": [m.away_shotsT for m in result],
        #             "h shots": [m.home_shots for m in result],
        #             "a shots": [m.away_shots for m in result],
        #             "h pos": [m.home_possession for m in result],
        #             "a pos": [m.away_possession for m in result],
        #             "h exp pos": [m.exp_home_possession for m in result],
        #             "h exp shots": [m.exp_home_shots for m in result],
        #             "a exp shots": [m.exp_away_shots for m in result],
        #         }
        #     )
        #     st.dataframe(df)
        if st.button("show results for week " + str(st.session_state.season.week_num)):
            st.session_state.show_week_results = True
        if st.session_state.show_week_results:
            # ---- 1. Get data for this week ----
            week_idx = st.session_state.season.week_num - 1
            matches = st.session_state.season.fixtures_by_week[week_idx]
            results = st.session_state.season.prev_result
            

            match_labels = [
                f"{m.home_team.name} vs {m.away_team.name}"
                for m in matches
            ]

            # ---- 2. Build overview table ----
            df = pd.DataFrame({
                "Match": match_labels,
                "Home": [m.home_goals for m in results],
                "Away": [m.away_goals for m in results],
                "Home Shots": [m.home_shots for m in results],
                "Away Shots": [m.away_shots for m in results],
                "Home ShotsT": [m.home_shotsT for m in results],
                "Away ShotsT": [m.away_shotsT for m in results],
                "Home pos": [m.home_possession for m in results],
                "Away pos": [m.away_possession for m in results]
            })

            st.subheader("Week Results")
            st.dataframe(df, use_container_width=True)

            # ---- 4. Show selected match details ----
            if (st.session_state.timeline):
                
                # ---- 3. Match selector ----
                selected_idx = st.selectbox(
                    "Select a match to view details",
                    options=list(range(len(results))),
                    format_func=lambda i: match_labels[i],
                    key="selected_match"
                )
                m = results[selected_idx]
                match = matches[selected_idx]
                st.divider()
                st.subheader(f"{match.home_team.name} vs {match.away_team.name}")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Home Goals", m.home_goals)
                    st.metric("Home Shots", m.home_shots)
                    st.metric("Home Shots on Target", m.home_shotsT)
                    st.metric("Home Possession", f"{m.home_possession:.1f}%")

                with col2:
                    st.metric("Away Goals", m.away_goals)
                    st.metric("Away Shots", m.away_shots)
                    st.metric("Away Shots on Target", m.away_shotsT)
                    st.metric("Away Possession", f"{m.away_possession:.1f}%")
                
                if st.session_state.timeline:
                    st.subheader("Goal Timeline")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### Home")
                        goals = [e[0] for e in m.home_tot_events if len(e) != 0 and e[0].goal] # change when every minute could have 2+ events
                        if goals:
                            for e in goals:
                                st.markdown(f"⚽ **{e.shooter.name}** — {e.minute}'")
                        else:
                            st.caption("No goals")

                    with col2:
                        st.markdown("### Away")
                        goals = [e[0] for e in m.away_tot_events if len(e) != 0 and e[0].goal] # change when every minute could have 2+ events
                        if goals:
                            for e in goals:
                                st.markdown(f"⚽ **{e.shooter.name}** — {e.minute}'")
                        else:
                            st.caption("No goals")






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


    # # always render table
    df = (
        pd.DataFrame.from_dict(
            st.session_state.table.table, orient="index"
        )
        .sort_values(["pts", "gd", "gf"], ascending=False)
    )
    st.dataframe(df)

    team_options = {
        team.name: team.id
        for team in season.teams
    }
    selected_team_name = st.selectbox(
        "Select a team",
        team_options.keys(),
        key="team_select_goals"
    )
    selected_team_id = team_options[selected_team_name]
    team_players = next(
        team.players for team in season.teams if team.id == selected_team_id
    )
    data = []
    for player in team_players:
        pg = season.player_Goals.get(player.id)
        if pg:
            data.append({
                "Player": pg.player_name,
                "Goals": pg.goals
            })
    df = pd.DataFrame(data).sort_values(
        "Goals", ascending=False
    ).reset_index(drop=True)
    st.dataframe(df, use_container_width=True)
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
        
