import tkinter
from tkinter import *
from PyQt5 import uic
from PyQt5 import QtWidgets, QtCore
import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QHeaderView

#from adminmenu import load_products
from adminmenu import load_products, ProductAddMenu


class WelcomeMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainmenu.ui', self)
        self.admin_Mode_Trigger.clicked.connect(self.go_admin_menu)

    def go_admin_menu(self):
        admin_menu.show()


class AdminMenu(QWidget):
    def __init__(self, parent=None):
        super(AdminMenu, self).__init__(parent)
        uic.loadUi('adminmenu.ui', self)
        header = self.productsTable.horizontalHeader()
        self.addproducter = ProductAddMenu(self)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.addProductButton.clicked.connect(self.addproducter.show)
        self.adminExitButton.clicked.connect(self.close)
        # header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        load_products(self)

    def addProductButton_clicked(self) -> None:
        addproducter.show()


app = QtWidgets.QApplication(sys.argv)
menu = WelcomeMenu()
menu.show()
admin_menu = AdminMenu()
addproducter = ProductAddMenu()
exit(app.exec_())




