import pymysql
import csi3335 as cfg

con = pymysql.connect(host=cfg.mysql['location'], user=cfg.mysql['user'], password=cfg.mysql['password'],
                      db=cfg.mysql['database'])

try:
    cur = con.cursor()

    bat = open("MLBBatting.txt", "r")
    pitch = open("MLBPitching.txt", "r")
    field = open("MLBFielding.txt", "r")

    batTable = bat.readlines()[1:]
    pitchTable = pitch.readlines()[1:]
    fieldTable = field.readlines()[1:]

    counter = 0

    for line in batTable:
        batLine = batTable[counter]
        pitchLine = pitchTable[counter]
        fieldLine = fieldTable[counter]

        batSplit = batLine.split(",")
        pitchSplit = pitchLine.split(",")
        fieldSplit = fieldLine.split(",")

        lgID = batSplit[29]
        team_name = batSplit[0]
        team_G = int(float(batSplit[4]))
        team_W = int(float(pitchSplit[4]))
        team_L = int(float(pitchSplit[5]))
        team_R = int(float(batSplit[7]))
        team_AB = int(float(batSplit[6]))
        team_H = int(float(batSplit[8]))
        team_2B = int(float(batSplit[9]))
        team_3B = int(float(batSplit[10]))
        team_HR = int(float(batSplit[11]))
        team_BB = int(float(batSplit[14]))
        team_SO = int(float(batSplit[15]))
        team_SB = int(float(batSplit[12]))
        team_CS = int(float(batSplit[13]))
        team_HBP = int(float(batSplit[23]))
        team_SF = int(float(batSplit[25]))
        team_RA = int(float(pitchSplit[17]))
        team_ER = int(float(pitchSplit[18]))
        team_ERA = int(float(pitchSplit[7]))
        team_CG = int(float(pitchSplit[11]))
        team_SHO = int(float(pitchSplit[12]))
        # team_SV =
        team_IPouts = int(float(pitchSplit[15])) * 3
        team_HA = int(float(pitchSplit[16]))
        team_HRA = int(float(pitchSplit[19]))
        team_BBA = int(float(pitchSplit[20]))
        team_SOA = int(float(pitchSplit[22]))
        team_E = int(float(fieldSplit[11]))
        team_DP = int(float(fieldSplit[12]))
        team_FP = int(float(fieldSplit[13]))
        # park_name =
        # team_attendance =
        # team_BPF =
        # team_PPF =

        print(team_name)

        teamSearchName = team_name
        if team_name == "Cleveland Guardians":
            teamSearchName = "Cleveland Indians"

        params = (teamSearchName)
        sql = '''SELECT DISTINCT teamSIdent FROM teamsUpd WHERE team_name = %s ORDER BY yearID DESC'''
        cur.execute(sql,params)
        results = cur.fetchall()
        SIdent = results[0][0]

        divID = "W"
        if team_name != "Los Angeles Angels":
            params = (teamSearchName)
            sql = '''SELECT divID FROM teamsUpd WHERE team_name = %s AND divID IS NOT NULL ORDER BY yearID DESC'''
            cur.execute(sql, params)
            results = cur.fetchall()
            divID = results[0][0]

        teamID = SIdent + "2022"

        params = (teamID, lgID, divID, team_name, team_G, team_W, team_L, team_R, team_AB, team_H, team_2B, team_3B,
                  team_HR, team_BB, team_SO, team_SB, team_CS, team_HBP, team_SF, team_RA, team_ER, team_ERA, team_CG,
                  team_SHO, team_IPouts, team_HA,
                  team_HRA, team_BBA, team_SOA, team_E, team_DP, team_FP, SIdent)
        sql = '''INSERT INTO teamsUpd (teamID, yearID, lgID, divID, team_name, team_G, team_W, team_L, team_R, team_AB, team_H,
        team_2B, team_3B, team_HR, team_BB, team_SO, team_SB, team_CS, team_HBP, team_SF, team_RA, team_ER, team_ERA,
        team_CG, team_SHO, team_IPouts, team_HA, team_HRA, team_BBA, team_SOA, team_E, team_DP, team_FP, teamSIdent)
        VALUES (%s, 2022, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s)'''
        cur.execute(sql, params)

        counter += 1

except Exception:
    con.rollback()
    print("Database exception.")
    raise
else:
    con.commit()
finally:
    con.close()
