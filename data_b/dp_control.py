import datetime
import sqlite3

import pytz

CONN = sqlite3.connect('data_b/scipio.db')
cur = CONN.cursor()


def get_cursor():
    return cur


# -----------------------------Users-----------------------------------------
def dp_all_users_list():
    cur.execute("""SELECT telegram_user_id FROM users;""")
    result = cur.fetchall()
    users_telegram_id_list = [i[0] for i in result]
    return users_telegram_id_list


def dp_user_create(telegram_user_id):
    cur.execute(f"""INSERT INTO users (telegram_user_id, date_reg)
VALUES ({telegram_user_id}, '{datetime.datetime.now()}');""")
    cur.connection.commit()
    return


# -----------------------------ANYTHING-----------------------------------------


def dp_all_telegram_id_flc_list():
    cur.execute("""SELECT DISTINCT user_id FROM flashcards;""")
    result = cur.fetchall()
    flashcards_telegram_id_list = [i[0] for i in result]
    return flashcards_telegram_id_list


def dp_all_telegram_id_time_list():
    cur.execute("""SELECT DISTINCT user_id FROM time;""")
    result = cur.fetchall()
    time_telegram_id_list = [i[0] for i in result]
    return time_telegram_id_list


def problem_translate_name(name):
    cur.execute(f"""SELECT translate_category FROM category
    WHERE '{name}' = value;""")
    result = cur.fetchall()
    return result[0][0]


def problem_category_random(name_category, tasks_theme):
    """
    :param name_category: Название категории вида: 'fractions'
    :param tasks_theme: Передаётся название таблици
    из которой будут брать задачи. Например: 'math'

    :return: Вся информация В СЛОВАРЕ, что есть по задаче. Например в задаче
    2 Условия и Ответ. Значит так и будет передоваться
    """
    cur.execute(
        f"""SELECT id, title, href, subcategory, complexity, classes, conditions, decisions_1, 
        decisions_2, answer, remarks FROM tasks_{tasks_theme}
                WHERE id_category = (SELECT id FROM category
                                WHERE value = '{name_category}')
                ORDER BY RANDOM()
                LIMIT 1;""")
    columns = ['id', 'title', 'href', 'subcategory', 'complexity', 'classes', 'conditions', 'decisions_1',
               'decisions_2', 'answer', 'remarks']
    result_0 = cur.fetchall()
    result = {}

    for i in range(len(result_0[0])):
        if result_0[0][i] is not None:
            result[columns[i]] = result_0[0][i]
        else:
            result[columns[i]] = ''

    return result


def finding_categories_table(tasks_theme):
    cur.execute(f"""SELECT value, translate_category FROM category
        WHERE id in (SELECT DISTINCT id_category FROM tasks_{tasks_theme});""")
    result_0 = cur.fetchall()
    return result_0


def finding_main_categories_table(tasks_theme):
    cur.execute(f"""SELECT main_value, main_translate_category FROM category
        WHERE id in (SELECT DISTINCT id_category FROM tasks_{tasks_theme});""")
    result_0 = set(cur.fetchall())
    return result_0


def finding_one_categories_table(tasks_theme):
    cur.execute(f"""SELECT value, translate_category FROM category
        WHERE main_value = '{tasks_theme}';""")
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
# -----------------------------FLASHCARD-----------------------------------------
def flashcard_dp_create(user_id, front, back, show):
    cur.execute(f"""INSERT INTO flashcards (user_id, front_card, back_card, show_card)
VALUES ({user_id}, '{front}', '{back}', {show});""")  # Без этого новые карточки не сохранялись
    cur.connection.commit()
    return


def flashcard_dp_info(user_id):
    cur.execute(f"""select id, front_card, back_card from flashcards
            where user_id = {user_id};""")
    result = cur.fetchall()
    return result


def flashcard_dp_info_game(user_id):
    cur.execute(f"""select id, front_card, back_card, show_card from flashcards
            where user_id = {user_id}""")
    result = cur.fetchall()
    return result


def flashcard_del(user_id, front_card, back_card):
    cur.execute(f"""DELETE FROM flashcards
        where user_id = {user_id} and front_card = '{front_card}' and back_card = '{back_card}';""")
    cur.connection.commit()
    return


def flashcard_one(user_id, id):
    cur.execute(f"""select id, front_card, back_card from flashcards
                where user_id = {user_id} and id = {id};""")
    result = cur.fetchall()
    return result


# -----------------------------TIMER-----------------------------------------

def timer_create_dp(user_id, time, tasks):
    cur.execute(f"""INSERT INTO Time (user_id, time, tasks)
VALUES ({user_id}, '{time}', '{tasks}');""")
    cur.connection.commit()
    return


def timer_del_dp(user_id, time):
    cur.execute(f"""DELETE FROM Time
where user_id = {user_id} and time = '{time}';""")
    cur.connection.commit()
    return


def timer_info_dp(user_id):
    cur.execute(f"""SELECT time FROM Time
where user_id == {user_id};""")
    c = cur.fetchall()
    all_timers = list(map(lambda x: x[0], c))
    return all_timers


def dp_timer_circle_user_time(time_now):
    cur.execute(f"""SELECT user_id, tasks FROM Time
                    where time == '{time_now}';""")
    results = cur.fetchall()
    return results


# -----------------------------add_action-----------------------------------------
def action_add(telegram_user_id, action, correct=None, id_category=None):
    """
    :param action: 'flc', 'mentally_math', 'cat_logic', 'cat_math'
    :param correct: добавляется для flashcard и mentally_math
    :param id_category: нужно только когда это задача из category
    """

    # ---------Данный алгоритм, лишь на короткое время-------------
    all_users_list = dp_all_users_list()
    if telegram_user_id not in all_users_list:
        dp_user_create(telegram_user_id)
    # -------------------------------------------------------------

    if id_category == None:
        id_category = 'Null'

    if correct == None:
        correct = 'Null'

    cur.execute(f"""INSERT INTO actions (telegram_user_id, action, correct, time_action, id_category)
VALUES ({telegram_user_id}, '{action}', {correct}, '{datetime.datetime.now()}', {id_category});""")
    cur.connection.commit()
    return


# -----------------------------statistics-----------------------------------------
def stat_general_bd(telegram_user_id):
    """
    :param
    :return: info[0] - количество показов flashcard(flc)
             info[1] - количество попыток mentally_math
             info[2] - количество показов category_math
             info[3] - количество показов category_logic
    """
    cur.execute(f"""SELECT count(*) AS flc, 
(SELECT count(*) FROM actions WHERE action='men_math' and telegram_user_id={telegram_user_id}) AS men_math,
(SELECT count(*) FROM actions WHERE action='cat_math' and telegram_user_id={telegram_user_id}) AS cat_math,
(SELECT count(*) FROM actions WHERE action='cat_logic' and telegram_user_id={telegram_user_id}) AS cat_logic
FROM actions WHERE action='flc' and telegram_user_id={telegram_user_id};""")
    info = cur.fetchall()
    return info


def stat_bar_general(telegram_user_id):
    """
    Вся данная функция работает очень медленно и требует дальнейшей доработки
    """

    time_moscow = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    arr_time_week = [(time_moscow - datetime.timedelta(days=6 - i)).strftime("%m-%d") for i in range(7)]

    list_time = []
    actions = ['flc', 'men_math', 'cat_math', 'cat_logic']

    for action in actions:
        cur.execute(f"""SELECT time_action FROM actions
        WHERE action='{action}' and telegram_user_id={telegram_user_id} and (strftime('%m-%d', `time_action`) = '{arr_time_week[0]}' or strftime('%m-%d', `time_action`) = '{arr_time_week[1]}' or strftime('%m-%d', `time_action`) = '{arr_time_week[2]}' or strftime('%m-%d', `time_action`) = '{arr_time_week[3]}' or strftime('%m-%d', `time_action`) = '{arr_time_week[4]}' or strftime('%m-%d', `time_action`) = '{arr_time_week[5]}' or strftime('%m-%d', `time_action`) = '{arr_time_week[6]}');""")
        list_time.append([i[0][5:10] for i in cur.fetchall()])

    return list_time

# -----------------------------main-----------------------------------------

# https://cloud.google.com/bigquery/docs/reference/standard-sql/arrays
