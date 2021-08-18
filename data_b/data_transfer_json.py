import json



with open('C:/Users/andrt/PycharmProjects/ConTia/data_b/json/logic.json', encoding='utf-8') as f:
    templates = json.load(f)
    count = 0
    for i in templates.values():
        print('--------------------------')
        list_cat = i[4:]
        for j in list_cat:
            print(j)
        if count > 1:
            exit()
        count += 1