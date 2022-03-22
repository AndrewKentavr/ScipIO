from collections import Counter
import datetime

import pytz

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def pie_chart(info_general, telegram_user_id):
    flc, men_math, cat_math, cat_logic = info_general
    vals = [cat_math, cat_logic, men_math, flc]
    labels = ['Категория Математика', 'Категория Логики', 'Задачки в уме', 'Flashcards']
    color = ['#EF3038', '#FFCF40', '#DD80CC', '#1dceb2']
    fig = plt.figure(figsize=(5, 4), facecolor='#b7e5db')
    ax = fig.add_subplot()
    wedges, texts, autotexts = ax.pie(vals, labels=labels, colors=color, autopct='%.1f%%', startangle=90,
                                      textprops=dict(fontfamily="Arial"))
    plt.setp(texts, fontsize=10)
    plt.setp(autotexts, fontsize=10)
    # lgd = ax.legend(wedges, labels, title="Категории заданий", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    # text = ax.text(-0.2, 1.05, "Aribitrary text", transform=ax.transAxes)
    # fig.savefig('saved_figure.png', bbox_extra_artists=(lgd, text), bbox_inches='tight')
    ax.set_title('Процент всех задач', fontsize=18, fontweight='bold')
    fig.savefig(f'handlers/statistics/{telegram_user_id}.png', dpi=100)
    return


def bar_chart(list_time, telegram_user_id):
    time_moscow = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    arr_time_week_0 = [(time_moscow - datetime.timedelta(days=6 - i)).strftime("%m-%d %w").split() for i in
                       range(7)]
    arr_time_week_days = [i[1] for i in arr_time_week_0]
    arr_time_week = [i[0] for i in arr_time_week_0]
    arr_time_week_dict = Counter(dict.fromkeys(arr_time_week, [0, 0, 0, 0]))

    flc_0, men_math_0, cat_math_0, cat_logic_0 = list_time
    flc, men_math, cat_math, cat_logic = Counter(flc_0), Counter(men_math_0), Counter(cat_math_0), Counter(cat_logic_0)

    for time in arr_time_week_dict:
        if time in flc:
            flc_count = arr_time_week_dict[time][0] + flc[time]
            arr_time_week_dict[time] = [flc_count, arr_time_week_dict[time][1], arr_time_week_dict[time][2],
                                        arr_time_week_dict[time][3]]

        if time in men_math:
            men_math_count = arr_time_week_dict[time][1] + men_math[time]
            arr_time_week_dict[time] = [arr_time_week_dict[time][0], men_math_count, arr_time_week_dict[time][2],
                                        arr_time_week_dict[time][3]]

        if time in cat_math:
            cat_math_count = arr_time_week_dict[time][2] + cat_math[time]
            arr_time_week_dict[time] = [arr_time_week_dict[time][0], arr_time_week_dict[time][1], cat_math_count,
                                        arr_time_week_dict[time][3]]

        if time in cat_logic:
            cat_logic_count = arr_time_week_dict[time][3] + cat_logic[time]
            arr_time_week_dict[time] = [arr_time_week_dict[time][0], arr_time_week_dict[time][1],
                                        arr_time_week_dict[time][2], cat_logic_count]

    time_week_data = sorted(arr_time_week_dict.keys())
    flc_data = [arr_time_week_dict[i][0] for i in time_week_data]
    men_math_data = [arr_time_week_dict[i][1] for i in time_week_data]
    cat_math_data = [arr_time_week_dict[i][2] for i in time_week_data]
    cat_logic_data = [arr_time_week_dict[i][3] for i in time_week_data]

    rus_weekdays = {'0': 'Вс.', '1': 'Пон.', '2': 'Вт.', '3': 'Ср.', '4': 'Чет.', '5': 'Пт.', '6': 'Суб.'}

    x = [rus_weekdays[i] for i in arr_time_week_days]

    fig = plt.figure(figsize=(6, 5), facecolor='#b7e5db')
    ax = fig.add_subplot()

    ax.bar(x, flc_data, color='#1dceb2')
    ax.bar(x, men_math_data, bottom=flc_data, color='#DD80CC')
    ax.bar(x, cat_math_data, bottom=[sum(i) for i in zip(flc_data, men_math_data)], color='#EF3038')
    ax.bar(x, cat_logic_data, bottom=[sum(i) for i in zip(flc_data, men_math_data, cat_math_data)], color='#FFCF40')

    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    lgd = ax.legend(labels=['Flashcards', 'Задачки в уме', 'Категория Математика', 'Категория Логики'],
                    title="Категории заданий", loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    text = ax.text(-0.2, 1.05, 'Выполненые задачи за неделю', fontsize=18, fontweight='bold', transform=ax.transAxes)

    fig.savefig(f'handlers/statistics/{telegram_user_id}.png', bbox_extra_artists=(lgd, text),
                bbox_inches='tight')
    return
