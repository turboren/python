#!/usr/bin/python
#ftpclient.py

import socket
import os
import getpass
from time import sleep

HOST='10.152.14.85'
PORT=50007
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
	
while True:
	user = raw_input('user:').strip()
	if user.isalnum():
		while True:
			passwd = getpass.getpass('passwd:').strip()
			s.sendall(user + ' ' + passwd)
			servercmd=s.recv(1024)
			if servercmd == 'login successful':
				print '\033[32m%s\033[m' %servercmd
				break
			else:
				print servercmd

		while True:
			cmd=raw_input('FTP>').strip()
			if cmd == '':
				continue
			if cmd.split()[0] == 'get':
				if cmd == 'get':continue
				for i in cmd.split()[1:]:
					if os.path.exists(i):
						confirm = raw_input("\033[31mPlease confirm whether the cover %s(Y/N):\033[m" %(i)).upper().startswith('Y')
						if not confirm:
							print '%s cancel' %i
							continue
					s.sendall('get ' + i)
					servercmd=s.recv(1024)
					if servercmd == 'inexistence':
						print '%s \t\033[32minexistence\033[m' %i
						continue
					elif servercmd == 'ready_file':
						f = file(i,'wb')
						while True:
							data=s.recv(1024)
							if data == 'get_done':break 
							f.write(data)
						f.close()
						print '%s \t\033[32mfile_done\033[m' %(i)
					elif servercmd == 'ready_dir':
						try:
							os.makedirs(i)
						except:
							pass
						while True:
							serverdir=s.recv(1024)
							if serverdir == 'get_done':break 
							os.system('mkdir -p %s' %serverdir)
							print '%s \t\033[32mdir_done\033[m' %(serverdir)
							while True:
								serverfile=s.recv(1024)
								if serverfile == 'dir_get_done':break 
								f = file('%s/%s' %(serverdir,serverfile),'wb')
								while True:
									data=s.recv(1024)
									if data == 'file_get_done':break 
									f.write(data)
								f.close()
								print '%s/%s \t\033[32mfile_done\033[m' %(serverdir,serverfile)

			elif cmd.split()[0] == 'send':
 			
				if cmd == 'send':continue
				for i in cmd.split()[1:]:
					if not os.path.exists(i):
						print '%s\t\033[31minexistence\033[m' %i
						continue
				
					s.sendall('send ' + i)
					servercmd=s.recv(1024)
					if servercmd == 'existing':
						confirm = raw_input("\033[31mPlease confirm whether the cover %s(Y/N):\033[m" %(i)).upper().startswith('Y')
						if confirm:
							s.sendall('cover')
							servercmd=s.recv(1024)
						else:
							s.sendall('cancel')
							print '%s\tcancel' %i
							continue
					
					if os.path.isfile(i):
						s.sendall('ready_file')
						sleep(0.5)
						f = file(i,'rb')
						s.send(f.read())
						sleep(0.5)
						s.sendall('file_send_done')
						print '%s\t\033[32mfile done\033[m' %(cmd.split()[1])
						f.close()
					elif os.path.isdir(i):
						s.sendall('ready_dir')
						sleep(0.5)
						for dirpath in os.walk(i):
							dir=dirpath[0].replace('%s/' %os.popen('pwd').read().strip(),'',1)
							s.sendall(dir)
							sleep(0.5)
							for filename in dirpath[2]:
								s.sendall(filename)
								sleep(0.5)
								f = file('%s/%s' %(dirpath[0],filename),'rb')
								s.send(f.read())
								f.close()
								sleep(0.5)
								s.sendall('file_send_done')
								msg=s.recv(1024)
								print msg

							else:
								s.sendall('dir_send_done')
								msg=s.recv(1024)
								print msg
						
					else:
						s.sendall('unknown_file')
						print '%s\t\033[31munknown type\033[m' %i
						continue
					sleep(0.5)
					s.sendall('get_done')
				
			elif cmd.split()[0] == 'cdir':
				if cmd == 'cdir':continue
				s.sendall(cmd)
				data=s.recv(1024)
				print data
				continue
			elif cmd == 'ls':
				list=os.popen(cmd).read().strip().split('\n')
				if list:
					dirlist,filelist = '',''
					for i in list:
						if os.path.isdir(i):
							dirlist = dirlist + '\033[32m' + i + '\033[m\t'
						else:
							filelist = filelist + i + '\t'
					results = dirlist + filelist
				else:
					results = '\033[31mnot find\033[m'
				print results
				continue
			elif cmd == 'pwd':
				os.system(cmd)
			elif cmd.split()[0] == 'cd':
				try:
					os.chdir(cmd.split()[1])
				except:
					print '\033[31mcd failure\033[m'
			elif cmd == 'dir':
				s.sendall(cmd)
				data=s.recv(1024)
				print data
				continue
			elif cmd == 'pdir':
				s.sendall(cmd)
				data=s.recv(1024)
				print data
				continue
			elif cmd.split()[0] == 'mdir':
				if cmd == 'mdir':continue
				s.sendall(cmd)
				data=s.recv(1024)
				print data
				continue
			elif cmd.split()[0] == 'help':
				print '''
	get [file] [dir]
	send [file] [dir]

	dir
	mdir
	cdir
	pdir
	
	pwd
	md
	cd
	ls
	
	help
	quit
	'''
				continue
			elif cmd == 'quit':
				break
			else:
				print '\033[31m%s: Command not found,Please see the "help"\033[m' %cmd
	else:
		continue		
	break
s.close()
