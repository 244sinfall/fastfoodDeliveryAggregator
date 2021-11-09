from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from foodproducts.foodproduct import get_partial_food_price
from foods.foods import get_food_json_dict
from json_commonoperations import open_json_to_read


class StatsView(QWidget):
    def __init__(self, parent, days):
        super().__init__()
        self.days = days
        self.parent = parent
        uic.loadUi('admin/statsview.ui', self)
        self.orders_list = open_json_to_read('orders/orders.json')
        self.foods_list = open_json_to_read('foods/foods.json')
        self.products_list = open_json_to_read('foodproducts/products.json')
        self.load_global_stats_table(days)
        self.load_realized_foods_stats_table(days)
        self.load_realized_products_stats_table()
        self.load_money_stats_table(days)
        self.closeStatsButton.clicked.connect(self.close)

    def load_global_stats_table(self, days):
        break_point = QDate.currentDate().addDays(-days)
        completed_orders = 0
        declined_orders = 0
        delivery_checks = 0
        attendance_checks = 0
        total_payment = 0
        for order in self.orders_list:
            if QDateTime.date(QDateTime.fromString(order['timeAndDate'], 'dd.MM.yyyy hh:mm')) >= break_point:
                if order['status'] == 4:  # ���������� ������ �� ����������� � �����
                    declined_orders += 1
                if order['status'] == 3:
                    completed_orders += 1
                    if order['delivery'] is True:
                        delivery_checks += 1
                    else:
                        attendance_checks += 1
                    total_payment += order['paycheck']
        daily_orders = completed_orders / days
        average_paycheck = 0.0
        if completed_orders > 0:
            average_paycheck = total_payment / completed_orders
        delivery_rate = '0.0%'
        if delivery_checks > 0:
            delivery_rate = str((delivery_checks / float(completed_orders)) * 100) + '%'
        attendance_rate = '0.0%'
        if attendance_checks > 0:
            attendance_rate = str((attendance_checks / float(completed_orders)) * 100) + '%'
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
                                    str(int(item_to_set.item(checker, 1).text()) + 1)
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

    def load_realized_products_stats_table(self):
        rowcounts = self.realizedFoodsStatsTable.rowCount()
        products_rowcount = self.realizedProductsStatsTable.rowCount()
        if rowcounts > 0:
            for row in range(rowcounts):  # Цикл по таблице с реализованной едой
                food_name = self.realizedFoodsStatsTable.item(row, 0).text()
                food_count = self.realizedFoodsStatsTable.item(row, 1).text()
                food_info = get_food_json_dict(food_name)
                for product in food_info['ingredients']:
                    if products_rowcount > 0:
                        for product_row in range(products_rowcount):  # Цикл по таблице с реализованными продуктами,
                            # проверка на отсутствие в списке
                            if self.realizedProductsStatsTable.item(product_row,
                                                                    0).text() == product:  # Уже есть в списке
                                new_amount = int(self.realizedProductsStatsTable.item(product_row, 1).text()) + (
                                            food_info['ingredients'][product] * int(food_count))
                                self.realizedProductsStatsTable.setItem(product_row, 1,
                                                                        QTableWidgetItem(
                                                                            str(int(
                                                                                self.realizedProductsStatsTable.item(
                                                                                    product_row, 1).text()) +
                                                                                (food_info['ingredients'][
                                                                                     product] * int(food_count)))))
                            else:
                                self.realizedProductsStatsTable.insertRow(products_rowcount)
                                self.realizedProductsStatsTable.setItem(products_rowcount, 0, QTableWidgetItem(product))
                                self.realizedProductsStatsTable.setItem(products_rowcount, 1, QTableWidgetItem(
                                    str(food_info['ingredients'][product] * int(food_count))
                                ))
                    else:
                        self.realizedProductsStatsTable.insertRow(0)
                        self.realizedProductsStatsTable.setItem(0, 0, QTableWidgetItem(product))
                        self.realizedProductsStatsTable.setItem(0, 1, QTableWidgetItem(
                            str(food_info['ingredients'][product] * int(food_count))
                        ))
        self.realizedProductsStatsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.realizedProductsStatsTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.realizedProductsStatsTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

    def load_money_stats_table(self, days):
        # Себестоимость продуктов:
        products_rowcount = self.realizedProductsStatsTable.rowCount()
        products_selfprice = 0.0
        if products_rowcount > 0:
            for product in range(products_rowcount):
                products_selfprice += get_partial_food_price(self.realizedProductsStatsTable.item(product, 0).text(),
                                                             int(self.realizedProductsStatsTable.item(product,
                                                                                                      1).text()))
        self.moneyStatsTable.setItem(0, 1, QTableWidgetItem(str(round(products_selfprice, 2))))
        # Прибыль от продаж
        foods_rowcount = self.realizedFoodsStatsTable.rowCount()
        foods_total_price = 0.0
        if foods_rowcount > 0:
            for foods_rows in range(foods_rowcount):
                food_info = get_food_json_dict(self.realizedFoodsStatsTable.item(foods_rows, 0).text())
                foods_total_price += food_info['price'] * int(self.realizedFoodsStatsTable.item(foods_rows, 1).text())
        self.moneyStatsTable.setItem(1, 1, QTableWidgetItem(str(round(foods_total_price, 2))))
        # Чистая прибыль
        self.moneyStatsTable.setItem(2, 1, QTableWidgetItem(str(
            round(float(self.moneyStatsTable.item(1, 1).text()) - float(self.moneyStatsTable.item(0, 1).text()), 2)
        )))
        self.moneyStatsTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.moneyStatsTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.moneyStatsTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
