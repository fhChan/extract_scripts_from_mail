import os,sys
# write files' name under the floder into file
# python dir.py floder_path  file_path
floder_path=sys.argv[1]
file_path=sys.argv[2]
f=open(file_path,'w')
files=[]
for filename in os.listdir(floder_path):
	files.append(filename+'\n')
f.writelines(files)
f.close()
