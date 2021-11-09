from json_commonoperations import check_existance, update, append, open_json_to_read


def create(name, protein, fats, carbohydrates, calories, mass, price) -> str:
    if check_existance(name, 'foodproducts/products.json') is False:
        product_info = {
            "name": name,
            "protein": protein,
            "fats": fats,
            "carbohydrates": carbohydrates,
            "calories": calories,
            "mass": mass,
            "price": price
        }
        append(product_info, 'foodproducts/products.json')
        return 'Продукт успешно добавлен'
    else:
        return 'Продукт уже существует. Измените его.'


def change(name, protein, fats, carbohydrates, calories, price) -> str:
    if check_existance(name, 'foodproducts/products.json') is True:
        checker = open_json_to_read('foodproducts/products.json')
        for objects in checker:
            if objects['name'] == name:
                objects['protein'] = protein
                objects['fats'] = fats
                objects['carbohydrates'] = carbohydrates
                objects['calories'] = calories
                objects['price'] = price
                update(checker, 'foodproducts/products.json')
                return 'Продукт успешно изменен'
        return 'Ошибка!'


def delete(name) -> str:
    deleter = open_json_to_read('foodproducts/products.json')
    for record in deleter:
        if record['name'] == name:
            deleter.remove(record)
            update(deleter, 'foodproducts/products.json')
            return 'Продукт успешно удален'
    return 'Такого продукта не существует'


def get_product_info(name) -> dict:
    getter = open_json_to_read('foodproducts/products.json')
    for record in getter:
        if record['name'] == name:
            return record


def get_products_list() -> list:
    getter = open_json_to_read('foodproducts/products.json')
    output = []
    for record in getter:
        output.append(record['name'])
    return output


def get_partial_food_price(name, mass) -> float:
    getter = open_json_to_read('foodproducts/products.json')
    for record in getter:
        if record['name'] == name:
            print((record['price']/record['mass'])*mass)
            return (record['price']/record['mass'])*mass
    return 0.0
