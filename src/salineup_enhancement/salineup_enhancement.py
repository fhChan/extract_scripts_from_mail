 # Author: Feihao Chen
 # Date: 2016/12/15

import os,sys
import csv
import url_rank
import xml.etree.cElementTree as ET
from behaviour_report_helper import BehaviourReportHelper

# analysis all .xml in sys.argv[1]
# judge JS confusion and urls order
class MalDetHelper(object):
    """

    """
    def __init__(self):
        self.BRH = BehaviourReportHelper()
        csvfile=file('analysis_log.csv','wb')
        writer=csv.writer(csvfile)
        writer.writerow(['sample-path','obfuscation','URL','rank','SA_decision'])
        csvfile.close()

    def url_judge(self,url_list):
        cur_no=0
        cur_url=''
        for url in url_list:
            no=url_rank.analysis_url(url)
            if no>cur_no:
                cur_no=no
                cur_url=url
        if not cur_no:
            cur_no=''
        return [cur_url,cur_no]

    def report_append(self, xml_file):
        self.BRH.set_xml_file(xml_file)
        self.BRH.parse_XML()
        cur_url,cur_no=self.url_judge(self.BRH.get_url_list())

        csvfile=file('analysis_log.csv','ab')
        writer=csv.writer(csvfile)
        writer.writerow([self.BRH.get_file_path(),str(self.BRH.get_obfuscation()),cur_url,str(cur_no),self.BRH.get_decision()])
        csvfile.close()

        self.BRH.clear()

def print_usage():
    print """
Usage:
    python tool.py input_dir
    """

def dir_process(folder_path):
    MDH = MalDetHelper()
    for f in os.listdir(folder_path):
        filepath = os.path.join(folder_path, f)
        try:
            if 'xml' in os.path.splitext(f)[1]:
                MDH.report_append(filepath)
        except:
            print 'Processing error: ' + f


if __name__=='__main__':
    if len(sys.argv)!=2:
        print_usage()
        exit(-1)

    folder_path=sys.argv[1]
    if not os.path.exists(folder_path):
        print 'folder not exists'
        exit(0)

    dir_process(folder_path)