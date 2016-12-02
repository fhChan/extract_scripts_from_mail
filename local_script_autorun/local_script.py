 # Author: Feihao Chen
 # Date: 2016/11/30

import os,sys,re
import csv
import subprocess

class xml_analyser(object):
    """

    """
    def __init__(self):
        csvfile=file('report.csv','wb')
        writer=csv.writer(csvfile)
        writer.writerow(['name','is_local','decision','rules','/*@cc_on','wscript.shell','shell.application','scripting.filesystemobject',\
'window.xxx','document.xxx','xmlhttp','adodb.stream','getElementsByTagName','getElementById','<div','console','parentNode',\
'window[xxx]','document[xxx]','$.'])
        csvfile.close()

    def f_reader(self,xml_file):
        file=open(xml_file,'r')
        s=file.read()
        file.close()
        return s

    # extract filename
    def xml_filename(self,xml_file):
        s=self.f_reader(xml_file)
        i1=s.find('<file_path>')
        i2=s.find('</file_path>')
        l=s[i1:i2].split('\\')
        if len(l)>1:
            js_name=l[-1]  #xx.js
        else:
            print 'file path error:\t',f
            exit(0)
        return js_name

    # extract decision
    def sa_decision(self,xml_file):
        s=self.f_reader(xml_file)
        i1=s.find('<decision>')+10
        i2=s.find('</decision>')
        return s[i1:i2]

    # extract rules
    def sa_rules(self,xml_file):
        s=self.f_reader(xml_file)
        i1=s.find('<matched_rules>')
        i2=s.find('</matched_rules>')
        rules=s[i1:i2]
        set1=set()
        i1=rules.find('<rule>')
        while i1 != -1:
            i2=rules.find('</rule>',i1)
            set1.add(rules[i1+6:i2])
            i1=rules.find('<rule>',i2)
        return ';'.join(set1)

    def xml_stru_error(self,xml_file):
        s=self.f_reader(xml_file)
        if s.count(js_tag)<3:
            raise 'xml stru error'

    # step over the first two pairs js tag
    def behaviour_reader(self,xml_file):
        js_tag='<evidence type="javascript"'
        s=self.f_reader(xml_file)
        i1=s.find(js_tag)+20
        i2=s.find(js_tag,i1)+20
        index=s.find(js_tag,i2)
        s=s[index+20:].lower()
        return s

    def find_feature(self,feature,xml_file):
        s=self.behaviour_reader(xml_file)
        if re.search(feature,s)!=None:
            return 1
        else:
            return 0

    def win_1(self,xml_file):
        s=self.behaviour_reader(xml_file)
        re_win=re.findall('\\bwindow\.[a-z0-9]+',s)
        return ';'.join(set(re_win))

    def doc_1(self,xml_file):
        s=self.behaviour_reader(xml_file)
        re_doc=re.findall('\\bdocument\.[a-z0-9]+',s)
        return ';'.join(set(re_doc))
        
    def win_2(self,xml_file):
        s=self.behaviour_reader(xml_file)
        re_win=re.findall('\\bwindow\[[a-z0-9]+\]',s)
        return ';'.join(set(re_win))

    def doc_2(self,xml_file):
        s=self.behaviour_reader(xml_file)
        re_doc=re.findall('\\bdocument\[[a-z0-9]+\]',s)
        return ';'.join(set(re_doc))

    def is_local_script(self,xml_file):
        flag=0
        flag+=self.find_feature(r'/*@cc_on',xml_file)
        flag+=self.find_feature('wscript.shell',xml_file)
        flag+=self.find_feature('shell.application',xml_file)
        flag+=self.find_feature('scripting.filesystemobject',xml_file)
        if flag>0:
            if self.win_1(xml_file)!='' and self.win_1(xml_file)!='window.eval':
                return False
            elif 'doc' in self.doc_1(xml_file):
                return False
            elif self.find_feature('getElementsByTagName',xml_file):
                return False
            elif self.find_feature('getElementById',xml_file):
                return False
            elif self.find_feature('<div',xml_file):
                return False
            elif self.find_feature('\\bconsole\.',xml_file):
                return False
            elif self.find_feature('parentNode',xml_file):
                return False
            elif 'win' in self.win_2(xml_file) and self.win_2(xml_file)!='window[eval]':
                return False
            elif 'doc' in self.doc_2(xml_file):
                return False
            elif self.find_feature('\s\$\.',xml_file):
                return False
            else:
                return True
        else:
            return False

    def report_append(self, xml_file):
        if self.is_local_script(xml_file):
            isl='T'
        else:
            isl='F'
        csvfile=file('report.csv','ab')
        writer=csv.writer(csvfile)
        writer.writerow([\
self.xml_filename(xml_file),\
isl,\
self.sa_decision(xml_file),\
self.sa_rules(xml_file),\
str(self.find_feature(r'/*@cc_on',xml_file)),\
str(self.find_feature('wscript.shell',xml_file)),\
str(self.find_feature('shell.application',xml_file)),\
str(self.find_feature('scripting.filesystemobject',xml_file)),\
self.win_1(xml_file),\
self.doc_1(xml_file),\
str(self.find_feature('xmlhttp',xml_file)),\
str(self.find_feature('adodb.stream',xml_file)),\
str(self.find_feature('getElementsByTagName',xml_file)),\
str(self.find_feature('getElementById',xml_file)),\
str(self.find_feature('<div',xml_file)),\
str(self.find_feature('\\bconsole\.',xml_file)),\
str(self.find_feature('parentNode',xml_file)),\
self.win_2(xml_file),\
self.doc_2(xml_file),\
str(self.find_feature('\s\$\.',xml_file))])
        csvfile.close()


def print_usage():
    print """
Usage:
    python local_script.py sample/sample_folder
    """


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        exit(-1)

    target_path = sys.argv[1]

    with open('SAL.log', 'w') as fout:
        subprocess.check_call('salineup_for_script_malware\SALineup.exe --productname=sc \
        --script-malware=true --loglevel=all \"' + target_path, stdout=fout)

    result_dir = os.path.join('salineup_for_script_malware', 'result')
    XA = xml_analyser()

    if os.path.isfile(target_path):
        last_modified_date = 0
        last_behavior = ''
        for behavior in os.listdir(result_dir):
            behavior_path = os.path.join(result_dir, behavior)
            mtime = os.path.getmtime(behavior_path)
            if (mtime > last_modified_date):
                last_modified_date, last_behavior = mtime, behavior_path
        try:
            if XA.is_local_script(last_behavior):
                print 'Is LocalScript!'
            else:
                print 'Is Not LocalScript!'
        except 'xml stru error':
            print 'xml stru error: ' + last_behavior
    else:
        for f in os.listdir(result_dir):
            filepath = os.path.join(result_dir, f)
            try:
                if 'xml' in os.path.splitext(f)[1]:
                    XA.report_append(filepath)
            except 'xml stru error':
                print 'xml stru error: ' + f
