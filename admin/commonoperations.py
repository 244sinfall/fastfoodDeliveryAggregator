from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from foodproducts import foodproduct


def update_selfprice(given_table, given_label):
    rowcounts = given_table.rowCount()
    if rowcounts > 0:
        price = 0.0
        for checker in range(rowcounts):
            try:
                ingprice = foodproduct.get_partial_food_price(given_table.item(checker, 0).text(),
                                                              int(given_table.item(checker, 1).text()))
                price += ingprice
                given_label.setText(f'Себестоимость: {round(price, 2)} руб.')
            except AttributeError:
                given_label.setText(f'Себестоимость: 0 руб.')
    else:
        given_label.setText(f'Себестоимость: 0 руб.')


def enable_del_button(given_table, given_button):
    if len(set(index.row() for index in given_table.selectedIndexes())) == 1:
        given_button.setEnabled(True)
    else:
        given_button.setEnabled(False)


def load_ingredients_to_list(given_list):
    ingredients = foodproduct.get_products_list()
    for item in ingredients:
        given_list.addItem(item)


def del_ingredient_from_list(given_table, given_label):
    given_table.removeRow(given_table.currentRow())
    update_selfprice(given_table, given_label)


def add_ingredients_to_list(given_table, given_list, statustext):
    rowcounts = given_table.rowCount()
    if rowcounts > 0:
        for checker in range(rowcounts):
            if given_table.item(checker, 0).text() == given_list.currentItem().text():
                statustext.setText('Ингредиент уже добавлен! Измените массу')  # исправить
                return
    given_table.insertRow(0)
    given_table.setItem(0, 0, QTableWidgetItem(given_list.currentItem().text()))  # наименование
    given_table.setItem(0, 1, QTableWidgetItem('100'))
    given_table.item(0, 0).setFlags(given_table.item(0, 0).flags() ^ QtCore.Qt.ItemIsEditable)


def enable_del_change_buttons(given_table, edit_button, delete_button):
    if len(set(index.row() for index in given_table.selectedIndexes())) == 1:
        edit_button.setEnabled(True)
        delete_button.setEnabled(True)
    elif len(set(index.row() for index in given_table.selectedIndexes())) > 1:
        edit_button.setEnabled(False)
        delete_button.setEnabled(False)
    elif len(set(index.row() for index in given_table.selectedIndexes())) == 0:
        edit_button.setEnabled(False)
        delete_button.setEnabled(False)