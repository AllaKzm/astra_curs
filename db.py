import datetime

import pymysql

class Database:

    def __init__(self):
        self.connection= pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='astra',
        )
#login
    def check_login(self):
        log = []
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT Login FROM Employee""")
        rows = cursor.fetchall()
        for i in rows:
            for j in i:
                log.append(j)
        return log

    def get_log(self, login):
        log = []
        cursor = self.connection.cursor()
        cursor.execute(f"""SELECT Password, PosID, EmpID FROM employee WHERE Login = '{login}'""")
        rows = cursor.fetchall()
        for i in rows:
            for j in i:
                log.append(j)
        return log

#client
    def get_client_name(self):
        clients = []
        cursor = self.connection.cursor()
        cursor.execute(f"select ClientName from clients")
        clnt = cursor.fetchall()
        cursor.close()
        for i in clnt:
            clients.append(str(i)[2:-3])
        return clients
    def get_client_id(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT ClientID FROM clients WHERE ClientName='{name}'")
        clnt = cursor.fetchone()
        cursor.close()
        return clnt[0]

#product type
    def get_prodtype_name(self):
        prodtype = []
        cursor = self.connection.cursor()
        cursor.execute('select ProdTitle from producttype')
        type = cursor.fetchall()
        cursor.close()
        for i in type:
            prodtype.append(str(i)[2:-3])
        return prodtype
    def get_prodtype_id(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT ProdID FROM producttype WHERE ProdTitle='{name}'")
        prod = cursor.fetchone()
        cursor.close()
        return prod[0]

    #status_pay
    def get_pay_stat_name(self):
        status_p = []
        cursor = self.connection.cursor()
        cursor.execute('select PayStatTitle from paystatus')
        pay = cursor.fetchall()
        cursor.close()
        for i in pay:
            status_p.append(str(i)[2:-3])
        return status_p
    def get_pay_stat_id(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT idPayStatus FROM paystatus WHERE PayStatTitle='{name}'")
        pay_stat = cursor.fetchone()
        cursor.close()
        return pay_stat[0]
    #status_load
    def get_load_stat_name(self):
        status_l = []
        cursor = self.connection.cursor()
        cursor.execute('select loadstatustitle from loadstatus')
        load = cursor.fetchall()
        cursor.close()
        for i in load:
            status_l.append(str(i)[2:-3])
        return status_l

    def get_load_stat_id(self, name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT idloadstatus FROM loadstatus WHERE loadstatustitle='{name}'")
        load_stat = cursor.fetchone()
        cursor.close()
        return load_stat[0]

    #вывод красиво заказов
    def print_order(self):
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT orders.OrderID,clients.ClientName, orders.OrderProduct,producttype.ProdTitle, "
                       f"orders.RegDate, orders.CloseDate, orders.PricePerPiece, orders.quntity, orders.Summ, orders.NDS, orders.TotalSum, "
                       f"paystatus.PayStatTitle,  loadstatus.loadstatustitle "
                       f"FROM orders AS orders "
                       f"INNER JOIN paystatus AS paystatus ON orders.Payed = paystatus.idPayStatus "
                       f"inner join clients as clients On orders.ClientID = clients.ClientID "
                       f"inner join loadstatus as loadstatus on orders.Loaded = loadstatus.idLoadStatus "
                       f"inner join producttype as producttype on orders.ProdTypeID = producttype.ProdID;")
        order = cursor.fetchall()
        cursor.close()
        return order

    def print_order_by_id(self,id):
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT orders.OrderID,clients.ClientName, orders.OrderProduct,producttype.ProdTitle, "
                       f"orders.RegDate, orders.CloseDate, orders.Summ, orders.quntity, orders.NDS, orders.TotalSum, "
                       f"paystatus.PayStatTitle,  loadstatus.loadstatustitle "
                       f"FROM orders AS orders "
                       f"INNER JOIN paystatus AS paystatus ON orders.Payed = paystatus.idPayStatus "
                       f"inner join clients as clients On orders.ClientID = clients.ClientID "
                       f"inner join loadstatus as loadstatus on orders.Loaded = loadstatus.idLoadStatus "
                       f"inner join producttype as producttype on orders.ProdTypeID = producttype.ProdID"
                       f" WHERE OrderID='{id}';")
        order = cursor.fetchall()
        cursor.close()
        return order

    def update_order(self,OrderID, OrderProduct, PricePerPiece, quntity, Summ, NDS, TotalSum, EmpID,ProdTypeID,ClientID, Loaded, Payed ):
        cursor = self.connection.cursor()
        cursor.execute(f"update orders SET OrderProduct='{OrderProduct}', PricePerPiece='{PricePerPiece}', quntity='{quntity}', Summ='{Summ}', NDS='{NDS}', TotalSum='{TotalSum}', EmpID='{EmpID}',ProdTypeID='{ProdTypeID}', ClientID='{ClientID}', Loaded='{Loaded}', Payed='{Payed}' WHERE OrderID='{OrderID}'")
        cursor.close()
        self.connection.commit()

    def update_order_close(self, OrderID, OrderProduct, PricePerPiece, quntity, Summ, NDS, TotalSum, CloseDate, EmpID,
                     ProdTypeID, ClientID, Loaded, Payed):
        cursor = self.connection.cursor()
        cursor.execute(
            f"update orders SET OrderProduct='{OrderProduct}', PricePerPiece='{PricePerPiece}', quntity='{quntity}', "
            f"Summ='{Summ}', NDS='{NDS}', TotalSum='{TotalSum}', CloseDate='{CloseDate}', EmpID='{EmpID}',"
            f"ProdTypeID='{ProdTypeID}', ClientID='{ClientID}', Loaded='{Loaded}', Payed='{Payed}' WHERE OrderID='{OrderID}'")
        cursor.close()
        self.connection.commit()

    def insert_order(self,  OrderProduct,RegDate, PricePerPiece, quntity, Summ, NDS, TotalSum, EmpID, ProdTypeID,
                     ClientID, Loaded, Payed):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO orders VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, NULL, %s, %s, %s, %s,%s)",
                       (OrderProduct,RegDate, PricePerPiece, quntity, Summ, NDS, TotalSum, EmpID, ProdTypeID, ClientID, Loaded, Payed))
        cursor.close()
        self.connection.commit()

    def insert_order_closed(self,  OrderProduct,RegDate, PricePerPiece, quntity, Summ, NDS, TotalSum, CloseDate, EmpID, ProdTypeID,
                     ClientID, Loaded, Payed):
        cursor = self.connection.cursor()
        cursor.execute(f"INSERT INTO orders VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                       (OrderProduct,RegDate, PricePerPiece, quntity, Summ, NDS, TotalSum,CloseDate, EmpID, ProdTypeID, ClientID, Loaded, Payed))
        cursor.close()
        self.connection.commit()

    def del_order(self,id):
        cursor = self.connection.cursor()
        cursor.execute(f"""DELETE from orders WHERE OrderID={id}""")
        cursor.close()
        self.connection.commit()

        # фильтр по году
        def get_ord_by_year(self, year):
            year_start = year + '-01-01'
            year_fin = year + '-12-31'
            date_start = datetime.datetime.strptime(year_start, '%Y-%m-%d').date()
            date_fin = datetime.datetime.strptime(year_fin, '%Y-%m-%d').date()
            print(date_start)
            print(date_fin)
            cursor = self.connection.cursor()
            cursor.execute(f" SELECT orders.OrderID,clients.ClientName, orders.OrderProduct,producttype.ProdTitle, "
                           f"orders.RegDate, orders.CloseDate, orders.PricePerPiece, orders.quntity, orders.Summ, orders.NDS, orders.TotalSum, "
                           f"paystatus.PayStatTitle,  loadstatus.loadstatustitle "
                           f"FROM orders AS orders "
                           f"INNER JOIN paystatus AS paystatus ON orders.Payed = paystatus.idPayStatus "
                           f"inner join clients as clients On orders.ClientID = clients.ClientID "
                           f"inner join loadstatus as loadstatus on orders.Loaded = loadstatus.idLoadStatus "
                           f"inner join producttype as producttype on orders.ProdTypeID = producttype.ProdID "
                           f" WHERE RegDate BETWEEN '{date_start}' AND '{date_fin}';")
            order = cursor.fetchall()
            cursor.close()
            return order

    def get_ord_by_year(self, year):
        year_start = year + '-01-01'
        year_fin = year + '-12-31'
        date_start = datetime.datetime.strptime(year_start, '%Y-%m-%d').date()
        date_fin = datetime.datetime.strptime(year_fin, '%Y-%m-%d').date()
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT orders.OrderID,clients.ClientName, orders.OrderProduct,producttype.ProdTitle, "
                       f"orders.RegDate, orders.CloseDate, orders.PricePerPiece, orders.quntity, orders.Summ, orders.NDS, orders.TotalSum, "
                       f"paystatus.PayStatTitle,  loadstatus.loadstatustitle "
                       f"FROM orders AS orders "
                       f"INNER JOIN paystatus AS paystatus ON orders.Payed = paystatus.idPayStatus "
                       f"inner join clients as clients On orders.ClientID = clients.ClientID "
                       f"inner join loadstatus as loadstatus on orders.Loaded = loadstatus.idLoadStatus "
                       f"inner join producttype as producttype on orders.ProdTypeID = producttype.ProdID"
                       f" WHERE RegDate BETWEEN '{date_start}' AND '{date_fin}';")
        order = cursor.fetchall()
        cursor.close()
        return order

    #счета
    def print_bill(self):
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT orders.OrderID,clients.ClientName, orders.OrderProduct, "
                       f"orders.RegDate, orders.TotalSum, "
                       f"paystatus.PayStatTitle,  loadstatus.loadstatustitle "
                       f"FROM orders AS orders "
                       f"INNER JOIN paystatus AS paystatus ON orders.Payed = paystatus.idPayStatus "
                       f"inner join clients as clients On orders.ClientID = clients.ClientID "
                       f"inner join loadstatus as loadstatus on orders.Loaded = loadstatus.idLoadStatus;")
        bill = cursor.fetchall()
        cursor.close()
        return bill
    def get_bill_by_year(self, year):
        year_start=year+'-01-01'
        year_fin = year + '-12-31'
        date_start = datetime.datetime.strptime(year_start, '%Y-%m-%d').date()
        date_fin = datetime.datetime.strptime(year_fin, '%Y-%m-%d').date()
        print(date_start)
        print(date_fin)
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT orders.OrderID,clients.ClientName, orders.OrderProduct, "
                       f"orders.RegDate, orders.TotalSum, "
                       f"paystatus.PayStatTitle,  loadstatus.loadstatustitle "
                       f"FROM orders AS orders "
                       f"INNER JOIN paystatus AS paystatus ON orders.Payed = paystatus.idPayStatus "
                       f"inner join clients as clients On orders.ClientID = clients.ClientID "
                       f"inner join loadstatus as loadstatus on orders.Loaded = loadstatus.idLoadStatus "
                       f"inner join producttype as producttype on orders.ProdTypeID = producttype.ProdID"
                       f" WHERE RegDate BETWEEN '{date_start}' AND '{date_fin}';")
        bill = cursor.fetchall()
        cursor.close()
        return bill
    def get_bill_by_client(self, client):
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT orders.OrderID,clients.ClientName, orders.OrderProduct, "
                       f"orders.RegDate, orders.TotalSum, "
                       f"paystatus.PayStatTitle,  loadstatus.loadstatustitle "
                       f"FROM orders AS orders "
                       f"INNER JOIN paystatus AS paystatus ON orders.Payed = paystatus.idPayStatus "
                       f"inner join clients as clients On orders.ClientID = clients.ClientID "
                       f"inner join loadstatus as loadstatus on orders.Loaded = loadstatus.idLoadStatus "
                       f"inner join producttype as producttype on orders.ProdTypeID = producttype.ProdID"
                       f" WHERE orders.ClientID ='{client}' ;")
        bill = cursor.fetchall()
        cursor.close()
        return bill
    def get_bill_all_filter(self,year,client):
        year_start = year + '-01-01'
        year_fin = year + '-12-31'
        date_start = datetime.datetime.strptime(year_start, '%Y-%m-%d').date()
        date_fin = datetime.datetime.strptime(year_fin, '%Y-%m-%d').date()
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT orders.OrderID,clients.ClientName, orders.OrderProduct, "
                       f"orders.RegDate, orders.TotalSum, "
                       f"paystatus.PayStatTitle,  loadstatus.loadstatustitle "
                       f"FROM orders AS orders "
                       f"INNER JOIN paystatus AS paystatus ON orders.Payed = paystatus.idPayStatus "
                       f"inner join clients as clients On orders.ClientID = clients.ClientID "
                       f"inner join loadstatus as loadstatus on orders.Loaded = loadstatus.idLoadStatus "
                       f"inner join producttype as producttype on orders.ProdTypeID = producttype.ProdID"
                       f" WHERE orders.ClientID ='{client}' AND RegDate BETWEEN '{date_start}' AND '{date_fin}' ;")
        bill = cursor.fetchall()
        cursor.close()
        return bill

#счета 90
    def bill_903(self):
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT OrderID, RegDate, TotalSum, NDS FROM orders WHERE Loaded=1 AND Payed=1;")
        bill = cursor.fetchall()
        cursor.close()
        return bill
    def bill_903_year(self, start,fin):
        start = start + '-01-01'
        fin = fin + '-12-31'
        date_start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        date_fin = datetime.datetime.strptime(fin, '%Y-%m-%d').date()
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT OrderID, RegDate, TotalSum, NDS FROM orders WHERE Loaded=1 AND Payed=1 AND RegDate BETWEEN '{date_start}' AND '{date_fin}';")
        bill = cursor.fetchall()
        cursor.close()
        return bill

    def bill_901(self):
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT orders.OrderID, orders.RegDate, orders.OrderProduct, producttype.ProdTitle, "
                       f"orders.quntity, orders.Summ "
                       f"FROM orders AS orders "
                       f"inner join producttype as producttype on orders.ProdTypeID = producttype.ProdID"
                       f" WHERE Loaded=1 AND Payed=1;")
        bill = cursor.fetchall()
        cursor.close()
        return bill
    def bill_901_year(self, start,fin):
        start = start + '-01-01'
        fin = fin + '-12-31'
        date_start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        date_fin = datetime.datetime.strptime(fin, '%Y-%m-%d').date()
        cursor = self.connection.cursor()
        cursor.execute(f" SELECT orders.OrderID, orders.RegDate, orders.OrderProduct, producttype.ProdTitle, "
                       f"orders.quntity, orders.Summ "
                       f"FROM orders AS orders "
                       f"inner join producttype as producttype on orders.ProdTypeID = producttype.ProdID"
                       f" WHERE Loaded=1 AND Payed=1 AND RegDate BETWEEN '{date_start}' AND '{date_fin}';")
        bill = cursor.fetchall()
        cursor.close()
        return bill








if __name__ == '__main__':
    db = Database()
    year="2022"
    id=db.get_client_id('Milka')


    print(db.bill_901_year('2023','2023'))

