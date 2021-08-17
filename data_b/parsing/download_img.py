from os.path import basename

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent

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

url = 'https://www.problems.ru/view_problem_details_new.php?id=88113'
gg = 'https://hsto.org/r/w1560/getpro/habr/upload_files/352/6c7/860/3526c78601c0097052d02e176a8271c5.png'

req = requests.get(url, form_data, headers=headers)
src = req.text
soup = BeautifulSoup(src, "lxml")

for link in soup.select("img"):
    lnk = link["src"]
    if "show_document" in lnk:
        print(lnk)
        with open(basename('https://www.problems.ru/' + lnk), "wb") as f:
            f.write(requests.get('https://www.problems.ru/' + lnk).content)

