import pymysql
import csi3335 as cfg

con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'], password=cfg.mysql['password'],
                      db=cfg.mysql['database'])

try:
    cur = con.cursor()

    sql = '''create table seriespostUpd(
    ID int primary key auto_increment, 
    teamIDwinner char(7),
    teamIDloser char(7),
    yearID smallint(6),
    round char(5),
    wins smallint(6),
    losses smallint(6),
    ties smallint(6),
    teamSIdentW char(3),
    teamSIdentL char(3)
    );'''
    cur.execute(sql)
    sql = '''IN-SERT INTO seriespostUpd (ID, teamSIdentW, teamSIdentL, yearID, round, wins, losses, ties) 
    SELECT ID, teamIDwinner, teamIDloser, yearID, round, wins, loses, ties FROM seriespost ORDER BY ID'''
    cur.execute(sql)

    sql = "UPDATE seriespostUpd SET teamIDwinner = CONCAT(teamSIdentW, yearID), teamIDLoser = CONCAT(teamSIdentL, yearID)"
    cur.execute(sql)

    post = open("seriespost.txt", "r")
    postTable = post.readlines()[1:]

    counter = 367

    for line in postTable:
        counter += 1
        split = line.split(",")

        params = (split[2], 2022)
        sql = '''SELECT teamID FROM teamsUpd WHERE team_name = %s AND yearID = %s'''
        cur.execute(sql, params)
        results = cur.fetchall()
        teamIDWinner = results[0][0]

        params = (split[3], 2022)
        sql = '''SELECT teamID FROM teamsUpd WHERE team_name = %s AND yearID = %s'''
        cur.execute(sql, params)
        results = cur.fetchall()
        teamIDLoser = results[0][0]

        params = (counter, teamIDWinner, teamIDLoser, 2022, split[4].replace("\n", ""), int(split[0]), int(split[1]), 0, teamIDWinner[0:3], teamIDLoser[0:3])
        sql = '''INSERT INTO seriespostUpd (ID, teamIDwinner, teamIDloser, yearID, round, wins, losses, ties, teamSIdentW, teamSIdentL)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cur.execute(sql, params)

except Exception:
    con.rollback()
    print("Database exception.")
    raise
else:
    con.commit()
finally:
    con.close()
