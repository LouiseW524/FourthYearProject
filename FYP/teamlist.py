import json

import psycopg2

from login_details import DB_PASSWORD, DB_USER

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER,DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor()

data = json.load(open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season14-15/season_stats.json'))

for match_id, match_value in data.items():
    for team_id, team_value in match_value.items(): ##document
        for match_details_key, match_deatils_value in team_value.items():
            if 'Player_stats' == match_details_key:
                 for player_id, player_value in team_value.items():
                     for player_detail_key, player_detail_value in player_value.items():
                        if isinstance(player_detail_value, dict):
                            for last_key, last_value in player_detail_value.items():
                                if last_key == 'player_details':
                                    cur.execute("""INSERT INTO teamlist (matchid, teamid, playerid) VALUES(%s,%s, %s)""", (match_id,team_id,last_value['player_id']))

