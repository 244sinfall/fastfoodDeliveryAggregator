import json

from PyQt5 import QtGui, uic, QtWidgets, QtCore
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem, QWidget

import foodproducts.foodproduct
from foodproducts import foodproduct
from foods import foods
from foods.foods import get_food_stats


def load_products(window) -> None:
    while window.productsTable.rowCount() > 0:
        window.productsTable.removeRow(0)
    with open('foodproducts/products.json', 'r', encoding='windows-1251') as inputfile:
        row = 0
        counter = json.load(inputfile)
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


def load_foods(window) -> None:
    while window.foodsTable.rowCount() > 0:
        window.foodsTable.removeRow(0)
    with open('foods/foods.json', 'r', encoding='windows-1251') as inputfile:
        row = 0
        counter = json.load(inputfile)
        for object_counter in counter:
            food_info = foods.get_food_info(object_counter['name'])
            window.foodsTable.insertRow(row)
            window.foodsTable.setItem(row, 0, QTableWidgetItem(str(food_info[0])))  # наименование
            window.foodsTable.setItem(row, 1, QTableWidgetItem(str(food_info[1]) + ' руб.'))
            window.foodsTable.setItem(row, 2, QTableWidgetItem(str(get_food_stats(food_info[0]))))
            window.foodsTable.setItem(row, 3, QTableWidgetItem(str(food_info[2])))

