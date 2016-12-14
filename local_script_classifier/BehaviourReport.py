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

    # step over the first two pairs js tag
    def behaviour_reader(self):
        js_tag='<evidence type="javascript"'
        s=self.line_reader
        i1=s.find(js_tag)+20
        i2=s.find(js_tag,i1)+20
        index=s.find(js_tag,i2)
        s=s[index+20:].lower()
        return s

    def get_name(self):
        return self.root[0].text

    def get_decision(self):
        return self.root[4].text

    def get_rules(self):
        return ';'.join(x.text for x in self.root[5])

