import mysql.connector
from configs.config import db_conn
connection = mysql.connector.connect(
    host=db_conn["host"],
    user=db_conn["user"],
    password=db_conn["password"],
    database="wsaa"
)
cursor = connection.cursor()
sql="delete from student where id = %s"
values = (2,)
cursor.execute(sql, values)
connection.commit()
print("delete done")
cursor.close()
connection.close()