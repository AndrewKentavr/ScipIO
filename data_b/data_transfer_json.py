import os

import json

print(os.listdir(path="C:/Users/andrt/PycharmProjects/ConTia/data_b/json"))

with open('C:/Users/andrt/PycharmProjects/ConTia/data_b/json/set_theory.json', encoding='utf-8') as f:
    templates = json.load(f)
    count = 0
    for i in templates.values():
        print('--------------------------')
        # print(i)
        list_cat = i[4:]
        for j in list_cat:
            if '\xa0' in j:
                text = j.replace("\xa0", " ")
            if '\r' in j:
                text = j.replace("\r", " ")

                print(text)
        if count > 1:
            exit()
        count += 1
