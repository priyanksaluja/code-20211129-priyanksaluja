import sqlite3
from datetime import datetime
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
datafilepath = SCRIPT_DIR + '/app/'

class dbConn():
    '''
    Context manager for database connection
    '''
    def __init__(self, path) -> None:
        self.path = path

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor
    
    def __exit__(self, exc_class, exc, traceback):
        self.conn.commit()
        self.conn.close()


def create_table():
    '''
    Create data tables required for this project
    '''
    try:
        print ("creating new table")
        sql_file_createtable = open(SCRIPT_DIR + "/create_tables.sql")
        sql_file_insertdata = open(SCRIPT_DIR + "/insert_data.sql")
        sql_as_string_createtable = sql_file_createtable.read()
        sql_as_string_insertdata = sql_file_insertdata.read()
        with dbConn(SCRIPT_DIR + '/BMIRefData.db') as con:    
            con.executescript(sql_as_string_createtable)
            con.executescript(sql_as_string_insertdata)
            return True
    except Exception as e:
        print (f"Error while creating tables:{str(e)}")
        return False

#create_table()
