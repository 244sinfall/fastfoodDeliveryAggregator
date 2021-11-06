from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QWidget

from guicommonoperations import load_foods
from orders.orders import get_order_by_id


class OrderPlaceMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('client/placeorder.ui', self)
        self.cancelPlacerButton.clicked.connect(self.close)
        self.deliveryTake.toggled.connect(lambda: self.lock_delivery_control(False))
        self.attendanceTake.toggled.connect(lambda: self.lock_delivery_control(True))
        self.cardPayment.toggled.connect(lambda: self.lock_card_control(False))
        self.cashPayment.toggled.connect(lambda: self.lock_card_control(True))
        self.foodsToAdd.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.foodsToAdd.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
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

    def lock_delivery_control(self, control: bool):
        if control is True:
            self.citySelector.setCurrentRow(0)
            self.streetInput.setText('Академика Киренского')
            self.houseInput.setText('26Б')
            self.aptInput.setText('')
            self.citySelector.setEnabled(False)
            self.streetInput.setEnabled(False)
            self.houseInput.setEnabled(False)
            self.aptInput.setEnabled(False)
        else:
            self.citySelector.setCurrentRow(0)
            self.streetInput.setText('')
            self.houseInput.setText('')
            self.aptInput.setText('')
            self.citySelector.setEnabled(True)
            self.streetInput.setEnabled(True)
            self.houseInput.setEnabled(True)
            self.aptInput.setEnabled(True)

    def lock_card_control(self, control: bool):
        if control is True:
            self.cardInputFirst.setText('1234')
            self.cardInputSecond.setText('1234')
            self.cardInputThird.setText('1234')
            self.cardInputFourth.setText('1234')
            self.cardMonthYear.setText('11/11')
            self.CVCInput.setText('123')
            self.cardInputFirst.setEnabled(False)
            self.cardInputSecond.setEnabled(False)
            self.cardInputThird.setEnabled(False)
            self.cardInputFourth.setEnabled(False)
            self.cardMonthYear.setEnabled(False)
            self.CVCInput.setEnabled(False)
            self.creditCardPayButton.setEnabled(False)
        else:
            self.cardInputFirst.setText('')
            self.cardInputSecond.setText('')
            self.cardInputThird.setText('')
            self.cardInputFourth.setText('')
            self.cardMonthYear.setText('')
            self.CVCInput.setText('')
            self.cardInputFirst.setEnabled(True)
            self.cardInputSecond.setEnabled(True)
            self.cardInputThird.setEnabled(True)
            self.cardInputFourth.setEnabled(True)
            self.cardMonthYear.setEnabled(True)
            self.CVCInput.setEnabled(True)
            self.creditCardPayButton.setEnabled(True)
