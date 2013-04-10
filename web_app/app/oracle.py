import cx_Oracle

# connection string params
user = "dy2212"
pswd = "dophie"
host = "w4111f.cs.columbia.edu"
port = "1521"
sid = "ADB"
dsn = cx_Oracle.makedsn(host, port, sid)

# connect and test
con = cx_Oracle.connect(user, pswd, dsn)
if (con):
	print "Hooray I'm connected"
else:
	print "BOO"

# try some queries
cursor = con.cursor()
cursor.prepare('insert into Users values (:new_user, :new_pass)')

cursor.execute(None, {'new_user':'don44', 'new_pass':'ggggggg'})

if cursor.fetchone():
 	print "already taken"
else:
 	print "okay"

con.commit()
cursor.close()
con.close()
