#!/usr/bin/python
#manage_ftp.py
import cPickle
import sys
import md5
import os
import getpass

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

while True:
	print '''
	1.add user
	2.del user
	3.change password
	4.query user
	0.exit
	'''
	i = raw_input(':').strip()
	userinfo=filer('user.pkl')
	if i == '':
		continue
	elif i == '1':
		while True:
			user=raw_input('user name:').strip()
			if user.isalnum():
				i = 0
				while i<3:
					passwd=getpass.getpass('passwd:').strip()
					if passwd == '':
						continue
					else:
						passwd1=getpass.getpass('Confirm password:').strip()
						if passwd == passwd1:
							mpasswd = md5.new(passwd).hexdigest()
							userinfo[user] = mpasswd
							os.system('mkdir -p %s' %user)
							print '%s creating successful ' %user
							break
						else:
							print "Passwords don't match "
							i = i + 1
							continue
				else:
					print 'Too many wrong'
					continue
				break
			else:
				print 'user not legal'
				continue
	elif i == '2':
		user=raw_input('user name:').strip()
		if userinfo.has_key(user):
			del userinfo[user]
			print 'Delete users successfully'
		else:
			print 'user not exist'
			continue
	elif i == '3':
		user=raw_input('user name:').strip()
		if userinfo.has_key(user):
			i = 0
			while i<3:
				passwd=getpass.getpass('passwd:').strip()
				if passwd == '':
					continue
				else:
					passwd1=getpass.getpass('Confirm password:').strip()
					if passwd == passwd1:
						mpasswd = md5.new(passwd).hexdigest()
						userinfo[user] = mpasswd
						print '%s password is changed' %user
						break
					else:
						print "Passwords don't match "
						i = i + 1
						continue
			else:
				print 'Too many wrong'
				continue
		else:
			print 'user not exist'
			continue
	elif i == '4':
		print userinfo.keys()
	elif i == '0':
		sys.exit()
	else:
		print 'select error'
		continue
	filew('user.pkl',content=userinfo)