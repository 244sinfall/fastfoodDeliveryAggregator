from PyQt5 import QtCore
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QTableWidgetItem
from foodproducts import foodproduct
from orders.orders import get_status_id


def update_selfprice(given_table, given_label):
    # Обновляет себестоимость в редакторе блюд
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


def load_ingredients_to_list(given_list):
    # Выгрузка продуктов из foodproducts/products.json в список в редакторе блюд
    ingredients = foodproduct.get_products_list()
    for item in ingredients:
        given_list.addItem(item)


def del_ingredient_from_list(given_table, given_label):
    # Удаление продуктов в редакторе блюд
    given_table.removeRow(given_table.currentRow())
    update_selfprice(given_table, given_label)


def add_ingredients_to_list(given_table, given_list, statustext):
    # Добавление продуктов в редактор блюд
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


def enable_del_change_buttons(given_table, edit_button=None, delete_button=None):
    # Триггер от изменения выбора полей в таблицах. Позволяем удалять или изменять только 1 выбранный элемент.
    # Было несколько функций для каждой кнопки, изменил на такую универсальную)
    if len(set(index.row() for index in given_table.selectedIndexes())) == 1:
        if edit_button is not None:
            edit_button.setEnabled(True)
        if delete_button is not None:
            delete_button.setEnabled(True)
    else:
        if edit_button is not None:
            edit_button.setEnabled(False)
        if delete_button is not None:
            delete_button.setEnabled(False)


def get_order_info_from_table(self, table, row) -> dict:
    # Спорное решение, брать информацию об изменении кнопок из виджета, или же из джсон. Это вариант брать
    # из виджета
    is_order_paid = True
    is_order_delivery = True
    if table.item(row, 4).text() == 'Не оплачено':
        is_order_paid = False
    if table.item(row, 5).text() == 'Самовывоз':
        is_order_delivery = False
    out_dict = {
        'id': int(table.item(row, 0).text()),
        'timeAndDate': QDateTime.fromString(table.item(row, 1).text(), 'dd.MM.yy hh:mm'),
        'username': table.item(row, 2).text(),
        'paycheck': float(table.item(row, 3).text()),
        'paid': is_order_paid,
        'delivery': is_order_delivery,
        'status': get_status_id(table.item(row, 6).text()),
        'address': table.item(row, 7).text(),
        'phone': table.item(row, 8).text(),
        'timeToDeliver': QDateTime.fromString(table.item(row, 9).text(), 'dd.MM.yy hh:mm'),
        'order': table.item(row, 9).text()
    }
    return out_dict


def get_city_name(row) -> str:
    # Возвращает название городв из селектора при создании/редактировании заказа
    if row == 0:
        return 'Красноярск'
    if row == 1:
        return 'Дивногорск'
    if row == 2:
        return 'Сосновоборск'
    else:
        return 'Красноярск'