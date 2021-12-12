import random as rd
import streamlit as st
teams = """Atlanta Hawks
Boston Celtics
Brooklyn Nets
Charlotte Hornets
Chicago Bulls
Cleveland Cavaliers
Dallas Mavericks
Denver Nuggets
Detroit Pistons
Golden State Warriors
Houston Rockets
Indiana Pacers
Los Angeles Clippers
Los Angeles Lakers
Memphis Grizzlies
Miami Heat
Milwaukee Bucks
New Orleans Pelicans
New York Knicks
Orlando Magic
Philadelphia 76ers
Minnesota Timberwolves
Phoenix Suns
Portland Trail Blazers
Sacramento Kings
San Antonio Spurs
Toronto Raptors
Utah Jazz
Washington Wizards"""


player = """LeBron James
Kevin Durant
Giannis Antetokounmpo
Stephen Curry
Kawhi Leonard
Damian Lillard
Luka Doncic
Nikola Jokic
James Harden
Jimmy Butler
Jayson Tatum
Paul George
Chris Paul
Bam Adebayo
Devin Booker
Kyrie Irving
Russell Westbrook
Nikola Vucevic
Bojan Bogdanovic
Marcus Smart
Josh Richardson
Tyler Herro
Cole Anthony
LaMelo Ball
Lonzo Ball
Seth Curry
Paul Millsap
Chuma Okeke
Kristaps Porzingis"""
@st.cache(suppress_st_warning=True)
def random_picker(cb):
    #cb: choose by (1: team, 0: player)
    if cb == 1:
        n = teams.splitlines()
    if cb == 0:
        n = player.splitlines()
    x = rd.randint(0, len(n) - 1)
    return n[x]
