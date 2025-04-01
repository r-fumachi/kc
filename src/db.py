from sqlite3 import *


DB = "data/database.db"


def generate_clist() -> Cursor:
    con = connect(DB)
    cur = con.cursor()
    if ("clist",) not in cur.fetchall():
        cur.execute("CREATE TABLE clist(favorited, id, indexed, name, service, updated)")
