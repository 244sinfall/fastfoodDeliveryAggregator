from PyQt5 import uic, QtGui
from PyQt5 import QtWidgets
import sys

from PyQt5.QtWidgets import QMainWindow, QWidget

from admin.foodaddmenu import FoodAddMenu
from admin.foodeditmenu import FoodEditMenu
from admin.productaddmenu import ProductAddMenu
from admin.producteditmenu import ProductEditMenu
from adminmenu import load_products, load_foods
from foodproducts import foodproduct
from foods import foods
from foods.foods import is_product_usable


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
        self.adminExitButton.clicked.connect(self.close)

        self.productsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.productsTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.addProductButton.clicked.connect(self.add_product)
        self.addproducter = None

        self.editProductButton.clicked.connect(self.edit_product)
        self.editproducter = None

        self.productsTable.itemSelectionChanged.connect(self.enable_del_change_buttons)
        self.deleteProductButton.clicked.connect(self.delete_product)
        load_products(self)

        self.foodsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.foodsTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.foodsTable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        self.addFoodButton.clicked.connect(self.add_food)
        self.addfooder = None

        self.editFoodButton.clicked.connect(self.edit_food)
        self.editfooder = None

        self.deleteFoodButton.clicked.connect(self.delete_food)

        self.foodsTable.itemSelectionChanged.connect(self.enable_del_change_buttons_foods)
        load_foods(self)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.show()
        super().closeEvent(a0)

    def delete_food(self):
        name_to_delete = str(self.foodsTable.item(self.foodsTable.currentRow(), 0).text())
        self.foodStatusLabel.setText(foods.delete(name_to_delete))
        load_foods(self)

    def delete_product(self):
        name_to_delete = str(self.productsTable.item(self.productsTable.currentRow(), 0).text())
        if is_product_usable(name_to_delete) is False:
            self.productStatusLabel.setText(foodproduct.delete(name_to_delete))
            load_products(self)
        else:
            self.productStatusLabel.setText('Удалите/измените блюда, в которых используется продукт')

    def add_product(self) -> None:
        self.addproducter = ProductAddMenu(parent=self)
        self.addproducter.show()

    def add_food(self) -> None:
        self.addfooder = FoodAddMenu(parent=self)
        self.addfooder.show()

    def edit_product(self) -> None:
        self.editproducter = ProductEditMenu(parent=self)
        self.editproducter.show()

    def edit_food(self) -> None:
        self.editfooder = FoodEditMenu(parent=self)
        self.editfooder.show()

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

    def enable_del_change_buttons_foods(self):
        if len(set(index.row() for index in self.foodsTable.selectedIndexes())) == 1:
            self.editFoodButton.setEnabled(True)
            self.deleteFoodButton.setEnabled(True)
        elif len(set(index.row() for index in self.foodsTable.selectedIndexes())) > 1:
            self.editFoodButton.setEnabled(False)
            self.deleteFoodButton.setEnabled(True)
        elif len(set(index.row() for index in self.foodsTable.selectedIndexes())) == 0:
            self.editFoodButton.setEnabled(False)
            self.deleteFoodButton.setEnabled(False)


app = QtWidgets.QApplication(sys.argv)
menu = WelcomeMenu()
menu.show()
exit(app.exec_())




