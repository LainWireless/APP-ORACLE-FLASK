import cx_Oracle

connection=cx_Oracle.connect(
	user='c##ivan',
	password='ivan',
	dsn='192.168.122.177:1521/ORCLCDB',
	encoding='UTF-8'
)
print(connection.version)

cursor = connection.cursor()

cursor.execute("select * from pedidos")
res = cursor.fetchall()

for linea in res:
    linea = list(linea)
    print(linea[3])