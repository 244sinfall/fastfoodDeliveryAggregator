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
            # window.foodsTable.setItem(row, 2, QTableWidgetItem(str(product_info['fats']) + ' г.'))
            # window.foodsTable.setItem(row, 3, QTableWidgetItem(str(product_info['carbohydrates']) + ' г.'))
            # window.foodsTable.setItem(row, 4, QTableWidgetItem(str(product_info['calories']) + ' ккал'))
            # window.foodsTable.setItem(row, 5, QTableWidgetItem(str(product_info['mass']) + ' г.'))
            # window.foodsTable.setItem(row, 6, QTableWidgetItem(str(product_info['price']) + ' руб.'))


class FoodAddMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('adminmenu/addfood.ui', self)
        self.cancelAdderButton.clicked.connect(self.close)
        self.ingredientsShow.itemDoubleClicked.connect(self.add_ingredients_to_list)
        self.addConfirmButton.clicked.connect(self.add_new_food)
        self.ingredientsToAdd.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ingredientsToAdd.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ingredientsToAdd.itemSelectionChanged.connect(self.enable_del_button)
        self.ingredientsToAdd.itemChanged.connect(self.update_selfprice)
        self.deleteIngredient.clicked.connect(self.del_ingredient_from_list)
        self.priceAdder.setValidator(QDoubleValidator(0, 10000, 2))
        self.load_ingredients_to_list()

    def add_new_food(self):
        try:
            name = self.nameAdder.text()
            price = float(self.priceAdder.text())
        except ValueError:
            self.adderStatusText.setText('Неверный формат!')
        else:
            try:
                rowcounts = self.ingredientsToAdd.rowCount()
                if rowcounts > 0:
                    ingredients_to_add = {}
                    for checker in range(rowcounts):
                        ingredients_to_add[f'{self.ingredientsToAdd.item(checker, 0).text()}'] = \
                            int(self.ingredientsToAdd.item(checker, 1).text())
                    self.parent.foodStatusLabel.setText(
                        foods.create(name, price, ingredients_to_add))
                    load_foods(self.parent)
                    self.close()
            except ValueError:
                self.adderStatusText.setText('Неверный формат!')

    def del_ingredient_from_list(self):
        self.ingredientsToAdd.removeRow(self.ingredientsToAdd.currentRow())
        self.update_selfprice()

    def enable_del_button(self):
        if len(set(index.row() for index in self.ingredientsToAdd.selectedIndexes())) == 1:
            self.deleteIngredient.setEnabled(True)
        else:
            self.deleteIngredient.setEnabled(False)

    def add_ingredients_to_list(self):
        rowcounts = self.ingredientsToAdd.rowCount()
        if rowcounts > 0:
            for checker in range(rowcounts):
                if self.ingredientsToAdd.item(checker, 0).text() == self.ingredientsShow.currentItem().text():
                    self.adderStatusText.setText('Ингредиент уже добавлен! Измените массу')
                    return
        self.ingredientsToAdd.insertRow(0)
        self.ingredientsToAdd.setItem(0, 0, QTableWidgetItem(self.ingredientsShow.currentItem().text()))  # наименование
        self.ingredientsToAdd.setItem(0, 1, QTableWidgetItem('100'))
        name = self.ingredientsToAdd.item(0, 0)
        name.setFlags(name.flags() ^ QtCore.Qt.ItemIsEditable)

    def load_ingredients_to_list(self):
        ingredients = foodproduct.get_products_list()
        for item in ingredients:
            self.ingredientsShow.addItem(item)

    def update_selfprice(self):
        rowcounts = self.ingredientsToAdd.rowCount()
        price = 0.0
        if rowcounts > 0:
            for checker in range(rowcounts):
                try:
                    ingprice = foodproduct.get_partial_food_price(self.ingredientsToAdd.item(checker, 0).text(),
                                                       int(self.ingredientsToAdd.item(checker, 1).text()))
                    price += ingprice
                except:
                    pass
            self.selfPrice.setText(f'Себестоимость: {round(price, 2)} руб.')
        else:
            self.selfPrice.setText(f'Себестоимость: {round(price, 2)} руб.')


class FoodEditMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('adminmenu/editfood.ui', self)
        self.cancelEditorButton.clicked.connect(self.close)
        self.editConfirmButton.clicked.connect(self.edit_old_food)
        self.priceEditor.setValidator(QDoubleValidator(0, 10000, 2))
        self.ingredientsShow.itemDoubleClicked.connect(self.add_ingredients_to_list)
        self.ingredientsToEdit.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ingredientsToEdit.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ingredientsToEdit.itemSelectionChanged.connect(self.enable_del_button)
        self.ingredientsToEdit.itemChanged.connect(self.update_selfprice)
        self.deleteIngredient.clicked.connect(self.del_ingredient_from_list)
        food_info = foods.get_food_json_dict(
            self.parent.foodsTable.item(self.parent.foodsTable.currentRow(), 0).text())
        self.priceEditor.setText(str(food_info['price']))
        for ingreds in food_info['ingredients']:
            self.ingredientsToEdit.insertRow(0)
            self.ingredientsToEdit.setItem(0, 0, QTableWidgetItem(ingreds))
            self.ingredientsToEdit.setItem(0, 1, QTableWidgetItem(str(food_info['ingredients'][ingreds])))
            name = self.ingredientsToEdit.item(0, 0)
            name.setFlags(name.flags() ^ QtCore.Qt.ItemIsEditable)
        self.load_ingredients_to_list()

    def enable_del_button(self):
        if len(set(index.row() for index in self.ingredientsToEdit.selectedIndexes())) == 1:
            self.deleteIngredient.setEnabled(True)
        else:
            self.deleteIngredient.setEnabled(False)

    def load_ingredients_to_list(self):
        ingredients = foodproduct.get_products_list()
        for item in ingredients:
            self.ingredientsShow.addItem(item)

    def del_ingredient_from_list(self):
        self.ingredientsToEdit.removeRow(self.ingredientsToEdit.currentRow())
        self.update_selfprice()

    def add_ingredients_to_list(self):
        rowcounts = self.ingredientsToEdit.rowCount()
        if rowcounts > 0:
            for checker in range(rowcounts):
                if self.ingredientsToEdit.item(checker, 0).text() == self.ingredientsShow.currentItem().text():
                    self.editorStatusText.setText('Ингредиент уже добавлен! Измените массу')
                    return
        self.ingredientsToEdit.insertRow(0)
        self.ingredientsToEdit.setItem(0, 0, QTableWidgetItem(self.ingredientsShow.currentItem().text()))  # наименование
        self.ingredientsToEdit.setItem(0, 1, QTableWidgetItem('100'))
        name = self.ingredientsToEdit.item(0, 0)
        name.setFlags(name.flags() ^ QtCore.Qt.ItemIsEditable)
        if self.editConfirmButton.isEnabled is False:
            self.editConfirmButton.setEnabled(True)

    def update_selfprice(self):
        rowcounts = self.ingredientsToEdit.rowCount()
        price = 0.0
        if rowcounts > 0:
            for checker in range(rowcounts):
                try:
                    ingprice = foodproduct.get_partial_food_price(self.ingredientsToEdit.item(checker, 0).text(),
                                                                  int(self.ingredientsToEdit.item(checker, 1).text()))
                    price += ingprice
                except:
                    pass
            self.selfPrice.setText(f'Себестоимость: {round(price, 2)} руб.')
        else:
            self.editConfirmButton.setEnabled(False)
            self.selfPrice.setText(f'Себестоимость: {round(price, 2)} руб.')

    def edit_old_food(self) -> None:
        price = float(self.priceEditor.text())
        try:
            rowcounts = self.ingredientsToEdit.rowCount()
            if rowcounts > 0:
                ingredients_to_edit = {}
                for checker in range(rowcounts):
                    ingredients_to_edit[f'{self.ingredientsToEdit.item(checker, 0).text()}'] = \
                        int(self.ingredientsToEdit.item(checker, 1).text())
                self.parent.foodStatusLabel.setText(
                    foods.change(self.parent.foodsTable.item(self.parent.foodsTable.currentRow(), 0).text(),
                                 price, ingredients_to_edit))
                load_foods(self.parent)
                self.close()
        except ValueError:
            self.editorStatusText.setText('Неверный формат!')


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
        self.priceAdder.setValidator(QDoubleValidator(0, 1000, 2))

    def add_new_product(self) -> None:
        try:
            name = self.nameAdder.text()
            protein = float(self.proteinAdder.text())
            fats = float(self.fatsAdder.text())
            carbohydrates = float(self.carbohydratesAdder.text())
            calories = int(self.caloriesAdder.text())
            mass = int(self.massAdder.text())
            price = float(self.priceAdder.text())
        except ValueError:
            self.adderStatusText.setText('Неверный формат!')
        else:
            self.parent.productStatusLabel.setText(
                foodproduct.create(name, protein, fats, carbohydrates, calories, mass, price))
            load_products(self.parent)
            self.close()


class ProductEditMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('adminmenu/editproduct.ui', self)
        self.cancelEditorButton.clicked.connect(self.close)
        self.editConfirmButton.clicked.connect(self.edit_old_product)
        self.proteinEditor.setValidator(QDoubleValidator(0, 100, 2))
        self.fatsEditor.setValidator(QDoubleValidator(0, 100, 2))
        self.carbohydratesEditor.setValidator(QDoubleValidator(0, 100, 2))
        self.caloriesEditor.setValidator(QIntValidator(0, 3000))
        self.priceEditor.setValidator(QDoubleValidator(0, 1000, 2))
        product_info = foodproduct.get_product_info(
            self.parent.productsTable.item(self.parent.productsTable.currentRow(), 0).text())
        self.proteinEditor.setText(str(product_info['protein']))
        self.fatsEditor.setText(str(product_info['fats']))
        self.carbohydratesEditor.setText(str(product_info['carbohydrates']))
        self.caloriesEditor.setText(str(product_info['calories']))
        self.priceEditor.setText(str(product_info['price']))

    def edit_old_product(self) -> None:
        try:
            protein = float(self.proteinEditor.text())
            fats = float(self.fatsEditor.text())
            carbohydrates = float(self.carbohydratesEditor.text())
            calories = int(self.caloriesEditor.text())
            price = float(self.priceEditor.text())
        except ValueError:
            self.editorStatusText.setText('Неверный формат!')
        else:
            self.parent.productStatusLabel.setText(
                foodproduct.change(self.parent.productsTable.item(self.parent.productsTable.currentRow(), 0).text(),
                                   protein, fats, carbohydrates, calories, price))
            load_products(self.parent)
            self.close()
