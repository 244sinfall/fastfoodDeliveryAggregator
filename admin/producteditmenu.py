from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from guicommonoperations import load_products
from foodproducts import foodproduct


class ProductEditMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('admin/editproduct.ui', self)
        self.cancelEditorButton.clicked.connect(self.close)
        self.editConfirmButton.clicked.connect(self.edit_old_product)

        product_info = foodproduct.get_product_info(
            self.parent.productsTable.item(self.parent.productsTable.currentRow(), 0).text())
        self.proteinEditor.setValue(product_info['protein'])
        self.fatsEditor.setValue(product_info['fats'])
        self.carbohydratesEditor.setValue(product_info['carbohydrates'])
        self.caloriesEditor.setValue(product_info['calories'])
        self.priceEditor.setValue(product_info['price'])

    def edit_old_product(self) -> None:
        try:
            protein = float(self.proteinEditor.value())
            fats = float(self.fatsEditor.value())
            carbohydrates = float(self.carbohydratesEditor.value())
            calories = self.caloriesEditor.value()
            price = float(self.priceEditor.value())
        except ValueError:
            self.editorStatusText.setText('Неверный формат!')
        else:
            self.parent.productStatusLabel.setText(
                foodproduct.change(self.parent.productsTable.item(self.parent.productsTable.currentRow(), 0).text(),
                                   protein, fats, carbohydrates, calories, price))
            load_products(self.parent)
            self.close()
