import MySQLdb


conn = MySQLdb.connect("127.0.0.1", "root", "cs411fa2016", "final")
cursor = conn.cursor()
cursor.execute("SELECT count(*) from Person where name='Bill Gates' or name='Steve Jobs';")
length = cursor.fetchone()[0]
cursor.execute("SELECT name FROM Person WHERE name='Bill Gates' OR name='Steve Jobs';" )

name_list = []
for i in range(length):
	name_list.append(cursor.fetchone()[0])

name_list = ",".join(name_list)

print name_list
