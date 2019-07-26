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
#import pandas as pd


#%%
# ##Beggining of the new dataset
# Please proceed from here

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
fifatable_df = pd.read_csv("fifatable.csv")
match_df = pd.read_json("../matchresults.jl", lines=True)
match_df = match_df[match_df["season"] != 2019]
#%%
fifa_df = pd.read_json("../sofifa.jl", lines=True)
table_df = pd.read_json("../worldfootball.jl", lines=True)
match_df = pd.read_json("../matchresults.jl", lines=True)
#%%
match_df = match_df[(match_df["season"] < 2019) & (match_df["season"] > 2006)]
table_df = table_df[(table_df["season"] < 2019) & (table_df["season"] > 2006)]
#%%
expanded_fifa_df = pd.DataFrame(columns=["Date","Team Name", "ID","OVA","ATT","MID","DEF","Transfer Budget",
                                    "Speed","Dribbling","BuildPassing","BuildPositioning",
                                    "Crossing","ChancePassing","Shooting","ChancePositioning",
                                    "Aggression","Pressure","Team Width","Defender Line",
                                    "DP","IP","SAA","TAA"])
# expanded_fifa_df["Date"] = fifa_df.agg(
#             lambda x: datetime.strptime(x["date"], "%Y-%m-%d"), axis = 1)
expanded_fifa_df["ID"] = pd.to_numeric(fifa_df.agg(lambda x:x[0][0], axis=1))
expanded_fifa_df["OVA"] = pd.to_numeric(fifa_df.agg(lambda x:x[0][1], axis=1))
expanded_fifa_df["ATT"] = pd.to_numeric(fifa_df.agg(lambda x:x[0][2], axis=1))
expanded_fifa_df["MID"] = pd.to_numeric(fifa_df.agg(lambda x:x[0][3], axis=1))
expanded_fifa_df["DEF"] = pd.to_numeric(fifa_df.agg(lambda x:x[0][4], axis=1))
expanded_fifa_df["Transfer Budget"] = fifa_df.agg(lambda x:x[0][5], axis=1)
expanded_fifa_df["Speed"] = fifa_df.agg(lambda x:x[1][0], axis=1)
expanded_fifa_df["Dribbling"] = fifa_df.agg(lambda x:x[1][0], axis=1)
expanded_fifa_df["BuildPassing"] = fifa_df.agg(lambda x:x[1][0], axis=1)
expanded_fifa_df["BuildPositioning"] = fifa_df.agg(lambda x:x[1][0], axis=1)
expanded_fifa_df["Crossing"] = fifa_df.agg(lambda x:x[2][0], axis=1)
expanded_fifa_df["ChancePassing"] = fifa_df.agg(lambda x:x[2][0], axis=1)
expanded_fifa_df["Shooting"] = fifa_df.agg(lambda x:x[2][0], axis=1)
expanded_fifa_df["ChancePositioning"] = fifa_df.agg(lambda x:x[2][0], axis=1)
expanded_fifa_df["Aggression"] = fifa_df.agg(lambda x:x[4][0], axis=1)
expanded_fifa_df["Pressure"] = fifa_df.agg(lambda x:x[4][1], axis=1)
expanded_fifa_df["Team Width"] = fifa_df.agg(lambda x:x[4][2], axis=1)
expanded_fifa_df["Defender Line"] = fifa_df.agg(lambda x:x[4][3], axis=1)
expanded_fifa_df["DP"] = pd.to_numeric(fifa_df.agg(lambda x:x[6][0], axis=1))
expanded_fifa_df["IP"] = pd.to_numeric(fifa_df.agg(lambda x:x[6][1], axis=1))
expanded_fifa_df["SAA"] = pd.to_numeric(fifa_df.agg(lambda x:x[6][2], axis=1))
expanded_fifa_df["TAA"] = pd.to_numeric(fifa_df.agg(lambda x:x[6][3], axis=1))
#%%
expanded_fifa_df["Team Name"] = fifa_df["name"]
expanded_fifa_df["Date"] = fifa_df["date"]
# teams_editted.drop_duplicates(inplace = True)
#%%
name_list = list(set(expanded_fifa_df["Team Name"]))
name_list2 = list(set(match_df["team"]))
name_list3 = []
for name in name_list:
    if name not in name_list2:
        name_list3.append(name)

#%%
expanded_fifa_df.to_csv("expanded_fifa.csv")
match_df.to_csv("matches_editted.csv")
#%%
dates = list(set(expanded_fifa_df["Date"].values))
dates.sort()
#%%
df = pd.DataFrame()
for i in tqdm(range(len(dates) - 1)):
    df = df.append(pd.merge(
        table_df.loc[(table_df["date"] >= dates[i])
                & (table_df["date"] <= dates[i + 1])],
        expanded_fifa_df.loc[expanded_fifa_df["Date"] == dates[i]], how = "left",
        left_on="team", right_on="Team Name"
        )
    )
df = df.append(pd.merge(
        table_df.loc[(table_df["date"] >= dates[-1])],
        expanded_fifa_df.loc[expanded_fifa_df["Date"] == dates[i]], how = "left",
        left_on="team", right_on="Team Name"
    )
)
#%%
df = df.drop_duplicates(["team", "season", "week"])
#%%
sorted_df = df.sort_values(["team", "date"])
filled_df = sorted_df.fillna(method='ffill')
filled_df = filled_df.fillna(method='bfill')
fifatable_df = filled_df
#%%
home_df = pd.merge(match_df, fifatable_df, how = "left", right_on = ["team", "season", "week"], 
                   left_on = ["home_team", "season", "week"], suffixes = ("", "_home"))
#home_df = home_df[home_df["season"] != 2005]
home_df = home_df.drop_duplicates(["home_team", "season", "week"])
#%%
whole_df = pd.merge(fifatable_df, home_df, how = "right", left_on = ["team", "season", "week"],
                    right_on = ["away_team", "season", "week"], suffixes = ("", "_away"))
#%%
sorted_df = df.sort_values(["team", "date"])
whole_df.to_csv("whole_dataset.csv", index = False)
whole_df.to_excel("whole_dataset.xlsx", index = False)
#%%
whole_df = pd.read_csv("whole_dataset.csv")
#%%
sorted_df = whole_df.sort_values(["team", "season", "week"])