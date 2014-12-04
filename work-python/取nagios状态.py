import os

def dat():
	data = os.popen(''' grep -E 'servicestatus|host_name=|service_description=|current_state=|[^_]plugin_output=' /usr/local/nagios/var/status.dat |awk -v RS='servicestatus {' 'NR!=1{print $0}' |awk -F '=' '$0!=""{print $2}' |awk '{if (NR%4==0){print $0} else {printf"%s ",$0"=="}}' ''').read().strip()
	
	return data

def all():
	statustmp = dat().split('\n')
	dic = {}
	for line in statustmp:
		if line == "":
			continue
		i=line.split('== ')
		if i[0] in dic.keys():
			key = dic[i[0]]
		else:
			key = []
		key.append([i[1],i[2],i[3]])
		dic[i[0]]=key
	return dic

def ipservice(ip):
	
	print all()[ip]

def dangerous():
	statustmp = dat().split('\n')
	dic = {}

	for line in statustmp:
		if line == "":
			continue

		i=line.split('== ')
		
		if i[2] != "0":
			if i[0] in dic.keys():
				key = dic[i[0]]
			else:
				key = []
			key.append([i[1],i[2],i[3]])
			dic[i[0]]=key
	print dic

if __name__ == '__main__':
	ipservice('10.10.10.12')
	#dangerous()
	#all()