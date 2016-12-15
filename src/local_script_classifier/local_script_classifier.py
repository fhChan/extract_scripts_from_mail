 # Author: Feihao Chen
 # Date: 2016/12/15

import os,sys
import csv
import subprocess
from behaviour_report_helper import BehaviourReportHelper

class xml_analyser(object):
    """

    """
    def __init__(self):
        self.BRH = BehaviourReportHelper()
        self.fieldnames = ['name','is_local','decision','rules','/*@cc_on','wscript.shell','shell.application','scripting.filesystemobject',\
'window.xxx','document.xxx','xmlhttp','adodb.stream','getElementsByTagName','getElementById','<div','console','parentNode',\
'window[xxx]','document[xxx]','$.']
        csvfile=file('report.csv','wb')
        writer=csv.writer(csvfile)
        writer.writerow(self.fieldnames)
        csvfile.close()

    def is_local_script(self):
        return self.BRH.get_is_local()

    def report_append(self,xml_file):
        self.BRH.set_xml_file(xml_file)
        self.BRH.parse_XML()
        csvfile=file('report.csv','ab')
        writer=csv.writer(csvfile)
        writer.writerow([\
self.BRH.get_file_path(),
self.BRH.get_is_local(),
self.BRH.get_decision(),
self.BRH.get_rules(),
self.BRH.get_feature_dict()[r'/*@cc_on'],
self.BRH.get_feature_dict()['wscript.shell'],
self.BRH.get_feature_dict()['shell.application'],
self.BRH.get_feature_dict()['scripting.filesystemobject'],
self.BRH.get_feature_dict()['\\bwindow\.[a-z0-9]+'],
self.BRH.get_feature_dict()['\\bdocument\.[a-z0-9]+'],
self.BRH.get_feature_dict()['xmlhttp'],
self.BRH.get_feature_dict()['adodb.stream'],
self.BRH.get_feature_dict()['getElementsByTagName'],
self.BRH.get_feature_dict()['getElementById'],
self.BRH.get_feature_dict()['<div'],
self.BRH.get_feature_dict()['\\bconsole\.'],
self.BRH.get_feature_dict()['parentNode'],
self.BRH.get_feature_dict()['\\bwindow\[[a-z0-9]+\]'],
self.BRH.get_feature_dict()['\\bdocument\[[a-z0-9]+\]'],
self.BRH.get_feature_dict()['\s\$\.']])
        csvfile.close()
        self.BRH.clear()

def print_usage():
    print """
Usage:
    python local_script.py XML_folder
    """

def print_single_result(result_dir):
    XA = xml_analyser()
    last_modified_date = 0
    last_behavior = ''
    for behavior in os.listdir(result_dir):
        behavior_path = os.path.join(result_dir, behavior)
        mtime = os.path.getmtime(behavior_path)
        if (mtime > last_modified_date):
            last_modified_date, last_behavior = mtime, behavior_path
    XA.BRH = BehaviourReportHelper(last_behavior)
    if XA.is_local_script():
        print '\nIt\'s local script!'
    else:
        print '\nIt\'s not local script!'

# form a csv file to show the features
def process_multi_xml(result_dir):
    XA = xml_analyser()
    for f in os.listdir(result_dir):
        filepath = os.path.join(result_dir, f)
        # try:
        if 'xml' in os.path.splitext(f)[1]:
            XA.report_append(filepath)
        # except:
        #     print 'processing error: ' + f

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
        print_single_result(result_dir)
    else:
        process_multi_xml(result_dir)
