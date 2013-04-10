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
#cursor = con.cursor()
#cursor.arraysize = 50
#cursor.execute("""
#       select Col1, Col2, Col3
#       from SomeTable
#       where Col4 = :arg_1
#         and Col5 between :arg_2 and :arg_3""",
#       arg_1 = "VALUE",
#       arg_2 = 5,
#       arg_3 = 15)

#for column_1, column_2, column_3 in cursor.fetchall():
#    print "Values from DB:", column_1, column_2, column_3

# print everything 
cursor = con.cursor()
cursor.execute(
    """
    select *
    from Events
    order by e_id desc
    """
    )

for e_id, name, description, date in cursor.fetchall():
    print "Event Name:", name
    print "Date:", date
    print "Event ID:", e_id
    print "Description:", description
    print 

con.commit()
cursor.close()
con.close()



