from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QWidget

from client.orderplacemenu import OrderPlaceMenu
from guicommonoperations import load_foods, load_orders_by_username


class ClientMenu(QWidget):
    def __init__(self, parent, client_name):
        super().__init__()
        self.parent = parent
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
