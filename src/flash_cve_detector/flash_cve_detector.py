# auther = Cheng Chang(SA)
# Date = 2016/11/28
# usage is in README.md
import ConfigParser
import argparse
import os
import re
import shutil
import sys
import time

import yara

from third_party.wrappers.flash_decompile_wrapper.decomplie_helper import FfdecHelper
from third_party.wrappers.flash_unpack_wrapper.unpack_helper import FlashUnpackHelper


def curr_time():
    return time.strftime("%H:%M:%S")


class FlashDetector:
    def __init__(self):
        self.tol_count = 0
        self.mal_count = 0
        self.nor_count = 0
        self.as3_count = 0
        self.exception_list = []
        self.matched_rules = {}
        self.root_path = sys.path[0]
        self.dumpTimeout = False
        self.conf = {}
        self.target_path = ''
        self.unpack_ = FlashUnpackHelper()
        self.decomplie_ = FfdecHelper()
        self.load_conf()

    def work(self):
        target_path = self.target_path
        self.check_env(target_path)
        self.clean_env()
        if os.path.isfile(target_path):
            self.analyze_file(target_path)
        elif os.path.isdir(target_path):
            self.analyze_dir(target_path)
        self.printSum()

    def set_target_path(self, target_path):
        self.target_path = target_path

    def load_conf(self):
        # load conf.ini
        cf = ConfigParser.ConfigParser()
        if os.path.exists('conf.ini'):
            cf.read('conf.ini')
            for attr in cf.options('base'):
                self.conf[attr] = cf.get('base', attr)
        else:
            print '[ERROR] conf.ini not exists!'
            exit(0)

    def check_env(self, folder_path):
        # check folder_path
        if os.path.exists(folder_path):
            print curr_time(), 'target path is [%s]' % folder_path
        else:
            print '[ERROR] the entered path not exists!please enter abs path'
            exit(0)
        # check sulo
        if not os.path.exists('sulo'):
            print '[ERROR] sulo not exists in current dir!'
            exit(0)
        # check ffdec
        if not os.path.exists('ffdec'):
            print '[ERROR] ffdec not exists in current dir!'
            exit(0)
        # check yara file
        if not os.path.exists('rules.yar'):
            print '[ERROR] yara file not exists!'
            exit(0)

    def clean_env(self):    # clean log file(and the past result)
        if os.path.exists('runtime.log'):
            os.remove('runtime.log')
        # clean up dump file
        for f in os.listdir(self.root_path):
            if re.search('.*_\d$', f):
                os.remove(f)
                continue
            if f.startswith('dumped_flash_'):
                os.remove(f)
        # clean up result folder
        if os.path.exists('result'):
            for f in os.listdir('result'):
                shutil.rmtree(os.path.join('result', f))
        else:
            os.mkdir('result')

    def analyze_dir(self, folder_path):
        for f in os.listdir(folder_path):
            print curr_time(), 'No.', self.tol_count + 1
            self.analyze_file(os.path.join(folder_path, f))

    def analyze_file(self, file_path):
        if not os.path.exists(file_path):
            print curr_time(), "[ERROR] Cannot find ", file_path
            return
        sig = ""
        with open(file_path, "r") as fh:
            sig = fh.read(3).upper()
            fh.close()
        if sig[1:3] != "WS":
            print curr_time(), "[ERROR] Cannot find flash signature ", file_path
            return
        file_path_without_ext, ext = os.path.splitext(file_path)
        prefix_path, file_name = os.path.split(file_path_without_ext)
        if ext.lower() != ".swf":
            os.rename(file_path, file_path + ".swf")
            file_path += ".swf"
        # dump embedded flash
        self.unpack_.set_file_path(file_path)
        embedded_list = self.unpack_.dump_flash()

        if len(embedded_list):
            embedded_list.insert(0, file_path)
            self.analyze_internal(Sample(file_path, True, embedded_list=embedded_list))
            # clean embedded flash
            for f in os.listdir(os.getcwd()):
                if f.startswith(file_name):
                    os.remove(f)
        else:
            self.analyze_internal((Sample(file_path, False)))
        print '\n'

    def analyze_internal(self, sample):
        # export as files
        print curr_time(), 'Now decomplie File : [%s]' % sample.file_path
        self.export_action_script(sample)
        # merge into one .as
        print curr_time(), 'Now merge as : [%s]' % sample.file_path
        self.merge_as(sample)
        # yara
        print curr_time(), 'Now match File : [%s]' % sample.file_path
        self.yara_match('rules.yar', sample)

        self.collect_info(sample)

    def export_action_script(self, sample):
        result_folder = sample.result_folder
        if os.path.exists(result_folder):
            shutil.rmtree(result_folder)
            os.mkdir(result_folder)
        if sample.embedded is True:
            count = 1
            for f in sample.embedded_list:
                print curr_time(), 'Now decomplie embedded flash %s: [%s]' % (count, f)
                count_folder = os.path.join(result_folder, str(count))
                self.decomplie_.set_file_path(f)
                self.decomplie_.set_result_path(count_folder)
                self.decomplie_.decomplie()
                count += 1
        else:
            self.decomplie_.set_file_path(sample.file_path)
            self.decomplie_.set_result_path(result_folder)
            self.decomplie_.decomplie()
        sample.as3 = True

    def merge_as(self, sample):
        if sample.embedded is True:
            end = len(sample.embedded_list)
            for i in range(1, end + 1):   # 1...end
                count_folder = os.path.join(sample.result_folder, str(i))
                decompiled_path = os.path.join(count_folder, 'decompiled_code.as')
                with open(decompiled_path, 'a') as fh_output:
                    for root, dirs, files in os.walk(os.path.join(count_folder, 'scripts')):
                        for name in files:
                            with open(os.path.join(root, name), 'r') as fh:
                                fh_output.write(fh.read() + '\n')

            decompiled_path = os.path.join(sample.result_folder, 'all_decompiled_code.as')
            with open(decompiled_path, 'w') as fh_output:
                for i in range(1, end + 1):
                    count_folder = os.path.join(sample.result_folder, str(i))
                    for f in os.listdir(count_folder):
                        if f == 'decompiled_code.as':
                            with open(os.path.join(count_folder, f), 'r') as fh:
                                fh_output.write(fh.read() + '\n')
                            break
        else:
            result_folder = sample.result_folder
            decompiled_path = os.path.join(result_folder, 'all_decompiled_code.as')
            with open(decompiled_path, 'w') as fh_output:
                for root, dirs, files in os.walk(os.path.join(result_folder, 'scripts')):
                    for name in files:
                        with open(os.path.join(root, name), 'r') as fh:
                            fh_output.write(fh.read() + '\n')

    def yara_match(self, yara_file, sample, externals=None):
        rules = yara.compile(yara_file)
        as_file = os.path.join(sample.result_folder, 'all_decompiled_code.as')
        matches = rules.match(as_file, externals=externals)

        file_name = sample.file_name
        judge = ''
        if len(matches) == 0:
            judge = curr_time() + ' Decision: [%s] on File: [%s]' % ('Normal', file_name)
            sample.malicious = False
        else:
            judge = curr_time() + ' Decision: [%s] on File: [%s]\n' % ('Malicious', file_name)
            judge += curr_time() + ' Rules: ' + str(matches)
            sample.malicious = True
        print judge

        debug = False
        if 'debug' in self.conf and self.conf['debug'] == 'true':
            debug = True
        if not debug:
            for file in sample.result_folder:
                shutil.rmtree(file)
        with open(os.path.join(sample.result_folder, 'behavior.log'), 'w') as f:
            f.write(judge)

        for r in matches:
            if r in self.matched_rules:
                self.matched_rules[r] += 1
            else:
                self.matched_rules[r] = 1

    def collect_info(self, sample):
        self.tol_count += 1
        if sample.as3 is True:
            self.as3_count += 1
        if sample.malicious is True:
            self.mal_count += 1
        else:
            self.nor_count += 1

    def printSum(self):
        count_by_rules = ''
        for k, v in self.matched_rules.iteritems():
            count_by_rules += '[%s]=[%s]\n' % (k, v)
        exception_str = '\n'.join(self.exception_list)
        print '''
------------------------------------------------------
Statistics Info :
Scan All Count=[%s]
AS3 File Count=[%s]
Count By Diagnosis
[Normal]=[%s]
[Malicious]=[%s]
Count By Rules
%s
Exception List
%s
        ''' % (self.tol_count, self.as3_count, self.nor_count, self.mal_count, count_by_rules, exception_str)


class Sample():
    def __init__(self, path, embedded=False, embedded_list=[]):
        self.embedded = embedded
        self.file_path = path
        prefix_path, file_name = os.path.split(path)
        file_name_without_ext, ext = os.path.splitext(file_name)
        self.file_name = file_name
        self.malicious = False
        self.as3 = False
        self.exception = False
        self.result_folder = os.path.join('result', file_name_without_ext)
        self.embedded_list = embedded_list


def main():
    opt = argparse.ArgumentParser(description="Flash cve detector - judge swf file is malicious or not")
    opt.add_argument("TargetPath", help="Enter the Path to .swf/swf folder")
    if len(sys.argv) != 2:
        opt.print_help()
        sys.exit(1)
    options = opt.parse_args()

    os.chdir(sys.path[0])
    detector = FlashDetector()
    detector.set_target_path(options.TargetPath)
    detector.work()


if __name__ == '__main__':
    main()
