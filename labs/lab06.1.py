import mysql.connector
from configs.config import db_conn
connection = mysql.connector.connect(
    host=db_conn["host"],
    user=db_conn["user"],
    password=db_conn["password"]
)
mycursor = connection.cursor()
mycursor.execute("CREATE database wsaa")
mycursor.close()
connection.close()