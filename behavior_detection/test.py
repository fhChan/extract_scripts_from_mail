import os,sys
import xml.etree.cElementTree as ET

if len(sys.argv)<2:
	print 'python test.py D:\result  --xml folder'
	exit(0)
else:
	folder_path=sys.argv[1]
	if not os.path.exists(folder_path):
		print 'folder not exists'
		exit(0)	

# analysis all .xml in sys.argv[1]
# judge JS confusion and urls order
def analysis_xml():
	file=open('analysis_log','a+')
	for f in os.listdir(folder_path):
		if f[-4:]=='.xml':
			log=[]
			file_path=os.path.join(folder_path,f)
			print 'Start analysis %s' % f
			log.append('Start analysis %s\n' % f)
			tree=ET.parse(file_path)
			root = tree.getroot()
			print 'Malicious is %s'%root[0].text
			log.append('Malicious is %s\n'%root[0].text)
			evidence=root[-1]
			if evidence.attrib.has_key('matched') and evidence[-1].tag=='content':
				content=evidence[-1].text
				line_list=content.split('\n')
				#judge JS confusion
				if line_list[1][:20].find('window.eval')!=-1:
					print 'JS confusion'
					log.append('JS confusion\n')
				else:
					print 'Not found JS confusion'
					log.append('Not found JS confusion\n')
				#judge url
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
						flag,no=analysis_url(url)
						print url,'\t',flag,'\t',no
						log.append(url+'\t'+str(flag)+'\t'+str(no)+'\n')
				print '\n'
				log.append('\n')
				file.writelines(log)
			else:
				return "the last one child isn't aimed element,script is uncorrect"
	file.close()

# >>> test.analysis_url('360.cn')
# (1, 20)
# 0 means not exists
# 1 means in [:10000]
# 2 means in [:100000]
# 3 means in [:1000000]
# db_folder_path='D:\\'
def analysis_url(_url):
	flag=0
	#db_path=os.path.join(db_folder_path,'top-1m.csv')
	db_path=os.path.join(sys.path[0],'top-1m.csv')
	if not os.path.exists(db_path):
		return -1
	for line in open(db_path,'r'):
		no,url=line.split(",")
		if _url.find(url[:-1])!=-1:
			if int(no)<=10000:
				flag=1
			elif int(no) <=100000:
				flag=2
			else:
				flag=3
			break
	if no=='1000000':
		no=0
	return flag,int(no)


def main():
	analysis_xml()

if __name__=='__main__':
	main()