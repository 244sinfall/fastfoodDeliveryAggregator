from PyQt5 import uic
from PyQt5.QtGui import QDoubleValidator, QIntValidator
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

        self.proteinEditor.setValidator(QDoubleValidator(0, 100, 2))
        self.fatsEditor.setValidator(QDoubleValidator(0, 100, 2))
        self.carbohydratesEditor.setValidator(QDoubleValidator(0, 100, 2))
        self.caloriesEditor.setValidator(QIntValidator(0, 3000))
        self.priceEditor.setValidator(QDoubleValidator(0, 1000, 2))

        product_info = foodproduct.get_product_info(
            self.parent.productsTable.item(self.parent.productsTable.currentRow(), 0).text())
        self.proteinEditor.setText(str(product_info['protein']))
        self.fatsEditor.setText(str(product_info['fats']))
        self.carbohydratesEditor.setText(str(product_info['carbohydrates']))
        self.caloriesEditor.setText(str(product_info['calories']))
        self.priceEditor.setText(str(product_info['price']))

    def edit_old_product(self) -> None:
        try:
            protein = float(self.proteinEditor.text())
            fats = float(self.fatsEditor.text())
            carbohydrates = float(self.carbohydratesEditor.text())
            calories = int(self.caloriesEditor.text())
            price = float(self.priceEditor.text())
        except ValueError:
            self.editorStatusText.setText('Неверный формат!')
        else:
            self.parent.productStatusLabel.setText(
                foodproduct.change(self.parent.productsTable.item(self.parent.productsTable.currentRow(), 0).text(),
                                   protein, fats, carbohydrates, calories, price))
            load_products(self.parent)
            self.close()