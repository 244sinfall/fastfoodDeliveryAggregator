from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QWidget

from client.orderplacemenu import OrderPlaceMenu
from guicommonoperations import load_foods, load_orders_by_username


class ClientMenuEnter(QWidget):
    # Запрос имени клиента, Валидатор блочит цифры и пробелы, аналог авторизации. Дальнейшее взаимодействие
    # описано в файле client/clientmenu.py
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.clientmenu = None
        uic.loadUi('client/clientmenuenter.ui', self)
        regexp = QRegExp("([А-Яа-яЁё]{1,50}\\S)")
        self.nameInput.setValidator(QRegExpValidator(regexp))
        self.toClientMenuTrigger.clicked.connect(lambda: self.to_client_menu(self.nameInput.text()))

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.show()
        super().closeEvent(a0)

    def to_client_menu(self, client_name):
        # Переход в полноценное меню клиента
        if len(self.nameInput.text()) > 0:
            self.clientmenu = ClientMenu(parent=self.parent, client_name=client_name)
            self.clientmenu.show()
            self.hide()


class ClientMenu(QWidget):
    def __init__(self, parent, client_name):
        super().__init__()
        self.parent = parent
        self.client_name = client_name
        uic.loadUi('client/clientmenu.ui', self)
        self.clientExitButton.clicked.connect(self.close)
        self.welcomingLabel.setText(f'Добро пожаловать, {client_name}!')
        self.orderplacer = None
        self.placeOrderButton.clicked.connect(self.place_order)
        self.foodsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.foodsTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.foodsTable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.myOrdersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.myOrdersTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        load_foods(self.foodsTable)
        load_orders_by_username(self.myOrdersTable, client_name)

    def place_order(self) -> None:
        self.orderplacer = OrderPlaceMenu(parent=self)
        self.orderplacer.show()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.show()
        super().closeEvent(a0)
