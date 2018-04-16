import json

import psycopg2

from login_details import DB_PASSWORD, DB_USER

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER,DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor()

data = json.load(open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season14-15/season_match_stats.json'))

match_id_dict = {}

for key, value in data.items():
    for underkey, undervalue in value.items():

        if 'home_team_id' in underkey:
            home_team = undervalue
        if 'away_team_id' in underkey:
            away_team = undervalue
        if 'full_time_score' in underkey:
            scores = undervalue.split(":")
            homegoalconceded = scores[1]
            awaygoalconceded = scores[0]
            match_id_dict[key] = (home_team,away_team,homegoalconceded,awaygoalconceded)
            break;

for key,value in match_id_dict.items():
    sql = """INSERT INTO match (matchid, hometeamid,awayteamid,hometeamgoalsconceded,awayteamgoalsconceded)
       VALUES (%s, %s , %s, %s , %s)"""
    data = (key, value[0], value[1], value[2], value[3])
    cur.execute(sql, data)
