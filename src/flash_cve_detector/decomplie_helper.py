import os
import sys
import subprocess


class FfdecHelper:
    def __init__(self):
        self.file_path = ''
        self.result_path = ''
        self.check_env()
        self.clean_env()

    def check_env(self):
        if not os.path.exists('ffdec'):
            print '[ERROR] ffdec not exists in current dir!'
            exit(0)

    def clean_env(self):
        pass

    def set_file_path(self, file_path):
        if not os.path.exists(file_path):
            print '[ERROR] the entered path not exists'
            exit(0)
        self.file_path = file_path

    def set_result_path(self, result_path):
        self.result_path = result_path

    def decomplie(self):
        if self.file_path != '' and self.result_path != '':
            ffdec_cmd = "\"ffdec\%s\" -export script \"%s\" \"%s\"" % ('ffdec.bat', self.result_path, self.file_path)
            proc = subprocess.Popen(ffdec_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.communicate()


def print_help():
    print """
Usage:
    python decomplie_helper.py target_file folder_path

Decomplie flash file by ffdec
    """


def main():
    if not 2 <= len(sys.argv) <= 3:
        print_help()
        exit(0)
    if not os.path.exists(sys.argv[1]):
        print 'target file not exists'
        exit(0)
    helper = FfdecHelper()
    helper.set_file_path(sys.argv[1])
    if len(sys.argv) == 3:
        helper.set_result_path(sys.argv[2])
    else:
        helper.set_result_path('result')
    helper.decomplie()


if __name__ == '__main__':
    main()
