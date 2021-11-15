import os

import json
from data_b.dp_control import get_cursor

all_files_names = os.listdir(path="C:/Users/andrt/PycharmProjects/ConTia/data_b/json")


def transfer_data_json():
    for file_name in all_files_names:
        print('------------------------------------------')
        print(file_name)

        with open(f'C:/Users/andrt/PycharmProjects/ConTia/data_b/json/{file_name}',
                  encoding='utf-8') as f:
            templates = json.load(f)
            count = 0
            for example_info in templates.values():
                task_info = {}
                keys = [i for i in templates.keys()]

                for i in example_info:
                    if 'Условие' in i:
                        task_info['conditions'] = i
                    elif 'Решение 2' in i:
                        task_info['decisions_2'] = i
                    elif ('Решение' in i) or ('Решение 1' in i):
                        task_info['decisions_1'] = i
                    elif 'Ответ' in i:
                        task_info['answer'] = i
                    elif ('Подсказка' in i) or ('Замечания' in i):
                        task_info['remarks'] = i
                convert_list = converter_string(task_info)
                # print(convert_list[0])
                # print(convert_list[1])

                file_name = file_name.split('.json')[0]

                cur = get_cursor()

                info = cur.execute(f'''SELECT id  FROM category 
                                    WHERE value = "{file_name}";''')
                for i in info:
                    id_category = i[0]

                print(keys[count])

                cur.execute(
                    f'''INSERT INTO tasks (id_category, title, href, subcategory, complexity, classes, {convert_list[0]})
                VALUES ("{id_category}", "{keys[count]}", "{example_info[0]}", "{example_info[1]}", "{example_info[2]}", "{example_info[3]}", {convert_list[1]});''')
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
            string_values += f'"{tk_1[i]}"'
        else:
            string_values += f'"{tk_1[i]}", '
    all_strings.append(string_insert)
    all_strings.append(string_values)
    return all_strings


if __name__ == '__main__':
    transfer_data_json()
