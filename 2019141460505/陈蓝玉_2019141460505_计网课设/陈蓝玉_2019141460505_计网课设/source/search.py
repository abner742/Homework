#	search.py
#  实现本地共享文件夹中的文件搜索

import os
import frozen_dir

def search(filename):
	#path = os.path.abspath(os.path.dirname(__file__)) + '/share'
	path = os.path.abspath(frozen_dir.app_path()) + '/share'
	#print(path)
	for root, dirs, files in os.walk(path):
		for file in files:
			#print(file)
			if str(file) == filename:
				return os.path.join(root,file)
	#若未找到该文件，则返回None
	return None


