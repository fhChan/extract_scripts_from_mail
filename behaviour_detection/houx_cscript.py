# Author: Feihao Chen
# Date: 2016/11/09

import sys,os,shutil
import subprocess

if len(sys.argv)!=2:
	print """
Usage:
    python houx_cscript.py input_dir
    """
else:
	folder_path=sys.argv[1]
	if not os.path.exists(folder_path):
		print 'folder not exists'
		exit(0)	

file=open('list.txt','w')
for root, dirs, files in os.walk(folder_path):
		for name in files:
			try:
				subprocess.check_call('cscript \"'+os.path.join(root,name)+'\"')
				file.write(os.path.join(root,name)+'\n')
			except:
				print 'Unknown Error Exists!\n'
file.close()