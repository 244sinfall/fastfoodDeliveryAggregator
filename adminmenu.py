import json

from PyQt5 import QtGui, uic
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QTableWidgetItem, QWidget

import foodproducts.foodproduct
from foodproducts import foodproduct


def load_products(window) -> None:
    while window.productsTable.rowCount() > 0:
        window.productsTable.removeRow(0)
    with open('foodproducts/products.json', 'r') as inputfile:
        row = 0
        counter = json.load(inputfile)
        for object_counter in counter:
            product_info = foodproduct.get_product_info(object_counter['name'])
            window.productsTable.insertRow(row)
            window.productsTable.setItem(row, 0, QTableWidgetItem(str(product_info['name'])))
            window.productsTable.setItem(row, 1, QTableWidgetItem(str(product_info['protein'])))
            window.productsTable.setItem(row, 2, QTableWidgetItem(str(product_info['fats'])))
            window.productsTable.setItem(row, 3, QTableWidgetItem(str(product_info['carbohydrates'])))
            window.productsTable.setItem(row, 4, QTableWidgetItem(str(product_info['calories']) + ' ккал'))
            window.productsTable.setItem(row, 5, QTableWidgetItem(str(product_info['mass']) + ' грамм'))
            window.productsTable.setItem(row, 6, QTableWidgetItem(str(product_info['price']) + ' руб.'))


class ProductAddMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('adminmenu/addproduct.ui', self)
        self.cancelAdderButton.clicked.connect(self.close)
        self.addConfirmButton.clicked.connect(self.add_new_product)
        self.proteinAdder.setValidator(QDoubleValidator(0, 100, 2))
        self.fatsAdder.setValidator(QDoubleValidator(0, 100, 2))
        self.carbohydratesAdder.setValidator(QDoubleValidator(0, 100, 2))
        self.caloriesAdder.setValidator(QIntValidator(0, 3000))
        self.massAdder.setValidator(QIntValidator(0, 1000))
        self.priceAdder.setValidator(QDoubleValidator(0, 1000,2))



    def add_new_product(self) -> None:
        name = self.nameAdder.text()
        protein = float(self.proteinAdder.text())
        fats = float(self.fatsAdder.text())
        carbohydrates = float(self.carbohydratesAdder.text())
        calories = int(self.caloriesAdder.text())
        mass = int(self.massAdder.text())
        price = float(self.priceAdder.text())
        foodproduct.create(name, protein, fats, carbohydrates, calories, mass, price)
        load_products(self.parent)
        self.close()


