import json
from json import *

from json_commonoperations import open_json_to_read, update


def get_order_by_id(order_id: int) -> dict:
    list_of_orders = open_json_to_read('orders/orders.json')
    for order in list_of_orders:
        if order['id'] == order_id:
            return order


def get_orders_by_username(username: str) -> list:
    output_list = []
    list_of_orders = open_json_to_read('orders/orders.json')
    for order in list_of_orders
        if order['username'] == username:
            output_list.append(order)
    return output_list


def set_order_item(order_id: int, order_object: str, replace_item)
    # Статусы заказа:
    # 0 - Заказ создан
    # 1 - Заказ принят
    # 2 - Заказ готов
    # 3 - Заказ доставлен
    # 4 - Заказ завершен
    list_of_orders = open_json_to_read('orders/orders.json')
    for order in list_of_orders:
        if order['id'] == order_id:
            order[order_object] = replace_item
            update(list_of_orders, 'orders/orders.json')
            return

