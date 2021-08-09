import sqlite3
from handlers.timer.class_timer import ALL_TIMERS, Timer


def check_timer_func(dp):
    CONN = sqlite3.connect('C:/Users/andrt/PycharmProjects/ConTia/dp/contia_dp.db')
    cur = CONN.cursor()
    cur.execute("SELECT * FROM time;")
    all_results = cur.fetchall()
    all_time_dp = [i[1] for i in all_results]
    s = ALL_TIMERS.keys()
    all_time = [i for i in s]
    exceptions = list(set(all_time_dp) - set(all_time))
    if exceptions:
        for msg in exceptions:
            time_msg = msg.split('_')
            hour, min = int(time_msg[0]), int(time_msg[1])
            Timer(dp, hour, min, user_id)
