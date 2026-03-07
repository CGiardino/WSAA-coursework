import mysql.connector
from configs.config import db_conn
connection = mysql.connector.connect(
    host=db_conn["host"],
    user=db_conn["user"],
    password=db_conn["password"],
    database="wsaa"
)
cursor = connection.cursor()
sql="update student set name= %s, age=%s where id = %s"
values = ("Joe",33, 2)
cursor.execute(sql, values)
connection.commit()
print("update done")