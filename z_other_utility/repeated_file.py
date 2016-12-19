 # Author: Feihao Chen
 # Date: 2016/12/19
import os,sys

def repeated_file(dir_1,dir_2):
    log_name=dir_1.split('\\')[-1]+'&'+dir_2.split('\\')[-1]+'.log'
    sys.stdout=open(log_name,'w')

    file_list=[]
    for f in os.listdir(dir_1):
        file_list.append(f)

    count=0
    for f in os.listdir(dir_2):
        if f in file_list:
            file_path = os.path.join(dir_2, f)
            print f
            # os.remove(file_path)
            count+=1

    print '\ntotal repeated:',str(count)

def print_usage():
    print """
Usage:
    python repeated_file.py dir_1 dir_2

To list out the repeated file in two different folders.
    """


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        exit(-1)

    dir_1=sys.argv[1]
    dir_2=sys.argv[2]

    repeated_file(dir_1,dir_2)
    