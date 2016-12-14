# usage : python get_local_script.py src_folder_path
import os
import sys
import re


def get_local_script(src_folder_path):
    folder_path = src_folder_path
    if not os.path.exists(folder_path):
        print "srcfolder don't exist"
        exit(0)
    js_tag = '<evidence type="javascript"'
    with open('local_script.txt', 'w') as local_list:
        for f in os.listdir(folder_path):
            if f.endswith('.xml'):
                la = 0
                f_path = os.path.join(folder_path, f)
                with open(f_path, 'r') as file:
                    s = file.read()

                    # extract filename
                    i1 = s.find('<file_path>') + len('<file_path>')
                    i2 = s.find('</file_path>')

                    file_path, file_name = os.path.split(s[i1:i2])
                    # xml structure error
                    if s.count(js_tag) < 3:
                        print 'xml structure error:\t', f
                        continue

                    # step over the first two pairs js tag
                    tag_len = len(js_tag)
                    i1 = s.find(js_tag) + tag_len
                    i2 = s.find(js_tag, i1) + tag_len
                    index = s.find(js_tag, i2) + tag_len
                    s = s[index:].lower()

                    if s.find(r'/*@cc_on') != -1:
                        local_list.write(file_name + '\n')
                        local_list.flush()
                        continue

                    if s.find('wscript.shell') != -1:
                        la = 1
                    elif s.find('shell.application') != -1:
                        la = 1
                    elif s.find('scripting.filesystemobject') != -1:
                        la = 1
                    else:
                        la = 0

                    if la == 0:
                        continue

                    re_win = re.findall('\\bwindow\.[a-z0-9]+', s)
                    flag = 0
                    if re_win:
                        for item in re_win:
                            if item != 'window.eval':
                                flag = 1
                                break
                    if flag == 1:
                        continue

                    re_doc = re.findall('\\bdocument\.[a-z0-9]+', s)
                    if re_doc:
                        continue

                    if s.find('getElementsByTagName') != -1:
                        continue
                    if s.find('getElementById') != -1:
                        continue
                    if s.find('<div') != -1:
                        continue
                    if s.find('\\bconsole\.') != -1:
                        continue
                    if s.find('parentNode') != -1:
                        continue

                    re_win = re.findall('\\bwindow\[[a-z0-9]+\]', s)
                    flag = 0
                    if re_win:
                        for item in re_win:
                            if item != 'window[eval]':
                                flag = 1
                                break
                    if flag == 1:
                        continue

                    re_doc = re.findall('\\bdocument\[[a-z0-9]+\]', s)
                    if re_doc:
                        continue
                    if re.search('\s\$\.', s) is not None:
                        continue
                local_list.write(file_name + '\n')
                local_list.flush()


def print_help():
    print """
Usage:
  python get_local_script.py src_folder_path

Get local script list from the folder of behavior
    """


def main():
    if len(sys.argv) != 2:
        print_help()
        exit(0)

    get_local_script(sys.argv[1])


if __name__ == '__main__':
    main()
