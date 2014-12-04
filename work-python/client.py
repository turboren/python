#!/usr/bin/python
#encoding:utf8
#client.py
import socket
from time import sleep

# 启动socket返回主机状态



HOST='10.152.14.117'
PORT=50007
host_time=30
server_time=120

interval=0
while True:
	sleep(host_time)
	s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect((HOST,PORT))
	s.sendall('alive')
	#interval = interval +30
	#if interval == server_time:
		#发送服务状态
	#	interval=0
	s.close()
	
	print "已发送状态"




