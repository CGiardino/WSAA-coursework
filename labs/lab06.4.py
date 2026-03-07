import mysql.connector
from configs.config import db_conn
connection = mysql.connector.connect(
    host=db_conn["host"],
    user=db_conn["user"],
    password=db_conn["password"],
    database="wsaa"
)
cursor = connection.cursor()
sql="select * from student where id = %s"
values = (3,)
cursor.execute(sql, values)
result = cursor.fetchall()
for x in result:
    print(x)
cursor.close()
connection.close()