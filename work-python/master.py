#!/usr/bin/python
#encoding:utf8
#master.py
import time
import MySQLdb
import os


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

#报警
def alarm(atime,ip):

	sqlcmd = "update host set monitor_state='F' where ip='%s';" %(ip)
	mydb(sqlcmd)
	msg="%s  %s  Host Downtime" %(atime,ip)
	os.system('echo %s |mail -s host_alarm quanzhou722@163.com' %msg)
	
	print '%s  %s  主机宕机' %(atime,ip)

#加载用户
os.system("python addhost.py")

#更新所有start_time时间
current_time = time.time()
sqlcmd = "update host set start_time='%s';" %(current_time)
mydb(sqlcmd)

#后台运行脚本启动监听
os.system("python listen.py &")

#通知被监控主机
sqlcmd = "select ip,monitor_state from host;"
sqlresult = mydb(sqlcmd)
iplist = []
for i in sqlresult:
	iplist.append(i[0])
	if i[1] == 'Y':
		#监控
		pass

#检测主机超时

while True:
	sqlcmd = "select ip,lately_time,monitor_state from host where monitor_state='Y' or monitor_state='F';"
	sqlresult = mydb(sqlcmd)
	for i in sqlresult:
		atime = time.strftime('%Y-%m-%d %X',time.localtime( time.time() ) )
		current_time = time.time()
		interval = int(current_time - float(i[1]))
		print interval
		if interval > 30:
			#超时
			b=os.system('ping -c 3 %s >>/dev/null' %(i[0]))
			if b == 0:
				#更新时间
				sqlcmd = "update host set lately_time='%s',alive='Y' where ip='%s';" %(current_time,i[0])
				mydb(sqlcmd)
				print '%s  %s  \033[33m主机存活，但未启动客户端\033[m' %(atime,i[0])
			else:
				sqlcmd = "update host set lately_time='%s',alive='N' where ip='%s';" %(current_time,i[0])
				mydb(sqlcmd)
				print '%s  %s  \033[31m主机不可达\033[m' %(atime,i[0])
				#报警
				if i[2] == 'Y':
					alarm(atime,i[0])
		time.sleep(15)




