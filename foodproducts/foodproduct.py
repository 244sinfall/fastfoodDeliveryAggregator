import json
from json import *


def update(list: list) -> None:
    with open('foodproducts/products.json', 'w') as outfile:
        json.dump(list, outfile, ensure_ascii=False)


def append(record) -> None:
    with open('foodproducts/products.json', 'r') as outfile:
        recorder = json.load(outfile)
        recorder.append(record)
        update(recorder)


def check_existance(name: str) -> bool:
    with open('foodproducts/products.json', 'r') as inputfile:
        checker = json.load(inputfile)
        for objects in checker:
            if objects['name'] == name:
                return True
        return False


def create(name, protein, fats, carbohydrates, calories, mass, price) -> str:
    if check_existance(name) is False:
        product_info = {
            "name": name,
            "protein": protein,
            "fats": fats,
            "carbohydrates": carbohydrates,
            "calories": calories,
            "mass": mass,
            "price": price
        }
        append(product_info)
        return 'Продукт успешно добавлен'
    else:
        return 'Продукт уже существует'


def delete(name) -> str:
    with open('foodproducts/products.json', 'r') as infile:
        deleter = json.load(infile)
        for record in deleter:
            if record['name'] == name:
                deleter.remove(record)
                update(deleter)
                return 'Продукт успешно удален'
        return 'Такого продукта не существует'


def get_product_info(name) -> dict:
    with open('foodproducts/products.json', 'r') as infile:
        getter = json.load(infile)
        for record in getter:
            if record['name'] == name:
                return record

