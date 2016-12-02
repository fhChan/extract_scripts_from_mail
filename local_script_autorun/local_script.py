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
        r=''
        i1=rules.find('<rule>')
        while i1 != -1:
            i2=rules.find('</rule>',i1)
            set1.add(rules[i1+6:i2])
            i1=rules.find('<rule>',i2)
            for i in set1:
                r+=i+';'
            set1.clear()
        if ';' in r:
            r=r[:-1]
        return r

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

    def cc_on(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if r'/*@cc_on' in s:
            return 1
        else:
            return 0

    def w_s(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if 'wscript.shell' in s:
            return 1
        else:
            return 0

    def s_a(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if 'shell.application' in s:
            return 1
        else:
            return 0

    def s_f(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if 'scripting.filesystemobject' in s:
            return 1
        else:
            return 0

    def win_1(self,xml_file):
        s=self.behaviour_reader(xml_file)
        set2=set()
        t=''
        re_win=re.findall('\\bwindow\.[a-z0-9]+',s)
        if re_win:
            for item in re_win:
                set2.add(item)
            for i in set2:
                t+=i+';'
            set2.clear()
            if ';' in t:
                t=t[:-1]
        return t

    def doc_1(self,xml_file):
        s=self.behaviour_reader(xml_file)
        set3=set()
        t=''
        re_doc=re.findall('\\bdocument\.[a-z0-9]+',s)
        if re_doc:
            for item in re_doc:
                set3.add(item)
            for i in set3:
                t+=i+';'
            set3.clear()
            if ';' in t:
                t=t[:-1]
        return t

    def xmlhttp(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if 'xmlhttp' in s:
            return 1
        else:
            return 0

    def adodb_stream(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if 'adodb.stream' in s:
            return 1
        else:
            return 0

    def gEBT(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if 'getElementsByTagName' in s:
            return 1
        else:
            return 0

    def gEBI(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if 'getElementById' in s:
            return 1
        else:
            return 0

    def div(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if '<div' in s:
            return 1
        else:
            return 0

    def console(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if '\\bconsole\.' in s:
            return 1
        else:
            return 0

    def parentNode(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if 'parentNode' in s:
            return 1
        else:
            return 0
        
    def win_2(self,xml_file):
        s=self.behaviour_reader(xml_file)
        set4=set()
        t=''
        re_win=re.findall('\\bwindow\[[a-z0-9]+\]',s)
        if re_win:
            for item in re_win:
                set4.add(item)
            for i in set4:
                t+=i+';'
            set4.clear()
            if ';' in t:
                t=t[:-1]
        return t

    def doc_2(self,xml_file):
        s=self.behaviour_reader(xml_file)
        set5=set()
        t=''
        re_doc=re.findall('\\bdocument\[[a-z0-9]+\]',s)
        if re_doc:
            for item in re_doc:
                set5.add(item)
            for i in set5:
                t+=i+';'
            set5.clear()
            if ';' in t:
                t=t[:-1]
        return t

    def dollar(self,xml_file):
        s=self.behaviour_reader(xml_file)
        if re.search('\s\$\.',s)!=None:
            return 1
        else:
            return 0


    def is_local_script(self,xml_file):
        flag=0
        flag+=self.cc_on(xml_file)
        flag+=self.w_s(xml_file)
        flag+=self.s_a(xml_file)
        flag+=self.s_f(xml_file)
        if flag>0:
            if self.win_1(xml_file)!='' and self.win_1(xml_file)!='window.eval':
                return False
            elif 'doc' in self.doc_1(xml_file):
                return False
            elif self.gEBT(xml_file):
                return False
            elif self.gEBI(xml_file):
                return False
            elif self.div(xml_file):
                return False
            elif self.console(xml_file):
                return False
            elif self.parentNode(xml_file):
                return False
            elif 'win' in self.win_2(xml_file) and self.win_2(xml_file)!='window[eval]':
                return False
            elif 'doc' in self.doc_2(xml_file):
                return False
            elif self.dollar(xml_file):
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
        writer.writerow([self.xml_filename(xml_file),isl,self.sa_decision(xml_file),self.sa_rules(xml_file),\
str(self.cc_on(xml_file)),str(self.w_s(xml_file)),str(self.s_a(xml_file)),str(self.s_f(xml_file)),\
self.win_1(xml_file),self.doc_1(xml_file),str(self.xmlhttp(xml_file)),str(self.adodb_stream(xml_file)),\
str(self.gEBT(xml_file)),str(self.gEBI(xml_file)),str(self.div(xml_file)),str(self.console(xml_file)),\
str(self.parentNode(xml_file)),self.win_2(xml_file),self.doc_2(xml_file),str(self.dollar(xml_file))])
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
