import json
from json import *


def update(to_update: list) -> None:
    with open('foodproducts/products.json', 'w', encoding='windows-1251') as outfile:
        json.dump(to_update, outfile, ensure_ascii=False, indent=4)


def append(record) -> None:
    with open('foodproducts/products.json', 'r', encoding='windows-1251') as outfile:
        recorder = json.load(outfile)
        recorder.append(record)
        update(recorder)


def check_existance(name: str) -> bool:
    with open('foodproducts/products.json', 'r', encoding='windows-1251') as inputfile:
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

def change(name, protein, fats, carbohydrates, calories, price) -> str:
    if check_existance(name) is True:
        with open('foodproducts/products.json', 'r', encoding='windows-1251') as inputfile:
            checker = json.load(inputfile)
            for objects in checker:
                if objects['name'] == name:
                    objects['protein'] = protein
                    objects['fats'] = fats
                    objects['carbohydrates'] = carbohydrates
                    objects['calories'] = calories
                    objects['price'] = price
                    update(checker)
                    return 'Продукт успешно изменен'
            return 'Ошибка!'


def delete(name) -> str:
    with open('foodproducts/products.json', 'r', encoding='windows-1251') as infile:
        deleter = json.load(infile)
        for record in deleter:
            if record['name'] == name:
                deleter.remove(record)
                update(deleter)
                return 'Продукт успешно удален'
        return 'Такого продукта не существует'


def get_product_info(name) -> dict:
    with open('foodproducts/products.json', 'r', encoding='windows-1251') as infile:
        getter = json.load(infile)
        for record in getter:
            if record['name'] == name:
                return record


def get_products_list() -> list:
    with open('foodproducts/products.json', 'r', encoding='windows-1251') as infile:
        getter = json.load(infile)
        output = []
        for record in getter:
            output.append(record['name'])
        return output


def get_partial_food_price(name, mass) -> float:
    with open('foodproducts/products.json', 'r', encoding='windows-1251') as infile:
        getter = json.load(infile)
        for record in getter:
            if record['name'] == name:
                return (record['price']/record['mass'])*mass
        return 0.0
