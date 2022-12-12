from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode

config = {
    'port': '3006',
    'user': 'root',
    'password': 'Studman081!',
    'host': 'localhost',
    'database': 'bacchus_winery',
    'raise_on_warnings': True
}
try:
    mydb = mysql.connector.connect(**config)

    print("\n Database user {} connected to MySQL on host {} with database {}".format(
        config["user"], config["host"], config["database"]))
    input("\n\n Press any key to continue...\n")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print(" The supplied username or password are invalid")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(" The specified database does not exist")
    else:
        print(err)

DB_NAME = 'bacchus_winery'

myCursor = mydb.cursor()


# Function to erase tables if they exist to start with a clean database
def drop_tables(myCursor):
    tables = "DROP TABLE IF EXISTS wine, orders, distributors, supplies, suppliers, deliveries, " \
             "employees, time_sheet"
    myCursor.execute(tables)
    mydb.commit()


drop_tables(myCursor)

# Create tables
TABLES = {'wine': (
    "CREATE TABLE wine"
    "(wine_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
    "wine_name varchar(25) NOT NULL,"
    "bottle_inventory int NOT NULL)"),
    'distributors': (
        "CREATE TABLE distributors"
        "(distributor_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "distributor_name varchar(25) NOT NULL,"
        "city varchar(25) NOT NULL,"
        "state varchar(25) NOT NULL)"),
    'orders': (
        "CREATE TABLE orders"
        "(order_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "order_date date NOT NULL,"
        "bottles int NOT NULL,"
        "distributor_id int NOT NULL,"
        "wine_id int NOT NULL,"
        "CONSTRAINT fk_distributors FOREIGN KEY (distributor_id) REFERENCES distributors"
        "(distributor_id),"
        "CONSTRAINT fk_wine FOREIGN KEY (wine_id) REFERENCES wine(wine_id))"),
    'supplies': (
        "CREATE TABLE supplies"
        "(supply_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "supply_name varchar(25) NOT NULL,"
        "inventory int NOT NULL)"),
    'suppliers': (
        "CREATE TABLE suppliers"
        "(supplier_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "supplier_name varchar(25) NOT NULL,"
        "city varchar(25) NOT NULL,"
        "state varchar(25) NOT NULL)"),
    'deliveries': (
        "CREATE TABLE deliveries"
        "(delivery_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "supply_id int NOT NULL,"
        "units int NOT NULL,"
        "expected_delivery_date DATE,"
        "actual_delivery_date DATE,"
        "supplier_id int NOT NULL,"
        "delivery_timing varchar(25) NOT NULL,"
        "CONSTRAINT fk_supplies FOREIGN KEY (supply_id) REFERENCES supplies(supply_id),"
        "CONSTRAINT fk_suppliers FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id))"),
    'employees': (
        "CREATE TABLE employees"
        "(employee_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "first_name varchar(25) NOT NULL,"
        "last_name varchar(25) NOT NULL,"
        "job_title varchar(50) NOT NULL)"),
    'time_sheet': (
        "CREATE TABLE time_sheet"
        "(input_id int NOT NULL AUTO_INCREMENT PRIMARY KEY,"
        "quarter_id int NOT NULL,"
        "regular_hours_worked_quarterly int NOT NULL,"
        "ot_worked_quarterly int NOT NULL,"
        "employee_id int NOT NULL,"
        "CONSTRAINT fk_employees FOREIGN KEY (employee_id) REFERENCES employees(employee_id))")}

# Show that each table is created okay or print out error
for table_name in TABLES:
    table_description = TABLES[table_name]
    try:
        print("Creating table {}: ".format(table_name), end='')
        myCursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
    else:
        print("OK\n")

# Inset values into wine table
add_wines = "INSERT INTO wine (wine_name, bottle_inventory) VALUES (%s, %s)"
wine_data = [('Merlot', 50), ('Cabernet', 40), ('Chablis', 60), ('Chardonnay', 50)]

myCursor.executemany(add_wines, wine_data)

# Insert values into distributors table
add_distributors = "INSERT INTO distributors(distributor_name, city, state) VALUES (%s, %s, %s)"
distributor_data = [('Wines to GO', 'Orlando', 'FL'), ('Partners in Wine', 'Anaheim', 'CA'),
                    ('Sip Happens Co.', 'Dallas', 'TX')]

myCursor.executemany(add_distributors, distributor_data)

# Insert values into orders table
ORDERS = {'order1': (
    "INSERT INTO orders (order_date,bottles, distributor_id, wine_id) VALUES (20220110, 10, "
    "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Sip Happens Co.'), "
    "(SELECT wine_id FROM wine WHERE wine_name = 'Merlot'))"),
    'order2': (
        "INSERT INTO orders (order_date, bottles, distributor_id, wine_id) VALUES (20220201, 15, "
        "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Wines to GO'), "
        "(SELECT wine_id FROM wine WHERE wine_name = 'Cabernet'))"),
    'order3': (
        "INSERT INTO orders (order_date, bottles, distributor_id, wine_id) VALUES (20220320, 12, "
        "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Partners in Wine'), "
        "(SELECT wine_id FROM wine WHERE wine_name = 'Chablis'))"),
    'order4': (
        "INSERT INTO orders (order_date, bottles, distributor_id, wine_id) VALUES (20220413, 10, "
        "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Wines to GO'), "
        "(SELECT wine_id FROM wine WHERE wine_name = 'Chardonnay'))"),
    'order5': (
        "INSERT INTO orders (order_date,bottles, distributor_id, wine_id) VALUES (20220710, 30, "
        "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Sip Happens Co.'), "
        "(SELECT wine_id FROM wine WHERE wine_name = 'Cabernet'))"),
    'order6': (
        "INSERT INTO orders (order_date, bottles, distributor_id, wine_id) VALUES (20220825, 25, "
        "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Partners in Wine'), "
        "(SELECT wine_id FROM wine WHERE wine_name = 'Merlot'))"),
    'order7': (
        "INSERT INTO orders (order_date, bottles, distributor_id, wine_id) VALUES (20220901, 15, "
        "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Wines to GO'), "
        "(SELECT wine_id FROM wine WHERE wine_name = 'Cabernet'))"),
    'order8': (
        "INSERT INTO orders (order_date, bottles, distributor_id, wine_id) VALUES (20221002, 15, "
        "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Partners in Wine'), "
        "(SELECT wine_id FROM wine WHERE wine_name = 'Chardonnay'))"),
    'order9': (
        "INSERT INTO orders (order_date, bottles, distributor_id, wine_id) VALUES (20221119, 10, "
        "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Wines to GO'), "
        "(SELECT wine_id FROM wine WHERE wine_name = 'Chardonnay'))"),
    'order10': (
        "INSERT INTO orders (order_date,bottles, distributor_id, wine_id) VALUES (20221218, 30, "
        "(SELECT distributor_id FROM distributors WHERE distributor_name = 'Sip Happens Co.'), "
        "(SELECT wine_id FROM wine WHERE wine_name = 'Chablis'))"),}

for order_number in ORDERS:
    orderNumbers = ORDERS[order_number]
    myCursor.execute(orderNumbers)

# Inset values into supplies table
add_supplies = "INSERT INTO supplies (supply_name, inventory) VALUES (%s, %s)"
supply_data = [('Bottles', 300), ('Corks', 420), ('Labels', 290), ('Boxes', 100), ('Vats', 75),
               ('Tubing', 80)]

myCursor.executemany(add_supplies, supply_data)

# Insert values into suppliers table
add_suppliers = "INSERT INTO suppliers(supplier_name, city, state) VALUES (%s, %s, %s)"
supplier_data = [('The New Corker', 'New York', 'NY'), ('Boxes n Stuff', 'Chicago', 'IL'),
                 ('Wine Supply', 'Fargo', 'ND')]

myCursor.executemany(add_suppliers, supplier_data)

# Insert values into deliveries table
DELIVERIES = {'delivery1': (
    "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
    "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
    "'Corks'), 50, 20220110, 20220115, (SELECT supplier_id FROM suppliers WHERE supplier_name = "
    "'The New Corker'), 'LATE - 5 Days')"),
    'delivery2': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Boxes'), 40, 20220215, 20220215, (SELECT supplier_id FROM suppliers WHERE supplier_name "
        "= 'Boxes n Stuff'), 'On Time')"),
    'delivery3': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Tubing'), 60, 20220320, 20220415, (SELECT supplier_id FROM suppliers WHERE supplier_name "
        "= 'Wine Supply'), 'LATE - 26 Days')"),
    'delivery4': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Bottles'), 100, 20220422, 20220420, (SELECT supplier_id FROM suppliers WHERE "
        "supplier_name = 'The New Corker'), 'Early - 2 Days')"),
    'delivery5': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Labels'), 200, 20220501, 20220505, (SELECT supplier_id FROM suppliers WHERE "
        "supplier_name = 'Boxes n Stuff'), 'LATE - 4 Days')"),
    'delivery6': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Vats'), 10, 20220601, null, (SELECT supplier_id FROM suppliers WHERE supplier_name = "
        "'Wine Supply'), 'LATE')"),
    'delivery7': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Boxes'), 40, 20220712, 20220715, (SELECT supplier_id FROM suppliers WHERE supplier_name "
        "= 'Boxes n Stuff'), 'LATE - 3 Days')"),
    'delivery8': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Tubing'), 60, 20220820, 20220815, (SELECT supplier_id FROM suppliers WHERE supplier_name "
        "= 'Wine Supply'), 'Early - 5 Days')"),
    'delivery9': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Bottles'), 100, 20220922, 20220922, (SELECT supplier_id FROM suppliers WHERE "
        "supplier_name = 'The New Corker'), 'On Time')"),
    'delivery10': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Labels'), 200, 20221001, 20221101, (SELECT supplier_id FROM suppliers WHERE "
        "supplier_name = 'Boxes n Stuff'), 'LATE - 30 Days')"),
    'delivery11': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Vats'), 10, 20221115, 20221125, (SELECT supplier_id FROM suppliers WHERE supplier_name = "
        "'Wine Supply'), 'LATE - 10 Days')"),
    'delivery12': (
        "INSERT INTO deliveries (supply_id, units, expected_delivery_date, actual_delivery_date, "
        "supplier_id, delivery_timing) VALUES ((SELECT supply_id FROM supplies WHERE supply_name = "
        "'Vats'), 10, 20221203, null, (SELECT supplier_id FROM suppliers WHERE supplier_name = "
        "'Wine Supply'), 'LATE')")}

for delivery_number in DELIVERIES:
    deliveryNumbers = DELIVERIES[delivery_number]
    myCursor.execute(deliveryNumbers)

# Insert values into employees table
add_employees = "INSERT INTO employees (first_name, last_name, job_title) VALUES (%s, %s, %s)"
employee_data = [('Stan', 'Bacchus', 'Co-Owner'), ('Scott', 'Jenks', 'Assistant'),
                 ('Davis', 'Bacchus', 'Co-Owner'), ('Rachel', 'Cewe', 'Assistant'),
                 ('Janet', 'Collins', 'Finance Manager'), ('Clint', 'Steadman', 'Assistant'),
                 ('Roz', 'Murphy', 'Marketing Manager'), ('Bob', 'Ulrich', 'Assistant'),
                 ('Maria', 'Costanza', 'Distribution Manager'), ('Liz', 'Fung', 'Assistant'),
                 ('Henry', 'Doyle', 'Production Line Manager'), ('Jan', 'Doe', 'Assistant'),
                 ('John', 'Doe', 'Accountant'), ('Mary', 'Smith', 'Sales Representative'),
                 ('Leslie', 'Goode', 'Warehouse Associate'),
                 ('Mike', 'Days', 'Warehouse Associate'), ('Sue', 'Brave', 'Warehouse Associate'),
                 ('George', 'Wayne', 'Warehouse Assistant Manager'),
                 ('Walker', 'Burns', 'Warehouse Assistant Manager'),
                 ('Milton', 'Shaker', 'Warehouse Associate'), ('Carol', 'Lee', 'Accountant'),
                 ('John', 'Berle', 'Sales Representative'), ('Lee', 'Moe', 'Warehouse Associate'),
                 ('Brian', 'Jacobs', 'Warehouse Associate'), ('Luiz', 'Soares', 'Accountant'),
                 ('Larry', 'Guy', 'Assistant Marketing Manager'),
                 ('Vicki', 'Cherry', 'Warehouse Associate')]

myCursor.executemany(add_employees, employee_data)

# Insert values into time_sheet table
PAYROLL = {'quarter1': (
    "INSERT INTO time_sheet (quarter_id, regular_hours_worked_quarterly,ot_worked_quarterly, employee_id) "
    "VALUES (1, 490, 10, (SELECT employee_id FROM employees WHERE employee_id = 1)), "
    "(1, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 2)), "
    "(1, 490, 10, (SELECT employee_id FROM employees WHERE employee_id = 3)), "
    "(1, 420, 0, (SELECT employee_id FROM employees WHERE employee_id = 4)), "
    "(1, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 5)), "
    "(1, 420, 0, (SELECT employee_id FROM employees WHERE employee_id = 6)), "
    "(1, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 7)), "
    "(1, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 8)), "
    "(1, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 9)), "
    "(1, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 10)), "
    "(1, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 11)), "
    "(1, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 12)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 13)), "
    "(1, 240, 0, (SELECT employee_id FROM employees WHERE employee_id = 14)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 15)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 16)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 17)), "
    "(1, 482, 2, (SELECT employee_id FROM employees WHERE employee_id = 18)), "
    "(1, 482, 2, (SELECT employee_id FROM employees WHERE employee_id = 19)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 20)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 21)), "
    "(1, 240, 0, (SELECT employee_id FROM employees WHERE employee_id = 22)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 23)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 24)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 25)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 26)), "
    "(1, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 27))"),
    'quarter2': (
        "INSERT INTO time_sheet (quarter_id, regular_hours_worked_quarterly,ot_worked_quarterly, "
        "employee_id) "
        "VALUES (2, 460, 0, (SELECT employee_id FROM employees WHERE employee_id = 1)), "
        "(2, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 2)), "
        "(2, 490, 10, (SELECT employee_id FROM employees WHERE employee_id = 3)), "
        "(2, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 4)), "
        "(2, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 5)), "
        "(2, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 6)), "
        "(2, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 7)), "
        "(2, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 8)), "
        "(2, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 9)), "
        "(2, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 10)), "
        "(2, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 11)), "
        "(2, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 12)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 13)), "
        "(2, 240, 0, (SELECT employee_id FROM employees WHERE employee_id = 14)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 15)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 16)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 17)), "
        "(2, 480, 2, (SELECT employee_id FROM employees WHERE employee_id = 18)), "
        "(2, 480, 2, (SELECT employee_id FROM employees WHERE employee_id = 19)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 20)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 21)), "
        "(2, 240, 0, (SELECT employee_id FROM employees WHERE employee_id = 22)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 23)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 24)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 25)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 26)), "
        "(2, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 27))"),
    'quarter3': (
        "INSERT INTO time_sheet (quarter_id, regular_hours_worked_quarterly,ot_worked_quarterly, "
        "employee_id) "
        "VALUES (3, 490, 10, (SELECT employee_id FROM employees WHERE employee_id = 1)), "
        "(3, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 2)), "
        "(3, 490, 10, (SELECT employee_id FROM employees WHERE employee_id = 3)), "
        "(3, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 4)), "
        "(3, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 5)), "
        "(3, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 6)), "
        "(3, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 7)), "
        "(3, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 8)), "
        "(3, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 9)), "
        "(3, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 10)), "
        "(3, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 11)), "
        "(3, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 12)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 13)), "
        "(3, 240, 0, (SELECT employee_id FROM employees WHERE employee_id = 14)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 15)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 16)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 17)), "
        "(3, 482, 2, (SELECT employee_id FROM employees WHERE employee_id = 18)), "
        "(3, 482, 2, (SELECT employee_id FROM employees WHERE employee_id = 19)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 20)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 21)), "
        "(3, 240, 0, (SELECT employee_id FROM employees WHERE employee_id = 22)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 23)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 24)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 25)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 26)), "
        "(3, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 27))"),
    'quarter4': (
        "INSERT INTO time_sheet (quarter_id, regular_hours_worked_quarterly,ot_worked_quarterly, "
        "employee_id) "
        "VALUES (4, 490, 10, (SELECT employee_id FROM employees WHERE employee_id = 1)), "
        "(4, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 2)), "
        "(4, 490, 10, (SELECT employee_id FROM employees WHERE employee_id = 3)), "
        "(4, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 4)), "
        "(4, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 5)), "
        "(4, 400, 0, (SELECT employee_id FROM employees WHERE employee_id = 6)), "
        "(4, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 7)), "
        "(4, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 8)), "
        "(4, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 9)), "
        "(4, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 10)), "
        "(4, 485, 5, (SELECT employee_id FROM employees WHERE employee_id = 11)), "
        "(4, 480, 0, (SELECT employee_id FROM employees WHERE employee_id = 12)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 13)), "
        "(4, 240, 0, (SELECT employee_id FROM employees WHERE employee_id = 14)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 15)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 16)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 17)), "
        "(4, 482, 2, (SELECT employee_id FROM employees WHERE employee_id = 18)), "
        "(4, 482, 2, (SELECT employee_id FROM employees WHERE employee_id = 19)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 20)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 21)), "
        "(4, 240, 0, (SELECT employee_id FROM employees WHERE employee_id = 22)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 23)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 24)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 25)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 26)), "
        "(4, 384, 0, (SELECT employee_id FROM employees WHERE employee_id = 27))")}


for quarterly_payroll in PAYROLL:
    quarterlyPayroll = PAYROLL[quarterly_payroll]
    myCursor.execute(quarterlyPayroll)

mydb.commit()

# Print out values
print("-Displaying Wine Records-")
query1 = "SELECT wine_name, bottle_inventory FROM wine"
myCursor.execute(query1)
wines = myCursor.fetchall()
for wine in wines:
    print("Wine Name: {}\nBottles of Wine: {}\n".format(wine[0], wine[1]))

print("-Displaying Distributor Information-")
query2 = "SELECT distributor_name, city, state FROM distributors"
myCursor.execute(query2)
distributors = myCursor.fetchall()
for distributor in distributors:
    print("Distributor Name: {}\nCity, State: {}, {}\n".format(distributor[0], distributor[1],
                                                               distributor[2]))

print("-Displaying Order Information-")
query3 = "SELECT orders.order_id AS 'Order Number', orders.bottles AS Bottles, " \
         "distributors.distributor_name AS 'Distributor Name', wine.wine_name AS 'Wine Name' " \
         "FROM orders INNER JOIN distributors ON orders.distributor_id = " \
         "distributors.distributor_id INNER JOIN wine ON orders.wine_id = wine.wine_id ORDER BY " \
         "order_id"
myCursor.execute(query3)
orders = myCursor.fetchall()
for order in orders:
    print("Order Number: {}\nAmount of Bottles: {}\nDistributor Name: {}\nWine: {}\n".format(
        order[0], order[1], order[2], order[3]))

print("-Displaying Supply Inventory-")
query4 = "SELECT supply_name, inventory FROM supplies"
myCursor.execute(query4)
supplies = myCursor.fetchall()
for supply in supplies:
    print("Supply: {}\nInventory: {}\n".format(supply[0], supply[1]))

print("-Displaying Supplier Information-")
query5 = "SELECT supplier_name, city, state FROM suppliers"
myCursor.execute(query5)
suppliers = myCursor.fetchall()
for supplier in suppliers:
    print("Supplier Name: {}\nCity, State: {}, {}\n".format(supplier[0], supplier[1], supplier[2]))

print("-Displaying Delivery Information-")
query6 = "SELECT deliveries.delivery_id AS 'Delivery Number', supplies.supply_name AS Supplies, " \
         "deliveries.units AS 'Supply Count', deliveries.expected_delivery_date AS 'Expected " \
         "Delivery Date', deliveries.actual_delivery_date AS 'Actual Delivery Date', " \
         "suppliers.supplier_name FROM deliveries INNER JOIN supplies ON supplies.supply_id = " \
         "deliveries.supply_id INNER JOIN suppliers ON suppliers.supplier_id = " \
         "deliveries.supplier_id ORDER BY delivery_id"
myCursor.execute(query6)
deliveries = myCursor.fetchall()
for delivery in deliveries:
    print("Delivery Number: {}\nSupply: {}\nSupply Count: {}\nExpected Delivery Date: {}\nActual "
          "Delivery Date: {}\nSupplier Name: {}\n".format(delivery[0], delivery[1], delivery[2],
                                                          delivery[3], delivery[4], delivery[5]))

print("-Displaying Employee Information-")
query7 = "SELECT first_name, last_name, job_title FROM employees"
myCursor.execute(query7)
employees = myCursor.fetchall()
for employee in employees:
    print("Employee Name: {} {}\nJob Title: {}\n".format(employee[0], employee[1], employee[2]))

print("-Displaying Quarterly Payroll Information-")
query8 = "SELECT employees.first_name AS 'First Name', employees.last_name AS 'Last Name', " \
         "time_sheet.quarter_id AS 'Quarter', time_sheet.regular_hours_worked_quarterly AS 'Quarterly Hours Worked'," \
         "time_sheet.ot_worked_quarterly AS 'Quarterly Overtime Worked' FROM time_sheet INNER JOIN employees " \
         "ON employees.employee_id = time_sheet.employee_id"
myCursor.execute(query8)
payroll = myCursor.fetchall()
for hours_worked in payroll:
    print("Employee Name: {} {}\nWork Quarter: {}\nHours Worked: {}\nOvertime Hours: {}\n".format
          (hours_worked[0], hours_worked[1], hours_worked[2], hours_worked[3], hours_worked[4]))
