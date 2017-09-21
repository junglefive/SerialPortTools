import sqlite3 as lite
import sys

con = None

try:
    con = lite.connect('test.db')
    cur = con.cursor()
    cur.execute('select sqlite_version()')
    data = cur.fetchone()
    print("version: %s"  %data)

    cur.execute("CREATE TABLE IF NOT EXISTS jh(Id TEXT, product TEXT)")
    cur.execute("INSERT INTO jh VALUES('3510', 'fail')")
    cur.execute("INSERT INTO jh VALUES('3520', 'fail')")
    cur.execute("INSERT INTO jh VALUES('3530', 'fail')")
    cur.execute("SELECT * FROM jh")
    jh = cur.fetchall()
    for row in jh:
        print(row)

except Exception as e:
    print(str(e))
    # sys.exit(1)

finally:
    pass
    if con:
        con.close()
    input()