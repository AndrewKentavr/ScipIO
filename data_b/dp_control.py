import sqlite3

CONN = sqlite3.connect('C:/Users/andrt/PycharmProjects/ConTia/data_b/contia_dp.db')
cur = CONN.cursor()


def get_cursor():
    return cur


# -----------------------------TIMER-----------------------------------------

def timer_create_dp(user_id, time):
    cur.execute(f"""INSERT INTO Time (user_id, time)
VALUES ({user_id}, '{time}');""")
    cur.connection.commit()
    return


def timer_del_dp(user_id, time):
    cur.execute(f"""DELETE FROM Time
where user_id = '{user_id}' and time = '{time}';""")
    cur.connection.commit()
    return


def timer_info_dp(user_id):
    cur.execute(f"""SELECT time FROM Time
where user_id == '{user_id}';""")
    c = cur.fetchall()
    all_timers = list(map(lambda x: x[0], c))
    return all_timers


# -----------------------------ANYTHING-----------------------------------------

def problem_translate_name(name):
    cur.execute(f"""SELECT translate_category FROM category
    WHERE '{name}' = value;""")
    result = cur.fetchall()
    return result[0][0]


def problem_category_random(name_category, tasks_theme):
    cur = get_cursor()
    cur.execute(
        f"""SELECT title, href, subcategory, complexity, classes, conditions, decisions_1, decisions_2, answer, remarks FROM tasks_{tasks_theme}
                WHERE id_category = (SELECT id FROM category
                                WHERE value = '{name_category}')
                ORDER BY RANDOM()
                LIMIT 1;""")
    result_0 = cur.fetchall()
    result = []
    for i in result_0[0]:
        if i is not None:
            result.append(i)

    return result


def finding_categories_table(tasks_theme):
    cur.execute(f"""SELECT value, translate_category FROM category
        WHERE id in (SELECT DISTINCT id_category FROM tasks_{tasks_theme});""")
    result_0 = cur.fetchall()
    return result_0


# -----------------------------MATH-----------------------------------------


def problem_search_random():  # <--------  Эта функция вообще где-то применяется?
    cur.execute(f"""SELECT * FROM math_problems 
    ORDER BY RANDOM() LIMIT 1;""")
    result = cur.fetchall()
    return result[0]


def formulas_search_random():
    cur.execute(f"""SELECT formulas, answer, explanation FROM math_formulas 
    ORDER BY RANDOM() LIMIT 1;""")
    result = cur.fetchall()
    return result[0]


# -----------------------------LOGIC-----------------------------------------
