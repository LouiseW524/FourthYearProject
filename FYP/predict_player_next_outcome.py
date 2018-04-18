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
        cur.execute("""SELECT saves FROM player_match_stats WHERE playerid = %s""", (player_id,))
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
    return single_value/count_matches_played_by_player

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
    if cell_for_sql ==2 :
        cur.execute("""SELECT cleansheet FROM player_match_stats WHERE playerid = %s """, (player_id[0],))

    goals_list = cur.fetchall()
    results = 0
    for goal in goals_list:
        if int(goal[0]) == 0:
            results += 1
    prob_no_conceded = results / count_matches_played_by_player
    return prob_no_conceded
if len(sys.argv[1]) > 1 & len(sys.argv[2]) :
    cur.execute("""SELECT DISTINCT playerid FROM teamlist where teamid = %s OR teamid = %s""", (sys.argv[1],sys.argv[2]) )
    all_player_ids = cur.fetchall()
else:
    print("not enough arguments")
    exit()

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
    proabaility_no_own_goals = 1 - probability_own_goals

# saves
    probability_save = get_probablity(player_id[0],7,count_matches_played_by_player)

#  penaltysaves
    probability_penalty_save = get_probablity(player_id[0],8,count_matches_played_by_player)

    print(player_id)
    print(goal_scoring_probability,assist_probability,prob_of_no_redcard,prob_of_no_yellowcard, prob_of_no_goals_conceded,probability_of_clean_sheet,probability_no_penalty_miss,proabaility_no_own_goals,probability_save,probability_penalty_save)
