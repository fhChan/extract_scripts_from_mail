import os,shutil

def copy_sample(name_file,src_folder,des_folder):
	# name_file='C:\\Users\\Administrator\\Desktop\\l.txt'
	# src_folder='E:\\ddei_samples_0907_0922_extracted'
	# des_folder='E:\\0907_js_confusion'
	f=open(name_file,'r')
	t=0
	for line in f.readlines():
		t+=1
		print t
		if line[-1]=='\n':
			name=line[:-1]
		#name+='.js'
		if os.path.exists(os.path.join(src_folder,name)):
			f_path=os.path.join(src_folder,name)
			shutil.copyfile(f_path,os.path.join(des_folder,name))
		else:
			print '[ERROR]  ',name
	f.close()