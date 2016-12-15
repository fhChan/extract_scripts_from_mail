import os, sys, shutil

if len(sys.argv) != 3:
	print """
	Usage:
		python copy_file_from_list.py list_file dest_dir
	"""

list_file = sys.argv[1]
dest_dir = sys.argv[2]

if not os.path.exists(dest_dir):
	os.makedirs(dest_dir)

with open(list_file, 'r') as fh:
	for line in fh.readlines():
		file_path = line.strip()
		if os.path.exists(file_path):
			shutil.copy2(file_path, dest_dir)
		else:
			print "[ERROR] cannot find " + file_path
