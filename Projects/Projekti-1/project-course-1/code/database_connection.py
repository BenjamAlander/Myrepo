import pymysql

def create_conn():
    connection_settings = {
        'host': 'iiwari-mariadb-server',
        'user': 'root',
        'password': 'd41k4Duu',
        'db': 'iiwari_org',
        'charset': 'utf8mb4',
        'cursorclass': pymysql.cursors.DictCursor,
        'port': 3306
    }
    return pymysql.connect(**connection_settings)
