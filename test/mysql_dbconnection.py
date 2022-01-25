from importlib import resources

from _mysql_connector import MySQLInterfaceError
from helper.mysql_dbconnection import mysql_dbconnection
from sqlalchemy  import create_engine
import config
# from helper import config
with resources.path('helper', 'mysql.cfg') as p:
    resource_path = str(p)
cfg = config.Config(resource_path)

# def mysql_dbconnection(database=None):
#     '''
#     database_url = mysql+mysqlconnector://<user>:<password>@<host>[:<port>]/<dbname>
#     '''
#     if database is None:
#         database_url = 'mysql+mysqlconnector://{}:{}@{}?charset=utf8mb4'.format(cfg['user'], cfg['password'],
#                                                                             cfg['host'])
#     else:
#         database_url = 'mysql+mysqlconnector://{}:{}@{}/{}?charset=utf8mb4'.format(cfg['user'], cfg['password'], cfg['host'], database)
#
#     sqlEngine = create_engine(database_url, pool_recycle=3600)
#
#     if cfg['password'] == "xxxxxxx":
#         print(f"Please modify mysql.cfg file under {resource_path} to connect mysql properly.")
#         exit()
#
#     return sqlEngine.connect()

if __name__ == '__main__':
    import pandas as pd
    test = 'READ'  # Set to 'WRITE' to test.
    if test == 'WRITE':
        userVitals = {"UserId": ["xxxxx", "yyyyy", "zzzzz", "aaaaa", "bbbbb", "ccccc", "ddddd"],

                      "UserFavourite": ["Greek Salad", "Philly Cheese Steak", "Turkey Burger", "Crispy Orange Chicken",
                                        "Atlantic Salmon", "Pot roast", "Banana split"],

                      "MonthlyOrderFrequency": [5, 1, 2, 2, 7, 6, 1],

                      "HighestOrderAmount": [30, 20, 16, 23, 20, 26, 9],

                      "LastOrderAmount": [21, 20, 4, 11, 7, 7, 7],

                      "LastOrderRating": [3, 3, 3, 2, 3, 2, 4],

                      "AverageOrderRating": [3, 4, 2, 1, 3, 4, 3],

                      "OrderMode": ["Web", "App", "App", "App", "Web", "Web", "App"],

                      "InMedicalCare": ["No", "No", "No", "No", "Yes", "No", "No"]};

        tableName = "UserVitals"

        dataFrame = pd.DataFrame(data=userVitals)

        dbConnection = mysql_dbconnection(database='test1')

        try:

            frame = dataFrame.to_sql(tableName, dbConnection, if_exists='fail');

        except ValueError as vx:

            print(vx)

        except Exception as ex:

            print(ex)

        else:

            print("Table %s created successfully." % tableName);

        finally:

            dbConnection.close()
        pass

    if test == 'READ':

        dbConnection = mysql_dbconnection('test1')

        frame = pd.read_sql("select * from uservitals", dbConnection);

        pd.set_option('display.expand_frame_repr', False)

        print(frame)

        dbConnection.close()