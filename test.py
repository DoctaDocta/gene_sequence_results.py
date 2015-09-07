import sqlite3 as lite
import sys


#LEARNING HOW TO USE SQL TO MAKE TABLES OF THE GENE INFO.
# WILL EXTEND THIS TO MAKE A TABLE FOR EACH SAMPLE NAME
# AND MAKE TABLE IN REAL TIME WHILE INFO IS BEING READ IN ANALYZE.PY

geneIds = [
	['alpha|2133', 1, 'TCGA-CHOL-68-393','TN'],
    ['alpha|123123', 2, 'TCGA-CHOL-G8-393','TN'],
    ['alpha|123', 1, 'TCGA-CHOL-V8-393','NT'],
    ['alpha|123234134', 3, 'TCGA-CHOL-B8-393','NT'],
    ['alpha|234', 2, 'TCGA-CHOL-A8-44493','TN'],
    ['alpha|2222', 2, 'TCGA-CHOL-A6-393','NT'],
    ['alpha|227', 2, 'TCGA-CHOL-A8-393','TN']
]


con = lite.connect('test.db')

with con:

    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS genes")
    cur.execute("CREATE TABLE genes (id int, name text, price int, day int)")
    cur.executemany('INSERT INTO genes VALUES (?,?,?,?)', geneIds)

    cur.execute("SELECT * FROM genes")

    rows = cur.fetchall()

    for row in rows:
        print row
