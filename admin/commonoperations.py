from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from adminmenu import load_foods
from foodproducts import foodproduct
from foods import foods

# ingredientsToAdd/Edit = given_table
# selfPrice = given_label


def update_selfprice(given_table, given_label):
    rowcounts = given_table.rowCount()
    price = 0.0
    if rowcounts > 0:
        for checker in range(rowcounts):
            try:
                ingprice = foodproduct.get_partial_food_price(given_table.item(checker, 0).text(),
                                                              int(given_table.item(checker, 1).text()))
                price += ingprice
            except:
                pass
        given_label.setText(f'Себестоимость: {round(price, 2)} руб.')
    else:
        given_label.setText(f'Себестоимость: {round(price, 2)} руб.')


def add_ingredients_to_list(given_table, given_list, statustext):
    rowcounts = given_table.rowCount()
    if rowcounts > 0:
        for checker in range(rowcounts):
            if given_table.item(checker, 0).text() == given_list.currentItem().text():
                statustext.setText('Ингредиент уже добавлен! Измените массу') # исправить
                return
    given_table.insertRow(0)
    given_table.setItem(0, 0, QTableWidgetItem(given_list.currentItem().text()))  # наименование
    given_table.setItem(0, 1, QTableWidgetItem('100'))
    given_table.item(0, 0).setFlags(given_table.item(0, 0).flags() ^ QtCore.Qt.ItemIsEditable)