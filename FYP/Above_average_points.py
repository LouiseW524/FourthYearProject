import psycopg2

from login_details import DB_PASSWORD, DB_USER

conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER, DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor()

sum = 0
count = 0

cur.execute("""SELECT playerpoints FROM training_player_points_per_match""")
all_points  = cur.fetchall()
for num in all_points:
   sum = sum + float(num[0])
   count = count + 1

average_points_per_player = (sum/count)

cur.execute("""SELECT * FROM training_player_points_per_match""")
stats = cur.fetchall()

for player in stats:
   if float(player[2]) > average_points_per_player:
      cur.execute("""UPDATE training_player_match_stats SET above_average_points = 1 WHERE playerid = %s AND matchid = %s""",(player[0], player[1]))
   else:
      cur.execute(
         """UPDATE training_player_match_stats SET above_average_points = 0 WHERE playerid = %s AND matchid = %s""",(player[0], player[1]))




