from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from guicommonoperations import load_products
from foodproducts import foodproduct


class ProductAddMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('admin/addproduct.ui', self)
        self.cancelAdderButton.clicked.connect(self.close)
        self.addConfirmButton.clicked.connect(self.add_new_product)

    def add_new_product(self) -> None:
        try:
            name = self.nameAdder.text()
            protein = float(self.proteinAdder.value())
            fats = float(self.fatsAdder.value())
            carbohydrates = float(self.carbohydratesAdder.value())
            calories = self.caloriesAdder.value()
            mass = self.massAdder.value()
            price = float(self.priceAdder.value())
        except ValueError:
            self.adderStatusText.setText('Неверный формат!')
        else:
            self.parent.productStatusLabel.setText(
                foodproduct.create(name, protein, fats, carbohydrates, calories, mass, price))
            load_products(self.parent)
            self.close()
