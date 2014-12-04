#!/usr/bin/python
#encoding:utf8
#listen.py
import SocketServer
import time
import os
import MySQLdb

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

class MyTCP(SocketServer.BaseRequestHandler):
	def handle(self):
		while True:
			cmd=self.request.recv(1024).strip()
			if cmd == 'alive':
				current_time = time.time()
				
				sqlcmd = "update host set lately_time='%s',alive='Y' where ip='%s';" %(current_time,self.client_address[0])
				mydb(sqlcmd)
				atime = time.strftime('%Y-%m-%d %X',time.localtime( time.time() ) )
				print '%s  %s  \033[32m%s\033[m' %(atime,self.client_address[0],cmd)
			break

HOST,PORT = '0.0.0.0',50007
try:
	server = SocketServer.ThreadingTCPServer((HOST,PORT),MyTCP)
	server.serve_forever()
except:
	pass





