import os,sys
import xml.etree.cElementTree as ET

if len(sys.argv)!=2:
	print """
Usage:
    python stat_new.py input_dir
    """
else:
	folder_path=sys.argv[1]
	if not os.path.exists(folder_path):
		print 'folder not exists'
		exit(0)	

# analysis all .xml in sys.argv[1]
# judge JS confusion and urls order
def analysis_xml_csv():
	file=open('analysis_log1.csv','w')
	file.write("sample-path,obfuscation,URL,rank,SA_decision\n")
	no_url_list=[]
	for f in os.listdir(folder_path):
		if f[-4:]=='.xml':
			try:
				log=''
				file_path=os.path.join(folder_path,f)
				tree=ET.parse(file_path)
				root = tree.getroot()
				log=log+root[0].text

				SALineup_decision=root[4].text

				evidence=root[-1]

				#if evidence.attrib.has_key('matched') and evidence[-1].tag=='content':
				if evidence[-1].tag=='content':
						content=evidence[-1].text
						line_list=content.split('\n')
						#judge JS confusion
						if line_list[1][:20].find('window.eval')!=-1:
							log=log+',yes'
						else:
							log=log+',no'
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
								no=analysis_url(url)
								if no>cur_no:
									cur_no=no
									cur_url=url
						if cur_no!=0:
							file.write(log+','+cur_url+','+str(cur_no)+','+SALineup_decision+'\n')
						else:
							no_url_list.append(log)
				else:
					return "the last one child isn't aimed element,script is uncorrect"
			except Exception:
				print "Exception exists!"
	file.close()
	file1=open('no_url_list.csv','w')
	file1.write("sample-path,obfuscation\n")
	for ele in no_url_list:
		file1.write(ele+'\n')
	file1.close()


def analysis_url(_url):
	flag=0
	#db_path=os.path.join(db_folder_path,'top-1m.csv')
	db_path=os.path.join(sys.path[0],'top-1m.csv')
	if not os.path.exists(db_path):
		return -1
	for line in open(db_path,'r'):
		no,url=line.split(",")
		if _url.find(url[:-1])!=-1:
			break
	return int(no)


def main():
	analysis_xml_csv()

if __name__=='__main__':
	main()