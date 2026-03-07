import mysql.connector
from configs.config import db_conn
class StudentDAO:
    host =""
    user =""
    password =""
    database =""
    connection =""
    cursor =""
    def __init__(self):
        self.host=db_conn["host"]
        self.user=db_conn["user"]
        self.password=db_conn["password"]
        self.password=db_conn["password"]
        self.database="wsaa"
    def getCursor(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def close_all(self):
        self.cursor.close()
        self.connection.close()

    def create(self, values):
        cursor = self.getCursor()
        sql="insert into student (name, age) values (%s,%s)"
        cursor.execute(sql, values)
        self.connection.commit()
        newid = cursor.lastrowid
        self.close_all()
        return newid

    def get_all(self):
        cursor = self.getCursor()
        cursor.execute("select * from student")
        rows = cursor.fetchall()
        self.close_all()
        return rows
    
    def find_by_id(self, id):
        cursor = self.getCursor()
        sql="select * from student where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        result = cursor.fetchone()
        self.close_all()
        return result
    
    def update(self, values):
        cursor = self.getCursor()
        sql="update student set name= %s, age=%s where id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.close_all()

    def delete(self, id):
        cursor = self.getCursor()
        sql="delete from student where id = %s"
        values = (id,)
        cursor.execute(sql, values)
        self.connection.commit()
        self.close_all()

studentDAO = StudentDAO()

if __name__ == "__main__":
    new_id = studentDAO.create(("Mary",21))
    print("getting all")
    print(studentDAO.get_all())
    print (f"getting by last id {new_id}")
    print(studentDAO.find_by_id(new_id))
    print(f"updating id {new_id}")
    studentDAO.update(("Joe",33, new_id))
    print(studentDAO.find_by_id(new_id))
    print(f"deleting id {new_id}")
    studentDAO.delete(new_id)
    print("getting all")
    print(studentDAO.get_all())