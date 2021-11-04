import tkinter
from tkinter import *
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets, QtCore
import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QHeaderView

#from adminmenu import load_products
from adminmenu import load_products, ProductAddMenu


class WelcomeMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('mainmenu.ui', self)
        self.admin_menu = None
        self.admin_Mode_Trigger.clicked.connect(self.go_admin_menu)

    def go_admin_menu(self):
        self.admin_menu = AdminMenu(parent=self)
        self.admin_menu.show()
        self.hide()


class AdminMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('adminmenu.ui', self)
        header = self.productsTable.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.addProductButton.clicked.connect(self.addProductButton_clicked)
        self.addproducter = None
        self.adminExitButton.clicked.connect(self.close)
        load_products(self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.show()
        super().closeEvent(a0)

    def addProductButton_clicked(self) -> None:
        self.addproducter = ProductAddMenu(parent=self)
        self.addproducter.show()


app = QtWidgets.QApplication(sys.argv)
menu = WelcomeMenu()
menu.show()
exit(app.exec_())




