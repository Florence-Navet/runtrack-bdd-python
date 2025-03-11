import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "123456",
    database = "laplateforme",
)

if mydb.is_connected():
    db_info = mydb.get_server_info()
    print(f"connecté à MYSQL, version : {db_info}")

    cursor = mydb.cursor()
    cursor.execute("SELECT DATABASE();")
    db_name = cursor.fetchone()

    cursor.close()
mydb.close()

