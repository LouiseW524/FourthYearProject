#!/usr/bin/python
import psycopg2
from login_details import DB_PASSWORD, DB_USER
conn = psycopg2.connect("dbname='fyp' user=%s host='localhost' password=%s" % (DB_USER, DB_PASSWORD))
conn.set_isolation_level(0)
cur = conn.cursor()

import sys

#cur.execute("""SELECT * FROM teamlist where matchid = %s """, (match_id, team_id))
#conceded = cur.fetchall()

print('Argument List:', sys.argv[1])