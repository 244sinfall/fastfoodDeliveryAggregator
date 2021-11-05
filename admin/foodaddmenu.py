from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget

from admin.commonoperations import add_ingredients_to_list, update_selfprice
from adminmenu import load_foods
from foodproducts import foodproduct
from foods import foods


class FoodAddMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('admin/addfood.ui', self)
        self.cancelAdderButton.clicked.connect(self.close)
        self.ingredientsShow.itemDoubleClicked.connect(
            lambda: add_ingredients_to_list(self.ingredientsToAdd, self.ingredientsShow, self.adderStatusText)
        )
        self.addConfirmButton.clicked.connect(self.add_new_food)
        self.ingredientsToAdd.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ingredientsToAdd.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.ingredientsToAdd.itemSelectionChanged.connect(self.enable_del_button)
        self.ingredientsToAdd.itemChanged.connect(lambda: update_selfprice(self.ingredientsToAdd, self.selfPrice))
        self.deleteIngredient.clicked.connect(self.del_ingredient_from_list)
        self.priceAdder.setValidator(QDoubleValidator(0, 10000, 2))
        self.load_ingredients_to_list()

    def add_new_food(self):
        try:
            name = self.nameAdder.text()
            price = float(self.priceAdder.text())
        except ValueError:
            self.adderStatusText.setText('Неверный формат!')
        else:
            try:
                rowcounts = self.ingredientsToAdd.rowCount()
                if rowcounts > 0:
                    ingredients_to_add = {}
                    for checker in range(rowcounts):
                        ingredients_to_add[f'{self.ingredientsToAdd.item(checker, 0).text()}'] = \
                            int(self.ingredientsToAdd.item(checker, 1).text())
                    self.parent.foodStatusLabel.setText(
                        foods.create(name, price, ingredients_to_add))
                    load_foods(self.parent)
                    self.close()
            except ValueError:
                self.adderStatusText.setText('Неверный формат!')

    def del_ingredient_from_list(self):
        self.ingredientsToAdd.removeRow(self.ingredientsToAdd.currentRow())
        update_selfprice(self.ingredientsToAdd, self.selfPrice)

    def enable_del_button(self):
        if len(set(index.row() for index in self.ingredientsToAdd.selectedIndexes())) == 1:
            self.deleteIngredient.setEnabled(True)
        else:
            self.deleteIngredient.setEnabled(False)

    def load_ingredients_to_list(self):
        ingredients = foodproduct.get_products_list()
        for item in ingredients:
            self.ingredientsShow.addItem(item)
