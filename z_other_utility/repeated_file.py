 # Author: Feihao Chen
 # Date: 2016/12/19
import os,sys
import hashlib

def calc_sha1(filepath):
    with open(filepath,'rb') as f:
        sha1obj = hashlib.sha1()
        sha1obj.update(f.read())
        hash = sha1obj.hexdigest()
        return hash

def main(dest_dir):
    list_file='unique_sha1_list.txt'
    sha1_list=[]
    if not os.path.exists(list_file):
        file=open(list_file,'wb')
        file.write('')
        file.close()
    else:
        file=open(list_file,'rb')
        for line in file:
            sha1_list.append(line.strip())

    remove_log=[]
    sha1_to_append=[]
    COUNT=0
    for root, dirs, files in os.walk(dest_dir):
        for f in files:
            COUNT+=1
            print COUNT
            filename=os.path.join(root,f)
            cur_sha1=calc_sha1(filename)
            if cur_sha1 in sha1_list:
                remove_log.append('REMOVE: ' + str(cur_sha1) +' PATH: ' + os.path.join(root,f))
                # os.remove(os.path.join(root,f))
            else:
                sha1_to_append.append(f)
                os.rename(filename,os.path.join(root,calc_sha1(filename)))

    with open('remove.log','w') as log:
        for line in remove_log:
            log.write(line+'\n')
    with open(list_file,'ab') as file:
        for sha1 in sha1_to_append:
            file.write(sha1+'\n')

def print_usage():
    print """
Usage:
    python repeated_file.py dest_dir
    """


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        exit(-1)

    dest_dir=sys.argv[1]

    main(dest_dir)
    