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
# cursor.prepare('insert into Users values (:new_user, :new_pass)')

# cursor.execute(None, {'new_user':'don44', 'new_pass':'ggggggg'})
cursor.execute(
	"""
	select pl.p_id, pl.l_id, l.name from 
	Preferences p, Locations l, preferredLocations pl, Users u, hasPreferences hp
	where pl.p_id = p.p_id and pl.l_id = l.l_id and p.p_id = hp.p_id and hp.username = 'don8yu'
	""")

print cursor.fetchall()
# if cursor.fetchone():
#  	print "already taken"
# else:
#  	print "okay"

con.commit()
cursor.close()
con.close()
