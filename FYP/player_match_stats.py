import json

import psycopg2

from login_details import DB_PASSWORD, DB_USER

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER, DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor()

data = json.load(
    open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season14-15/season_stats.json'))
count = 0
points_list = ['red_card', 'yellow_card',  'goal_assist', 'goals', 'att_pen_target', 'own_goals', 'saves' ,'penalty_save']
player_details = {}
player_points = {}
for match_id, match_value in data.items():
    player_details[match_id] = []
    for team_id, team_value in match_value.items():
        for match_details_key, match_details_value in team_value.items():
            if 'Player_stats' == match_details_key:
                for player_name, player_value in match_details_value.items():
                    for player_detail_key, player_detail_value in player_value.items():
                        if player_detail_key == 'player_details':
                            if player_detail_value['player_position_info'] in ["DL", "DC","DR"]:
                                player_position ='1'
                            elif player_detail_value['player_position_info'] in ["DMC", "ML", "MR", "MC","AMC","AML","AMR","DML","DMR"]:
                                player_position = '2'
                            elif player_detail_value['player_position_info'] in ["FW","FWR","FWL"]:
                                player_position = '3'
                            elif player_detail_value['player_position_info'] in ["GK"]:
                                player_position ='0'
                            elif player_detail_value['player_position_info'] in ["Sub"]:
                                player_position = '4'


                            player_rating = player_detail_value['player_rating']
                            player_id = player_detail_value['player_id']
                            player_points[player_id] = []

                        if player_detail_key == 'Match_stats':
                            for word in points_list:
                                if (word in player_detail_value):
                                    player_points[player_id].append((word, player_detail_value[word]))
                                else:
                                    player_points[player_id].append((word, '0'))
                        if player_points[player_id]:

                            cur.execute("""SELECT * FROM match where matchid LIKE %s""", (match_id, ))
                            rows = cur.fetchall()
                            for list in rows:
                                if team_id == list[1]:
                                    cur.execute("""SELECT hometeamgoalsconceded FROM match where matchid = %s AND hometeamid = %s""", (match_id, team_id))
                                    conceded = cur.fetchall()
                                elif team_id == list[2]:
                                    cur.execute("""SELECT awayteamgoalsconceded FROM match where matchid = %s AND awayteamid = %s""", (match_id, team_id))
                                    conceded = cur.fetchall()
                            cur.execute("""INSERT INTO player_match_stats ( playerid , matchid , playerposition , redcard , yellowcard , goalassists , playerrating ,    goalsscored , goalsconceded , cleansheet , penaltymissed , owngoals, saves ,penaltysaves) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                                        (player_id,match_id, player_position, player_points[player_id][0][1], player_points[player_id][1][1], player_points[player_id][2][1], player_rating, player_points[player_id][3][1], conceded[0][0],conceded[0][0], player_points[player_id][4][1], player_points[player_id][5][1], player_points[player_id][6][1], player_points[player_id][7][1] ))
