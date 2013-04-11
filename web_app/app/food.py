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


cursor = con.cursor()

#get keywords
cursor.execute(
    """
    select *
    from Events 
    where name like '%Bwog%'
    """
    )

print "GET KEYWORD BWOG IN NAME"

for e_id, name, description, date in cursor.fetchall():
    print "Event Name:", name
    print "Date:", date
    print "Event ID:", e_id
    print "Description:", description
    print 

#get tags
cursor.execute(
    """
    select distinct Events.name, Tags.tag_name
    from Events, Tags, tagged_with
    where Events.e_id = tagged_with.e_id 
        and Tags.tag_name = tagged_with.tag_name
    """
    )

print "GET TAGS"

for name, tag in cursor.fetchall():
    print "Name:", name
    print "Tag:", tag

#get location
cursor.execute(
    """
    select distinct Events.name, Locations.name
    from Events, Locations, located
    where Events.e_id = located.e_id 
        and Locations.l_id = located.l_id
    """
    )

print "GET LOCATION"

for name, location in cursor.fetchall():
    print "Name:", name
    print "Location:", location


#get by date
print "GET DATE 12-MAR-13"

cursor.execute(
    """
    select *
    from Events 
    where dateof = '12-MAR-13'
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



