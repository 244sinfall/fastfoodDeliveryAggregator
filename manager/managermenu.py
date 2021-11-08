from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget

from commonoperations import get_order_info_from_table
from guicommonoperations import load_orders_to_manager
from manager.ordercanceler import OrderCanceler
from manager.ordereditor import OrderEditor
from orders.orders import set_order_item


class ManagerMenu(QWidget):
    # Меню администратора. Дальнейшее взаимодействие идет по директории /admin
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('manager/managermenu.ui', self)
        self.managerExitButton.clicked.connect(self.close)

        self.currentOrdersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.currentOrdersTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.archiveOrdersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.archiveOrdersTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.currentOrdersTable.itemSelectionChanged.connect(self.buttons_trigger)
        self.acceptOrderButton.clicked.connect(self.accept_order)  # Подразумевает уведомление о принятии заказов
        # и установке точных сроков (если требуется их поменять)
        self.setReadyButton.clicked.connect(self.set_order_ready)  # Подразумевает уведомление о приготовлении заказа
        self.getPaidButton.clicked.connect(self.get_cash_of_order)  # Подразумевает принятие оплаты на кассе заведения
        self.toDeliveryButton.clicked.connect(self.push_to_delivery)  # Доставка обозначает оплату курьеру, работа
        # доставки данной программой не регулируется
        self.editOrderButton.clicked.connect(self.edit_order)  # Подразумевает возможность изменять время приготовления
        # заказа или адрес получения для доставки
        self.editorderer = None
        self.cancelButton.clicked.connect(self.cancel_order)  # Подразумевает возможность отменить заказ с окном
        # подтверждения
        self.order_cancel_confirm = None

        load_orders_to_manager(self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.show()
        super().closeEvent(a0)

    def accept_order(self):  # Кнопка доступна только при выполнении всех условий. Простая смена статуса.
        order_id = int(self.currentOrdersTable.item(self.currentOrdersTable.currentRow(), 0).text())
        set_order_item(order_id, 'status', 1)
        self.managerStatusLabel.setText(f'Заказ №{order_id} принят!')
        load_orders_to_manager(self)

    def set_order_ready(self):  # Кнопка доступна только при выполнении всех условий. Простая смена статуса.
        row = self.currentOrdersTable.currentRow()
        order_id = int(self.currentOrdersTable.item(row, 0).text())
        if self.currentOrdersTable.item(row, 4).text() == 'Оплачено' \
                and self.currentOrdersTable.item(row, 5).text() == 'Самовывоз':
            set_order_item(order_id, 'status', 3)
            self.managerStatusLabel.setText(f'Заказ №{order_id} выполнен!')
        else:
            set_order_item(order_id, 'status', 2)
            self.managerStatusLabel.setText(f'Заказ №{order_id} готов к выдаче!')
        load_orders_to_manager(self)

    def get_cash_of_order(self):
        row = self.currentOrdersTable.currentRow()
        order_id = int(self.currentOrdersTable.item(row, 0).text())
        if self.currentOrdersTable.item(row, 6).text() == 'Заказ готов' \
                and self.currentOrdersTable.item(row, 5).text() == 'Самовывоз':
            set_order_item(order_id, 'status', 3)
            set_order_item(order_id, 'paid', True)
            self.managerStatusLabel.setText(f'Заказ №{order_id} выполнен!')
        load_orders_to_manager(self)

    def push_to_delivery(self):
        row = self.currentOrdersTable.currentRow()
        order_id = int(self.currentOrdersTable.item(row, 0).text())
        if self.currentOrdersTable.item(row, 6).text() == 'Заказ готов' \
                and self.currentOrdersTable.item(row, 5).text() == 'Доставка':
            set_order_item(order_id, 'status', 3)
            set_order_item(order_id, 'paid', True)
            self.managerStatusLabel.setText(f'Заказ №{order_id} передан в доставку!')
        load_orders_to_manager(self)

    def cancel_order(self):
        self.order_cancel_confirm = OrderCanceler(parent=self)
        self.order_cancel_confirm.show()
        self.cancelButton.setEnabled(False)

    def edit_order(self):
        self.editorderer = OrderEditor(parent=self)
        self.editorderer.show()
        self.cancelButton.setEnabled(False)

    def buttons_trigger(self):
        table = self.currentOrdersTable
        if len(set(index.row() for index in table.selectedIndexes())) == 1:
            order_info = get_order_info_from_table(self, table, table.currentRow())
            # Статус оплаты:
            if order_info['paid'] is True:
                self.getPaidButton.setText('Оплачено')
                self.getPaidButton.setEnabled(False)
            else:
                if order_info['delivery'] is True:
                    self.getPaidButton.setText('Оплата курьеру')
                    self.getPaidButton.setEnabled(False)
                else:
                    self.getPaidButton.setText('Принять оплату')
                    if order_info['status'] == 1 or order_info['status'] == 2:
                        self.getPaidButton.setEnabled(True)
                    else:
                        self.getPaidButton.setEnabled(False)
            # Статус доставки:
            if order_info['delivery'] is True:
                self.toDeliveryButton.setText('В доставку')
                if order_info['status'] == 2:  # Доставка доступна только при Заказ готов
                    self.toDeliveryButton.setEnabled(True)
                else:
                    self.toDeliveryButton.setEnabled(False)
            else:
                self.toDeliveryButton.setText('Самовывоз')
                self.toDeliveryButton.setEnabled(False)
            # Статус заказа:
            if order_info['status'] == 0:
                self.acceptOrderButton.setEnabled(True)
                self.setReadyButton.setEnabled(False)
            if order_info['status'] == 1:
                self.acceptOrderButton.setEnabled(False)
                self.acceptOrderButton.setText('Принято')
                self.setReadyButton.setEnabled(True)
            if order_info['status'] == 2:
                self.acceptOrderButton.setEnabled(False)
                self.acceptOrderButton.setText('Принято')
                self.setReadyButton.setEnabled(False)
                self.setReadyButton.setText('Приготовлено')
            # Отмена и изменение активно всегда
            self.cancelButton.setEnabled(True)
            self.editOrderButton.setEnabled(True)
        else:
            # При выборе 2 и более, или же 0 полей все управление отключается
            self.acceptOrderButton.setEnabled(False)
            self.acceptOrderButton.setText('Принять')
            self.cancelButton.setEnabled(False)
            self.editOrderButton.setEnabled(False)
            self.getPaidButton.setEnabled(False)
            self.getPaidButton.setText('Принять оплату')
            self.setReadyButton.setEnabled(False)
            self.setReadyButton.setText('Приготовлен')
            self.toDeliveryButton.setEnabled(False)
            self.toDeliveryButton.setText('В доставку')
