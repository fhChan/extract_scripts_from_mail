 # Author: Feihao Chen
 # Date: 2016/10/24

import sys,os

is_vbs = False
vbs_count = 0
with open(sys.argv[1]) as f_in:
    for line in f_in:
        if line.startswith('VBA MACRO'):
            cur_file_name = line.split('VBA MACRO')[-1].strip()
        if line.startswith('- - - - - - -'):
            vbs_count += 1
            portion = os.path.splitext(sys.argv[1])
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
