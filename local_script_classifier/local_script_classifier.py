 # Author: Feihao Chen
 # Date: 2016/12/13

import os,sys,re
import csv
import subprocess
from BehaviourReport import BehaviourReport

class xml_analyser(object):
    """

    """
    def __init__(self):
        self.BR = None

        csvfile=file('report.csv','wb')
        writer=csv.writer(csvfile)
        writer.writerow(['name','is_local','decision','rules','/*@cc_on','wscript.shell','shell.application','scripting.filesystemobject',\
'window.xxx','document.xxx','xmlhttp','adodb.stream','getElementsByTagName','getElementById','<div','console','parentNode',\
'window[xxx]','document[xxx]','$.'])
        csvfile.close()

    # def xml_stru_error(self):
    #     s=self.f_reader(xml_file)
    #     if s.count(js_tag)<3:
    #         print 'xml stru error: '

    def behaviour_reader(self):
        return self.BR.behaviour_reader

    def find_feature(self,feature):
        s=self.behaviour_reader()
        return 1 if re.search(feature,s)!=None else 0

    def match_feature(self,feature):
        s=self.behaviour_reader()
        return ';'.join(set(re.findall(feature,s)))

    def is_local_script(self):
        flag=0
        flag+=self.find_feature(r'/*@cc_on')
        flag+=self.find_feature('wscript.shell')
        flag+=self.find_feature('shell.application')
        flag+=self.find_feature('scripting.filesystemobject')
        if flag>0:
            if 'w' in self.match_feature('\\bwindow\.[a-z0-9]+') and self.match_feature('\\bwindow\.[a-z0-9]+')!='window.eval':
                return False
            elif 'd' in self.match_feature('\\bdocument\.[a-z0-9]+'):
                return False
            elif self.find_feature('getElementsByTagName'):
                return False
            elif self.find_feature('getElementById'):
                return False
            elif self.find_feature('<div'):
                return False
            elif self.find_feature('\\bconsole\.'):
                return False
            elif self.find_feature('parentNode'):
                return False
            elif 'w' in self.match_feature('\\bwindow\[[a-z0-9]+\]') and self.match_feature('\\bwindow\[[a-z0-9]+\]')!='window[eval]':
                return False
            elif 'd' in self.match_feature('\\bdocument\[[a-z0-9]+\]'):
                return False
            elif self.find_feature('\s\$\.'):
                return False
            else:
                return True
        else:
            return False

    def report_append(self,xml_file):
        self.BR = BehaviourReport(xml_file)
        csvfile=file('report.csv','ab')
        writer=csv.writer(csvfile)
        writer.writerow([\
self.BR.filename,\
'T' if self.is_local_script() else 'F',\
self.BR.sa_decison,\
self.BR.rules,\
str(self.find_feature(r'/*@cc_on')),\
str(self.find_feature('wscript.shell')),\
str(self.find_feature('shell.application')),\
str(self.find_feature('scripting.filesystemobject')),\
self.match_feature('\\bwindow\.[a-z0-9]+'),\
self.match_feature('\\bdocument\.[a-z0-9]+'),\
str(self.find_feature('xmlhttp')),\
str(self.find_feature('adodb.stream')),\
str(self.find_feature('getElementsByTagName')),\
str(self.find_feature('getElementById')),\
str(self.find_feature('<div')),\
str(self.find_feature('\\bconsole\.')),\
str(self.find_feature('parentNode')),\
self.match_feature('\\bwindow\[[a-z0-9]+\]'),\
self.match_feature('\\bdocument\[[a-z0-9]+\]'),\
str(self.find_feature('\s\$\.'))])
        csvfile.close()

def print_usage():
    print """
Usage:
    python local_script.py XML_folder
    """

def process_single_xml(result_dir):
    XA = xml_analyser()
    last_modified_date = 0
    last_behavior = ''
    for behavior in os.listdir(result_dir):
        behavior_path = os.path.join(result_dir, behavior)
        mtime = os.path.getmtime(behavior_path)
        if (mtime > last_modified_date):
            last_modified_date, last_behavior = mtime, behavior_path
    if XA.is_local_script(last_behavior):
        print 'Is LocalScript!'
    else:
        print 'Is Not LocalScript!'

def process_multi_xml(result_dir):
    XA = xml_analyser()
    for f in os.listdir(result_dir):
        filepath = os.path.join(result_dir, f)
        try:
            if 'xml' in os.path.splitext(f)[1]:
                XA.report_append(filepath)
        except:
            print 'processing error: ' + f

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        exit(-1)

    target_path = sys.argv[1]
    with open('SAL.log', 'w') as fout:
        subprocess.check_call('salineup_for_script_malware\SALineup.exe --productname=sc \
        --script-malware=true --loglevel=all \"' + target_path, stdout=fout)
    result_dir = os.path.join('salineup_for_script_malware','result')

    if os.path.isfile(target_path):
        process_single_xml(result_dir)
    else:
        process_multi_xml(result_dir)
