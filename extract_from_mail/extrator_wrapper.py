import os, sys, shutil
from extract_from_mail import *


def process(input_dir, output_dir):
    if not os.path.exists(input_dir):
        print "[ERROR] cannot find " + input_dir
        return
    # if os.path.exists(output_dir):
    #     shutil.rmtree(output_dir)
    # os.makedirs(output_dir)

    for root, dirs, files in os.walk(input_dir):
        for name in dirs:
            cur_dir = os.path.join(root, name)
            target_dir = os.path.join(output_dir, cur_dir.replace(input_dir, '').strip('\\'))
            #print target_dir
            mail_extractor = MailExtactor()
            mail_extractor.set_dest_dir(target_dir)
            mail_extractor.process_multiple_mail(cur_dir)

def print_usage():
    print """
Usage:
    python extractor_wrapper.py input_dir_path output_dir_path
    """

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        exit(-1)
    process(sys.argv[1], sys.argv[2])