from PyQt5.QtWidgets import QTableWidgetItem
from foodproducts import foodproduct
from foods import foods
from foods.foods import get_food_stats
from json_commonoperations import open_json_to_read
from orders.orders import get_status_name, get_address_name, get_order_list


def load_orders_routine(table, object_counter, row=0):
    # Типовая функция, которая выгружает список заказов в выбранную таблицу.
    table.insertRow(row)
    table.setItem(row, 0, QTableWidgetItem(str(object_counter['id'])))
    table.setItem(row, 1, QTableWidgetItem(QTableWidgetItem(str(object_counter['timeAndDate']))))
    table.setItem(row, 2, QTableWidgetItem(str(object_counter['username'])))
    table.setItem(row, 3, QTableWidgetItem(str(object_counter['paycheck'])))
    if object_counter['paid'] is True:
        table.setItem(row, 4, QTableWidgetItem('Оплачено'))
    if object_counter['paid'] is False:
        table.setItem(row, 4, QTableWidgetItem('Не оплачено'))
    if object_counter['delivery'] is True:
        table.setItem(row, 5, QTableWidgetItem('Доставка'))
    if object_counter['delivery'] is False:
        table.setItem(row, 5, QTableWidgetItem('Самовывоз'))
    table.setItem(row, 6, QTableWidgetItem(get_status_name(object_counter['status'])))
    table.setItem(row, 7, QTableWidgetItem(get_address_name(object_counter['address'])))
    table.setItem(row, 8, QTableWidgetItem(QTableWidgetItem(str(object_counter['phone']))))
    table.setItem(row, 9, QTableWidgetItem(QTableWidgetItem(str(object_counter['timeToDeliver']))))
    table.setItem(row, 10, QTableWidgetItem(QTableWidgetItem(get_order_list(object_counter['order']))))


def load_orders_to_manager(window) -> None:
    # Этот код распределяет заказы между двумя окнами. Отмененные и завершенные заказы помещаются в архив,
    # Остальные в текущие заказы
    while window.currentOrdersTable.rowCount() > 0:
        window.currentOrdersTable.removeRow(0)
    while window.archiveOrdersTable.rowCount() > 0:
        window.archiveOrdersTable.removeRow(0)
    current_row = 0
    archive_row = 0
    counter = open_json_to_read('orders/orders.json')
    for object_counter in counter:
        if object_counter['status'] != 3 and object_counter['status'] != 4:
            load_orders_routine(window.currentOrdersTable, object_counter, current_row)
            current_row += 1
        else:
            load_orders_routine(window.archiveOrdersTable, object_counter, archive_row)
            archive_row += 1


def load_orders_by_username(table, username: str) -> None:
    # Этот код выгружает список заказов с фильтрацией по имени клиента (для списка у клиента)
    while table.rowCount() > 0:
        table.removeRow(0)
    row = 0
    counter = open_json_to_read('orders/orders.json')
    for object_counter in counter:
        if object_counter['username'] == username:
            load_orders_routine(table, object_counter, row)
            row += 1


def load_orders(window) -> None:
    # выгружает все заказы, администратору и менеджеру
    table = window.ordersTable
    while table.rowCount() > 0:
        table.removeRow(0)
    row = 0
    counter = open_json_to_read('orders/orders.json')
    for object_counter in counter:
        load_orders_routine(table, object_counter, row)
        row += 1


def load_products(window) -> None:
    # выгружает список продуктов из JSON, для администратора
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


def load_foods(table) -> None:
    # выгружает список блюд в выбранную таблицу, используется у администратора и клиента при заказе
    while table.rowCount() > 0:
        table.removeRow(0)
    row = 0
    counter = open_json_to_read('foods/foods.json')
    for object_counter in counter:
        food_info = foods.get_food_info(object_counter['name'])
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(str(food_info[0])))  # наименование
        table.setItem(row, 1, QTableWidgetItem(str(food_info[1]) + ' руб.'))
        table.setItem(row, 2, QTableWidgetItem(str(get_food_stats(food_info[0]))))
        table.setItem(row, 3, QTableWidgetItem(str(food_info[2])))
        row += 1

