import json
from json import *

from foodproducts.foodproduct import get_product_info


def update(to_update: list) -> None:
    with open('foods/foods.json', 'w', encoding='windows-1251') as outfile:
        json.dump(to_update, outfile, ensure_ascii=False, indent=4)


def append(record) -> None:
    with open('foods/foods.json', 'r', encoding='windows-1251') as outfile:
        recorder = json.load(outfile)
        recorder.append(record)
        update(recorder)


def check_existance(name: str) -> bool:
    with open('foods/foods.json', 'r', encoding='windows-1251') as inputfile:
        checker = json.load(inputfile)
        for objects in checker:
            if objects['name'] == name:
                return True
        return False


def create(name, price, ingredients: dict) -> str:
    if check_existance(name) is False:
        product_info = {
            "name": name,
            "price": price,
            "ingredients": ingredients
        }
        append(product_info)
        return 'Блюдо успешно добавлено'
    else:
        return 'Блюдо уже существует'


def change(name, price, ingredients: dict) -> str:
    if check_existance(name) is True:
        with open('foods/foods.json', 'r', encoding='windows-1251') as inputfile:
            checker = json.load(inputfile)
            for objects in checker:
                if objects['name'] == name:
                    objects['price'] = price
                    objects['ingredients'] = ingredients
                    update(checker)
                    return 'Блюдо успешно изменено'
            return 'Ошибка!'


def delete(name) -> str:
    with open('foods/foods.json', 'r', encoding='windows-1251') as infile:
        deleter = json.load(infile)
        for record in deleter:
            if record['name'] == name:
                deleter.remove(record)
                update(deleter)
                return 'Продукт успешно удален'
        return 'Такого продукта не существует'


def get_food_json_dict(name) -> dict:
    with open('foods/foods.json', 'r', encoding='windows-1251') as infile:
        getter = json.load(infile)
        for record in getter:
            if record['name'] == name:
                return record


def get_food_info(name) -> list:
    with open('foods/foods.json', 'r', encoding='windows-1251') as infile:
        getter = json.load(infile)
        for record in getter:
            if record['name'] == name:
                ingreds = ", ".join(record['ingredients'])
                newrecord = [record['name'], record['price'], ingreds]
                return newrecord


def is_product_usable(productname) -> bool:
    with open('foods/foods.json', 'r', encoding='windows-1251') as infile:
        getter = json.load(infile)
        for record in getter:
            if productname in record['ingredients']:
                return True
        return False


def get_food_stats(name) -> str:
    with open('foods/foods.json', 'r', encoding='windows-1251') as infile:
        getter = json.load(infile)
        for record in getter:
            if record['name'] == name:
                protein = 0.0
                fats = 0.0
                carbohydrates = 0.0
                calories = 0.0
                mass = 0.0
                ingredients = record['ingredients']
                for ingredient in ingredients:
                    mass += ingredients[ingredient]
                    localmass = ingredients[ingredient]
                    localstats = get_product_info(ingredient)
                    calories += (localstats['calories']/localstats['mass'])*localmass
                    protein += (localstats['protein'] / localstats['mass']) * localmass
                    fats += (localstats['fats'] / localstats['mass']) * localmass
                    carbohydrates += (localstats['carbohydrates'] / localstats['mass']) * localmass
                return f'Масса: {mass} г. (Белки: {round(protein, 2)} г, \n' \
                       f'Жиры: {round(fats, 2)} г, Углеводы: {round(carbohydrates, 2)} г)\n' \
                       f'Ценность: {round(calories)} ккал.'
        return 'Ошибка!'
