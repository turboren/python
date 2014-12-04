#!/usr/bin/python
#ftpserver.py

import SocketServer
import os
import cPickle
import md5
from time import sleep

def filer(file1):
	try:
		f = file(file1,'rb')
		return cPickle.load(f)
	except IOError:
		return {}
	except EOFError:
		return {}
	f.close()

def filew(file1,content):
	f = file(file1,'wb')
	cPickle.dump(content,f)
	f.close()

class MyTCP(SocketServer.BaseRequestHandler):
	def handle(self):
		i = 0
		while i<3:
			user=self.request.recv(1024).strip()
			userinfo=filer('user.pkl')
			if userinfo.has_key(user.split()[0]):
				if md5.new(user.split()[1]).hexdigest() == userinfo[user.split()[0]]:
					results='login successful'
					self.request.sendall(results)
					login='successful'
					break
				else:
					i = i + 1
					results='Error:password not correct'
					self.request.sendall(results)
					continue
			else:
				i = i + 1
				results='Error:password not correct'
				self.request.sendall(results)
				continue
			break
		else:
			results = 'Error:Wrong password too many times'
			self.request.sendall(results)
			login='failure'
		home_path = os.popen('pwd').read().strip() + '/' + user.split()[0]
		current_path = '/'
		print home_path
		while True:
			if login == 'failure':
				break
			print 'home_path:%s=current_path:%s' %(home_path,current_path)
			cmd=self.request.recv(1024).strip()
			print cmd
			if cmd == 'quit':
				break
			elif cmd == 'dir':
				list=os.listdir('%s%s' %(home_path,current_path))
				if list:
					dirlist,filelist = '',''
					for i in list:
						if os.path.isdir('%s%s%s' %(home_path,current_path,i)):
							dirlist = dirlist + '\033[32m' + i + '\033[m\t'
						else:
							filelist = filelist + i + '\t'
					results = dirlist + filelist
				else:
					results = '\033[31mnot find\033[m'
				self.request.sendall(results)
			elif cmd == 'pdir':
				self.request.sendall(current_path)
			elif cmd.split()[0] == 'mdir':
				if cmd.split()[1].isalnum():
					tmppath='%s%s%s' %(home_path,current_path,cmd.split()[1])
					os.makedirs(tmppath)
					self.request.sendall('\033[32mcreating successful\033[m')
				else:
					self.request.sendall('\033[31mcreate failure\033[m')
			elif cmd.split()[0] == 'cdir':
				if cmd.split()[1] == '/':
					tmppath='%s%s' %(home_path,cmd.split()[1])
					if os.path.isdir(tmppath):
						current_path = cmd.split()[1]
						self.request.sendall(current_path)
					else:
						self.request.sendall('\033[31mnot_directory\033[m')
				elif cmd.split()[1].startswith('/'):
					tmppath='%s%s' %(home_path,cmd.split()[1])
					if os.path.isdir(tmppath):
						current_path = cmd.split()[1] + '/'
						self.request.sendall(current_path)
					else:
						self.request.sendall('\033[31mnot_directory\033[m')
				else:
					tmppath='%s%s%s' %(home_path,current_path,cmd.split()[1])
					if os.path.isdir(tmppath):
						current_path = current_path + cmd.split()[1] + '/'
						self.request.sendall(current_path)
					else:
						self.request.sendall('\033[31mnot_directory\033[m')
			elif cmd.split()[0] == 'get':
				if os.path.isfile('%s%s%s' %(home_path,current_path,cmd.split()[1])):
					f = file('%s%s%s' %(home_path,current_path,cmd.split()[1]),'rb')
					self.request.sendall('ready_file')
					sleep(0.5)
					self.request.send(f.read())
					f.close()
					sleep(0.5)
				elif os.path.isdir('%s%s%s' %(home_path,current_path,cmd.split()[1])):
					self.request.sendall('ready_dir')
					sleep(0.5)
					for dirpath in os.walk('%s%s%s' %(home_path,current_path,cmd.split()[1])):
						dir=dirpath[0].replace('%s%s' %(home_path,current_path),'',1)
						self.request.sendall(dir)
						sleep(0.5)
						for filename in dirpath[2]:
							self.request.sendall(filename)
							sleep(0.5)
							f = file('%s/%s' %(dirpath[0],filename),'rb')
							self.request.send(f.read())
							f.close()
							sleep(0.5)
							self.request.sendall('file_get_done')
							sleep(0.5)
						else:
							self.request.sendall('dir_get_done')
						sleep(0.5)
				else:
					self.request.sendall('get_failure')
					continue
				self.request.sendall('get_done')
		
			elif cmd.split()[0] == 'send':
				if os.path.exists('%s%s%s' %(home_path,current_path,cmd.split()[1])):
					self.request.sendall('existing')
					action=self.request.recv(1024)
					if action == 'cancel':
						continue
				self.request.sendall('ready')
				msg=self.request.recv(1024)
				if msg == 'ready_file':
					f = file('%s%s%s' %(home_path,current_path,cmd.split()[1]),'wb')
					while True:
						data=self.request.recv(1024)
						if data == 'file_send_done':break
						f.write(data)
					f.close()

				elif msg == 'ready_dir':
					os.system('mkdir -p %s%s%s' %(home_path,current_path,cmd.split()[1]))
					while True:
						dir=self.request.recv(1024)
						if dir == 'get_done':break
						os.system('mkdir -p %s%s%s' %(home_path,current_path,dir))
						while True:
							filename=self.request.recv(1024)
							if filename == 'dir_send_done':break
							f = file('%s%s%s/%s' %(home_path,current_path,dir,filename),'wb')
							while True:
								data=self.request.recv(1024)
								if data == 'file_send_done':break 
								f.write(data)
							f.close()
							self.request.sendall('%s/%s\t\033[32mfile_done\033[m' %(dir,filename))
						self.request.sendall('%s\t\033[32mdir_done\033[m' %(dir))
				elif msg == 'unknown_file':
					continue
				
			else:
				results = cmd.split()[0] + ': Command not found'
				self.request.sendall(results)

if __name__ == '__main__':
	HOST,PORT = '10.152.14.85',50007
	server = SocketServer.ThreadingTCPServer((HOST,PORT),MyTCP)
	server.serve_forever()