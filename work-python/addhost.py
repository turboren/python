#!/usr/bin/python
#addhost.py
#encoding:utf8
import MySQLdb
import time

def mydb(dbcmd):
	try:
		conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='monitor',port=3306)
		cur=conn.cursor()
		cur.execute(dbcmd)
		sqlresult = cur.fetchall()
		conn.commit()
		cur.close()
		conn.close()
		return sqlresult
	except MySQLdb.Error,e:
		print 'mysql error msg: ',e

#create database if not exists monitor;
#sqlcmd = "CREATE TABLE host ( id BIGINT(20) NOT NULL AUTO_INCREMENT, ip VARCHAR(50) DEFAULT NULL, hostname VARCHAR(50) DEFAULT NULL, monitor_state VARCHAR(1) DEFAULT NULL, start_time VARCHAR(50) DEFAULT NULL, lately_time VARCHAR(50) DEFAULT NULL,alive VARCHAR(1) DEFAULT NULL,PRIMARY KEY (id) );"
#mydb(sqlcmd)

f=file('host.list')
c = f.readlines()
f.close()

iplist = []
for ipinfo in c:
	ip=ipinfo.split()[0]
	iplist.append(ip)
	hostname=ipinfo.split()[1]
	monitor_state=ipinfo.split()[2]
	current_time = time.time()
	start_time=current_time
	lately_time=current_time
	alive='U'

	sqlcmd = "select ip from host;"
	sqlresult = mydb(sqlcmd)
	sqllist = []
	for i in sqlresult:
		sqllist.append(i[0])

	if ip in sqllist:
		sqlcmd = "update host set monitor_state='%s',hostname='%s' where ip='%s';" %(monitor_state,hostname,ip)
		
		mydb(sqlcmd)
	else:
		sqlcmd = "insert into host (ip,hostname,monitor_state,start_time,lately_time,alive)values('%s','%s','%s','%s','%s','%s');" %(ip,hostname,monitor_state,start_time,lately_time,alive)
		mydb(sqlcmd)
		
for i in sqllist:
	if i not in iplist:
		sqlcmd = "DELETE FROM  host WHERE ip = '%s';" %(i)
		mydb(sqlcmd)

sqlcmd = "select * from host;"
print mydb(sqlcmd)
