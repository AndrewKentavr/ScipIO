import matplotlib.pyplot as plt


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
    fig.savefig(f'handlers/statistics/data_figure/{telegram_user_id}.png', dpi=100)
    return
