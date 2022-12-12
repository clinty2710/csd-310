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

print("-Displaying Delivery Information-")

query1 = "SELECT deliveries.delivery_id AS 'Delivery Number', suppliers.supplier_name, " \
         "supplies.supply_name AS Supplies, deliveries.units AS 'Supply Count', " \
         "deliveries.expected_delivery_date AS 'Expected Delivery Date', " \
         "deliveries.actual_delivery_date AS 'Actual Delivery Date', " \
         "deliveries.delivery_timing " \
         "FROM deliveries INNER JOIN supplies ON supplies.supply_id = deliveries.supply_id " \
         "INNER JOIN suppliers ON suppliers.supplier_id = deliveries.supplier_id ORDER BY " \
         "supplier_name"
myCursor.execute(query1)
deliveries = myCursor.fetchall()
for delivery in deliveries:
    print("Delivery Number: {}\nSupplier Name: {}\nSupply: {}\nSupply Count: {}\nExpected "
          "Delivery Date: {}\nActual Delivery Date: {}\nDelivery Timing: {}\n".format(
        delivery[0], delivery[1], delivery[2], delivery[3], delivery[4], delivery[5],
        delivery[6]))

print("-Displaying Distribution Information-")
query2 = "SELECT orders.order_id AS 'Order Number', distributors.distributor_name AS 'Distributor " \
         "Name', orders.order_date AS 'Date',wine.wine_name AS 'Distributes', orders.bottles AS " \
         "'Bottles Ordered' FROM orders INNER JOIN distributors ON distributors.distributor_id = " \
         "orders.distributor_id INNER JOIN wine ON wine.wine_id = orders.wine_id ORDER BY " \
         "distributor_name"
myCursor.execute(query2)
distributors = myCursor.fetchall()
for distributor in distributors:
    print("Order Number: {}\nDistributor Name: {}\nOrder Date: {}\nWine Ordered: {}\nBottles "
          "Ordered: {}\n".format (distributor[0], distributor[1], distributor[2], distributor[3],
                                  distributor[4]))

print("-Displaying Wine Bought by Distributors Information-")
query3 = "SELECT wine.wine_name AS 'Wine Name', orders.bottles AS 'Bottles Ordered', " \
         "orders.order_date AS 'Date Bought' FROM orders INNER JOIN wine ON " \
         "wine.wine_id = orders.wine_id ORDER BY wine_name"
myCursor.execute(query3)
wine_bought = myCursor.fetchall()
for wine in wine_bought:
    print("Wine Name: {}\nNumber of Bottles Ordered: {}\nDate Bought: {}\n".format (wine[0],
        wine[1], wine[2]))

print("-Displaying Quarterly Payroll Information-")
query4 = "SELECT employees.first_name AS 'First Name', employees.last_name AS 'Last Name', " \
         "time_sheet.quarter_id AS 'Quarter', time_sheet.regular_hours_worked_quarterly AS 'Quarterly Hours Worked'," \
         "time_sheet.ot_worked_quarterly AS 'Quarterly Overtime Worked' FROM time_sheet INNER JOIN employees " \
         "ON employees.employee_id = time_sheet.employee_id"
myCursor.execute(query4)
payroll = myCursor.fetchall()
for hours_worked in payroll:
    print("Employee Name: {} {}\nWork Quarter: {}\nHours Worked: {}\nOvertime Hours: {}\n".format
          (hours_worked[0], hours_worked[1], hours_worked[2], hours_worked[3], hours_worked[4]))