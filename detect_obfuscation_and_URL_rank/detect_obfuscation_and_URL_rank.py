import os,sys
import csv
import url_rank
import xml.etree.cElementTree as ET
    

# analysis all .xml in sys.argv[1]
# judge JS confusion and urls order
def analysis_xml_csv():
    csvfile=file('analysis_log.csv','wb')
    writer=csv.writer(csvfile)
    writer.writerow(['sample-path','obfuscation','URL','rank','SA_decision'])
    for f in os.listdir(folder_path):
        if 'xml' in os.path.splitext(f)[1]:
            # try:
            file_path=os.path.join(folder_path,f)
            tree=ET.parse(file_path)
            root = tree.getroot()

            evidence=root[-1]

            #if evidence.attrib.has_key('matched') and evidence[-1].tag=='content':
            if evidence[-1].tag=='content':
                    content=evidence[-1].text
                    line_list=content.split('\n')
                    #judge JS confusion
                    if line_list[1][:20].find('window.eval')!=-1:
                        ob='yes'
                    else:
                        ob='no'
                    #judge url
                    cur_no=0
                    cur_url=''
                    for line in line_list[2:]:
                        if line.find(' URL =')!=-1:
                            start=line.find(' URL =')+7
                            if line[start:start+4]=='http':
                                start=start+7              #pass http://
                                end=line.find('/',start)     
                                if end ==-1:
                                    end=line.find('\"',start)
                            else:           #other url
                                end=line.find('\"',start)
                            url=line[start:end]
                            no=url_rank.analysis_url(url)
                            if no>cur_no:
                                cur_no=no
                                cur_url=url
                    if cur_no!=0:
                        writer.writerow([root[0].text,ob,cur_url,str(cur_no),root[4].text])
                    else:
                        writer.writerow([root[0].text,ob,'','',root[4].text])
            else:
                return "the last one child isn't aimed element,script is uncorrect"
            # except:
            #     print "Exception exists!"
    csvfile.close()


if __name__=='__main__':
    if len(sys.argv)!=2:
        print """
    Usage:
        python tool.py input_dir
        """
    else:
        folder_path=sys.argv[1]
        if not os.path.exists(folder_path):
            print 'folder not exists'
            exit(0)

    analysis_xml_csv()