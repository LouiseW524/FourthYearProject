import json
import re
import psycopg2
from lxml import html
import requests
import calendar
from datetime import datetime as dt
from login_details import DB_PASSWORD, DB_USER

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER,DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor()
data = json.load(open('C:/Users/louis/Downloads/english-premier-league-match-data/datafile/season16-17/season_match_stats.json'))

def get_gameweek_dates():
    page = requests.get("http://www.worldfootball.net/all_matches/eng-premier-league-2016-2017/")
    tree = html.fromstring(page.content)
    gameweeks = tree.xpath('//a/text()')
    date_reg_exp = re.compile('(\d+[-/]\d+[-/]\d+)')
    date_list = []
    gameweek = {}

    for game in gameweeks:
        if 'Round' in game:
            round = game.split(".")
            date_list.clear()
            date_list.append(round[0])

        matches_list = date_reg_exp.findall(game)
        if (matches_list):
            date_list.append(matches_list)
        if len(date_list) > 1:
            gameweek[int(date_list[0])] = date_list[1]
    return gameweek


match_id_dict = {}
date_string = ''
home_team = ''
for key, value in data.items():
    away_team = value['away_team_id']
    home_team = value['home_team_id']
    date  = str(value['date_string'])
    date  = date.split()
    date = dt.strptime( date[0], "%d/%m/%Y")
    scores = value['full_time_score'].split(":")
    homegoalconceded = scores[0]
    awaygoalconceded = scores[1]

    match_id_dict[key] = (home_team,away_team,homegoalconceded,awaygoalconceded,date)

#for key,value in match_id_dict.items():
 #   sql = """INSERT INTO match (matchid, hometeamid,awayteamid,hometeamgoalsconceded,awayteamgoalsconceded,Date)
  #     VALUES (%s, %s , %s, %s , %s, %s)"""
   # data = (key, value[0], value[1], value[2], value[3], value[4])
    #cur.execute(sql, data)

gameweek = get_gameweek_dates()

cur.execute("""SELECT * FROM match ORDER BY date""")
all_matches = cur.fetchall()
week = 0

for match in all_matches:
    date = dt.strptime(str(match[5]), "%Y-%m-%d")
    for key,value in gameweek.items():
        gameweek_start_date = dt.strptime(str(value[0]), "%d/%m/%Y")
        if key == len(gameweek):
            week = key
            cur.execute("""UPDATE match SET week = %s WHERE matchid  = %s """, (week, match[0]))

        else:
            next_gameweek_date = dt.strptime(str(gameweek[key + 1][0]), "%d/%m/%Y")
            if (date >= gameweek_start_date) & (date < next_gameweek_date):
                week = key
                cur.execute("""UPDATE match SET week = %s WHERE matchid  = %s """, (week, match[0]))
                break