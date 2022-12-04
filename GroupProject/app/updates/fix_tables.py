import pymysql
import sys
from datetime import date
import csi3335fa2022 as cfg

con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'], password=cfg.mysql['password'],
                      db=cfg.mysql['database'])

try:
    cur = con.cursor()

    # Fix teams table
    sql = "ALTER TABLE teamsUpd ADD COLUMN teamSIdent char(3) NOT NULL"
    cur.execute(sql)
    sql = "UPDATE teamsUpd SET teamSIdent = teamID"
    cur.execute(sql)
    sql = "ALTER TABLE teamsUpd MODIFY teamID char(7) NOT NULL"
    cur.execute(sql)
    sql = "UPDATE teamsUpd SET teamID = CONCAT(teamSIdent, yearID)"
    cur.execute(sql)
    sql = "ALTER TABLE teamsUpd ADD PRIMARY KEY(teamID)"
    cur.execute(sql)
    sql = "ALTER TABLE teamsUpd DROP COLUMN ID"
    cur.execute(sql)

    # Fix batting table
    sql = "ALTER TABLE battingUpd ADD COLUMN teamSIdent char(3) NOT NULL"
    cur.execute(sql)
    sql = "UPDATE battingUpd SET teamSIdent = teamID"
    cur.execute(sql)
    sql = sql = "ALTER TABLE battingUpd MODIFY teamID char(7) NOT NULL"
    cur.execute(sql)
    sql = "UPDATE battingUpd SET teamID = CONCAT(teamSIdent, yearID)"
    cur.execute(sql)

    # Fix pitching table
    sql = "ALTER TABLE pitchingUpd ADD COLUMN teamSIdent char(3) NOT NULL"
    cur.execute(sql)
    sql = "UPDATE pitchingUpd SET teamSIdent = teamID"
    cur.execute(sql)
    sql = sql = "ALTER TABLE pitchingUpd MODIFY teamID char(7) NOT NULL"
    cur.execute(sql)
    sql = "UPDATE pitchingUpd SET teamID = CONCAT(teamSIdent, yearID)"
    cur.execute(sql)

except Exception:
    con.rollback()
    print("Database exception.")
    raise
else:
    con.commit()
finally:
    con.close()
