from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class StatsView(QWidget):
    def __init__(self, parent, days):
        super().__init__()
        self.parent = parent
        uic.loadUi('admin/statsview.ui', self)
