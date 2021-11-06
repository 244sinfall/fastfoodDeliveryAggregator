from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget

from admin.commonoperations import add_ingredients_to_list, update_selfprice, load_ingredients_to_list, \
    del_ingredient_from_list, enable_del_button
from guicommonoperations import load_foods
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
        self.ingredientsToAdd.itemSelectionChanged.connect(
            lambda: enable_del_button(self.ingredientsToAdd, self.deleteIngredient)
        )
        self.ingredientsToAdd.itemChanged.connect(lambda: update_selfprice(self.ingredientsToAdd, self.selfPrice))
        self.deleteIngredient.clicked.connect(
            lambda: del_ingredient_from_list(self.ingredientsToAdd, self.selfPrice)
        )
        self.priceAdder.setValidator(QDoubleValidator(0, 10000, 2))
        load_ingredients_to_list(self.ingredientsShow)

    def add_new_food(self):
        # try:
            # name = self.nameAdder.text()
        price = float(self.priceAdder.text())
        # except ValueError:
            #self.adderStatusText.setText('Неверный формат!')
        try:
            rowcounts = self.ingredientsToAdd.rowCount()
            if rowcounts > 0:
                ingredients_to_add = {}
                for checker in range(rowcounts):
                    ingredients_to_add[f'{self.ingredientsToAdd.item(checker, 0).text()}'] = \
                        int(self.ingredientsToAdd.item(checker, 1).text())
                self.parent.foodStatusLabel.setText(
                    foods.create(self.nameAdder.text(), price, ingredients_to_add))
                load_foods(self.parent.foodsTable)
                self.close()
        except ValueError:
            self.adderStatusText.setText('Неверный формат!')


