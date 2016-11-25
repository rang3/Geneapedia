#this is a test for mysqldb library
import MySQLdb

db = MySQLdb.connect('127.0.0.1', 'root', 'cs411fa2016', 'wiki')
cursor = db.cursor()
cursor.execute('SELECT * FROM page')

row = cursor.fetchone()

while row is not None:
    print(row)
    row = cursor.fetchone()
