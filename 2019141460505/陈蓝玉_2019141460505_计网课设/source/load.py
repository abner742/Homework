#	load.py
import os
import frozen_dir

def getIPList():
	ipList = []
	path = os.path.abspath(frozen_dir.app_path()) + '/.iplist'
	try:
		for line in open(path):
			ipList.append(line)
	except:
		return []
	return ipList