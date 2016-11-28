# auther = Cheng(SA)
# usage is in README.md
import os
import sys
import time
import re
import argparse
import ConfigParser
import subprocess
import threading
import psutil
import shutil
import yara

global tol_count
global mal_count
global nor_count
global as3_count
global matched_rules
global root_path
global exception_list
tol_count = 0
mal_count = 0
nor_count = 0
as3_count = 0
exception_list = []
matched_rules = {}
root_path = sys.path[0]


class Sample():
    def __init__(self, path, embedded, embedded_list=[]):
        self.embedded = embedded
        self.file_path = path
        prefix_path, file_name = os.path.split(path)
        self.file_name = file_name
        self.malicious = False
        self.as3 = False
        self.exception = False
        self.result_folder = os.path.join('result', file_name)[:-4]
        self.embedded_list = embedded_list


class Ffdec_ParseError(Exception):
    def __init__(self, sample):
        self.sample = sample

    def getMessage(self):
        print curr_time(), "[ERROR] ffdec can't parse ", self.sample.file_path


class Ffdec_Timeout(Exception):
    def __init__(self, sample):
        self.sample = sample

    def getMessage(self):
        print curr_time(), '[WARN] ffdec be kill for timeout ', self.sample.file_path


class Unknown_Ffdec_Error(Exception):
    def __init__(self, sample):
        self.sample = sample

    def getMessage(self):
        print curr_time(), '[ERROR] donnot have scripts folder', self.sample.file_path


def curr_time():
    return time.strftime("%H:%M:%S")


def check_env(folder_path):
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


def clean_env():    # clean log file(and the past result)
    if os.path.exists('runtime.log'):
        os.remove('runtime.log')
    # clean up dump file
    for f in os.listdir(os.getcwd()):
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


def analyze_dir(folder_path):
    global tol_count
    for f in os.listdir(folder_path):
        print curr_time(), 'No.', tol_count + 1
        analyze_file(os.path.join(folder_path, f))


def analyze_file(file_path):
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
    embedded_list = dump_flash(file_path)

    if len(embedded_list) != 0:
        analyze_internal(Sample(file_path, True, embedded_list=embedded_list))

        # clean embedded flash
        for f in os.listdir(os.getcwd()):
            if f.startswith(file_name):
                os.remove(f)
    else:
        analyze_internal((Sample(file_path, False)))
    print '\n'


def dump_flash(file_path):
    global dumpTimeout
    dumpTimeout = False

    # f0fad08da4212cc398160c38d2ba1f8a1930cfd1  10->dump,11->no dump
    # solu_cmd = 'sulo\pin -t sulo.dll -- flashplayer10_3r181_23_win_sa.exe '+file_path
    solu_cmd = 'sulo\pin -t sulo.dll -- flashplayer11_1r102_62_win_sa_32bit.exe ' + file_path

    proc = subprocess.Popen(solu_cmd)
    # proc.communicate()
    t = threading.Timer(20, kill_process, [proc])
    t.start()
    t.join()

    global root_path
    if dumpTimeout is True:
        DumpFlag = False
        for f in os.listdir(root_path):
            if f[:12] == 'dumped_flash':
                DumpFlag = True
                break
        if DumpFlag is False:
            print curr_time(), 'dump timeout,give up dumping'
            return []

    embedded_list = []
    prefix_path, file_name = os.path.split(file_path)
    embedded_count = 0

    for f in os.listdir(root_path):
        if f[:12] == 'dumped_flash':
            new_name = file_name[:-4] + '_%s' % embedded_count  # xxx_0
            os.rename(f, new_name)
            embedded_list.append(os.path.join(root_path, new_name))
            embedded_count += 1
    if embedded_count == 0:
        print curr_time(), 'no need to dump'
    else:
        print curr_time(), 'dump dembedded flash', embedded_list
    return embedded_list


def analyze_internal(sample):
    # export as files
    print curr_time(), 'Now decomplie File : [%s]' % sample.file_path
    export_action_script(sample)

    # merge into one .as
    print curr_time(), 'Now merge as : [%s]' % sample.file_path
    merge_as(sample)

    # yara
    print curr_time(), 'Now match File : [%s]' % sample.file_path
    yara_match('rules.yar', sample)

    collect_info(sample)


def export_action_script(sample):
    # global timeout
    # timeout=False
    result_folder = sample.result_folder
    if os.path.exists(result_folder):
        shutil.rmtree(result_folder)
        os.mkdir(result_folder)
    if sample.embedded is True:
        count = 1
        for f in sample.embedded_list:
            print curr_time(), 'Now decomplie embedded flash %s: [%s]' % (count, f)
            count_folder = os.path.join(result_folder, str(count))
            ffdec_cmd = "\"ffdec\%s\" -export script \"%s\" \"%s\"" % ('ffdec.bat', count_folder, f)

            proc = subprocess.Popen(ffdec_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.communicate()
            if len(proc.stderr.read()) != 0:
                sample.exception = True
                raise Ffdec_ParseError(sample)
            count += 1
    else:
        ffdec_cmd = "\"ffdec\%s\" -export script \"%s\" \"%s\"" % ('ffdec.bat', result_folder, sample.file_path)

        proc = subprocess.Popen(ffdec_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        # t = threading.Timer(10, kill_process, [proc] )
        # t.start()
        # t.join()

        if len(proc.stderr.read()) != 0:
            sample.exception = True
            exception_list.append(sample)
            raise Ffdec_ParseError(sample)
        # if timeout==True:
        #   sample.exception=True
        #     raise Ffdec_Timeout(sample)
    sample.as3 = True


def merge_as(sample):
    # if not os.path.exists(os.path.join(sample.result_folder, "scripts")):
    #     sample.exception=True
    #     exception_list.append(sample)
    #     raise Unknown_Ffdec_Error(sample)
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
        with open(decompiled_path, 'a') as fh_output:
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
        with open(decompiled_path, 'a') as fh_output:
            for root, dirs, files in os.walk(os.path.join(result_folder, 'scripts')):
                for name in files:
                    with open(os.path.join(root, name), 'r') as fh:
                        fh_output.write(fh.read() + '\n')


def yara_match(yara_file, sample, externals=None):
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

    global conf
    debug = False
    if 'debug' in conf and conf['debug'] == 'true':
        debug = True
    if not debug:
        for file in sample.result_folder:
            shutil.rmtree(file)
    with open(os.path.join(sample.result_folder, 'behavior.log'), 'w') as f:
        f.write(judge)
    global matched_rules
    for r in matches:
        if r in matched_rules:
            matched_rules[r] += 1
        else:
            matched_rules[r] = 1


def kill_process(proc):
    if proc.poll() is None:
        print curr_time(), '[WARN] process taking too long to complete - kill'
        for child in psutil.Process(proc.pid).children(recursive=True):
            child.kill()
        proc.kill()
        global dumpTimeout
        dumpTimeout = True


def collect_info(sample):
    global tol_count
    global mal_count
    global nor_count
    global as3_count
    tol_count += 1
    if sample.as3 is True:
        as3_count += 1
    if sample.malicious is True:
        mal_count += 1
    else:
        nor_count += 1


def printSum():
    global tol_count
    global mal_count
    global nor_count
    global as3_count
    global matched_rules
    count_by_rules = ''
    for k, v in matched_rules.iteritems():
        count_by_rules += '[%s]=[%s]\n' % (k, v)

    exception_str = ''
    for e in exception_list:
        exception_str += e + '\n'

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
    ''' % (tol_count, as3_count, nor_count, mal_count, count_by_rules, exception_str)


def main():
    opt = argparse.ArgumentParser(description="Flash cve detector - judge swf file is malicious or not")
    opt.add_argument("TargetPath", help="Enter the Path to .swf/swf folder")
    if len(sys.argv) != 2:
        opt.print_help()
        sys.exit(1)
    options = opt.parse_args()

    global root_path
    os.chdir(root_path)
    # load conf.ini
    cf = ConfigParser.ConfigParser()
    if os.path.exists('conf.ini'):
        cf.read('conf.ini')
        global conf
        conf = {}
        for attr in cf.options('base'):
            conf[attr] = cf.get('base', attr)
    else:
        print '[ERROR] conf.ini not exists!'
        exit(0)

    target_path = options.TargetPath
    check_env(target_path)
    clean_env()

    if os.path.isfile(target_path):
        analyze_file(target_path)
    elif os.path.isdir(target_path):
        analyze_dir(target_path)
    printSum()


if __name__ == '__main__':
    main()
