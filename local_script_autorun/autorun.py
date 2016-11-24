 # Author: Feihao Chen
 # Date: 2016/11/21

import sys,os,shutil
import subprocess
import local_script_feature,local_list

def print_usage():
    print """
Usage:
    python autorun.py srcfolder_path
    """

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        exit(-1)

    srcfolder_path=sys.argv[1]
    with open('SAL.log', 'w') as fout:
        subprocess.check_call('salineup_for_script_malware\SALineup.exe --productname=sc \
        --script-malware=true --loglevel=all \"'+srcfolder_path, stdout=fout)

    result_dir=os.path.join('salineup_for_script_malware','result')
    # form a CSV file to display the characters
    local_script_feature.parse_behavior(result_dir)

    # list the sha1 of local scripts in local_list.txt
    local_list.local_list(result_dir)