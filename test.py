import sys
from unittest import TestCase

from PyQt5 import QtCore
from PyQt5.QtCore import QDate, QItemSelectionModel
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication

from db import Database
from gui import MainWindow, DialogAutorization, AddOrder, UpdateOrder, AccountantWindow


class Test_database(TestCase):
    def setUp(self):
        self.qapp = QApplication(sys.argv)
        self.db = Database()
        self.window = MainWindow()
        self.menu = AccountantWindow()
        self.ord = AddOrder()
        self.auth = DialogAutorization(self.window)

    def test_auth(self):
        self.auth.ui.login_line.setText('test')
        self.auth.ui.pass_line.setText('1')
        QTest.mouseClick(self.auth.ui.auth_btn, QtCore.Qt.MouseButton.LeftButton)

    def test_push_order(self):
        self.test_auth()
        self.ord.prod_line.setText("Test")
        self.ord.ui.price_line.setValue(700)
        self.ord.ui.kol_line.setValue(10)

        QTest.mouseClick(self.ord.ui.add_order_btn, QtCore.Qt.MouseButton.LeftButton)

    def test_del_ord(self):
        rowcount = self.menu.table.rowCount()
        self.menu.table.setCurrentCell(rowcount - 1, 1, QItemSelectionModel.SelectionFlag.Select)
        QTest.mouseClick(self.menu.ui.del_order_btn, QtCore.Qt.MouseButton.LeftButton)

    def test_year_filter(self):
        self.menu.ui.year_filter_line.setText("2022")
        QTest.mouseClick(self.menu.ui.year_filter_btn, QtCore.Qt.MouseButton.LeftButton)


