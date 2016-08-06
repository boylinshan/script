import sys
import re
from os.path import expanduser
import os

DEFAULT_PATH = expanduser('~') + '/.ssh/config'
pattren = re.compile('^Host\s\w+$')

def get_host_info(config_file):
	host_list = []
	for line in config_file:
		data = line.strip().split(' ')

		if not data[0]:
			continue

		if data[0] == 'Host':
			host_list.append({data[0]:data[1]})
		else:
			host_list[-1][data[0]] = data[1]

	return host_list

def connect(host):
	command = 'ssh %s' % host['Host']
	os.system(command)

if __name__ == '__main__':
	with open(DEFAULT_PATH, 'r') as config_file:
		host_list = get_host_info(config_file)

	for num in range(len(host_list)):
		host = host_list[num]
		print '%s.%s(%s:%s)' % (num+1, host.get('Host','None'), host.get('HostName','None'), host.get('Port', '22'))

	num = input(':')
	
	if num < 1 or num > len(host_list):
		exit(0)

	connect(host_list[num-1])

