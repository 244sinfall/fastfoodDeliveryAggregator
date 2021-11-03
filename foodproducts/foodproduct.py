import json
from json import *


def writeproduct(name, protein, fats, carbohydrates, calories, mass, price) -> str:
    productinfo = {
        "name": name,
        "protein": protein,
        "fats": fats,
        "carbohydrates": carbohydrates,
        "calories": calories,
        "mass": mass,
        "price": price
    }
    with open('products.json','r+') as infile:
        data = json.loads(infile.read())
        if name in data['name']:
            return 'Такой продукт уже существует'
        else:
            with open('products.json','a') as outfile:
                json.dump(productinfo, outfile)
                return 'Продукт успешно добавлен'

def deleteproduct(name) -> str:
    with open('products.json', 'r') as infile:
        data = json.loads(infile.read())
        for dicts in data:
            if name in dicts['name']:
                dicts.pop()
                return 'Продукт успешно удален'
        else:
            return 'Такого продукта не существует'

def getcertainproduct(name) -> dict:
    with open('products.json', 'r') as infile:
        data = json.loads(infile.read())
        for dicts in data:
            if name == dicts['name']:
                return dicts
            else:
                return {"": ''}

def getproductlist() -> list:
    with open('products.json', 'r') as infile:
        data = json.loads(infile.read())
        return data

#def deleteproduct(name) -> str:
#    with open('products.json', 'rw') as outfile:
#        if name['name'] in outfile:



