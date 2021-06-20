import os
import hashlib


def get_file_md5(file):
	if not os.path.isfile(file):
		return
	my_hash = hashlib.md5()
	with open(file, 'rb') as f:
		while True:
			b = f.read(4096)
			if not b:
				break
			my_hash.update(b)
	return my_hash.hexdigest()


def compare_file_md5(file, md5):
	res = 0
	cur_md5 = get_file_md5(file)
	if md5 == cur_md5:
		res = 1
	return res
