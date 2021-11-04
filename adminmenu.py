import json

from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QTableWidgetItem, QWidget

import foodproducts.foodproduct
from foodproducts import foodproduct


def load_products(window) -> None:
    with open('foodproducts/products.json', 'r') as inputfile:
        row = 0
        counter = json.load(inputfile)
        for object_counter in counter:
            window.productsTable.insertRow(row)
            product_info = foodproduct.get_product_info(object_counter['name'])
            window.productsTable.setItem(row, 0, QTableWidgetItem(str(product_info['name'])))
            window.productsTable.setItem(row, 1, QTableWidgetItem(str(product_info['protein'])))
            window.productsTable.setItem(row, 2, QTableWidgetItem(str(product_info['fats'])))
            window.productsTable.setItem(row, 3, QTableWidgetItem(str(product_info['carbohydrates'])))
            window.productsTable.setItem(row, 4, QTableWidgetItem(str(product_info['calories']) + ' ккал'))
            window.productsTable.setItem(row, 5, QTableWidgetItem(str(product_info['mass']) + ' грамм'))
            window.productsTable.setItem(row, 6, QTableWidgetItem(str(product_info['price']) + ' руб.'))


class ProductAddMenu(QWidget):
    def __init__(self, parent=None):
        super(ProductAddMenu, self).__init__(parent)
        uic.loadUi('adminmenu/addproduct.ui', self)
        self.cancelAdderButton.clicked.connect(self.close)
        self.addConfirmButton.clicked.connect(self.add_new_product)

    def add_new_product(self) -> None:
        name = self.nameAdder.text()
        protein = self.proteinAdder.text()
        fats = self.fatsAdder.text()
        carbohydrates = self.carbohydratesAdder.text()
        calories = self.caloriesAdder.text()
        mass = self.massAdder.text()
        price = self.priceAdder.text()
        if isValuesCorrect(name, protein, fats, carbohydrates, calories, mass, price):
            foodproduct.create(name, protein, fats, carbohydrates, calories, mass, price)
            load_products(admin_menu)
            self.close()
        else:
            self.adderStatusLabel.setText('Некорректный формат!')


def isValuesCorrect(name, protein, fats, carbohydrates, calories, mass, price) -> str:
    try:
        str(name)
        float(protein)
        float(fats)
        float(carbohydrates)
        int(calories)
        int(mass)
        int(price)
        return True
    except:
        return False

