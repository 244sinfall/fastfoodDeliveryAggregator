from PyQt5.QtCore import QDateTime

from json_commonoperations import open_json_to_read, update, append


def get_new_order_id() -> int:
    id_selector = 0
    list_of_orders = open_json_to_read('orders/orders.json')
    for order in list_of_orders:
        if id_selector == order['id']:
            id_selector += 1
        else:
            return id_selector
    return len(list_of_orders)

def get_order_by_id(order_id: int) -> dict:
    list_of_orders = open_json_to_read('orders/orders.json')
    for order in list_of_orders:
        if order['id'] == order_id:
            return order


def get_orders_by_username(username: str) -> list:
    output_list = []
    list_of_orders = open_json_to_read('orders/orders.json')
    for order in list_of_orders:
        if order['username'] == username:
            output_list.append(order)
    return output_list


def delete(order_id: int) -> str:
    list_of_orders = open_json_to_read('orders/orders.json')
    for order in list_of_orders:
        if order['id'] == order_id:
            list_of_orders.remove(order)
            update(list_of_orders, 'orders/orders.json')
            return 'Заказ успешно удален'


def set_order_item(order_id: int, order_object: str, replace_item):
    list_of_orders = open_json_to_read('orders/orders.json')
    for order in list_of_orders:
        if order['id'] == order_id:
            order[order_object] = replace_item
            update(list_of_orders, 'orders/orders.json')
            return


def get_status_name(status: int) -> str:
    if status == 0:
        return 'Заказ создан'
    if status == 1:
        return 'Заказ принят'
    if status == 2:
        return 'Заказ готов'
    if status == 3:
        return 'Заказ доставлен'
    if status == 4:
        return 'Заказ завершен'


def get_address_name(address: dict) -> str:
    out_address = f"г. {address['city']}, ул. {address['street']}, дом/стр. {address['house']}"
    if len(address['apt']) > 0:
        out_address += f", кв/офис. {address['apt']}"
    return out_address


def get_order_list(order: dict) -> str:
    out_order = ''
    for item in order:
        out_order += f"{order[item]} {item}. "
    return out_order


def create_order(username: str, paycheck: float, paid: bool, delivery: bool, status: int, address: dict, phone: str,
                 time_to_deliver: str, order: dict) -> str:
    order_dict = {
        'id': get_new_order_id(),
        'timeAndDate': QDateTime.currentDateTime().toString('dd.MM.yy hh:mm'),
        'username': username,
        'paycheck': paycheck,
        'paid': paid,
        'delivery': delivery,
        'status': status,
        'address': address,
        'phone': phone,
        'timeToDeliver': time_to_deliver,
        'order': order
    }
    print(order_dict)
    append(order_dict, 'orders/orders.json')
