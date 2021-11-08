from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from guicommonoperations import load_orders_to_manager
from orders.orders import set_order_item


class OrderCanceler(QWidget):
    # Меню администратора. Дальнейшее взаимодействие идет по директории /admin
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('manager/ordercanceler.ui', self)
        self.row = self.parent.currentOrdersTable.currentRow()
        self.order_id = int(self.parent.currentOrdersTable.item(self.row, 0).text())
        self.cancelConfirm.clicked.connect(self.cancel_order)
        self.cancelNo.clicked.connect(self.cancel_decline)

    def cancel_order(self):
        set_order_item(self.order_id, 'status', 4)
        if self.parent.currentOrdersTable.item(self.row, 4).text() == 'Оплачено':
            self.parent.managerStatusLabel.setText(f'Заказ №{self.order_id} отменен. Деньги возвращены.')
        else:
            self.parent.managerStatusLabel.setText(f'Заказ №{self.order_id} отменен.')
        load_orders_to_manager(self.parent)
        self.close()

    def cancel_decline(self):
        self.parent.cancelButton.setEnabled(True)
        self.close()
