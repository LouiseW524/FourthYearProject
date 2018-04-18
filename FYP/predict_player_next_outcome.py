import psycopg2.extras
from login_details import DB_PASSWORD, DB_USER
import sys

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER, DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


def select_player_id_condition(player_id, cell_for_sql):

    if cell_for_sql == 1:
        cur.execute("""SELECT goalsscored FROM player_match_stats WHERE playerid = %s""", ( player_id,))
    if cell_for_sql == 2:
        cur.execute("""SELECT goalassists FROM player_match_stats WHERE playerid = %s""", ( player_id,))
    if cell_for_sql == 3:
        cur.execute("""SELECT redcard FROM player_match_stats WHERE playerid = %s""", ( player_id,))
    if cell_for_sql == 4:
        cur.execute("""SELECT yellowcard FROM player_match_stats WHERE playerid = %s""", (player_id,))
    if cell_for_sql == 5:
        cur.execute("""SELECT penaltymissed FROM player_match_stats WHERE playerid = %s""", (player_id,))
    if cell_for_sql == 6 :
        cur.execute("""SELECT owngoals FROM player_match_stats WHERE playerid = %s""", (player_id,))
    if cell_for_sql == 7:
        cur.execute("""SELECT count(saves) FROM player_match_stats WHERE playerid = %s AND saves !='0' AND saves !='1'""", (player_id,))
    if cell_for_sql == 8:
        cur.execute("""SELECT penaltysaves FROM player_match_stats WHERE playerid = %s""", (player_id,))

    results = cur.fetchall()
    return results

def add_sum_values(value):
    result = 0
    for items in value:
        for item_values in items:
            result += int(item_values)
    return result

def get_probabilities_maths(single_value, count_matches_played_by_player):
    return (single_value + 1)/(count_matches_played_by_player +1)

def total_matches_per_player(player_id):
    cur.execute("""SELECT count(*) FROM player_match_stats WHERE playerid = %s""", (player_id, ))
    count_matches_played_by_player = cur.fetchall();
    count_matches_played_by_player = count_matches_played_by_player[0][0]
    return count_matches_played_by_player

def get_probablity(player_id, sql_number,count_matches_played_by_player):
    list_from_sql = select_player_id_condition(player_id, sql_number )
    sum_list = add_sum_values(list_from_sql)
    probability = get_probabilities_maths(float(sum_list), float(count_matches_played_by_player))
    return probability

def get_zeroes_from_list_prob(player_id, cell_for_sql, count_matches_played_by_player):
    if cell_for_sql == 1:
        cur.execute("""SELECT goalsconceded FROM player_match_stats WHERE playerid = %s """, (player_id[0],))
        goals_list = cur.fetchall()
        results = 0
        for goal in goals_list:
            if int(goal[0]) <= 1:
                results += 1
    if cell_for_sql ==2 :
        cur.execute("""SELECT cleansheet FROM player_match_stats WHERE playerid = %s """, (player_id[0],))
        goals_list = cur.fetchall()
        results = 0
        for goal in goals_list:
            if int(goal[0]) == 0:
                results += 1

    prob_no_conceded = (results + 1) / (count_matches_played_by_player +1)
    return prob_no_conceded

cur.execute("""SELECT DISTINCT playerid FROM teamlist where teamid = %s OR teamid = %s""", ("13", "96"))##(sys.argv[1],sys.argv[2]) )
all_player_ids = cur.fetchall()

GK = []
DF = []
MID = []
FW = []

for player_id in all_player_ids:

##get_total number of matches per player
    count_matches_played_by_player = total_matches_per_player(player_id[0])

##get probability of goal
    goal_scoring_probability = get_probablity(player_id[0],1,count_matches_played_by_player)

##get probability of assist
    assist_probability = get_probablity(player_id[0],2,count_matches_played_by_player)

##redcard
    red_probability = get_probablity(player_id[0],3,count_matches_played_by_player)
    prob_of_no_redcard = 1 - red_probability

##yellowcard
    yellow_probability = get_probablity(player_id[0],4,count_matches_played_by_player)
    prob_of_no_yellowcard = 1 - yellow_probability

##probability_of_no_goals_conceded
    prob_of_no_goals_conceded = get_zeroes_from_list_prob(player_id[0], 1, count_matches_played_by_player)

##probability_of_clean_sheet
    probability_of_clean_sheet = get_zeroes_from_list_prob(player_id[0], 2, count_matches_played_by_player)

##penaltymissed
    probability_penalty_miss = get_probablity(player_id[0],5,count_matches_played_by_player)
    probability_no_penalty_miss = 1 - probability_penalty_miss

##owngoals
    probability_own_goals = get_probablity(player_id[0],6,count_matches_played_by_player)
    probability_no_own_goals = 1 - probability_own_goals

# saves
    probability_save = get_probablity(player_id[0],7,count_matches_played_by_player)

#  penaltysaves
    probability_penalty_save = get_probablity(player_id[0],8,count_matches_played_by_player)
    cur.execute("""select playername from players where playerid = %s""", (player_id[0],))
    player_name = cur.fetchall()

    cur.execute("""SELECT playerposition from player_match_stats where playerid = %s""", (player_id[0],))
    position =  cur.fetchall()
    for pos in position:
        for item in pos:
            player_pos = int(item[0])

    overall_positive_probability = 0.0
    if player_pos == 0:
        overall_positive_probability = probability_penalty_save * probability_save * assist_probability * prob_of_no_redcard * prob_of_no_yellowcard * prob_of_no_goals_conceded * probability_of_clean_sheet * probability_no_own_goals
        GK.append((overall_positive_probability, player_name))
    if player_pos == 1:
        overall_positive_probability = goal_scoring_probability * assist_probability *  prob_of_no_redcard * prob_of_no_yellowcard * prob_of_no_goals_conceded * probability_of_clean_sheet * probability_no_own_goals
        DF.append((overall_positive_probability, player_name))
    if player_pos == 2:
        overall_positive_probability = goal_scoring_probability * assist_probability *  prob_of_no_redcard * prob_of_no_yellowcard * probability_of_clean_sheet * probability_no_penalty_miss * probability_no_own_goals
        MID.append((overall_positive_probability, player_name))
    if player_pos == 3:
        overall_positive_probability = goal_scoring_probability * assist_probability *  prob_of_no_redcard * prob_of_no_yellowcard * probability_no_penalty_miss * probability_no_own_goals
        FW.append((overall_positive_probability, player_name))

print("GK")
print(GK)
print("DF")
print(DF)
print("MID")
print(MID)
print("FW")
print(FW)
    # print("goal scoring:", goal_scoring_probability)
    # print("goal assist:", assist_probability)
    # print("no red:", prob_of_no_redcard)
    # print("no yellow:", prob_of_no_yellowcard)
    # print("no_conceded:", prob_of_no_goals_conceded)
    # print("cleansheet:", probability_of_clean_sheet)
    # print("no_penalty_miss:", probability_no_penalty_miss)
    # print("proabaility_no_own_goals:", probability_no_own_goals)
    # print("probability_save:", probability_save)
    # print("probability_penalty_save", probability_penalty_save)
    # print(overall_positive_probability)
