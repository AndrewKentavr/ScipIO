import os

import json
from data_b.dp_math import get_cursor

all_files_names = os.listdir(path="C:/Users/andrt/PycharmProjects/ConTia/data_b/json")


def transfer_data_json():
    with open(f'C:/Users/andrt/PycharmProjects/ConTia/data_b/json/straight_lines_rays_segments_angles.json',
              encoding='utf-8') as f:
        templates = json.load(f)
        count = 0
        for example_info in templates.values():
            task_info = {}
            keys = [i for i in templates.keys()]

            for i in example_info:
                if 'Условие' in i:
                    task_info['conditions'] = i
                elif ('Решение' in i) or ('Решение 1' in i):
                    task_info['decisions_1'] = i
                elif 'Решение 2' in i:
                    task_info['decisions_2'] = i
                elif 'Ответ' in i:
                    task_info['answer'] = i
                elif ('Подсказка' in i) or ('Замечания' in i):
                    task_info['remarks'] = i
            convert_list = converter_string(task_info)
            print(convert_list[0])
            print(convert_list[1])

            cur = get_cursor()
            cur.execute(f"""INSERT INTO tasks (title, href, subcategory, complexity, classes, {convert_list[0]})
            VALUES ('{keys[count]}', '{example_info[0]}', '{example_info[1]}', '{example_info[2]}', '{example_info[3]}', {convert_list[1]});""")
            cur.connection.commit()

            count += 1


def converter_string(task_info):
    all_strings = []
    string_insert = ''
    string_values = ''

    tk_0 = [i for i in task_info.keys()]

    tk_1 = [i for i in task_info.values()]

    for i in range(len(tk_0)):
        if i + 1 == len(tk_0):
            string_insert += f'{tk_0[i]}'
        else:
            string_insert += f'{tk_0[i]}, '

    for i in range(len(tk_1)):
        if i + 1 == len(tk_1):
            string_values += f"'{tk_1[i]}'"
        else:
            string_values += f"'{tk_1[i]}', "
    all_strings.append(string_insert)
    all_strings.append(string_values)
    return all_strings


# for num_file in range(len(all_files_names)):
#     with open(f'C:/Users/andrt/PycharmProjects/ConTia/data_b/json/{all_files_names[num_file]}',
#               encoding='utf-8') as f:
#         templates = json.load(f)
#         count = 0
#         print(all_files_names[num_file])
#         for i in templates.values():
#             cat = True
#             if count != 0:
#                 cat = False
#             if not cat:
#                 break
#             cat = True
#             list_cat = i[4:]
#             for j in list_cat:
#                 print(j)
#             count += 1
#         print('**************************')
#         print()

if __name__ == '__main__':
    transfer_data_json()
