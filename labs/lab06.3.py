import mysql.connector
from configs.config import db_conn
connection = mysql.connector.connect(
    host=db_conn["host"],
    user=db_conn["user"],
    password=db_conn["password"],
    database="wsaa"
)
cursor = connection.cursor()
sql="insert into student (name, age) values (%s,%s)"
values = ("Mary",21)
cursor.execute(sql, values)
connection.commit()
print("1 record inserted, ID:", cursor.lastrowid)
cursor.close()
connection.close()