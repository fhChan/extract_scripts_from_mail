 # Author: Feihao Chen
 # Date: 2016/11/21

import sys,os,shutil
import subprocess

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

    # form a CSV file to display the characters
    os.system('python parse_behavior.py '+'salineup_for_script_malware\\result')

    # list the sha1 of local scripts in local_list.txt
    os.system('python local_list.py '+'salineup_for_script_malware\\result')