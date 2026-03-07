import mysql.connector
from configs.config import db_conn
connection = mysql.connector.connect(
    host=db_conn["host"],
    user=db_conn["user"],
    password=db_conn["password"],
    database="wsaa"
)
mycursor = connection.cursor()
sql="CREATE TABLE student (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)"
mycursor.execute(sql)
mycursor.close()
connection.close()