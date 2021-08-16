import json
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

from random import randrange
from time import sleep
from math import ceil


def checking_quantity_start():
    number_tasks_0 = [tag for tag in soup.select('div[id]')][2].text.split('\n')[1]
    number_tasks_1 = number_tasks_0.split('Всего задач: ')[1]
    number_tasks_2 = int(number_tasks_1.split(']')[0])
    number_start = ceil(number_tasks_2 / 100)
    return number_start


def add_example_info(soup):
    table_example = soup.find_all(class_="problemsmallcaptiontable")
    for i in table_example[::3]:
        all_info = []
        href = i.find(class_="componentboxlink")
        all_info.append(href.text.split('\n\t\t\t\t\t\t')[1])
        all_info.append('https://www.problems.ru' + href.get("href"))
        all_info.append(
            i.find(class_="problemsmallsubjecttablecell").find(class_="componentboxlink").text.split('\t\t\t\t\t\t\t')[
                1].split('\t')[1])
        difficult = (i.find(class_="problemsmalldifficulty").find_all('nobr'))
        for i in difficult:
            all_info.append(i.text)
        all_examples_hrefs.append(all_info)


url = "https://www.problems.ru/view_by_subject_new.php"
all_examples_hrefs = []
problems_dict = {}

headers = {
    "Accept": "*/*",
    "User-Agent": generate_user_agent()
}

form_data = {
    'parent': 79,
    'start': 0,
    'viewing_params[view_amount]': 100,
    'difficulty_min': 2,
    'difficulty_max': 10,
    'grade_min': 8,
    'grade_max': 11
}

req = requests.get(url, form_data, headers=headers)
src = req.text
soup = BeautifulSoup(src, "lxml")

add_example_info(soup)

number_start = checking_quantity_start()
if number_start > 1:
    for page in range(number_start - 1):
        sleep(randrange(2, 4))
        page += 1
        headers = {
            "Accept": "*/*",
            "User-Agent": generate_user_agent()
        }

        form_data = {
            'parent': 79,
            'start': page,
            'viewing_params[view_amount]': 100,
            'difficulty_min': 2,
            'difficulty_max': 10,
            'grade_min': 8,
            'grade_max': 11
        }

        req = requests.get(url, form_data, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        add_example_info(soup)

for i in range(len(all_examples_hrefs)):
    item = all_examples_hrefs[i]
    id = item[0]

    problems_dict[id] = item[1:]

with open("Logic.json", "w", encoding="utf-8") as file:
    json.dump(problems_dict, file, indent=4, ensure_ascii=False)
