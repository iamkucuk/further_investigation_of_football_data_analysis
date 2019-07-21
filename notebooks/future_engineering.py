#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'notebooks'))
	print(os.getcwd())
except:
	pass

#%%
import sqlite3
import pandas as pd
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
from datetime import datetime

#%%
with sqlite3.connect('../data/database.sqlite') as con:
    countries = pd.read_sql_query("SELECT * from Country", con)
    matches = pd.read_sql_query("SELECT * from Match", con)
    leagues = pd.read_sql_query("SELECT * from League", con)
    teams = pd.read_sql_query("SELECT * from Team", con)
    player = pd.read_sql_query("SELECT * from Player",con)
    player_attributes = pd.read_sql_query("SELECT * from Player_Attributes",con)
    sequence = pd.read_sql_query("SELECT * from sqlite_sequence",con)
    team_attributes = pd.read_sql_query("SELECT * from Team_Attributes",con)


#%%
df = pd.read_csv("../data.csv")
teams = df[["league_id", "country", "league", "home_team_api_id", "home_team_lname"]]
teams = teams.drop_duplicates().reset_index().drop("index", axis=1)


#%%
teams_with_api = pd.merge(teams,
                team_attributes,
                how="left",
                left_on="home_team_api_id",
                right_on="team_api_id")
teams_with_api = teams_with_api[["league_id", "country", "league", "team_api_id", "team_fifa_api_id", "home_team_lname"]]
teams = teams_with_api.drop_duplicates().reset_index().drop("index", axis=1)


#%%
teams.dropna(inplace=True)
teams = teams.drop_duplicates().reset_index().drop("index", axis=1)


#%%
df = pd.read_json("../sofifa.jl", lines=True)


#%%
expanded_df = pd.DataFrame(columns=["Date", "ID","OVA","ATT","MID","DEF","Transfer Budget",
                                    "Speed","Dribbling","BuildPassing","BuildPositioning",
                                    "Crossing","ChancePassing","Shooting","ChancePositioning",
                                    "Aggression","Pressure","Team Width","Defender Line",
                                    "DP","IP","SAA","TAA"])
expanded_df["Date"] = df.agg(lambda x:x[3], axis=1)
expanded_df["ID"] = pd.to_numeric(df.agg(lambda x:x[0][0], axis=1))
expanded_df["OVA"] = pd.to_numeric(df.agg(lambda x:x[0][1], axis=1))
expanded_df["ATT"] = pd.to_numeric(df.agg(lambda x:x[0][2], axis=1))
expanded_df["MID"] = pd.to_numeric(df.agg(lambda x:x[0][3], axis=1))
expanded_df["DEF"] = pd.to_numeric(df.agg(lambda x:x[0][4], axis=1))
expanded_df["Transfer Budget"] = df.agg(lambda x:x[0][5], axis=1)
expanded_df["Speed"] = df.agg(lambda x:x[1][0], axis=1)
expanded_df["Dribbling"] = df.agg(lambda x:x[1][0], axis=1)
expanded_df["BuildPassing"] = df.agg(lambda x:x[1][0], axis=1)
expanded_df["BuildPositioning"] = df.agg(lambda x:x[1][0], axis=1)
expanded_df["Crossing"] = df.agg(lambda x:x[2][0], axis=1)
expanded_df["ChancePassing"] = df.agg(lambda x:x[2][0], axis=1)
expanded_df["Shooting"] = df.agg(lambda x:x[2][0], axis=1)
expanded_df["ChancePositioning"] = df.agg(lambda x:x[2][0], axis=1)
expanded_df["Aggression"] = df.agg(lambda x:x[4][0], axis=1)
expanded_df["Pressure"] = df.agg(lambda x:x[4][1], axis=1)
expanded_df["Team Width"] = df.agg(lambda x:x[4][2], axis=1)
expanded_df["Defender Line"] = df.agg(lambda x:x[4][3], axis=1)
expanded_df["DP"] = pd.to_numeric(df.agg(lambda x:x[5][0], axis=1))
expanded_df["IP"] = pd.to_numeric(df.agg(lambda x:x[5][1], axis=1))
expanded_df["SAA"] = pd.to_numeric(df.agg(lambda x:x[5][2], axis=1))
expanded_df["TAA"] = pd.to_numeric(df.agg(lambda x:x[5][3], axis=1))


#%%
teams_complete = pd.merge(teams, expanded_df, how="outer", left_on="team_fifa_api_id", right_on="ID")


#%%
teams_complete.dropna(inplace=True)


#%%
teams_complete = teams_complete[["Date", "ID","team_api_id", "home_team_lname", "league_id", "league",
                                "OVA","ATT","MID","DEF","Transfer Budget",
                                "Speed","Dribbling","BuildPassing","BuildPositioning",
                                "Crossing","ChancePassing","Shooting","ChancePositioning",
                                "Aggression","Pressure","Team Width","Defender Line",
                                "DP","IP","SAA","TAA"]]


#%%
#teams_complete.to_csv("../team_data.csv", index=False)
#

#%%
teams_complete = pd.read_csv("../team_data.csv")
teams_complete = teams_complete.rename(columns = {"Date" : "date"})
#%%
match_goal_statistics = pd.read_csv("../data/match_goal_statistics.csv")

#%%
teams_complete.sort_values("date",
                        inplace = True)
match_goal_statistics.sort_values("date",
                        inplace = True)

#%%
teams_complete["date"] = teams_complete.agg(
            lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), axis = 1)

#%%
match_goal_statistics["date"] = match_goal_statistics.agg(
            lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M:%S"), axis = 1)
dates = list(teams_complete["date"].unique())
#grouped_matches = match_goal_statistics.groupby("date")

#%%
# For home team
df = pd.DataFrame()
for i in range(len(dates) - 1):
    df = df.append(pd.merge(
        match_goal_statistics.loc[(match_goal_statistics["date"] > dates[i])
                                & (match_goal_statistics["date"] < dates[i + 1])],
        teams_complete.loc[teams_complete["date"] == dates[i]], how = "left",
        left_on="home_team_api_id", right_on="team_api_id",
        suffixes=("", "_home")
        )
    )
df = df.append(pd.merge(
        match_goal_statistics.loc[(match_goal_statistics["date"] > dates[-1])],
        teams_complete.loc[teams_complete["date"] == dates[i]], how = "left",
        left_on="home_team_api_id", right_on="team_api_id",
        suffixes=("", "_home")
    )
)

#%%
# For away team
merged_df = pd.DataFrame()
for i in range(len(dates) - 1):
    merged_df = merged_df.append(pd.merge(
        df.loc[(df["date"] > dates[i])
                                & (df["date"] < dates[i + 1])],
        teams_complete.loc[teams_complete["date"] == dates[i]], how = "left",
        left_on="away_team_api_id", right_on="team_api_id",
        suffixes=("", "_away")
        )
    )
merged_df = merged_df.append(pd.merge(
        df.loc[(df["date"] > dates[-1])],
        teams_complete.loc[teams_complete["date"] == dates[i]], how = "left",
        left_on="away_team_api_id", right_on="team_api_id",
        suffixes=("", "_away")
    )
)

#%%
merged_df.to_csv("../match_data.csv", index=False)
#%%
dropped_df = merged_df.dropna()

#%%
df = pd.read_json("../sofifa/output.jl", lines=True)

#%%
