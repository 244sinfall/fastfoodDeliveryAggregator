from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from json_commonoperations import open_json_to_read


class StatsView(QWidget):
    def __init__(self, parent, days):
        super().__init__()
        self.days = days
        self.parent = parent
        uic.loadUi('admin/statsview.ui', self)
        self.orders_list = open_json_to_read('orders/orders.json')
        self.load_global_stats_table(days)
        self.load_realized_foods_stats_table(days)
        #self.load_realized_products_stats_table(days)
        #self.load_money_stats_table(days)

    def load_global_stats_table(self, days):
        break_point = QDate.currentDate().addDays(-days)
        completed_orders = 0
        declined_orders = 0
        delivery_checks = 0
        attendance_checks = 0
        total_payment = 0
        for order in self.orders_list:
            if QDateTime.date(QDateTime.fromString(order['timeAndDate'], 'dd.MM.yyyy hh:mm')) >= break_point:
                if order['status'] == 4:  # Отмененные заказы не учитываются в долях
                    declined_orders += 1
                if order['status'] == 3:
                    completed_orders += 1
                    if order['delivery'] is True:
                        delivery_checks += 1
                    else:
                        attendance_checks += 1
                    total_payment += order['paycheck']
        daily_orders = completed_orders/days
        average_paycheck = total_payment/completed_orders
        delivery_rate = '0.0%'
        if delivery_checks > 0:
            delivery_rate = str((delivery_checks/float(completed_orders))*100) + '%'
        attendance_rate = '0.0%'
        if attendance_checks > 0:
            attendance_rate = str((attendance_checks/float(completed_orders))*100) + '%'
        self.globalStatsTable.setItem(0, 1, QTableWidgetItem(str(completed_orders)))
        self.globalStatsTable.setItem(1, 1, QTableWidgetItem(str(declined_orders)))
        self.globalStatsTable.setItem(2, 1, QTableWidgetItem(str(daily_orders)))
        self.globalStatsTable.setItem(3, 1, QTableWidgetItem(str(average_paycheck)))
        self.globalStatsTable.setItem(4, 1, QTableWidgetItem(delivery_rate))
        self.globalStatsTable.setItem(5, 1, QTableWidgetItem(attendance_rate))
        self.globalStatsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.globalStatsTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.globalStatsTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def load_realized_foods_stats_table(self, days):
        break_point = QDate.currentDate().addDays(-days)
        for order in self.orders_list:
            if QDateTime.date(QDateTime.fromString(order['timeAndDate'], 'dd.MM.yyyy hh:mm')) >= break_point:
                for food in order['order']:
                    counted = False
                    rowcounts = self.realizedFoodsStatsTable.rowCount()
                    if rowcounts > 0:
                        for checker in range(rowcounts):
                            if self.realizedFoodsStatsTable.item(checker, 0).text() == food:
                                item_to_set = self.realizedFoodsStatsTable
                                item_to_set.setItem(checker, 1, QTableWidgetItem(
                                    str(int(item_to_set.item(checker, 1).text())+1)
                                ))
                                counted = True
                                break
                    if not counted:
                        self.realizedFoodsStatsTable.insertRow(rowcounts)
                        self.realizedFoodsStatsTable.setItem(rowcounts, 0, QTableWidgetItem(food))
                        self.realizedFoodsStatsTable.setItem(rowcounts, 1, QTableWidgetItem('1'))
        self.realizedFoodsStatsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.realizedFoodsStatsTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.realizedFoodsStatsTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)




