# from sqlite_dp import *

import sqlite3

CONN = sqlite3.connect('C:/Users/andrt/PycharmProjects/ConTia/dp/contia_dp.db')


def timer_create_dp(id_user, time):
    cur = CONN.cursor()
    cur.execute(f"""INSERT INTO Time (id_user, time)
VALUES ({id_user}, '{time}');""")
    CONN.commit()
    cur.close()
    CONN.close()
