 # Author: Feihao Chen
 # Date: 2016/10/31

import sys,os,shutil
import re
import subprocess
import extract_from_mail
from unzip_classify import unzip
from oletools.olevba import VBA_Parser

def eml_process(input_dir,output_dir):
    if not os.path.exists(os.path.join(output_dir,'logs')):
        os.makedirs(os.path.join(output_dir,'logs'))
    ext_log = os.path.join(output_dir,'logs','ext.log')
    mail_extractor = extract_from_mail.MailExtactor()
    mail_extractor.set_dest_dir(os.path.join(output_dir,'extracted'))
    with open(ext_log, 'w') as sys.stdout:
        if input_dir.endswith('.eml'):
            mail_extractor.process_single_mail(input_dir)
        else:
            mail_extractor.process_multiple_mail(input_dir)

def classify(input_folder, output_dir):
    for root, dirs, files in os.walk(input_folder):
        for name in files:
            filename = os.path.join(root,name)
            por = os.path.splitext(filename)
            ext = por[1]
            if ext.lower()=='.js':
                shutil.copy2(filename, os.path.join(output_dir,'js'))
            elif ext=='.wsf':
                shutil.copy2(filename, os.path.join(output_dir,'wsf'))
            elif '.doc' in ext:
                shutil.copy2(filename, os.path.join(output_dir,'office'))
            elif '.xls' in ext:
                shutil.copy2(filename, os.path.join(output_dir,'office'))
            elif ext=='.jse':
                if not os.path.exists(os.path.join(output_dir,'jse')):
                    os.makedirs(os.path.join(output_dir,'jse'))
                shutil.copy2(filename, os.path.join(output_dir,'jse'))
            elif ext=='.vbs':
                if not os.path.exists(os.path.join(output_dir,'vbs')):
                    os.makedirs(os.path.join(output_dir,'vbs'))
                shutil.copy2(filename, os.path.join(output_dir,'vbs'))
            elif ext!='.zip':
                if not os.path.exists(os.path.join(output_dir,'others')):
                    os.makedirs(os.path.join(output_dir,'others'))
                shutil.copy2(filename, os.path.join(output_dir,'others'))

def extract_macros(input_folder): # ./office
    for root, dirs, files in os.walk(input_folder):
        for name in files:
            filename = os.path.join(root,name)
            try:
                vbaparser = VBA_Parser(filename)
                if vbaparser.detect_vba_macros():
                    portion = os.path.splitext(filename)
                    new_dir = portion[0]
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                    for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
                        with open(os.path.join(new_dir,vba_filename),'w') as vba:
                            vba.write(re.sub('attribute.*\n','',vba_code))
            except Exception as e:
                print filename
                print e

def get_parent_path(path, grade):
    if grade > 0 and path.count('\\') >= grade:
        l = path.split('\\')
        return '\\'.join(l[:0-grade])
    else:
        return path

def print_usage():
    print """
Usage:
    python autorun.py input_dir output_dir
    """

def main():
    __console__= sys.stdout
    if len(sys.argv) != 3:
        print_usage()
        exit(-1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # extract from mail
    eml_process(input_dir,output_dir)

    # unzip files
    extracted_folder = os.path.join(output_dir,'extracted')
    sys.stdout = open(os.path.join(output_dir,'logs','unzip.log'), 'w')
    unzipped_folder = os.path.join(output_dir,'unzipped')
    if not os.path.exists(unzipped_folder):
        os.makedirs(unzipped_folder)
    unzip(extracted_folder,unzipped_folder)

    # classify
    sys.stdout = __console__
    if not os.path.exists(os.path.join(output_dir,'js')):
        os.makedirs(os.path.join(output_dir,'js'))
    if not os.path.exists(os.path.join(output_dir,'wsf')):
        os.makedirs(os.path.join(output_dir,'wsf'))
    if not os.path.exists(os.path.join(output_dir,'office')):
        os.makedirs(os.path.join(output_dir,'office'))
    classify(extracted_folder, output_dir)
    classify(unzipped_folder, output_dir)

    # extract macros
    extract_macros(os.path.join(output_dir,'office'))

    # analyse js and wsf files
    curr_path = os.path.split(os.path.realpath(__file__))[0]
    project_dir = get_parent_path(curr_path, 2)
    sal_path_ = os.path.join(project_dir, 'third_party', 'wrappers', 'salineup_wrapper','salineup')
    sal = os.path.join(sal_path_, 'SALineup.exe')
    print "\nNow Processing JS Files :"
    with open(os.path.join(output_dir,'logs','js-log.log'), 'w') as sys.stdout:
        subprocess.check_call(sal + ' --productname=sc --script-malware=true --loglevel=all \"'+\
            os.path.join(output_dir,'js') + '\"', stdout=sys.stdout)
    sys.stdout = __console__
    print "\nNow Processing WSF Files :"
    with open(os.path.join(output_dir,'logs','wsf-log.log'), 'w') as sys.stdout:
        subprocess.check_call(sal + ' --productname=sc --script-malware=true --loglevel=all \"'+\
            os.path.join(output_dir,'wsf') + '\"', stdout=sys.stdout)
    sys.stdout = __console__


if __name__ == '__main__':
	main()