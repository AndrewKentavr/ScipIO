import json
import re

with open('Logic.json', encoding='utf-8') as f:
    templates = json.load(f)
    count = 0
    for i in templates.values():
        list_cat = i[4:]
        for j in list_cat:
            print(j)
        if count != 0:
            exit()
        print(i)
        count += 1