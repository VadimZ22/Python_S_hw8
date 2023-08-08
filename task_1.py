import csv
import json
import os
import pickle
from os.path import getsize, abspath, join

def get_directory_size(directory):
    directory = abspath(directory)
    total = 0
    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_directory_size(entry.path)
    except NotADirectoryError:
        return getsize(directory)
    except PermissionError:
        return 0
    return total

res_list =[]

def get_directory_items(path=os.getcwd()):
    for dir_path, dir_name, file_name in os.walk(path):
        dict = {
            f'Родительская директория': dir_path,
            f'Вложенные директории': {dir: get_directory_size(join(dir_path, dir)) for dir in dir_name},
            f'Вложенные файлы':{file: getsize(join(dir_path, file)) for file in file_name}
        }
        res_list.append(dict)
    return res_list


def write_files(result):
    with open('new_JSON.json', 'w', encoding='UTF-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    with open('new_CSV.csv', 'w', newline='', encoding='utf-8') as f:
        csv_write = csv.DictWriter(f, fieldnames=['Родительская директория', 'Вложенные директории', 'Вложенные файлы'],
                                    dialect='excel-tab', quoting=csv.QUOTE_ALL)
        csv_write.writeheader()
        csv_write.writerows(result)

    with open('new_PICKLE', 'wb') as f:
        pickle.dump(result, f)



write_files(get_directory_items())
