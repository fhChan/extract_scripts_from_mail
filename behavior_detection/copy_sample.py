# auther = Cheng(SA)
import os
import sys
import shutil


def copy_sample(name_list, src_folder, des_folder):
    count = 0
    with open(name_list, "r") as f:
        for line in f:
            count += 1
            print count
            if line[-1] == '\n':
                name = line[:-1]
            if os.path.exists(os.path.join(src_folder, name)):
                f_path = os.path.join(src_folder, name)
                shutil.copyfile(f_path, os.path.join(des_folder, name))
            else:
                print '[ERROR] %s donnot exists in %s ' % (name, src_folder)


def main():
    if len(sys.argv) != 4:
        print """
Usage:
    python copy_sample.py sha1s.txt src_folder des_folder

copy sample in sha1s.txt from src_folder to des_folder
    """
        exit(0)
    if not os.path.exists(sys.argv[1]):
        print "name_list don't exists"
        exit(0)
    if not os.path.exists(sys.argv[2]):
        print "src_folder don't exists"
        exit(0)
    if not os.path.exists(sys.argv[3]):
        print "des_folder don't exists"
        exit(0)
    copy_sample(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == '__main__':
    main()
