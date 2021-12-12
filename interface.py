import streamlit as st
import matplotlib.pyplot as mplt
from random_tp import *
from data import *
import pandas as pd
import datetime as dt


t = dt.datetime.now().year
bd = st.container()
sb = st.container()
option = ["Statistic summary", "Glossary"]
navi = st.sidebar.selectbox("web functions:", option)
if navi == option[0]:
    with sb:
        met = ["Team", "Player"]
        m_opt = st.sidebar.radio("Summary by", met)
        if m_opt == met[0]:
            method = st.sidebar.radio("how to choose team", ["Random", "Manual input"])
            if method == "Random":
                name = random_picker(1)
                
            else:
                name = st.sidebar.text_input("enter team name:")
                
            
            
            t_opt = {"Roster": 0,   "Per Game": 1, "Advance": 5}
            wt = st.sidebar.radio("Which information about the team do you want to see?", t_opt.keys())
            season = st.sidebar.selectbox("choose season:", range(t+1, 2019, -1))
            if name:
                url = fix_linkt(name, season)
                img = get_image(url)
                try:
                    df = load_data(url, t_opt[wt])
                except:
                    t_opt = {"Roster": 0,   "Per Game": 1, "Advance": 3}
                    df = load_data(url, t_opt[wt])
                
                df = df.dropna(axis = 0, how = "all")
                df = df.dropna(axis = 1, how = "all")
                if wt == "Roster":
                    df = df.rename(columns = {"Unnamed: 6": "Nationality"})
                    conv_h = st.sidebar.radio("view height by:", ["feet", "meters"])
                    conv_w = st.sidebar.radio("view weight by:", ["pounds", "kilograms"])
                    if conv_h == "meters":
                        df["Ht"] = df["Ht"].apply(feet_to_meters)
                    if conv_w == "kilograms":
                        df["Wt"] = df["Wt"].apply(pound_to_kg)
                        
                if wt == "Per Game" or wt == "Advance":
                    df = df.rename(columns = {"Unnamed: 1": "Player"})
                    fil_r = st.sidebar.multiselect("Filter by players:", df["Player"], default= df["Player"])
                    df = df[df["Player"].notna()]
                    df = df[df.Player.isin(fil_r)]
                    vis = st.sidebar.radio("Visualize by:", df.columns[2:])
                    with bd:
                        st.header(f"Showing {wt} statistic of {season - 1} - {season} season")
                        st.image(img)
                        st.dataframe(df)
                        st.download_button("download this table", df.to_csv())
                        df = df.sort_values(vis)
                        mplt.bar(df["Player"], df[vis])
                        mplt.xticks(rotation=90)
                        gr_s = mplt.show()
                        st.pyplot(gr_s)
                        st.header(f"Summary of {vis}")
                        stat_summary(df, by = vis, name = "Player")
                else:
                    st.header(f"Showing {wt} of {name} in {season - 1} - {season} season")
                    st.image(img)
                    st.dataframe(df)
                    st.download_button("download this table", df.to_csv())
                
    if m_opt == met[1]:
        method = st.sidebar.radio("how to choose Player", ["Random", "Manual input"])
        if method == "Random":
            name = random_picker(0)
        else:
            name = st.sidebar.text_input("enter player name:")
        if name:
                
            url = fix_linkp(name)
            img = get_image(url)
            try:
                if len(pd.read_html(url, header = 0)) >= 6:
                    p_opt = {"Per Game (regular season)": 0, "Per Game (Playoff)": 1, "Total (regular season)": 2, "Total (Playoff)": 3, "Advance (regular seasons)": 4, "Advance(Playoff)": 5}
                else:
                    p_opt = {"Per Game (regular season)": 0, "Total (regular season)": 1, "Advance (regular seasons)": 2}
            except:
                st.error("This data is not available, please enter another name")
            
            wt = st.sidebar.radio("Which information about the team do you want to see?", p_opt.keys())
            df = load_data(url, p_opt[wt])
            df = df.dropna(axis = 0, how = "all")
            df = df.dropna(axis = 1, how = "all")
            df = df.loc[:, (df != 0).any(axis=0)]
            vis = st.sidebar.multiselect("Data to visualise", df.columns[5:])
            apply = st.sidebar.button("Apply")
            with bd:
                st.header(f"Showing{wt} of {name}")
                st.image(img)
                st.dataframe(df)
                st.download_button("download this table", df.to_csv())
                if apply:
                    dr = df.index[df["Season"] == "Career"].tolist()
                    df = df.drop(df.tail(len(df)-dr[0]).index)
                    
                    if "Total" in wt:
                        df = clean_player_data_total(df)
                    elif "Per Game" in wt:
                        df = clean_player_data_pergame(df)
                    for i in vis:
                        mplt.plot(df["Season"], df[i], marker = ".")
                        
                        if len(df) > 2:
                            st.header(f"Summary of {i}")
                            stat_summary(df, i, "Season")
                        mplt.legend(labels = vis)
                        mplt.xticks(rotation = 90)
                    gr = mplt.show()
                    st.pyplot(gr)
            
else:
    st.write("""2P - 2-Point Field Goals

2P% - 2-Point Field Goal Percentage; the formula is 2P / 2PA.

2PA - 2-Point Field Goal Attempts

3P - 3-Point Field Goals (available since the 1979-80 season in the NBA)

3P% - 3-Point Field Goal Percentage (available since the 1979-80 season in the NBA); the formula is 3P / 3PA.

3PA - 3-Point Field Goal Attempts (available since the 1979-80 season in the NBA)

Age - Age; player age on February 1 of the given season.

AST - Assists

AST% - Assist Percentage (available since the 1964-65 season in the NBA); the formula is 100 * AST / (((MP / (Tm MP / 5)) * Tm FG) - FG). Assist percentage is an estimate of the percentage of teammate field goals a player assisted while he was on the floor.

Award Share - The formula is (award points) / (maximum number of award points). For example, in the 2002-03 MVP voting Tim Duncan had 962 points out of a possible 1190. His MVP award share is 962 / 1190 = 0.81.

BLK - Blocks (available since the 1973-74 season in the NBA)

BLK% - Block Percentage (available since the 1973-74 season in the NBA); the formula is 100 * (BLK * (Tm MP / 5)) / (MP * (Opp FGA - Opp 3PA)). Block percentage is an estimate of the percentage of opponent two-point field goal attempts blocked by the player while he was on the floor.

BPM - Box Plus/Minus (available since the 1973-74 season in the NBA); a box score estimate of the points per 100 possessions that a player contributed above a league-average player, translated to an average team. Please see the article About Box Plus/Minus (BPM) for more information.

DPOY - Defensive Player of the Year

DRB - Defensive Rebounds (available since the 1973-74 season in the NBA)

DRB% - Defensive Rebound Percentage (available since the 1970-71 season in the NBA); the formula is 100 * (DRB * (Tm MP / 5)) / (MP * (Tm DRB + Opp ORB)). Defensive rebound percentage is an estimate of the percentage of available defensive rebounds a player grabbed while he was on the floor.

DRtg - Defensive Rating (available since the 1973-74 season in the NBA); for players and teams it is points allowed per 100 posessions. This rating was developed by Dean Oliver, author of Basketball on Paper. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.

DWS - Defensive Win Shares; please see the article Calculating Win Shares for more information.

eFG% - Effective Field Goal Percentage; the formula is (FG + 0.5 * 3P) / FGA. This statistic adjusts for the fact that a 3-point field goal is worth one more point than a 2-point field goal. For example, suppose Player A goes 4 for 10 with 2 threes, while Player B goes 5 for 10 with 0 threes. Each player would have 10 points from field goals, and thus would have the same effective field goal percentage (50%).

FG - Field Goals (includes both 2-point field goals and 3-point field goals)

FG% - Field Goal Percentage; the formula is FG / FGA.

FGA - Field Goal Attempts (includes both 2-point field goal attempts and 3-point field goal attempts)

FT - Free Throws

FT% - Free Throw Percentage; the formula is FT / FTA.

FTA - Free Throw Attempts"

Four Factors - Dean Oliver's "Four Factors of Basketball Success"; please see the article Four Factors for more information.

G - Games
GS - Games Started (available since the 1982 season)
TL - Steals (available since the 1973-74 season in the NBA)

STL% - Steal Percentage (available since the 1973-74 season in the NBA); the formula is 100 * (STL * (Tm MP / 5)) / (MP * Opp Poss). Steal Percentage is an estimate of the percentage of opponent possessions that end with a steal by the player while he was on the floor.

Stops - Stops; Dean Oliver's measure of individual defensive stops. Please see the article Calculating Individual Offensive and Defensive Ratings for more information.

Tm - Team

TOV - Turnovers (available since the 1977-78 season in the NBA)

TOV% - Turnover Percentage (available since the 1977-78 season in the NBA); the formula is 100 * TOV / (FGA + 0.44 * FTA + TOV). Turnover percentage is an estimate of turnovers per 100 plays.

TRB - Total Rebounds (available since the 1950-51 season)

TRB% - Total Rebound Percentage (available since the 1970-71 season in the NBA); the formula is 100 * (TRB * (Tm MP / 5)) / (MP * (Tm TRB + Opp TRB)). Total rebound percentage is an estimate of the percentage of available rebounds a player grabbed while he was on the floor.
PER - Player Efficiency Rating (available since the 1951-52 season); PER is a rating developed by ESPN.com columnist John Hollinger. In John's words, "The PER sums up all a player's positive accomplishments, subtracts the negative accomplishments, and returns a per-minute rating of a player's performance." Please see the article Calculating PER for more information.
Poss - Possessions (available since the 1973-74 season in the NBA); the formula for teams is 0.5 * ((Tm FGA + 0.4 * Tm FTA - 1.07 * (Tm ORB / (Tm ORB + Opp DRB)) * (Tm FGA - Tm FG) + Tm TOV) + (Opp FGA + 0.4 * Opp FTA - 1.07 * (Opp ORB / (Opp ORB + Tm DRB)) * (Opp FGA - Opp FG) + Opp TOV)). This formula estimates possessions based on both the team's statistics and their opponent's statistics, then averages them to provide a more stable estimate. Please see the article Calculating Individual Offensive and Defensive Ratings for more informatio
PTS - Points
""")
                       
st.set_option('deprecation.showPyplotGlobalUse', False)