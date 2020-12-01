import json

def def_type(a):
    if type(a) == bool:
        return 'boolean'
    elif type(a) == str:
        return 'string'
    elif type(a) == dict:
        return 'object'
    elif type(a) == int:
        return 'integer'
    elif type(a) == list:
        return 'array'
    return 'null'

list_of_files = [r'C:\Users\rusel\Desktop\1234\Новая папка\task_folder\event\ba25151c-914f-4f47-909a-7a65a6339f34.json',
                 r'C:\Users\rusel\Desktop\1234\Новая папка\task_folder\event\cc07e442-7986-4714-8fc2-ac2256690a90.json',
                 r'C:\Users\rusel\Desktop\1234\Новая папка\task_folder\event\1eba2aa1-2acf-460d-91e6-55a8c3e3b7a3.json']

filename = r'C:\Users\rusel\Desktop\1234\Новая папка\task_folder\schema\label_selected.json'
with open(filename) as file:
    scheme = json.load(file)

required, properties = scheme['required'], scheme["properties"]
labels, user = properties['labels'], properties['user']
labels_properties = labels['items']['properties']
for filenames in list_of_files:
    filename1 = filenames
    with open(filename1) as file:
        data = json.load(file)

    scheme_name = 'label_selected'
    data_name = data["event"]
    if data_name != scheme_name:
        print(f'В файле {filename1} не совпадают имя со схемой {filename}')

    data = data['data']

    # данные которые есть в обрабатываем файле
    if type(data) != dict:
        print(f'В файле {filename1} тип данных "data" не верный')
    else:
        dataValue = tuple({i for i in data} & {j for j in required})
        if len(dataValue) == 0:
            print(f'В файле{filename1} отсуствуют требуемые значения')
        else:
            # данные которых нет в обрабатываемом файле
            no_value_in_file = set(required) - set(dataValue)
            print(f'Значений {no_value_in_file} не хватает в файле {filename1}')

            # сравнение type данных в файле со схемой
            for i in dataValue:

                if type(properties[i]['type']) == list:
                    if def_type(data[i]) != properties[i]['type'][0] and def_type(data[i]) != properties[i]['type'][1]:
                        print(f'Тип данных f{data[i]} не верный')
                else:
                    if def_type(data[i]) != properties[i]['type']:
                        print(f'Тип данных f{data[i]} не верный')

        if 'labels' in dataValue:
            labels_in_data = (set(j for i in data['labels'] for j in i) & set(i for i in labels['items']['required']))
            for i in labels_in_data:
                if type(labels_properties[i]['type']) == list:
                    if def_type(data['labels'][0][i]) != labels_properties[i]['type'][0] \
                            and def_type(data['labels'][0][i]) != labels_properties[i]['type'][1]:
                        print(f'Тип данных {data["labels"][0][i]} не верный')
                else:
                    if def_type(data['labels'][0][i]) != labels_properties[i]['type']:
                        print(f'Тип данных {data["labels"][0][i]} не верный')
        if 'user' in dataValue:
            user_in_data = (set(i for i in properties['user']['required'])
                            & set(i for i in data['user']))
            no_value_in_user_data = set(set(i for i in properties['user']['required']) - user_in_data)
            if len(no_value_in_user_data) != 0:
                print(f'Значений {no_value_in_user_data} не хватает в {data["user"]} ')
            if len(user_in_data) != 0:
                for i in user_in_data:
                    if def_type(data['user'][i]) != properties['user']['properties'][i]['type']:
                        print(f'Тип данных {data["user"][i]} неверный')

