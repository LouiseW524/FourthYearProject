import psycopg2.extras
from login_details import DB_PASSWORD, DB_USER
import sys

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER, DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
list_all_teams = []
all_players = []
goalkeepers = []
defenders = []
forwards = []
mids = []
all_points = 0
all_players_point_list = []
captain_calc = []

goalkeeper_dict = {}
overall_goalkeeper_dict = {}
overall_defender_dict = {}
overall_mid_dict = {}
overall_fw_dict = {}
defender_dict = {}
mid_dict = {}
fw_dict = {}

def delete_weekly_historical_data(all_matchid_before_this_week):
    for match_id in all_matchid_before_this_week:
      cur.execute("""DELETE FROM training_matches where matchid = %s""", (match_id[0],))
      cur.execute("""DELETE FROM training_player_match_stats where matchid = %s""", (match_id[0],))

def get_matches_this_week(week):
    cur.execute("""SELECT matchid , hometeamid , awayteamid FROM match where week = %s """, (week,))
    return cur.fetchall()

def insert_new_weeks_into_training_data(week, all_matchid_before_this_week):
    cur.execute("""INSERT INTO training_matches SELECT * FROM match where week < %s""", (week,))
    for match_id in all_matchid_before_this_week:
      cur.execute("""INSERT INTO training_player_match_stats SELECT * FROM player_match_stats where matchid = %s""", (match_id[0],))

def get_all_matches_before_this_week(week):
    cur.execute("""SELECT matchid from match where week < %s""", (week,))
    return cur.fetchall()

def get_total_goals_previous_per_match(matchid):
    cur.execute("""SELECT goalsscored from training_player_match_stats where matchid = %s and goalsscored != '0'""",(matchid,))
    all_goals = cur.fetchall()
    if all_goals:
        list_goals = list(sum(all_goals, []))
        list_goals = [int(x) for x in list_goals]
        return sum(list_goals)
    else:
        return 0

def get_total_redcards_previous_per_match(matchid):
    cur.execute("""SELECT redcard from training_player_match_stats where matchid = %s and redcard != '0'""",(matchid,))
    all_card = cur.fetchall()
    if all_card:
        list_cards = list(sum(all_card, []))
        list_cards = [int(x) for x in list_cards]
        return sum(list_cards)
    else:
        return 0

def get_total_yellowcards_previous_per_match(matchid):
    cur.execute("""SELECT yellowcard from training_player_match_stats where matchid = %s and yellowcard != '0'""", (matchid,))
    all_card = cur.fetchall()
    if all_card:
        list_cards = list(sum(all_card, []))
        list_cards = [int(x) for x in list_cards]
        return sum(list_cards)
    else:
        return 0

def get_total_goal_assists_previous_per_match(matchid):
    cur.execute("""SELECT goalassists from training_player_match_stats where matchid = %s and goalassists != '0'""", (matchid,))
    all_assist = cur.fetchall()
    if all_assist:
        list_assist = list(sum(all_assist, []))
        list_assist = [int(x) for x in list_assist]
        return sum(list_assist)
    else:
        return 0

def get_total_clean_sheets_previous_per_match(matchid):
    cur.execute("""SELECT cleansheet from training_player_match_stats where matchid = %s and cleansheet = 0""",(matchid,))
    all_cleansheet = cur.fetchall()
    if all_cleansheet:
        list_cleansheet = list(sum(all_cleansheet, []))
        return len(list_cleansheet)
    else:
            return 0

def get_total_saves_previous_per_match(matchid):
    cur.execute("""SELECT saves from training_player_match_stats where matchid = %s and saves != '0' and saves !='1'""",(matchid,))
    all_saves = cur.fetchall()
    if all_saves:
        list_saves = list(sum(all_saves, []))
        list_saves = [int(x) for x in list_saves]
        if sum(list_saves)/3 >= 1 :
            return  int(sum(list_saves)/3)
        else:
            return 0
    else:
        return 0

def get_total_penalty_saves_previous_per_match(matchid):
    cur.execute("""SELECT penaltysaves from training_player_match_stats where matchid = %s and goalassists != '0'""",(matchid,))
    all_assist = cur.fetchall()
    if all_assist:
        list_assist = list(sum(all_assist, []))
        list_assist = [int(x) for x in list_assist]
        return sum(list_assist)
    else:
        return 0

def get_player_position(player,all_matches_this_week):
    for match in all_matches_this_week:
        cur.execute("""SELECT playerposition FROM player_match_stats where matchid = %s AND playerid = %s""",(match[0], player))
        player_pos = cur.fetchall()
        if player_pos :
            for pos in player_pos:
                return pos[0]
                break

def goalkeeper_saves_points_per_match(player, previous_matches_between_teams):
    saves = 0
    overall_saves = 0
    cur.execute("""select saves from training_player_match_stats where playerid = %s AND saves !='0' AND saves !='1' AND saves!='2'""",(player[0],))
    list_overall_saves = cur.fetchall()
    if list_overall_saves:
        for g_saves in list_overall_saves:
            if int(int(g_saves[0]) / 3) >= 1:
                overall_saves += int(int(g_saves[0]) / 3)
    for match in previous_matches_between_teams:
        cur.execute("""select saves from training_player_match_stats where playerid = %s and matchid = %s AND saves !='0' AND saves !='1' AND saves!='2'""", (player[0], match[0]))
        list_saves = cur.fetchall()
        if list_saves:
            for g_saves in list_saves:
                if int(int(g_saves[0])/3) >= 1:
                    saves += int(int(g_saves[0])/3)
    return saves,overall_saves

def assists_points_per_match(player, previous_matches_between_teams):
    assists = 0
    overall_assists = 0
    cur.execute("""SELECT goalassists from training_player_match_stats where playerid = %s""", (player[0], ))
    total_assists = cur.fetchall()
    if total_assists:
        list_total_assists = list(sum(total_assists, []))
        list_total_assists = [int(x) for x in list_total_assists]
        overall_assists = sum(list_total_assists)

    for match in previous_matches_between_teams:
        cur.execute("""select goalassists from training_player_match_stats where playerid = %s and matchid = %s""", (player[0], match[0]))
        list_assists = cur.fetchall()
        if list_assists:
            for g_assists in list_assists:
                assists += int(g_assists[0])
    return assists,overall_assists

def cleansheet_points_per_match(player, previous_matches_between_teams):
    clean = 0
    overall_cleansheet = 0
    cur.execute( """select cleansheet from training_player_match_stats where playerid = %s AND cleansheet = 0 """,(player[0], ))
    list_clean = cur.fetchall()
    if list_clean:
        for g_clean in list_clean:
            overall_cleansheet += 1
    for match in previous_matches_between_teams:
        cur.execute("""select cleansheet from training_player_match_stats where playerid = %s and matchid = %s AND cleansheet = 0 """, (player[0], match[0]))
        list_clean = cur.fetchall()
        if list_clean:
            for g_clean in list_clean:
                clean += 1
    return clean,overall_cleansheet

def goalkeeper_penalty_save_points_per_match(player, previous_matches_between_teams):
    penalty = 0
    overall_penalty = 0
    cur.execute("""select penaltysaves from training_player_match_stats where playerid = %s """,(player[0], ))
    list_penalty = cur.fetchall()
    if list_penalty:
        list_overall_penalty = list(sum(list_penalty, []))
        list_overall_penalty = [int(x) for x in list_overall_penalty]
        overall_penalty = sum(list_overall_penalty)

    for match in previous_matches_between_teams:
        cur.execute("""select penaltysaves from training_player_match_stats where playerid = %s and matchid = %s""", (player[0], match[0]))
        list_penalty = cur.fetchall()
        if list_penalty:
            for g_penalty in list_penalty:
                penalty += int(g_penalty[0])

    return penalty,overall_penalty

def goal_points_per_match(player, previous_matches_between_teams):
    goals = 0
    overall_goals = 0

    cur.execute("""select goalsscored from training_player_match_stats where playerid = %s """, (player[0], ))
    list_goals = cur.fetchall()
    if list_goals:
        for g_goals in list_goals:
            overall_goals += int(g_goals[0])

    for match in previous_matches_between_teams:
        cur.execute("""select goalsscored from training_player_match_stats where playerid = %s and matchid = %s""", (player[0], match[0]))
        list_goals = cur.fetchall()
        if list_goals:
            for g_goals in list_goals:
                goals += int(g_goals[0])
    return goals,overall_goals

def get_all_previous_goals_total():
    cur.execute("""SELECT goalsscored from training_player_match_stats WHERE goalsscored != '0' """)
    total_goals = cur.fetchall()
    if total_goals:
        list_goals = list(sum(total_goals, []))
        list_goals = [int(x) for x in list_goals]
        return sum(list_goals)

def get_all_previous_assists_total():
    cur.execute("""SELECT goalassists from training_player_match_stats WHERE goalassists != '0' """)
    total_goalassists = cur.fetchall()
    if total_goalassists:
        list_total_goalassists = list(sum(total_goalassists, []))
        list_total_goalassists = [int(x) for x in list_total_goalassists]
        return sum(list_total_goalassists)

def get_all_previous_clean_sheets_total():
    cur.execute("""SELECT cleansheet from training_player_match_stats WHERE cleansheet = 0 """)
    list_clean = cur.fetchall()
    clean = 0
    if list_clean:
        for g_clean in list_clean:
            clean += 1
    return clean

def get_all_previous_saves_total():
    saves = 0
    cur.execute("""select saves from training_player_match_stats where saves !='0' AND saves !='1' AND saves!='2'""")
    list_saves = cur.fetchall()
    if list_saves:
        for g_saves in list_saves:
            if int(int(g_saves[0]) / 3) >= 1:
                saves += int(int(g_saves[0]) / 3)
    return saves

def get_all_penalty_save_previous_total():
    cur.execute("""SELECT penaltysaves from training_player_match_stats WHERE penaltysaves != '0' """)
    total_penaltysaves = cur.fetchall()
    if total_penaltysaves:
        list_total_penaltysaves = list(sum(total_penaltysaves, []))
        list_total_penaltysaves = [int(x) for x in list_total_penaltysaves]
        return sum(list_total_penaltysaves)

########################################################################################################################
#
all_matchid_before_this_week = get_all_matches_before_this_week(sys.argv[1], )
insert_new_weeks_into_training_data(sys.argv[1],all_matchid_before_this_week)
all_matches_this_week = get_matches_this_week(sys.argv[1])
player_position = []

all_previous_goals = get_all_previous_goals_total()
all_previous_assists = get_all_previous_assists_total()
all_clean_sheets_previous = get_all_previous_clean_sheets_total()
all_save_previous = get_all_previous_saves_total()
all_penalty_save_previous = get_all_penalty_save_previous_total()

for matches in all_matches_this_week:

    total_goals_previous = 0
    total_redcards_previous = 0
    total_yellowcards_previous = 0
    total_goal_assists_previous = 0
    total_clean_sheets_previous = 0
    total_save_previous = 0
    total_penalty_save_previous = 0

    cur.execute("""SELECT matchid from training_matches where (hometeamid = %s OR hometeamid = %s) AND (awayteamid = %s OR awayteamid = %s)""", (matches[1],matches[2],matches[1],matches[2]))
    previous_matches_between_teams = cur.fetchall()
    number_of_previous_matches_between_team = len(previous_matches_between_teams)
    for match in previous_matches_between_teams:

        total_goals_previous += get_total_goals_previous_per_match(match[0])
        total_redcards_previous += get_total_redcards_previous_per_match(match[0])
        total_yellowcards_previous += get_total_yellowcards_previous_per_match(match[0])
        total_goal_assists_previous += get_total_goal_assists_previous_per_match(match[0])
        total_clean_sheets_previous += get_total_clean_sheets_previous_per_match(match[0])
        total_save_previous += get_total_saves_previous_per_match(match[0])
        total_penalty_save_previous += get_total_penalty_saves_previous_per_match(match[0])

    cur.execute("""SELECT playerid FROM teamlist where matchid = %s """, (matches[0],))
    players_in_this_match_this_week = cur.fetchall()

    for player in players_in_this_match_this_week:

        total_stats_for_this_player = 0
        player_position = int(get_player_position(player[0],all_matches_this_week))

        if player_position == 0:
            goalkeeper_total = 0
            goalkeeper_overall_total = 0
            goalkeeper_saves, overall_player_saves = goalkeeper_saves_points_per_match(player, previous_matches_between_teams)
            goalkeeper_assists, overall_player_assists = assists_points_per_match(player, previous_matches_between_teams)
            goalkeeper_cleansheet, overall_cleansheet = cleansheet_points_per_match(player, previous_matches_between_teams)
            goalkeeper_penalty_save, overall_peno_saves = goalkeeper_penalty_save_points_per_match(player, previous_matches_between_teams)

            goalkeeper_overall = ((overall_player_saves+1)/(all_save_previous+1)) * ((overall_player_assists+1)/(all_previous_assists+1)) * ((overall_cleansheet+1)/(all_clean_sheets_previous+1)) * ((overall_peno_saves+1)/(all_penalty_save_previous +1) )
            overall_goalkeeper_dict[player[0]] = goalkeeper_overall

            goalkeeper_total = ((goalkeeper_saves+1)/(total_save_previous+1)) * ((goalkeeper_assists+1)/(total_goal_assists_previous+1)) * ((goalkeeper_cleansheet+1)/(total_clean_sheets_previous+1)) * ((goalkeeper_penalty_save+1)/(total_penalty_save_previous +1) )
            goalkeeper_dict[player[0]] = goalkeeper_total

        if player_position == 1:
            defender_total = 0
            defender_overall_total = 0

            defender_assists, overall_assists = assists_points_per_match(player, previous_matches_between_teams)
            defender_cleansheet, overall_cleansheet = cleansheet_points_per_match(player, previous_matches_between_teams)
            defender_goals, overall_goals = goal_points_per_match(player, previous_matches_between_teams)

            defender_overall_total = ((overall_assists+1)/(all_previous_assists+1)) * ((overall_cleansheet+1)/(all_clean_sheets_previous+1)) * ((overall_goals+1)/(all_previous_goals+1))
            overall_defender_dict[player[0]] = defender_overall_total

            defender_total = ((defender_assists+1)/(total_goal_assists_previous+1)) * ((defender_cleansheet+1)/(total_clean_sheets_previous+1)) * ((defender_goals+1)/(total_goals_previous+1))
            defender_dict[player[0]] = defender_total

        if player_position == 2:
            mid_total = 0
            mid_overall_total = 0

            mid_assists, overall_assists = assists_points_per_match(player, previous_matches_between_teams)
            mid_cleansheet,overall_cleansheet = cleansheet_points_per_match(player, previous_matches_between_teams)
            mid_goals,overall_goals = goal_points_per_match(player, previous_matches_between_teams)

            mid_overall_total = ((overall_assists + 1) / (all_previous_assists + 1)) * ((overall_cleansheet + 1) / (all_clean_sheets_previous + 1)) * ((overall_goals + 1) / (all_previous_goals + 1))
            overall_mid_dict[player[0]] = mid_overall_total

            mid_total = ((mid_assists + 1) / (total_goal_assists_previous + 1)) * ((mid_cleansheet + 1) / (total_clean_sheets_previous + 1)) * ((mid_goals + 1) / (total_goals_previous + 1))
            mid_dict[player[0]] = mid_total

        if player_position == 3:
            fw_overall_total = 0
            fw_total = 0

            fw_assists, overall_assists = assists_points_per_match(player, previous_matches_between_teams)
            fw_goals, overall_goals = goal_points_per_match(player, previous_matches_between_teams)

            fw_overall_total = ((overall_assists + 1) / (all_previous_assists + 1))  * ((overall_goals + 1) / (all_previous_goals + 1))
            overall_fw_dict[player[0]] = fw_overall_total

            fw_total = ((fw_assists + 1) / (total_goal_assists_previous + 1))  * ((fw_goals + 1) / (total_goals_previous + 1))
            fw_dict[player[0]] = fw_total

overall_goalkeepers = []
overall_defenders = []
overall_fw = []
overall_all_players = []

for goalie in sorted(overall_goalkeeper_dict, key=overall_goalkeeper_dict.get, reverse=True)[:1]:
    overall_goalkeepers.append(goalie)

for goalie in sorted(goalkeeper_dict, key=goalkeeper_dict.get, reverse=True)[:2]:
    goalkeepers.append(goalie)

for defender in sorted(overall_defender_dict, key=overall_defender_dict.get, reverse=True)[:4]:
    cur.execute("""SELECT playername from players where playerid = %s """, (defender,))
    overall_defender_dict.pop(defender, None)
    defender = cur.fetchall()
    for defe in defender:
        overall_defenders.append(defe[0])

for defender in sorted(defender_dict, key=defender_dict.get, reverse=True)[:4]:
    cur.execute("""SELECT playername from players where playerid = %s """, (defender,))
    defender_dict.pop(defender, None)
    defender = cur.fetchall()
    for defe in defender:
        defenders.append(defe[0])

for fw in sorted(overall_fw_dict, key=overall_fw_dict.get, reverse=True)[:2]:
    cur.execute("""SELECT playername from players where playerid = %s """,(fw,) )
    overall_fw_dict.pop(fw, None)
    fw = cur.fetchall()
    for f in fw:
        overall_fw.append(f[0])

for fw in sorted(fw_dict, key=fw_dict.get, reverse=True)[:2]:
    cur.execute("""SELECT playername from players where playerid = %s """,(fw,) )
    fw_dict.pop(fw, None)
    fw = cur.fetchall()
    for f in fw:
        forwards.append(f[0])

cur.execute("""SELECT playername from players where playerid = %s""", (overall_goalkeepers[0],))
overall_gk = cur.fetchall()

cur.execute("""SELECT playername from players where playerid = %s""", (goalkeepers[0],))
first_choice_gk = cur.fetchall()

cur.execute("""SELECT playername from players where playerid = %s""", (goalkeepers[1],))
second_choice_gk = cur.fetchall()

dic2 = dict(defender_dict, **mid_dict)
all_player_dict = dict(dic2, **fw_dict)

dic3 = dict(overall_defender_dict, **overall_mid_dict)
overall_all_player_dict = dict(dic3, **overall_fw_dict)

for player in sorted(all_player_dict, key=all_player_dict.get, reverse=True)[:6]:
    cur.execute("""SELECT playername from players where playerid = %s """, (player,))
    players = cur.fetchall()
    for p in players:
        all_players.append(p)
all_players.append(first_choice_gk[0])


for player in sorted(overall_all_player_dict, key=overall_all_player_dict.get, reverse=True)[:6]:
    cur.execute("""SELECT playername from players where playerid = %s """, (player,))
    players = cur.fetchall()
    for p in players:
        overall_all_players.append(p)
overall_all_players.append(overall_gk[0])

for d in overall_defenders[:3]:
    overall_all_players.append([d])
overall_all_players.append(overall_fw[:1])

for d in defenders[:3]:
    all_players.append([d])
all_players.append(forwards[:1])

overall_defender_dict.update(overall_mid_dict)
overall_defender_dict.update(overall_fw_dict)
for player in sorted(overall_defender_dict, key=overall_defender_dict.get, reverse=True)[:1]:
    overall_captain = player


defender_dict.update(mid_dict)
defender_dict.update(fw_dict)
for player in sorted(defender_dict, key=all_player_dict.get, reverse=True)[:1]:
    captain = player

print("TEAM FOR WEEK :", sys.argv[1], "Per_all_matches_prediction")
for player in overall_all_players:
    print(player)

    cur.execute("""SELECT playerid from players where playername = %s""" ,(player[0],))
    player_ids = cur.fetchall()

    for match in all_matches_this_week:
        for playerid in player_ids:
            cur.execute("""SELECT playerpoints from player_points_per_match where playerid = %s AND matchid = %s""", (playerid[0],match[0]))
            points = cur.fetchall()
            if points:
                for p in points:
                    if playerid[0] == overall_captain:
                        print("CAPTAIN")
                        all_points += int(p[0])*2
                    else:
                        all_points += int(p[0])

print(" \n TOTAL POINTS : ", all_points, "\n")


print("TEAM FOR WEEK :", sys.argv[1] , "Per_passed_match_prediction")

all_points = 0
for player in all_players:
    print(player)

    cur.execute("""SELECT playerid from players where playername = %s""" ,(player[0],))
    player_ids = cur.fetchall()

    for match in all_matches_this_week:
        for playerid in player_ids:
            cur.execute("""SELECT playerpoints from player_points_per_match where playerid = %s AND matchid = %s""", (playerid[0],match[0]))
            points = cur.fetchall()
            if points:
                for p in points:
                    if playerid[0] == captain:
                        print("CAPTAIN")
                        all_points += int(p[0])*2
                    else:
                        all_points += int(p[0])

print(" \n TOTAL POINTS : ", all_points)


delete_weekly_historical_data(all_matchid_before_this_week)





