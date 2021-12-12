import streamlit as st
import pandas as pd
import requests as req
import random as rd
from bs4 import BeautifulSoup

# web scraping
def getdata(url):
    # turn content of a web to text
    r = req.get(url)
    return r.text
def load_data(url, wt):
    # return dataframe in a web
    # url: link
    # wt: which table
    html = pd.read_html(url, header = 0)
    df = html[wt]
    return pd.DataFrame(df)
def get_image(url):
    # return link of an image
    # url : link
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser') 
    image = soup.find_all('img')[1]
    return image['src']
# team names:
def fix_team(name):
    # return abbreviation for team name
    # name (str): team name or abbreviation of team name
    n = name.split()
    if len(name) == 3:
        return name.upper()
    elif name.lower() == "brooklyn nets":
        return "BRK"
    elif name.lower() == "charlotte hornets":
        return "CHO"
    elif len(n) > 2:
        res = ""
        for i in n:
            res += i[0]
        return res.upper()
    else:
        res = name[0:3]
        return res.upper()
def fix_linkt(team, season):
    # use abbreviation of team name to access data from basketball reference
    # team (str): team name
    # season (str): season
    team = fix_team(team)
    return f"https://www.basketball-reference.com/teams/{team}/{season}.html"
# player names:
def fix_player(name):
    # turn player name to code used in the web's link
    # name (str): player name (has to be full name)
    n = name.split()
    if len(n) >= 2:
        n = [n[0], n[-1]]
    if len(n[1]) > 5:
        res = n[1][0:5] + n[0][0:2] + "01"
    else:
        res = n[1] + n[0][0:2] + "01"
    return res.lower()
def fix_linkp(player):
    # use fixed player name to get link to player's data
    pl = fix_player(player)
    return f"https://www.basketball-reference.com/players/{pl[0]}/{pl}.html"
    
#calculation
def feet_to_meters(x):
    #convert height in feet in the form (feet - inch) to meters
    # x (str): feet
    l = x.split("-")
    return round(float(l[0])/3.281 + float(l[1])/39.37,2)
def pound_to_kg(x):
    #convert pounds to kg
    return round(x/2.205,2)
def stat_summary(df, by, name):
    #descriptive statistics to a dataframe
    # df: dataframe
    # by: column name to summary by
    # name: column name ("Season", or "Player")
    st.write(f"mean: {round(df[by].mean(), 3)}")
    st.write(f"median: {df[by].median()}")
    st.write(f"kurtosis: {df[by].kurtosis().round(3)}")
    st.write(f"skewness: {df[by].skew().round(3)}")
    st.write(f"variance: {round(df[by].var(),3)}")
    st.write(f"standard deviation: {round(df[by].std(), 3)}")
    st.write(f"min: {df[by].min()}", f"{name}: {list(df[df[by] == df[by].min()][name])}")
    st.write(f"max: {df[by].max()}", f"{name}: {list(df[df[by] == df[by].max()][name])}")
          
# clean data for visualizing
def clean_player_data_pergame(df):
    # clean data of a player in pergame section to avoid error in visualizing
    # for countable columns return sum of columns of same lable
    # for ratio columns return mean of columns of the same lable
    # df: dataframe
    df[df["Tm"].str.contains("Did Not Play")==False]
    c = df.groupby("Season")
    for i in c.groups:
        if len(i) > 1:
            d = c.get_group(i)
            d["G"] = d["G"].sum()
            d["GS"] = d["GS"].sum()
            d[d.columns[7:]] = d[d.columns[7:]].mean().round(3)
            df[df["Season"] == i] = d
def clean_player_data_total(df):
    # clean data of a player in pergame section to avoid error in visualizing
    # for countable columns return sum of columns of same lable
    # for ratio columns return mean of columns of the same lable
    # df: dataframe
    
    df[df["Tm"].str.contains("Did Not Play")==False]
    
    c = df.groupby("Season")
    for i in c.groups:
        if len(i) > 1:
            
            d = c.get_group(i)
            for j in d[d.columns[5:]]:
                if "%" in j:
                    d[j] = d[j].mean()
                else:
                    d[j] = d[j].sum()
        df[df["Season"] == i] = d