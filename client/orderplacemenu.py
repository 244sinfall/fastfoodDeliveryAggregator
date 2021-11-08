from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from commonoperations import get_city_name, enable_del_change_buttons
from foods.foods import get_food_info, get_food_price
from guicommonoperations import load_foods, load_orders_by_username
from orders.orders import get_order_by_id, create_order


def get_order_from_list(input_list_order: list) -> dict:
    output_dict = {}
    for each_element in range(len(input_list_order)):
        if input_list_order[each_element] in output_dict:
            output_dict[input_list_order[each_element]] += 1
        else:
            output_dict[input_list_order[each_element]] = 1
    return output_dict


class OrderPlaceMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.cardPaid = False
        self.orderReady = False
        self.elementsInOrder = []
        self.orderPrice = 0.0
        self.deliveryPrice = 0.0
        uic.loadUi('client/placeorder.ui', self)
        self.cancelPlacerButton.clicked.connect(self.close)
        self.deliveryTake.toggled.connect(lambda: self.unlock_delivery_control(True))
        self.attendanceTake.toggled.connect(lambda: self.unlock_delivery_control(False))
        self.cardPayment.toggled.connect(lambda: self.unlock_card_control(True))
        self.cashPayment.toggled.connect(lambda: self.unlock_card_control(False))
        self.foodsToAdd.itemDoubleClicked.connect(self.add_food_to_order_builder)
        self.orderBuilder.itemSelectionChanged.connect(
            lambda: enable_del_change_buttons(self.orderBuilder, delete_button=self.deleteElement)
        )
        self.citySelector.itemSelectionChanged.connect(self.count_delivery)
        self.deleteElement.clicked.connect(
            lambda: self.remove_element_from_order(self.orderBuilder.currentRow())
        )
        self.creditCardPayButton.clicked.connect(self.pay_order_with_card)
        self.placeOrderButton.clicked.connect(self.place_order)

        self.cardInputFirst.setValidator(QIntValidator(1000, 9999))
        self.cardInputSecond.setValidator(QIntValidator(1000, 9999))
        self.cardInputThird.setValidator(QIntValidator(1000, 9999))
        self.cardInputFourth.setValidator(QIntValidator(1000, 9999))
        self.CVCInput.setValidator(QIntValidator(100, 999))
        self.cardMonth.setValidator(QIntValidator(0, 12))
        self.cardYear.setValidator(QIntValidator(21, 99))

        self.foodsToAdd.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.foodsToAdd.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.orderBuilder.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.orderBuilder.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.timeToDeliver.setDate(QDate.currentDate())
        self.currentTime = QTime.currentTime()
        self.hour = self.currentTime.hour()
        self.minute = self.currentTime.minute()
        self.fastestTime = QTime()
        QTime.setHMS(self.fastestTime, self.hour+1, self.minute, 0, 0)
        self.timeToDeliver.setTime(self.fastestTime)
        self.timeToDeliver.setMinimumDate(QDate.currentDate())
        self.timeToDeliver.setMinimumTime(self.fastestTime)

        load_foods(self.foodsToAdd)

        if self.parent.myOrdersTable.rowCount() > 0:
            last_row = self.parent.myOrdersTable.rowCount()
            autofilled_info = get_order_by_id(int(self.parent.myOrdersTable.item(last_row-1, 0).text()))
            self.phoneInput.setText(autofilled_info['phone'])
            if autofilled_info['delivery'] is True:
                self.deliveryTake.setChecked(True)
                if autofilled_info['address']['city'] == 'Красноярск':
                    self.citySelector.setCurrentRow(0)
                if autofilled_info['address']['city'] == 'Дивногорск':
                    self.citySelector.setCurrentRow(1)
                if autofilled_info['address']['city'] == 'Сосновоборск':
                    self.citySelector.setCurrentRow(2)
                self.streetInput.setText(autofilled_info['address']['street'])
                self.houseInput.setText(autofilled_info['address']['house'])
                self.aptInput.setText(autofilled_info['address']['apt'])

    def is_credit_card_valid(self) -> bool:
        if len(self.cardInputFirst.text()) < 4 or len(self.cardInputSecond.text()) < 4 or \
                len(self.cardInputThird.text()) < 4 or len(self.cardInputFourth.text()) < 4:
            self.placerStatusLabel.setText('Неверный номер карты!')
            return False
        if len(self.CVCInput.text()) < 3:
            self.placerStatusLabel.setText('Неверный CVV/CVC карты!')
            return False
        if len(self.cardMonth.text()) < 2 or len(self.cardYear.text()) < 2 or \
                int(self.cardMonth.text()) > 13 or int(self.cardYear.text()) < 21:
            self.placerStatusLabel.setText('Неверный срок действия карты!')
            return False
        return True

    def pay_order_with_card(self):
        if self.is_credit_card_valid() is True:
            if self.orderReady is True:
                self.cardPaid = True
                self.place_order()
            else:
                self.placerStatusLabel.setText('Сначала подтвердите заказ!')

    def place_order(self):
        # Проверки корректности заполнения
        if len(self.phoneInput.text()) != 16:
            self.placerStatusLabel.setText('Некорретный номер телефона!')
            return
        if self.deliveryTake.isChecked() is True:
            if len(self.streetInput.text()) < 3:
                self.placerStatusLabel.setText('Введите адрес доставки!')
                return
            if len(self.houseInput.text()) == 0:
                self.placerStatusLabel.setText('Введите номер дома доставки!')
                return
        if self.cardPayment.isChecked() is True:
            if self.is_credit_card_valid() is True:
                if self.cardPaid is False:
                    self.orderReady = True
                    self.placerStatusLabel.setText('Нажмите оплатить для перехода к платежу!')
                    return
            else:
                self.is_credit_card_valid()
                return
        # Установка значений
        username = self.parent.client_name
        address_dict = {}
        if self.deliveryTake.isChecked is False:
            address_dict['city'] = 'Красноярск'
            address_dict['street'] = 'Академика Киренского'
            address_dict['house'] = '26Б'
        else:
            address_dict['city'] = get_city_name(self.citySelector.currentRow())
            address_dict['street'] = self.streetInput.text()
            address_dict['house'] = self.houseInput.text()
            if len(self.aptInput.text()) == 0:
                address_dict['apt'] = ''
            else:
                address_dict['apt'] = self.aptInput.text()
        # Отправка в JSON
        create_order(username, (self.orderPrice+self.deliveryPrice),
                     self.cardPaid, self.deliveryTake.isChecked(), 0, address_dict,
                     self.phoneInput.text(), self.timeToDeliver.dateTime().toString('dd.MM.yyyy hh:mm'),
                     get_order_from_list(self.elementsInOrder))
        self.parent.orderStatusLabel.setText('Заказ успешно создан. Ожидайте СМС или смотрите статус в "Мои заказы"')
        load_orders_by_username(self.parent.myOrdersTable, username)
        self.close()

    def count_delivery(self):
        if self.deliveryTake.isChecked() is True:
            if self.citySelector.currentRow() == 0:  # Красноярск
                self.deliveryPrice = 60
            if self.citySelector.currentRow() == 1:  # Дивногорск
                self.deliveryPrice = 200
            if self.citySelector.currentRow() == 2:  # Сосновоборск
                self.deliveryPrice = 140
            self.deliveryCounter.setText(f'Стоимость доставки: {self.deliveryPrice} рублей')
        else:
            self.deliveryCounter.setText('')
        self.update_order_price()

    def add_food_to_order_builder(self) -> None:
        selected_row = self.foodsToAdd.currentRow()
        food_info = get_food_info(self.foodsToAdd.item(selected_row, 0).text())
        order_rows = self.orderBuilder.rowCount()
        for item in range(order_rows):
            if self.orderBuilder.item(item, 0).text() == food_info[0]:
                self.orderBuilder.item(item, 1).setText(str(int(self.orderBuilder.item(item, 1).text())+1))
                self.add_element_to_order(food_info[0])
                return
        self.orderBuilder.insertRow(order_rows)
        self.orderBuilder.setItem(order_rows, 0, QTableWidgetItem(str(food_info[0])))
        self.orderBuilder.setItem(order_rows, 1, QTableWidgetItem('1'))
        self.orderBuilder.setItem(order_rows, 2, QTableWidgetItem(str(food_info[1]) + ' руб.'))
        self.add_element_to_order(food_info[0])
        self.orderReady = False

    def remove_element_from_order(self, row):
        self.elementsInOrder.remove(self.orderBuilder.item(row, 0).text())
        if int(self.orderBuilder.item(row, 1).text()) == 1:
            self.orderBuilder.removeRow(row)
        else:
            self.orderBuilder.setItem(row, 1, QTableWidgetItem(str(int(self.orderBuilder.item(row, 1).text()) - 1 )))
        self.update_order_price()
        self.orderReady = False
        if self.elementsInOrder is False:
            self.placeOrderButton.Enabled(False)

    def add_element_to_order(self, element: str):
        self.elementsInOrder.append(element)
        self.update_order_price()
        if self.deleteElement.isEnabled() is False:
            self.placeOrderButton.setEnabled(True)

    def update_order_price(self):
        self.orderPrice = 0.0
        for element in self.elementsInOrder:
            self.orderPrice += get_food_price(element)
            self.placeOrderButton.setText(f'Подтвердить заказ ({self.orderPrice + self.deliveryPrice} руб.)')
        if self.orderPrice == 0:
            self.placeOrderButton.setEnabled(False)
            self.placeOrderButton.setText(f'Подтвердить заказ')

    def unlock_delivery_control(self, control: bool):
        if control is False:
            self.citySelector.setCurrentRow(0)
            self.streetInput.setText('Академика Киренского')
            self.houseInput.setText('26Б')
            self.aptInput.setText('')
        else:
            self.citySelector.setCurrentRow(0)
            self.streetInput.setText('')
            self.houseInput.setText('')
            self.aptInput.setText('')
        self.citySelector.setEnabled(control)
        self.streetInput.setEnabled(control)
        self.houseInput.setEnabled(control)
        self.aptInput.setEnabled(control)
        self.count_delivery()

    def unlock_card_control(self, control: bool):
        if control is False:
            self.cardInputFirst.setText('1234')
            self.cardInputSecond.setText('1234')
            self.cardInputThird.setText('1234')
            self.cardInputFourth.setText('1234')
            self.cardMonth.setText('11')
            self.cardYear.setText('11')
            self.CVCInput.setText('123')
        else:
            self.cardInputFirst.setText('')
            self.cardInputSecond.setText('')
            self.cardInputThird.setText('')
            self.cardInputFourth.setText('')
            self.cardMonth.setText('')
            self.cardYear.setText('')
            self.CVCInput.setText('')
        self.cardInputFirst.setEnabled(control)
        self.cardInputSecond.setEnabled(control)
        self.cardInputThird.setEnabled(control)
        self.cardInputFourth.setEnabled(control)
        self.cardMonth.setEnabled(control)
        self.cardYear.setEnabled(control)
        self.CVCInput.setEnabled(control)
        self.creditCardPayButton.setEnabled(control)
