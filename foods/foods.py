import json
from json import *

from foodproducts.foodproduct import get_product_info
from json_commonoperations import check_existance, append, update, open_json_to_read


def create(name, price, ingredients: dict) -> str:
    if check_existance(name, 'foods/foods.json') is False:
        product_info = {
            "name": name,
            "price": price,
            "ingredients": ingredients
        }
        append(product_info, 'foods/foods.json')
        return 'Блюдо успешно добавлено'
    else:
        return 'Блюдо уже существует. Измените его.'


def change(name, price, ingredients: dict) -> str:
    if check_existance(name, 'foods/foods.json') is True:
        checker = open_json_to_read('foods/foods.json')
        for objects in checker:
            if objects['name'] == name:
                objects['price'] = price
                objects['ingredients'] = ingredients
                update(checker, 'foods/foods.json')
                return 'Блюдо успешно изменено'
        return 'Ошибка!'


def delete(name) -> str:
    deleter = open_json_to_read('foods/foods.json')
    for record in deleter:
        if record['name'] == name:
            deleter.remove(record)
            update(deleter, 'foods/foods.json')
            return 'Продукт успешно удален'
    return 'Такого продукта не существует'


def get_food_json_dict(name) -> dict:
    getter = open_json_to_read('foods/foods.json')
    for record in getter:
        if record['name'] == name:
            return record


def get_food_price(name) -> float:
    getter = open_json_to_read('foods/foods.json')
    for record in getter:
        if record['name'] == name:
            return record['price']


def get_food_info(name) -> list:
    getter = open_json_to_read('foods/foods.json')
    for record in getter:
        if record['name'] == name:
            ingreds = ", ".join(record['ingredients'])
            newrecord = [record['name'], record['price'], ingreds]
            return newrecord


def is_product_usable(productname) -> bool:
    getter = open_json_to_read('foods/foods.json')
    for record in getter:
        if productname in record['ingredients']:
            return True
    return False


def get_food_stats(name) -> str:
    getter = open_json_to_read('foods/foods.json')
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
