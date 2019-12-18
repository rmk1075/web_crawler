import pymysql

conn = pymysql.connect(host='localhost', user='root', password='jjmin100705!', db='mydb', charset='utf8')

curs = conn.cursor()

sql = 'select * from students'
curs.execute(sql)

rows = curs.fetchall()
print(rows)

conn.close()
