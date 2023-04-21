import pymysql
import mysql.connector as database

class databaseConnector(object):
    def __init__(self, db_name, db_host, db_username, db_passwd):
        self.db_name = db_name
        self.db_host = db_host
        self.db_username = db_username
        self.db_passwd = db_passwd
        
    def connectDB(db_name, db_host, db_username, db_passwd):
        conn=pymysql.connect(host=db_host,
        port=int(3306),
        user="root",
        passwd=db_passwd,
        db=db_name)
        return conn
            
        
    
       
    
            
