from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

from admin.statsview import StatsView


class StatsInputMenu(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        uic.loadUi('admin/statsinput.ui', self)
        self.cancelStatsButton.clicked.connect(self.close)
        self.getFinaleStats.clicked.connect(lambda: self.get_stats_window(int(self.statsDaysInput.text())))
        self.statsview = None

    def get_stats_window(self, days):
        if days > 365:
            self.statsDaysInput.setText('Не больше 365...')
        else:
            self.statsview = StatsView(parent=self, days=days)
            self.statsview.show()
            self.hide()


