import json
from json import *


def check_existance(name: str, file: str) -> bool:
    with open(file, 'r', encoding='ISO-8859-5') as f:
        checker = json.load(f)
        for objects in checker:
            if objects['name'] == name:
                return True
        return False


def update(to_update: list, file: str) -> None:
    with open(file, 'w', encoding='ISO-8859-5') as f:
        json.dump(to_update, f, ensure_ascii=False, indent=4)


def append(record: list, file: str) -> None:
    to_append = open_json_to_read(file)
    to_append.append(record)
    update(to_append, file)


def open_json_to_read(file: str) -> list:
    with open(file, 'r', encoding='windows-1251') as f:
        read_list = json.load(f)
        return read_list

