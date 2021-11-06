import json
from PyQt5.QtWidgets import QTableWidgetItem
from foodproducts import foodproduct
from foods import foods
from foods.foods import get_food_stats
from json_commonoperations import open_json_to_read


def load_orders(window) -> None:
    while window.ordersTable.rowCount() > 0:
        window.ordersTable.removeRow(0)
    row = 0
    counter = open_json_to_read('orders/orders.json')
    for object_counter in counter:
        window.ordersTable.insertRow(row)
        window.ordersTable.setItem(row, 0, QTableWidgetItem(str(object_counter['id'])))
        window.ordersTable.setItem(row, 1, QTableWidgetItem(str(object_counter['username'])))



def load_products(window) -> None:
    while window.productsTable.rowCount() > 0:
        window.productsTable.removeRow(0)
    row = 0
    counter = open_json_to_read('foodproducts/products.json')
    for object_counter in counter:
        product_info = foodproduct.get_product_info(object_counter['name'])
        window.productsTable.insertRow(row)
        window.productsTable.setItem(row, 0, QTableWidgetItem(str(product_info['name'])))
        window.productsTable.setItem(row, 1, QTableWidgetItem(str(product_info['protein']) + ' г.'))
        window.productsTable.setItem(row, 2, QTableWidgetItem(str(product_info['fats']) + ' г.'))
        window.productsTable.setItem(row, 3, QTableWidgetItem(str(product_info['carbohydrates']) + ' г.'))
        window.productsTable.setItem(row, 4, QTableWidgetItem(str(product_info['calories']) + ' ккал'))
        window.productsTable.setItem(row, 5, QTableWidgetItem(str(product_info['mass']) + ' г.'))
        window.productsTable.setItem(row, 6, QTableWidgetItem(str(product_info['price']) + ' руб.'))
        row += 1


def load_foods(window) -> None:
    while window.foodsTable.rowCount() > 0:
        window.foodsTable.removeRow(0)
    row = 0
    counter = open_json_to_read('foods/foods.json')
    for object_counter in counter:
        food_info = foods.get_food_info(object_counter['name'])
        window.foodsTable.insertRow(row)
        window.foodsTable.setItem(row, 0, QTableWidgetItem(str(food_info[0])))  # наименование
        window.foodsTable.setItem(row, 1, QTableWidgetItem(str(food_info[1]) + ' руб.'))
        window.foodsTable.setItem(row, 2, QTableWidgetItem(str(get_food_stats(food_info[0]))))
        window.foodsTable.setItem(row, 3, QTableWidgetItem(str(food_info[2])))
        row += 1

