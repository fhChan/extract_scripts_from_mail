import os,shutil

def copy_sample(name_list,src_folder,des_folder):
	f=open(name_list,'r')
	t=0
	for line in f.readlines():
		t+=1
		print t
		if line[-1]=='\n':
			name=line[:-1]
		if os.path.exists(os.path.join(src_folder,name)):
			f_path=os.path.join(src_folder,name)
			shutil.copyfile(f_path,os.path.join(des_folder,name))
		else:
			print '[ERROR]  ',name
	f.close()

def main():
  	if len(sys.argv)!=4:
    	print """
Usage:
  python copy_sample.py sha1s.txt src_folder des_folder
    """
    	exit(0)
    if not os.path.exists(sys.argv[1]):
      	print "name_list don't exists"
      	exit(0)
    if not os.path.exists(sys.argv[2]):
      	print "src_folder don't exists"
      	exit(0)
    if not os.path.exists(sys.argv[3]):
      	print "des_folder don't exists"
      	exit(0)    
    copy_sample(sys.argv[1],sys.argv[2],sys.argv[3])

if __name__ == '__main__':
    main()