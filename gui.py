import datetime
import sys
from db import Database
import pymysql
import random
from PyQt5.QtCore import Qt
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QDialog, QGraphicsScene, QTableWidgetItem

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = uic.loadUi("forms/admin.ui", self)
        self.setWindowTitle("ничто")

    def authtarization(self, wnd):
        dialog = DialogAutorization(wnd)
        dialog.show()
        dialog.exec_()

class DialogAutorization(QDialog):
    def __init__(self, wnd, parent = None):
        self.wnd = wnd
        super(DialogAutorization, self).__init__(parent)
        self.ui = uic.loadUi("forms/auth.ui", self)
        self.setWindowTitle("Авторизация")
        self.db = Database()
        #password set
        self.ui.pass_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ui.pass_show_btn.clicked.connect(self.pass_show)
        self.hiden = True
        #cap set
        self.ui.cap_text.hide()
        self.ui.cap_line.hide()
        self.ui.cap_scene.hide()
        self.scene = QGraphicsScene(0, 0, 350, 50)
        self.scene.clear()
        self.ui.cap_update_btn.hide()
        self.ui.cap_update_btn.clicked.connect(self.gen_capcha)
        self.ui.cap_scene.setScene(self.scene)
        self.enter_try = 0
        self.cur_captcha = None
        #btn set
        self.ui.auth_btn.clicked.connect(self.auth)

    def auth(self):
        global auth_emp_id
        errorcount = 0
        lock = True
        login = self.ui.login_line.text()
        password = self.ui.pass_line.text()

        #проверка правильности капчи, вывод ошибки
        if self.enter_try>0 and self.ui.cap_line.text() != self.cur_captcha:
            print('i want it:')
            print(self.ui.cap_line.text())
            if errorcount == 0:
                self.error()
                errorcount+=1

            self.enter_try += 1
            lock = False
        else:
            lock = True
        print(lock)
        #генерация капчи
        if self.enter_try >= 1:
            self.gen_capcha()
        #ошибка пустых полей
        if login == '' or password == '':
            if errorcount == 0:
                self.error()
                errorcount += 1

        #несуществующий пользователь
        if login not in self.db.check_login():
            if errorcount == 0:
                self.error()
                errorcount += 1
            self.enter_try += 1
        #пользователь есть, проверка пароля
        else:
            aut = self.db.get_log(login)
            autpas = aut[0]
            role = aut[1]
            auth_emp_id = aut[2]
            #неверный пароль
            if password != autpas:
                self.enter_try += 1
                if errorcount == 0:
                    self.error()
                    errorcount += 1
            # верный пароль
            elif lock== True:
                self.ui.close()
                self.ui = AccountantWindow()
                self.ui.show()
        errorcount = 0

    def gen_capcha(self):
        self.scene.clear()
        self.ui.cap_scene.show()
        self.ui.cap_text.show()
        self.ui.cap_line.show()
        self.ui.cap_update_btn.show()
        symb = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
        s_count = 5

        cur_symb = [1, 2, 3, 4, 5]
        x, y = 30, 20
        self.scene.addLine(20, random.randint(10, 40), 300, random.randint(10, 40))
        for i in range(s_count):
            cur_symb[i] = symb[random.randint(0, 61)]
            text = self.scene.addText(f"{cur_symb[i]}")
            x += 40
            text.moveBy(x, y + random.randint(-10, 10))
        self.cur_captcha = ''.join(cur_symb)
        print('i create it:')
        print(self.cur_captcha)

    def error(self):
        self.mesbox = QMessageBox(self)
        self.mesbox.setWindowTitle("Ошибка")
        self.mesbox.setText("Ошибка входа")
        self.mesbox.setStandardButtons(QMessageBox.Ok)
        self.mesbox.show()

    def pass_show(self):
        if self.hiden == True:
            self.hiden = False
            self.ui.pass_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.hiden = True
            self.ui.pass_line.setEchoMode(QtWidgets.QLineEdit.Password)

class AccountantWindow(QMainWindow):
    def __init__(self):
        super(AccountantWindow, self).__init__()
        self.ui = uic.loadUi("forms/accountant1.ui", self)
        self.setWindowTitle("бухгалтер")
        self.table = self.ui.order_table
        self.table_bill =self.ui.bill_table
        self.table_90 = self.ui.bill_90_table
        self.db = Database()
        self.order_view()
        self.bill_view()
        #спрятать
        self.hiden_menu = True
        self.ui.Filter_Widget.hide()
        self.ui.filter_btn.clicked.connect(self.hide_menu_order)

        self.hiden_menu_bill = True
        self.ui.bill_menu.hide()
        self.ui.menu_bill_btn.clicked.connect(self.hide_menu_bill)
        self.build_combobox_clients()
        #кнопки order
        self.ui.year_filter_btn.clicked.connect(self.year_filter)
        self.ui.del_order_btn.clicked.connect(self.del_order_row)
        self.ui.update_window_btn.clicked.connect(self.upadate_order)
        self.ui.add_order_btn.clicked.connect(self.add_order_dialog)
        self.ui.dropp_filter_order_btn.clicked.connect(self.order_view)
        self.ui.exit_order_btn.clicked.connect(self.exit)
        #bill btn
        self.ui.year_bill_btn.clicked.connect(self.bill_year_filter)
        self.ui.client_bill_btn.clicked.connect(self.bill_client_filter)
        self.ui.all_filter_on.clicked.connect(self.bill_all_filter)
        self.ui.dropp_bill_filter_btn.clicked.connect(self.bill_view)
        self.ui.bill_exit_btn.clicked.connect(self.exit)
        #bill90 btn
        self.ui.btn_901.clicked.connect(self.bill_901_get)
        self.ui.btn_903.clicked.connect(self.bill_903_get)
        self.ui.exit_90.clicked.connect(self.exit)


    def hide_menu_order(self):
        if self.hiden_menu == True:
            self.ui.Filter_Widget.show()
            self.hiden_menu = False
        else:
            self.ui.Filter_Widget.hide()
            self.hiden_menu = True

    def hide_menu_bill(self):
        if self.hiden_menu_bill == True:
            self.ui.bill_menu.show()
            self.hiden_menu_bill = False
        else:
            self.ui.bill_menu.hide()
            self.hiden_menu_bill = True

    def build_combobox_clients(self):
        clients = self.db.get_client_name()
        self.client_bill_box.clear()
        if self.client_bill_box is not None:
            self.client_bill_box.addItems(clients)

    def exit(self):
        dialog = DialogAutorization(self.window)
        self.ui.close()
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()

    def get_ID(self):
        ID_data=self.ui.table.item(self.ui.table.currentRow(), 0).text()
        print(ID_data)
        return ID_data

    def is_it_intable(self, numb):
        try:
            numb=int(numb)
            return True
        except ValueError:
            self.mesbox = QMessageBox(self)
            self.mesbox.setWindowTitle("Ошибка")
            self.mesbox.setText("Введены неверные данные")
            self.mesbox.setStandardButtons(QMessageBox.Ok)
            self.mesbox.show()
            return False

    def order_view(self):
        out = self.db.print_order()
        self.print_table_order(out)

    def print_table_order(self, out):
        self.table.clear()
        self.table.setColumnCount(13)  # кол-во столбцов
        self.table.setRowCount(len(out))  # кол-во строк
        self.table.setHorizontalHeaderLabels(['ID', 'Контрагент', 'Заказанная продукция','Тип продукции','Дата регистрации', 'Дата закрытия','Цена за единицу','Количество', 'Сумма','НДС','Итоговая сумма','Статус оплаты','статус отгрузки'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.table.setItem(i, x, item)

    def upadate_order(self):
        global update_id
        update_id = self.get_ID()
        dialog = UpdateOrder()
        dialog.setWindowTitle("Редактирование заказа")
        dialog.show()
        dialog.exec_()

    def add_order_dialog(self):
        dialog = AddOrder()
        dialog.setWindowTitle("Создание заказа")
        dialog.show()
        dialog.exec_()

    def del_order_row(self):
        ID = self.get_ID()
        self.db.del_order(int(ID))
        self.order_view()

    def year_filter(self):
        if self.ui.year_filter_line.text() != '' :
            year = self.ui.year_filter_line.text()
            if self.is_it_intable(year)==True:
                if int(year)>999:
                    out = self.db.get_ord_by_year(year)
                    if out!= ():
                        self.print_table_order(out)
                    else:
                        self.mesbox = QMessageBox(self)
                        self.mesbox.setWindowTitle("нет данных")
                        self.mesbox.setText("За данный год нет заказов")
                        self.mesbox.setStandardButtons(QMessageBox.Ok)
                        self.mesbox.show()
                else:
                    self.mesbox = QMessageBox(self)
                    self.mesbox.setWindowTitle("Невозможно")
                    self.mesbox.setText("Невозможно найти данные по введенному запросу")
                    self.mesbox.setStandardButtons(QMessageBox.Ok)
                    self.mesbox.show()

        else:
            self.mesbox = QMessageBox(self)
            self.mesbox.setWindowTitle("Оштбка")
            self.mesbox.setText("Введите год")
            self.mesbox.setStandardButtons(QMessageBox.Ok)
            self.mesbox.show()


    def bill_view(self):
        out = self.db.print_bill()
        self.print_table_bill(out)

    def print_table_bill(self,out):
        self.table_bill.clear()
        self.table_bill.setColumnCount(7)  # кол-во столбцов
        self.table_bill.setRowCount(len(out))  # кол-во строк
        self.table_bill.setHorizontalHeaderLabels(
            ['ID', 'Контрагент', 'Заказанная продукция', 'Дата регистрации', 'Итоговая сумма', 'Статус оплаты', 'статус отгрузки'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.table_bill.setItem(i, x, item)

    def bill_year_filter(self):
        if self.ui.year_bill_line.text() != '':
            year = self.ui.year_bill_line.text()
            if self.is_it_intable(year) == True:
                if int(year)>999:
                    out = self.db.get_bill_by_year(year)
                    if out != ():
                        self.print_table_bill(out)
                    else:
                        self.mesbox = QMessageBox(self)
                        self.mesbox.setWindowTitle("нет данных")
                        self.mesbox.setText("За данный год нет счетов")
                        self.mesbox.setStandardButtons(QMessageBox.Ok)
                        self.mesbox.show()
                else:
                    self.mesbox = QMessageBox(self)
                    self.mesbox.setWindowTitle("Невозможно")
                    self.mesbox.setText("Невозможно найти данные по введенному запросу")
                    self.mesbox.setStandardButtons(QMessageBox.Ok)
                    self.mesbox.show()
        else:
            self.mesbox = QMessageBox(self)
            self.mesbox.setWindowTitle("Оштбка")
            self.mesbox.setText("Введите год")
            self.mesbox.setStandardButtons(QMessageBox.Ok)
            self.mesbox.show()

    def bill_client_filter(self):
        Client = self.client_bill_box.currentText()
        ClientID = self.db.get_client_id(Client)
        out=self.db.get_bill_by_client(ClientID)
        if out != ():
            self.print_table_bill(out)
        else:
            self.mesbox = QMessageBox(self)
            self.mesbox.setWindowTitle("нет данных")
            self.mesbox.setText("У данного контрагента нет счетов")
            self.mesbox.setStandardButtons(QMessageBox.Ok)
            self.mesbox.show()

    def bill_all_filter(self):
        Client = self.client_bill_box.currentText()
        ClientID = self.db.get_client_id(Client)
        if self.ui.year_bill_line.text() != '':
            year = self.ui.year_bill_line.text()
            if self.is_it_intable(year) == True:
                out = self.db.get_bill_all_filter(year, ClientID)
                if out != ():
                    self.print_table_bill(out)
                else:
                    self.mesbox = QMessageBox(self)
                    self.mesbox.setWindowTitle("нет данных")
                    self.mesbox.setText("по данному запросу ничего не найдено")
                    self.mesbox.setStandardButtons(QMessageBox.Ok)
                    self.mesbox.show()
        else:
            self.mesbox = QMessageBox(self)
            self.mesbox.setWindowTitle("Ошибка")
            self.mesbox.setText("Введите год")
            self.mesbox.setStandardButtons(QMessageBox.Ok)
            self.mesbox.show()



    def bill_901_print(self, out):
        self.table_90.clear()
        self.table_90.setColumnCount(6)  # кол-во столбцов
        self.table_90.setRowCount(len(out))  # кол-во строк
        self.table_90.setHorizontalHeaderLabels(
            ['ID Закза', 'Дата регистрации', 'Заказанная продукция', 'Тип продукции', 'Количество з. продукции', 'Сумма'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.table_90.setItem(i, x, item)

    def bill_901_get(self):
        if self.ui.year_1_line.text() != '' and self.ui.year_2_line.text() != '':
            self.bill_901_get_by_year()
        else:
            self.mesbox = QMessageBox(self)
            self.mesbox.setWindowTitle("Вывод")
            self.mesbox.setText("Фильтр не был применен, введите данные полностью")
            self.mesbox.setStandardButtons(QMessageBox.Ok)
            self.mesbox.show()
            out = self.db.bill_901()
            self.bill_901_print(out)

    def bill_901_get_by_year(self):
        start = self.ui.year_1_line.text()
        fin = self.ui.year_2_line.text()

        if self.is_it_intable(start) == True and self.is_it_intable(fin) == True:
            if int(start) > 999 and int(fin) > 999:
                out = self.db.bill_901_year(start, fin)
                self.bill_901_print(out)
            else:
                self.mesbox = QMessageBox(self)
                self.mesbox.setWindowTitle("Невозможно")
                self.mesbox.setText("Невозможно найти данные по введенному запросу")
                self.mesbox.setStandardButtons(QMessageBox.Ok)
                self.mesbox.show()

    def bill_903_print(self, out):
        self.table_90.clear()
        self.table_90.setColumnCount(4)  # кол-во столбцов
        self.table_90.setRowCount(len(out))  # кол-во строк
        self.table_90.setHorizontalHeaderLabels(
            ['ID Закза', 'Дата регистрации', 'Сумма Закза', 'НДС'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.table_90.setItem(i, x, item)
    def bill_903_get(self):
        if self.ui.year_1_line.text() != '' and self.ui.year_2_line.text() != '':
            self.bill_903_get_by_year()
        else:
            self.mesbox = QMessageBox(self)
            self.mesbox.setWindowTitle("Вывод")
            self.mesbox.setText("Фильтр не был применен, введите данные полностью")
            self.mesbox.setStandardButtons(QMessageBox.Ok)
            self.mesbox.show()
            out = self.db.bill_903()
            self.bill_903_print(out)
    def bill_903_get_by_year(self):
        start = self.ui.year_1_line.text()
        fin = self.ui.year_2_line.text()
        if self.is_it_intable(start) == True and self.is_it_intable(fin) == True:
            if int(start) > 999 and int(fin) > 999:
                out = self.db.bill_903_year(start, fin)
                self.bill_903_print(out)
            else:
                self.mesbox = QMessageBox(self)
                self.mesbox.setWindowTitle("Невозможно")
                self.mesbox.setText("Невозможно найти данные по введенному запросу")
                self.mesbox.setStandardButtons(QMessageBox.Ok)
                self.mesbox.show()




class UpdateOrder(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("forms/dialog_update.ui", self)
        self.setWindowTitle("Редактировать заказ")
        self.db = Database()
        self.preview = self.ui.oreder
        self.print_update_order(update_id)
        self.ui.update_btn_save.clicked.connect(self.update_order_upload)
        self.build_combobox_clients()
        self.build_combobox_prodtype()
        self.build_combobox_pay_stat()
        self.build_combobox_load_stat()


    def build_combobox_clients(self):
        clients = self.db.get_client_name()
        self.combo_client.clear()
        if self.combo_client is not None:
            self.combo_client.addItems(clients)

    def build_combobox_prodtype(self):
        prodtype = self.db.get_prodtype_name()
        self.combo_prod.clear()
        if self.combo_prod is not None:
            self.combo_prod.addItems(prodtype)

    def build_combobox_pay_stat(self):
        paystat = self.db.get_pay_stat_name()
        self.combo_pay.clear()
        if self.combo_pay is not None:
            self.combo_pay.addItems(paystat)

    def build_combobox_load_stat(self):
        load_stat = self.db.get_load_stat_name()
        self.combo_load.clear()
        if self.combo_load is not None:
            self.combo_load.addItems(load_stat)

    def print_update_order(self, update_id):
        self.preview.clear()
        out = self.db.print_order_by_id(update_id)
        print(out)
        self.preview.setColumnCount(13)  # кол-во столбцов
        self.preview.setRowCount(len(out))  # кол-во строк
        self.preview.setHorizontalHeaderLabels(
            ['ID', 'Контрагент', 'Заказанная продукция', 'Тип продукции', 'Дата регистрации', 'Дата закрытия',
             'Цена за единицу', 'Количество', 'Сумма', 'НДС', 'Итоговая сумма', 'Статус оплаты', 'статус отгрузки'])
        for i, order in enumerate(out):
            for x, field in enumerate(order):  # i, x - координаты ячейки, в которую будем записывать текст
                item = QTableWidgetItem()
                item.setText(str(field))  # записываем текст в ячейку
                item.setFlags(Qt.ItemIsEnabled)
                self.preview.setItem(i, x, item)

    def update_order_upload(self):
        OrderProduct =self.ui.prod_line.text()
        Client=self.combo_client.currentText()
        ClientID= self.db.get_client_id(Client)
        PricePerPiece = self.ui.price_line.value()
        quntity= self.ui.kol_line.value()
        Summ = PricePerPiece*quntity
        NDS= 0.2*Summ
        TotalSum= Summ+NDS
        EmpID = auth_emp_id
        ProdType = self.combo_prod.currentText()
        ProdTypeID = self.db.get_prodtype_id(ProdType)
        Loaded_stat=self.combo_load.currentText()
        Loaded=self.db.get_load_stat_id(Loaded_stat)
        Payed_stat=self.combo_pay.currentText()
        Payed = self.db.get_pay_stat_id(Payed_stat)
        if Loaded == 1 and Payed ==1:
           CloseDate=datetime.datetime.now().date()
           self.db.update_order_close(update_id, OrderProduct, PricePerPiece, quntity, Summ, NDS, TotalSum, CloseDate, EmpID,
                                ProdTypeID, ClientID, Loaded, Payed)
        else:
            self.db.update_order(update_id, OrderProduct, PricePerPiece, quntity, Summ, NDS, TotalSum, EmpID,ProdTypeID,
                                 ClientID, Loaded, Payed)
        self.ui.close()
class AddOrder(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("forms/dialog_add.ui", self)
        self.setWindowTitle("Создание заказа")
        self.db = Database()

        self.ui.add_order_btn.clicked.connect(self.add_order)
        self.build_combobox_clients()
        self.build_combobox_prodtype()
        self.build_combobox_pay_stat()
        self.build_combobox_load_stat()


    def build_combobox_clients(self):
        clients = self.db.get_client_name()
        self.combo_client.clear()
        if self.combo_client is not None:
            self.combo_client.addItems(clients)

    def build_combobox_prodtype(self):
        prodtype = self.db.get_prodtype_name()
        self.combo_prod.clear()
        if self.combo_prod is not None:
            self.combo_prod.addItems(prodtype)

    def build_combobox_pay_stat(self):
        paystat = self.db.get_pay_stat_name()
        self.combo_pay.clear()
        if self.combo_pay is not None:
            self.combo_pay.addItems(paystat)

    def build_combobox_load_stat(self):
        load_stat = self.db.get_load_stat_name()
        self.combo_load.clear()
        if self.combo_load is not None:
            self.combo_load.addItems(load_stat)


    def add_order(self):
        OrderProduct = self.ui.prod_line.text()
        Client = self.combo_client.currentText()
        ClientID = self.db.get_client_id(Client)
        PricePerPiece = self.ui.price_line.value()
        quntity = self.ui.kol_line.value()
        RegDate = datetime.datetime.now().date()
        Summ = PricePerPiece * quntity
        NDS = 0.2 * Summ
        TotalSum = Summ + NDS
        ProdType = self.combo_prod.currentText()
        ProdTypeID = self.db.get_prodtype_id(ProdType)
        Loaded_stat = self.combo_load.currentText()
        Loaded = self.db.get_load_stat_id(Loaded_stat)
        Payed_stat = self.combo_pay.currentText()
        Payed = self.db.get_pay_stat_id(Payed_stat)
        CloseDate = datetime.datetime.now().date()
        EmpID = auth_emp_id
        if Loaded == 1 and Payed ==1:
            self.db.insert_order_closed(OrderProduct,RegDate, PricePerPiece, quntity, Summ, NDS,
                                        TotalSum, CloseDate, EmpID, ProdTypeID,ClientID, Loaded, Payed)
        else:
            self.db.insert_order(OrderProduct,RegDate, PricePerPiece, quntity, Summ, NDS,
                                 TotalSum, EmpID, ProdTypeID, ClientID, Loaded, Payed)
        self.ui.close()

class Builder:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.wnd = MainWindow()
        self.auth()

    def auth(self):
        self.wnd.authtarization(self.wnd)
        self.app.exec()

if __name__ == '__main__':
    B = Builder()
