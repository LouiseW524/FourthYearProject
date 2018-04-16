import json

import psycopg2

from login_details import DB_PASSWORD, DB_USER

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER,DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor()

data = json.load(open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season14-15/season_stats.json'))
match_team_player_dict = {}
team_name_id = {}
players = []
list_team_details =[]
player_id_list = []

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
                 for basekey, basevalue in subvalue.items():
                     count = count + 1
                     list_team_details.append(basevalue)
                     if count == 2:
                         break;


             if (subkey == 'Player_stats'):
                 for basekey, basevalue in subvalue.items(): ##Players
                     players.append(basevalue)
                     for lastkey, lastvalue in basevalue.items():
                        if lastkey == 'player_details':
                            if lastvalue['player_id'] not in player_id_list:
                                 player_id_list.append(lastvalue['player_id'])
                                 #insert_player(lastvalue['player_name'],lastvalue['player_id'])


team_detail = d = dict([(k, v) for k, v in zip(list_team_details[::2], list_team_details[1::2])])

                     ####  ADDING TEAM NAMES/ IDS to POSTGRES team Table
for key, value in team_detail.items():
      cur.execute("""INSERT INTO teams (teamid, teamname) VALUES(%s,%s)""", (key, value))

