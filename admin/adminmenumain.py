from PyQt5 import uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget

from commonoperations import enable_del_change_buttons
from admin.foodaddmenu import FoodAddMenu
from admin.foodeditmenu import FoodEditMenu
from admin.productaddmenu import ProductAddMenu
from admin.producteditmenu import ProductEditMenu
from admin.statsinputmenu import StatsInputMenu
from foodproducts import foodproduct
from foods import foods
from foods.foods import is_product_usable
from guicommonoperations import load_orders, load_products, load_foods
from orders.orders import delete


class AdminMenu(QWidget):
    # Меню администратора. Дальнейшее взаимодействие идет по директории /admin
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('admin/adminmenu.ui', self)
        self.adminExitButton.clicked.connect(self.close)

        self.ordersTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ordersTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ordersTable.itemSelectionChanged.connect(self.delete_order_trigger)
        self.deleteOrderButton.clicked.connect(self.delete_order)

        self.getStatsButton.clicked.connect(self.stat_input_menu)
        self.statsinputer = None
        load_orders(self)

        self.productsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.productsTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.addProductButton.clicked.connect(self.add_product)
        self.addproducter = None

        self.editProductButton.clicked.connect(self.edit_product)
        self.editproducter = None

        self.productsTable.itemSelectionChanged.connect(
            lambda: enable_del_change_buttons(self.productsTable, edit_button=self.editProductButton,
                                              delete_button=self.deleteProductButton)
        )
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

        self.foodsTable.itemSelectionChanged.connect(
            lambda: enable_del_change_buttons(self.foodsTable, edit_button=self.editFoodButton,
                                              delete_button=self.deleteFoodButton)
        )
        load_foods(self.foodsTable)

    def delete_order_trigger(self):
        if len(set(index.row() for index in self.ordersTable.selectedIndexes())) == 1:
            self.deleteOrderButton.setEnabled(True)
        else:
            self.deleteOrderButton.setEnabled(False)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.show()
        super().closeEvent(a0)

    def delete_food(self):
        name_to_delete = str(self.foodsTable.item(self.foodsTable.currentRow(), 0).text())
        self.foodStatusLabel.setText(foods.delete(name_to_delete))
        load_foods(self.foodsTable)

    def delete_order(self):
        id_to_delete = int(self.ordersTable.item(self.ordersTable.currentRow(), 0).text())
        self.orderStatusLabel.setText(delete(id_to_delete))  # orders/orders.py
        load_orders(self)

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

    def stat_input_menu(self) -> None:
        self.statsinputer = StatsInputMenu(parent=self)
        self.statsinputer.show()