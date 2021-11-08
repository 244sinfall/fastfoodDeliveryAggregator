from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from commonoperations import add_ingredients_to_list, update_selfprice, load_ingredients_to_list, \
    del_ingredient_from_list, enable_del_change_buttons
from guicommonoperations import load_foods
from foods import foods


class FoodEditMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('admin/editfood.ui', self)
        self.cancelEditorButton.clicked.connect(self.close)
        self.editConfirmButton.clicked.connect(self.edit_old_food)
        self.ingredientsShow.itemDoubleClicked.connect(
            lambda: add_ingredients_to_list(self.ingredientsToEdit, self.ingredientsShow, self.editorStatusText)
        )
        self.ingredientsToEdit.itemSelectionChanged.connect(
            lambda: enable_del_change_buttons(self.ingredientsToEdit, delete_button=self.deleteIngredient)
        )
        self.ingredientsToEdit.itemChanged.connect(
            lambda: update_selfprice(self.ingredientsToEdit, self.selfPrice)
        )
        self.deleteIngredient.clicked.connect(
            lambda: del_ingredient_from_list(self.ingredientsToEdit, self.selfPrice)
        )
        self.ingredientsToEdit.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.ingredientsToEdit.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        food_info = foods.get_food_json_dict(
            self.parent.foodsTable.item(self.parent.foodsTable.currentRow(), 0).text())
        self.priceEditor.setValue(food_info['price'])
        for ingreds in food_info['ingredients']:
            self.ingredientsToEdit.insertRow(0)
            self.ingredientsToEdit.setItem(0, 0, QTableWidgetItem(ingreds))
            self.ingredientsToEdit.setItem(0, 1, QTableWidgetItem(str(food_info['ingredients'][ingreds])))
            name = self.ingredientsToEdit.item(0, 0)
            name.setFlags(name.flags() ^ QtCore.Qt.ItemIsEditable)
        load_ingredients_to_list(self.ingredientsShow)

    def edit_old_food(self) -> None:
        price = float(self.priceEditor.value())
        try:
            rowcounts = self.ingredientsToEdit.rowCount()
            if rowcounts > 0:
                ingredients_to_edit = {}
                for checker in range(rowcounts):
                    ingredients_to_edit[f'{self.ingredientsToEdit.item(checker, 0).text()}'] = \
                        int(self.ingredientsToEdit.item(checker, 1).text())
                self.parent.foodStatusLabel.setText(
                    foods.change(self.parent.foodsTable.item(self.parent.foodsTable.currentRow(), 0).text(),
                                 price, ingredients_to_edit))
                load_foods(self.parent.foodsTable)
                self.close()
        except ValueError:
            self.editorStatusText.setText('Неверный формат!')