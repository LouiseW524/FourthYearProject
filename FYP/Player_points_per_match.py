import json

import psycopg2

from login_details import DB_PASSWORD, DB_USER

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER, DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor()

data = json.load( open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season14-15/season_stats.json'))

goal_scored_by_GK_Defender = 6
goal_scored_midfield = 5
goal_scored_forward = 4
goal_assist = 3
clean_sheet_GK_Defender = 4
clean_sheet_midfield = 1
three_shot_save_GK = 1
penalty_save = 5
penalty_miss = -2
best_player = 3
second_best = 2
third_best = 1
two_goals_concede_GK_defender = -1
yellow_card = -1
red_card = -3
OG = -2

cur.execute("""SELECT * FROM player_match_stats where playerposition LIKE '0' OR playerposition LIKE '1'""")
rows = cur.fetchall()
for row in rows:
    best_players = []
    total_points = 0
    cur.execute("""SELECT * FROM player_match_stats where matchid = %s ORDER BY playerrating DESC LIMIT(3)""", (row[1],))
    top_players  = cur.fetchall()
    for player in top_players:
        if player[0] == row[0]:
            best_players.append(player)

    total_points =(int(row[3]) * red_card) + (int(row[4]) * yellow_card) + (int(row[5]) * goal_assist) + (int(row[7]) * goal_scored_by_GK_Defender) + (int(row[10]) * penalty_miss) + (int(row[11]) * OG) + (int(row[13]) * penalty_save)

    if int(row[12]) % 3 == 0:
        saves_point = int(row[12])/3
        total_points = total_points + (saves_point * three_shot_save_GK)

    if int(row[8]) >= 2 :
        total_points = total_points + two_goals_concede_GK_defender

    if int(row[9]) == 0 :
        total_points = total_points + clean_sheet_GK_Defender

    if best_players:
        if row == best_players[0]:
            total_points = total_points + best_player
        elif row == best_players[1]:
            total_points = total_points + second_best
        elif row == best_players[2]:
            total_points = total_points + third_best
        best_players.clear()

    cur.execute("""INSERT INTO player_points_per_match ( playerid , matchid , playerpoints) VALUES (%s, %s, %s)""",(row[0], row[1], total_points))


cur.execute("""SELECT * FROM player_match_stats where playerposition LIKE '2'""")
midfielders = cur.fetchall()
for mids in midfielders:
    total_points = 0
    best_players = []
    total_points =(int(mids[3]) * red_card) + (int(mids[4]) * yellow_card) + (int(mids[5]) * goal_assist) + (int(mids[7]) * goal_scored_midfield) + (int(mids[10]) * penalty_miss) + (int(mids[11]) * OG)
    if int(mids[9]) == 0 :
        total_points = total_points + clean_sheet_midfield
    cur.execute("""SELECT * FROM player_match_stats where matchid = %s ORDER BY playerrating DESC LIMIT(3)""",(mids[1],))
    top_players = cur.fetchall()
    for player in top_players:
        if player[0] == mids[0]:
            best_players.append(player)
    if best_players:
        if mids == best_players[0]:
            total_points = total_points + best_player
        elif mids == best_players[1]:
            total_points = total_points + second_best
        elif mids == best_players[2]:
            total_points = total_points + third_best
        best_players.clear()

    cur.execute("""INSERT INTO player_points_per_match ( playerid , matchid , playerpoints) VALUES (%s, %s, %s)""",(mids[0], mids[1], total_points))

cur.execute("""SELECT * FROM player_match_stats where playerposition LIKE '3'""")
forwards = cur.fetchall()
for fw in forwards:
    total_points = 0
    best_players = []
    total_points =(int(fw[3]) * red_card) + (int(fw[4]) * yellow_card) + (int(fw[5]) * goal_assist) + (int(fw[7]) * goal_scored_forward) + (int(fw[10]) * penalty_miss) + (int(fw[11]) * OG)

    cur.execute("""SELECT * FROM player_match_stats where matchid = %s ORDER BY playerrating DESC LIMIT(3)""",(fw[1],))
    top_players = cur.fetchall()
    for player in top_players:
        if player[0] == fw[0]:
            best_players.append(player)
    if best_players:
        if fw == best_players[0]:
            total_points = total_points + best_player
        elif fw == best_players[1]:
            total_points = total_points + second_best
        elif fw == best_players[2]:
            total_points = total_points + third_best
        best_players.clear()

    cur.execute("""INSERT INTO player_points_per_match ( playerid , matchid , playerpoints) VALUES (%s, %s, %s)""",(fw[0], fw[1], total_points))

cur.execute("""SELECT * FROM player_match_stats where playerposition LIKE '4'""")
subs = cur.fetchall()
for sub in subs:
    cur.execute("""INSERT INTO player_points_per_match ( playerid , matchid , playerpoints) VALUES (%s, %s, %s)""",
                (sub[0], sub[1], 0))