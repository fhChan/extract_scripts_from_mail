 # Author: Feihao Chen
 # Date: 2016/10/31

import sys,os,shutil
import subprocess
import extract_from_mail
from unzip_classify import unzip
import oletools

def classify(input_folder):
	for root, dirs, files in os.walk(input_folder):
		for name in files:
			filename = os.path.join(root,name)
			por = os.path.splitext(filename)
			if por[1].lower()=='.js':
				shutil.copy2(filename, sys.argv[2]+'\\js')
			elif por[1]=='.wsf':
				shutil.copy2(filename, sys.argv[2]+'\\wsf')
			elif '.doc' in por[1]:
				shutil.copy2(filename, sys.argv[2]+'\\office')
			elif '.xls' in por[1]:
				shutil.copy2(filename, sys.argv[2]+'\\office')
			elif por[1]=='.jse':
				if not os.path.exists(sys.argv[2]+'\\jse'):
					os.makedirs(sys.argv[2]+'\\jse')
				shutil.copy2(filename, sys.argv[2]+'\\jse')
			elif por[1]!='.zip':
				if not os.path.exists(sys.argv[2]+'\\others'):
					os.makedirs(sys.argv[2]+'\\others')
				shutil.copy2(filename, sys.argv[2]+'\\others')

def extract_macros(input_folder):
	for root, dirs, files in os.walk(input_folder):
		for name in files:
			filename=os.path.join(root,name)
			por = os.path.splitext(filename)
			log_name=por[0]+'.log'
			with open(log_name, 'w') as fout:
				try:
					subprocess.check_call('python oletools\olevba.py \"'+filename+'\"', stdout=fout)
				except e:
					print e
			os.system('python extract_vbs_from_log.py \"'+log_name+'\"')




def print_usage():
    print """
Usage:
    python autorun.py input_dir output_dir
    """

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        exit(-1)

    # extract from mail
    if not os.path.exists(sys.argv[2]+'\\logs'):
        os.makedirs(sys.argv[2]+'\\logs')
    ext_log=sys.argv[2]+'\\logs'+'\\ext.log'
    with open(ext_log, 'w') as fout:
        if sys.argv[1].endswith('.eml'):
            subprocess.check_call('python extract_from_mail.py --file \"'+sys.argv[1]+'\" \"'+sys.argv[2]+'\\extracted\"', stdout=fout)
        else:
            subprocess.check_call('python extract_from_mail.py --dir \"'+sys.argv[1]+'\" \"'+sys.argv[2]+'\\extracted\"', stdout=fout)

    # unzip files
    if not os.path.exists(sys.argv[2]+'\\unzipped'):
        os.makedirs(sys.argv[2]+'\\unzipped')
    unzip(sys.argv[2]+'\\extracted',sys.argv[2]+'\\unzipped')

    # classify
    if not os.path.exists(sys.argv[2]+'\\js'):
        os.makedirs(sys.argv[2]+'\\js')
    if not os.path.exists(sys.argv[2]+'\\wsf'):
        os.makedirs(sys.argv[2]+'\\wsf')
    if not os.path.exists(sys.argv[2]+'\\office'):
        os.makedirs(sys.argv[2]+'\\office')
    classify(sys.argv[2]+'\\extracted\\office')
    classify(sys.argv[2]+'\\extracted')
    classify(sys.argv[2]+'\\unzipped\\office')
    classify(sys.argv[2]+'\\unzipped')

    # extract macros
    extract_macros(sys.argv[2]+'\\office')
    if not os.path.exists(sys.argv[2]+'\\logs\\macros'):
        os.makedirs(sys.argv[2]+'\\logs\\macros')
	for root, dirs, files in os.walk(sys.argv[2]+'\\office'):
		for name in files:
			filename=os.path.join(root,name)
			por = os.path.splitext(filename)
			log_name=por[0]+'.log'
			if por[1]=='.log':
				shutil.move(log_name,sys.argv[2]+'\\logs\\macros')

	# analyse js and wsf files
	print "\nNow Processing JS Files :"
	with open(sys.argv[2]+'\\logs\\js-log.log', 'w') as fout:
		subprocess.check_call('salineup_for_script_malware\SALineup.exe --productname=sc --script-malware=true \"'+\
			sys.argv[2]+'\\js'+'\"', stdout=fout)
	print "\nNow Processing WSF Files :"
	with open(sys.argv[2]+'\\logs\\wsf-log.log', 'w') as fout:
		subprocess.check_call('salineup_for_script_malware\SALineup.exe --productname=sc --script-malware=true \"'+\
			sys.argv[2]+'\\wsf'+'\"', stdout=fout)