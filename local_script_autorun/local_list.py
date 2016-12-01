# usage : python local_list.py srcfolder_path
import os,sys,re

def local_list(srcfolder_path):
    folder_path=srcfolder_path
    count=0
    if not os.path.exists(folder_path):
        print "srcfolder don't exist"
        exit(0)
    l_list=open('local_list.txt','w')
    js_tag='<evidence type="javascript"'
    set1=set()
    for f in os.listdir(folder_path):
        if f[-4:]=='.xml':
            la=0
            f_path=os.path.join(folder_path,f)
            file=open(f_path,'r')
            s=file.read()

            # extract filename
            i1=s.find('<file_path>')
            i2=s.find('</file_path>')
            l=s[i1:i2].split('\\')
            if len(l)>1:
                js_name=l[-1]  #xx.js
            else:
                print 'file path error:\t',f
                exit(0)

            # xml stru error
            if s.count(js_tag)<3:
                print 'xml stru error:\t',f
                continue

            # step over the first two pairs js tag
            i1=s.find(js_tag)+20
            i2=s.find(js_tag,i1)+20
            index=s.find(js_tag,i2)
            s=s[index+20:].lower()

            if r'/*@cc_on' in s:
                la=1
            elif 'wscript.shell' in s:
                la=1
            elif 'shell.application' in s:
                la=1
            elif 'scripting.filesystemobject' in s:
                la=1
            else:
                la=0

            if la==0:
                continue

            re_win=re.findall('\\bwindow\.[a-z0-9]+',s)
            flag=0
            if re_win:
                 for item in re_win:
                     if item!='window.eval':
                         flag=1
                         break
            if flag==1:
                continue

            re_doc=re.findall('\\bdocument\.[a-z0-9]+',s)
            if re_doc:
                 continue

            if s.find('getElementsByTagName')>-1:
                continue
            if s.find('getElementById')>-1:
                continue 
            if s.find('<div')>-1:
                continue
            if s.find('\\bconsole\.')>-1:
                continue
            if s.find('parentNode')>-1:
                continue
            
            re_win=re.findall('\\bwindow\[[a-z0-9]+\]',s)
            flag=0
            if re_win:
                 for item in re_win:
                     if item!='window[eval]':
                         flag=1
                         break
            if flag==1:
                continue

            re_doc=re.findall('\\bdocument\[[a-z0-9]+\]',s)
            if re_doc:
                continue
            if re.search('\s\$\.',s)!=None:
                continue

            file.close()
            l_list.write(js_name+'\n')
            l_list.flush()
    l_list.close()


def main():
    if len(sys.argv)!=2:
        print 'python local_list.py srcfolder_path'
        exit(0)

    local_list(sys.argv[1])

if __name__=='__main__':
    main()
