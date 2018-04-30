import json

import psycopg2

from login_details import DB_PASSWORD, DB_USER

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER,DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor()

data = json.load(open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season16-17/season_stats.json', encoding="utf8"))
players = []
player_id_list = []
team_id_list = []


def insert_player(player_name, player_id):
    sql = """INSERT INTO players (playerid, playername)
    VALUES (%s, %s)"""
    data = (player_id, player_name)
    cur.execute(sql, data)

for key, value in data.items():

    for underkey, undervalue in value.items(): ##document
         count = 0
         for subkey, subvalue in undervalue.items(): ##team
             if (subkey == 'team_details'):
                 t1 = (subvalue['team_id'], subvalue['team_name'])
                 if t1 not in team_id_list:
                        team_id_list.append(t1)


             if (subkey == 'Player_stats'):
                 for basekey, basevalue in subvalue.items(): ##Players
                     players.append(basevalue)
                     for lastkey, lastvalue in basevalue.items():
                        if lastkey == 'player_details':
                            if lastvalue['player_id'] not in player_id_list:
                                 player_id_list.append(lastvalue['player_id'])
                                 insert_player(lastvalue['player_name'],lastvalue['player_id'])


                     ####  ADDING TEAM NAMES/ IDS to POSTGRES team Table
for item in team_id_list:
    cur.execute("""INSERT INTO teams (teamid, teamname) VALUES(%s,%s)""", (item[0], item[1]))

