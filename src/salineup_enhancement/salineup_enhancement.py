 # Author: Feihao Chen
 # Date: 2016/12/14

import os,sys
import csv
import url_rank
import xml.etree.cElementTree as ET
from behaviour_report_helper import BehaviourReport

# analysis all .xml in sys.argv[1]
# judge JS confusion and urls order
class MalDetHelper(object):
    """

    """
    def __init__(self):
        csvfile=file('analysis_log.csv','wb')
        writer=csv.writer(csvfile)
        writer.writerow(['sample-path','obfuscation','URL','rank','SA_decision'])
        csvfile.close()

    def obfuscation_exists(self,evidence):
        content=evidence[-1].text.split('\n')
        if content[1][:20].find('window.eval')!=-1:
            return True
        else:
            return False

    def url_judge(self,evidence):
        line_list=evidence[-1].text.split('\n')
        cur_no=0
        cur_url=''
        for line in line_list[2:]:
            if line.find(' URL =')!=-1:
                start=line.find(' URL =')+7
                if line[start:start+4]=='http':
                    start=start+7              #pass http://
                    end=line.find('/',start)     
                    if end ==-1:
                        end=line.find('\"',start)
                else:           #other url
                    end=line.find('\"',start)
                url=line[start:end]
                no=url_rank.analysis_url(url)
                if no>cur_no:
                    cur_no=no
                    cur_url=url
        if not cur_no:
            cur_no=''
        return [cur_url,cur_no]

    def report_append(self, xml_file):
        BR = BehaviourReport(xml_file)
        ob=self.obfuscation_exists(BR.root[-1])
        cur_url,cur_no=self.url_judge(BR.root[-1])

        csvfile=file('analysis_log.csv','ab')
        writer=csv.writer(csvfile)
        writer.writerow([BR.filename,str(ob),cur_url,str(cur_no),BR.sa_decison])
        csvfile.close()

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