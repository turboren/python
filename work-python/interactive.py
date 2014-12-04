# Copyright (C) 2003-2007  Robey Pointer <robeypointer@gmail.com>
#
# This file is part of paramiko.
#
# Paramiko is free software; you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation; either version 2.1 of the License, or (at your option)
# any later version.
#
# Paramiko is distrubuted in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Paramiko; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.
# sudo vim /usr/lib/python2.7/dist-packages/record.py

import socket
import os,sys,datetime,time
import MySQLdb
# windows does not have termios...
try:
	import termios
	import tty
	has_termios = True
except ImportError:
	has_termios = False

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

def interactive_shell(chan,loginuser,username,hostname):
	print """\033[;34m------ Welcome %s Login %s ------\033[0m""" % (loginuser,hostname)
	if has_termios:
		posix_shell(chan,loginuser,username,hostname)
	else:
		windows_shell(chan)


def posix_shell(chan,loginuser,username,hostname):
	import select
	
	oldtty = termios.tcgetattr(sys.stdin)
	try:
		tty.setraw(sys.stdin.fileno())
		tty.setcbreak(sys.stdin.fileno())
		chan.settimeout(0.0)

		record = []
		record_dic = {}

		''' record operation log '''
		day_time = time.strftime('%Y_%m_%d')
		#triaquae_path = os.path.abspath('.')
		triaquae_path = '/usr/local/src/triWeb_frontend'
		#f = open('/tmp/user_ops.log','a')
		while True:
			try:
				remoteip = os.environ['SSH_CLIENT'].split()[0]
			except KeyError:
				remoteip = 'web'
			date_time = time.strftime('%Y_%m_%d %H:%M:%S')
			r, w, e = select.select([chan, sys.stdin], [], [])
			if chan in r:
				try:
					x = chan.recv(1024)
					if len(x) == 0:
						print '\r\n*** EOF\r\n',
						break
					sys.stdout.write(x)
					sys.stdout.flush()
				except socket.timeout:
					pass
				#print x,'-------recv\n'
			if sys.stdin in r:
				x = sys.stdin.read(1)
				if len(x) == 0:
					break
				record.append(x)
				chan.send(x)

			if x == '\r':
				#print record
				cmd = ''.join(record).split('\r')[-2]
				sqlcmd=[]
				sqlcmd.append("insert into login_log (loginuser,remoteip,date_time,hostname,username,cmd)values('%s','%s','%s','%s','%s','%s');" %(loginuser,remoteip,date_time,hostname,username,cmd))
				mydb(sqlcmd)
				#log = "%s\t%s\t%s\t%s\t%s\t*%s\n" % (remoteip,hostname,date_time,loginuser,username,cmd)
				#f.write(log)
				#f.write("%s\n" % str(cmd))
				#f.flush()
		#f.close()

	finally:
		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

	
# thanks to Mike Looijmans for this code
def windows_shell(chan):
	import threading

	sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
		
	def writeall(sock):
		while True:
			data = sock.recv(256)
			if not data:
				sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
				sys.stdout.flush()
				break
			sys.stdout.write(data)
			sys.stdout.flush()
		
	writer = threading.Thread(target=writeall, args=(chan,))
	writer.start()
		
	try:
		while True:
			d = sys.stdin.read(1)
			if not d:
				break
			chan.send(d)
	except EOFError:
		# user hit ^Z or F6
		pass

