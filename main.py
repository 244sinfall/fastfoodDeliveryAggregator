import tkinter
from tkinter import *
from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets, QtCore
import sys

from PyQt5.QtWidgets import QMainWindow, QWidget, QHeaderView

#from adminmenu import load_products
from adminmenu import load_products, ProductAddMenu, ProductEditMenu
from foodproducts import foodproduct


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
        self.addProductButton.clicked.connect(self.add_product)
        self.addproducter = None
        self.editproducter = None
        self.adminExitButton.clicked.connect(self.close)
        self.productsTable.itemSelectionChanged.connect(self.enable_del_change_buttons)
        self.deleteProductButton.clicked.connect(self.delete_product)
        self.editProductButton.clicked.connect(self.edit_product)
        load_products(self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.show()
        super().closeEvent(a0)

    def delete_product(self):
        name_to_delete = str(self.productsTable.item(self.productsTable.currentRow(), 0).text())
        self.productStatusLabel.setText(foodproduct.delete(name_to_delete))
        load_products(self)

    def add_product(self) -> None:
        self.addproducter = ProductAddMenu(parent=self)
        self.addproducter.show()

    def edit_product(self) -> None:
        self.editproducter = ProductEditMenu(parent=self)
        self.editproducter.show()

    def enable_del_change_buttons(self):
        if len(set(index.row() for index in self.productsTable.selectedIndexes())) == 1:
            self.editProductButton.setEnabled(True)
            self.deleteProductButton.setEnabled(True)
        elif len(set(index.row() for index in self.productsTable.selectedIndexes())) > 1:
            self.editProductButton.setEnabled(False)
            self.deleteProductButton.setEnabled(True)
        elif len(set(index.row() for index in self.productsTable.selectedIndexes())) == 0:
            self.editProductButton.setEnabled(False)
            self.deleteProductButton.setEnabled(False)



app = QtWidgets.QApplication(sys.argv)
menu = WelcomeMenu()
menu.show()
exit(app.exec_())




