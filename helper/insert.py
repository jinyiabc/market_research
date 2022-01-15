from __future__ import print_function
from datetime import date, datetime, timedelta
import mysql.connector
from helper.configSQL import config

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

# emp_no = cursor.lastrowid
tomorrow = datetime.now().date() + timedelta(days=1)
add_sector = ("INSERT INTO 000300_SH "
               "(wind_code, date, i_weight) "
               "VALUES (%s, %s, %s)")
data_sector = ('000001.SZ','2021-12-03', '0.8638')
cursor.execute(add_sector, data_sector)


# Make sure data is committed to the database
cnx.commit()

cursor.close()
cnx.close()