from PyQt5 import uic
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QWidget

from commonoperations import get_city_name
from guicommonoperations import load_orders_to_manager
from orders.orders import set_order_item, get_order_by_id


class OrderEditor(QWidget):
    # Меню администратора. Дальнейшее взаимодействие идет по директории /admin
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('manager/ordereditor.ui', self)
        self.new_delivery_Take = False
        self.new_date_time = QDateTime()
        self.new_address = {}
        self.row = self.parent.currentOrdersTable.currentRow()
        self.order_id = int(self.parent.currentOrdersTable.item(self.row, 0).text())
        self.autofilled_info = get_order_by_id(self.order_id)
        if self.autofilled_info['delivery'] is True:
            self.deliveryTake.setChecked(True)
            if self.autofilled_info['address']['city'] == 'Красноярск':
                self.citySelector.setCurrentRow(0)
            if self.autofilled_info['address']['city'] == 'Дивногорск':
                self.citySelector.setCurrentRow(1)
            if self.autofilled_info['address']['city'] == 'Сосновоборск':
                self.citySelector.setCurrentRow(2)
            self.streetInput.setText(self.autofilled_info['address']['street'])
            self.houseInput.setText(self.autofilled_info['address']['house'])
            self.aptInput.setText(self.autofilled_info['address']['apt'])
            self.streetInput.setEnabled(True)
            self.houseInput.setEnabled(True)
            self.aptInput.setEnabled(True)
        else:
            self.attendanceTake.setChecked(True)
            self.citySelector.setCurrentRow(0)
            self.streetInput.setText('Академика Киренского')
            self.houseInput.setText('26Б')
            self.aptInput.setText('')
            self.streetInput.setEnabled(False)
            self.houseInput.setEnabled(False)
            self.aptInput.setEnabled(False)
        self.deliveryTake.toggled.connect(lambda: self.open_address_editor(True))
        self.attendanceTake.toggled.connect(lambda: self.open_address_editor(False))
        self.cancelEditorButton.clicked.connect(self.close)
        self.editOrderButton.clicked.connect(self.edit_order)
        self.timeToDeliverTime = QDateTime.fromString(self.autofilled_info['timeToDeliver'], 'dd.MM.yyyy hh:mm')
        self.timeToDeliver.setDateTime(self.timeToDeliverTime)
        self.timeToDeliver.setMinimumDateTime(self.timeToDeliverTime)

    def edit_order(self):
        if self.attendanceTake.isChecked() is True:
            self.new_delivery_Take = False
            self.new_address = {
                'city': 'Красноярск',
                'street': 'Академика Киренского',
                'house': '26Б'
            }
        else:
            self.new_delivery_Take = True
            if len(self.streetInput.text()) < 3:
                self.placerStatusLabel.setText('Введите адрес доставки!')
                return
            if len(self.houseInput.text()) == 0:
                self.placerStatusLabel.setText('Введите номер дома доставки!')
                return
            self.new_address = {
                'city': get_city_name(self.citySelector.currentRow()),
                'street': self.streetInput.text(),
                'house': self.houseInput.text(),
                'apt': self.aptInput.text()
            }
        self.new_date_time = self.timeToDeliver.dateTime()
        if self.autofilled_info['delivery'] is not self.new_delivery_Take:
            set_order_item(self.order_id, 'delivery', self.new_delivery_Take)
        if self.new_date_time != QDateTime.fromString(self.autofilled_info['timeToDeliver'], 'dd.MM.yyyy hh:mm'):
            set_order_item(self.order_id, 'timeToDeliver', self.new_date_time.toString('dd.MM.yyyy hh:mm'))
        if self.new_address != self.autofilled_info['address']:
            set_order_item(self.order_id, 'address', self.new_address)
        self.parent.managerStatusLabel.setText(f'Заказ №{self.order_id} был изменен!')
        load_orders_to_manager(self.parent)
        self.close()

    def open_address_editor(self, state: bool):
        if state is True:
            if self.autofilled_info['address']['city'] == 'Красноярск':
                self.citySelector.setCurrentRow(0)
            if self.autofilled_info['address']['city'] == 'Дивногорск':
                self.citySelector.setCurrentRow(1)
            if self.autofilled_info['address']['city'] == 'Сосновоборск':
                self.citySelector.setCurrentRow(2)
            self.streetInput.setText('')
            self.houseInput.setText('')
            self.aptInput.setText('')
        else:
            self.citySelector.setCurrentRow(0)
            self.streetInput.setText('Академика Киренского')
            self.houseInput.setText('26Б')
            self.aptInput.setText('')
        self.streetInput.setEnabled(state)
        self.houseInput.setEnabled(state)
        self.aptInput.setEnabled(state)
