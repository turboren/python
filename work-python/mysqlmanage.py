#!/usr/bin/python
# -*- coding:utf-8 -*-
#mysqlmanage.py

import MySQLdb
import sys
import md5
import getpass

def mydb(dbcmdlist):
	try:
		conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='fortress',port=3306)
		cur=conn.cursor()
		result=[]
		for dbcmd in dbcmdlist:
			cur.execute(dbcmd)
			sqlresult = cur.fetchall()
			result.append(sqlresult)
		conn.commit()
		cur.close()
		conn.close()
		return result
	except MySQLdb.Error,e:
		print 'mysql error msg: ',e

while True:
	print '''
	1.创建用户
	2.删除用户
	3.添加主机
	4.添加用户权限主机
	5.查看用户权限主机
	6.查看用户日志
	7.查看所有日志
	8.初始化表
	0.退出
	'''
	i = raw_input('select:')
	sqlcmd = []
	if i == '':
		continue
	elif i == '1':
		
		while True:
			adduser = raw_input('adduser:').strip()
			if adduser.isalnum():break
		while True:
			pwd = getpass.getpass('passwd:').strip()
			if pwd != '':break
		md5pwd=md5.new(pwd).hexdigest()
		sqlcmd.append("insert into user (userName,password)values('%s','%s');" %(adduser,md5pwd))
		mydb(sqlcmd)

	elif i == '2':
		while True:
			deluser = raw_input('deluser:').strip()
			if deluser.isalnum():break
		sqlcmd.append("DELETE FROM  user WHERE userName = '%s';" %(deluser))
		mydb(sqlcmd)

	elif i == '3':
		while True:
			hostIp = raw_input('hostIp:').strip()
			if hostIp != '':break
		while True:
			host_port = int(raw_input("host_port:").strip())
			if host_port < 65500:break
		while True:
			host_user = raw_input('host_user:').strip()
			if host_user.isalnum():break
		while True:
			host_pw = raw_input('host_pw:').strip()
			if host_pw != '':break
		sqlcmd.append("insert into host (hostIp,host_port,host_user,host_pw)values('%s','%s','%s','%s');" %(hostIp,host_port,host_user,host_pw))
		mydb(sqlcmd)
	elif i == '4':
		
		while True:
			sqlcmd=[]
			while True:
				user = raw_input('user:').strip()
				if user.isalnum():break
			sqlcmd.append("select * from user where userName = '%s';" %(user))
			result = mydb(sqlcmd)
			if len(result[0]) >= 1:break

		while True:
			sqlcmd=[]
			while True:
				hostIP = raw_input('hostIP:').strip()
				if hostIP != '':break
			sqlcmd.append("select * from host where hostIp = '%s';" %(hostIP))
			result = mydb(sqlcmd)
			if len(result[0]) >= 1:break
		sqlcmd=[]
		sqlcmd.append("insert into user_host (user_id,host_id)values('%s','%s');" %(user,hostIP))
		mydb(sqlcmd)
		
	elif i == '5':
		while True:
			sqlcmd=[]
			while True:
				user = raw_input('user:').strip()
				if user.isalnum():break
			sqlcmd.append("select * from user where userName = '%s';" %(user))
			result = mydb(sqlcmd)
			if len(result[0]) >= 1:break
		sqlcmd=[]
		sqlcmd.append("select host_id from user_host where user_id = '%s';" %(user))
		result = mydb(sqlcmd)
		for i in result[0]:
			print i[0]
			
	elif i == '6':
		while True:
			sqlcmd=[]
			while True:
				user = raw_input('user:').strip()
				if user.isalnum():break
			sqlcmd.append("select * from user where userName = '%s';" %(user))
			result = mydb(sqlcmd)
			if len(result[0]) >= 1:break
		sqlcmd=[]
		sqlcmd.append("select * from login_log where loginuser = '%s';" %(user))
		result = mydb(sqlcmd)
		print result
		for i in result[0]:
			print i
	elif i == '7':
		sqlcmd=[]
		sqlcmd.append("select * from login_log;")
		result = mydb(sqlcmd)
		print result
		for i in result[0]:
			print i
		
	elif i == '8':

		try:
			conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',port=3306)
			cur=conn.cursor()
			cur.execute('create database if not exists fortress;')
			conn.select_db('fortress')
			cur.execute('drop table if exists user;')
			cur.execute('drop table if exists host;')
			cur.execute('drop table if exists user_host;')
			cur.execute('drop table if exists login_log;')
			
			cur.execute('CREATE TABLE user ( id BIGINT(20) NOT NULL AUTO_INCREMENT, userName VARCHAR(50) DEFAULT NULL, password VARCHAR(50) DEFAULT NULL, PRIMARY KEY (id) );')
			cur.execute('CREATE TABLE host ( id BIGINT(20) NOT NULL AUTO_INCREMENT, hostIp VARCHAR(50) DEFAULT NULL, host_port VARCHAR(50) DEFAULT NULL, host_user VARCHAR(50) DEFAULT NULL, host_pw VARCHAR(50) DEFAULT NULL, PRIMARY KEY (id) );')
			cur.execute('CREATE TABLE user_host ( id BIGINT(20) NOT NULL AUTO_INCREMENT, user_id VARCHAR(50) NOT NULL , host_id VARCHAR(50) NOT NULL , PRIMARY KEY (id) );')
			cur.execute('CREATE TABLE login_log ( id BIGINT(20) NOT NULL AUTO_INCREMENT, loginuser VARCHAR(50) DEFAULT NULL , remoteip VARCHAR(50) DEFAULT NULL , date_time VARCHAR(50) DEFAULT NULL  , hostname VARCHAR(50) DEFAULT NULL ,username VARCHAR(50) DEFAULT NULL , cmd VARCHAR(256) DEFAULT NULL , PRIMARY KEY (id) ) ;')
			
			conn.commit()
			cur.close()
			conn.close()
		except MySQLdb.Error,e:
			print "mysql error %d:%s" %(e.args[0],e.args[1])
	
	elif i == '0':
		sys.exit()
	else:
		print 'reselect'
		continue
