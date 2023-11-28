import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'pranav05',
    'database': 'sportal'
}

db_connection = mysql.connector.connect(**db_config)
db_connection.autocommit = True
cursor = db_connection.cursor(dictionary=True, buffered=True)
