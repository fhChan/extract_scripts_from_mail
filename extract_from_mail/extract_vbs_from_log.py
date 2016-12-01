 # Author: Feihao Chen
 # Date: 2016/10/24

import sys,os

def extract_vbs_from_log(log_name):
    is_vbs = False
    vbs_count = 0
    with open(log_name) as f_in:
        for line in f_in:
            if line.startswith('VBA MACRO'):
                cur_file_name = line.split('VBA MACRO')[-1].strip()
            if line.startswith('- - - - - - -'):
                vbs_count += 1
                portion = os.path.splitext(log_name)
                new_dir=portion[0]
                if not os.path.exists(new_dir):
    	            os.makedirs(new_dir)
                f_out = open(new_dir + '\\' + cur_file_name, 'w')
                is_vbs = True
                continue
            if line.startswith('-------')or line.startswith('+------'):
                is_vbs = False
                try:
                    f_out.close()
                except:
                    pass
            if is_vbs:
                f_out.write(line)

def print_usage():
    print """
Usage:
    python extract_vbs_from_log.py log_name
    """

def main():
    if len(sys.argv) != 2:
        print_usage()
        exit(-1)

    extract_vbs_from_log(sys.argv[1])

if __name__ == '__main__':
    main()