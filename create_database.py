import mysql.connector as sql
conn = sql.connect(host='localhost', user='root', password='12345678')
if conn.is_connected():
    print("Successfully connected")
c1 = conn.cursor()
database_name = 'ATM_MACHINE'
c1.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
print(f"Database '{database_name}' created successfully")
c1.execute(f"USE {database_name}")

mn = "CREATE TABLE RECORDS(ACCONT_NO INT(3) PRIMARY KEY,Password INT(3),NAME VARCHAR(20),CR_AMT INT DEFAULT(0),WITHDRAWL INT DEFAULT(0),BALANCE INT DEFAULT(0))"
c1.execute(mn)
print("Succesfully created")