import psycopg2
from lxml import html
import requests
import re

gameweek = {}
page = requests.get("http://www.worldfootball.net/all_matches/eng-premier-league-2016-2017/")
tree = html.fromstring(page.content)
gameweeks = tree.xpath('//a/text()')
date_reg_exp = re.compile('(\d+[-/]\d+[-/]\d+)')
date_list = []
round = []
gameweek = {}

for game in gameweeks:
    if 'Round' in game:
        round = game.split(".")
        date_list.clear()
        date_list.append(round[0])

    matches_list = date_reg_exp.findall(game)
    if(matches_list):
        date_list.append(matches_list)
    if len(date_list) > 1:

        gameweek[int(date_list[0])] = date_list[1]
print(gameweek)