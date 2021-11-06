from PyQt5 import uic
from PyQt5.QtGui import QDoubleValidator, QIntValidator
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
        self.proteinAdder.setValidator(QDoubleValidator(0, 100, 2))
        self.fatsAdder.setValidator(QDoubleValidator(0, 100, 2))
        self.carbohydratesAdder.setValidator(QDoubleValidator(0, 100, 2))
        self.caloriesAdder.setValidator(QIntValidator(0, 3000))
        self.massAdder.setValidator(QIntValidator(0, 1000))
        self.priceAdder.setValidator(QDoubleValidator(0, 1000, 2))

    def add_new_product(self) -> None:
        try:
            name = self.nameAdder.text()
            protein = float(self.proteinAdder.text())
            fats = float(self.fatsAdder.text())
            carbohydrates = float(self.carbohydratesAdder.text())
            calories = int(self.caloriesAdder.text())
            mass = int(self.massAdder.text())
            price = float(self.priceAdder.text())
        except ValueError:
            self.adderStatusText.setText('Неверный формат!')
        else:
            self.parent.productStatusLabel.setText(
                foodproduct.create(name, protein, fats, carbohydrates, calories, mass, price))
            load_products(self.parent)
            self.close()
