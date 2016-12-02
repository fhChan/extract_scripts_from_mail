import os
import sys
import subprocess
import threading
import time
import psutil
import re


def curr_time():
    return time.strftime("%H:%M:%S")


class FlashUnpackHelper:
    def __init__(self):
        self.dumpTimeout = False
        self.file_path = ''
        self.root_path = sys.path[0]
        self.check_env()
        self.clean_env()

    def set_file_path(self, file_path):
        self.file_path = file_path

    def check_env(self):
        # check sulo
        if not os.path.exists('sulo'):
            print '[ERROR] sulo not exists in current dir!'
            exit(0)

    def clean_env(self):
        # clean up dump file
        for f in os.listdir(self.root_path):
            if re.search('.*_\d$', f):
                os.remove(f)
                continue
            if f.startswith('dumped_flash_'):
                os.remove(f)

    def dump_flash(self):
        self.dumpTimeout = False
        # f0fad08da4212cc398160c38d2ba1f8a1930cfd1  10->dump,11->no dump
        # solu_cmd = 'sulo\pin -t sulo.dll -- flashplayer10_3r181_23_win_sa.exe '+file_path
        solu_cmd = 'sulo\pin -t sulo.dll -- flashplayer11_1r102_62_win_sa_32bit.exe ' + self.file_path
        proc = subprocess.Popen(solu_cmd)
        t = threading.Timer(30, self.kill_process, [proc])
        t.start()
        t.join()
        if self.dumpTimeout is True:
            DumpFlag = False
            for f in os.listdir(sys.path[0]):
                if f.startswith('dumped_flash'):
                    DumpFlag = True
                    break
            if DumpFlag is False:
                print curr_time(), 'dump timeout,give up dumping'
                return []
        embedded_list = []
        file_path_without_ext, ext = os.path.splitext(file_path)
        prefix_path, file_name = os.path.split(file_path_without_ext)
        embedded_count = 0
        for f in os.listdir(self.root_path):
            if f.startswith('dumped_flash'):
                new_name = file_name + '_%s' % embedded_count  # xxx_0
                os.rename(f, new_name)
                embedded_list.append(os.path.join(self.root_path, new_name))
                embedded_count += 1
        if embedded_count == 0:
            print curr_time(), 'no need to dump'
        else:
            print curr_time(), 'dump dembedded flash', embedded_list
        return embedded_list

    def kill_process(self, proc):
        if proc.poll() is None:
            print curr_time(), '[WARN] process taking too long to complete - kill'
            for child in psutil.Process(proc.pid).children(recursive=True):
                child.kill()
            proc.kill()
            self.dumpTimeout = True


def print_help():
    print """
Usage:
    python unpack_helper.py target

Unpack flash file by solu
    """


def main():
    if len(sys.argv) != 2:
        print_help()
        exit(0)
    if not os.path.exists(sys.argv[1]):
        print 'target file not exists'
        exit(0)
    helper = FlashUnpackHelper()
    helper.set_file_path(sys.argv[1])
    helper.dump_flash()


if __name__ == '__main__':
    main()
