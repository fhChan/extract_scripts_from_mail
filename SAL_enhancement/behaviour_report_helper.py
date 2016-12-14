 # Author: Feihao Chen
 # Date: 2016/12/13

import os,sys
import xml.etree.cElementTree as ET

class BehaviourReport(object):
    """

    """
    def __init__(self,xml_file):
        self.root=self.root_reader(xml_file)
        self.line_reader=self.line_reader(xml_file)
        self.behaviour_reader=self.behaviour_reader()
        self.filename=self.get_name()
        self.sa_decison=self.get_decision()
        self.rules=self.get_rules()

    # read xml by root
    def root_reader(self,xml_file):
        tree=ET.parse(xml_file)
        return tree.getroot()

    # read xml by line
    def line_reader(self,xml_file):
        with open(xml_file,'r') as file:
            return file.read()

    def behaviour_reader(self):
        s=''
        label=0
        for e in self.root: 
            if e.tag!='evidence':
                continue
            if e.attrib['type']=='javascript' and '// This is JS Runtime file' in e[2].text:
                label=1
                continue
            if e.attrib['type']=='javascript_behavior' and label==1:
                label=0
                continue
            s=s+e[-1].text
        return s.lower()

    def get_name(self):
        return self.root[0].text

    def get_decision(self):
        for e in self.root:
            if e.tag=='decision':
                return e.text

    def get_rules(self):
        for e in self.root:
            if e.tag=='matched_rules':
                return ';'.join(x.text for x in e)

