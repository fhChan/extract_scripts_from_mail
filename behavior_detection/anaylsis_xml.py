# encoding = UTF-8
import os,sys
import xml.etree.cElementTree as ET
import time

if len(sys.argv)<2:
	print 'python anaylsis_xml.py D:\xml_floder'
	exit(0)
else:
	folder_path=sys.argv[1]
	if not os.path.exists(folder_path):
		print 'folder not exists'
		exit(0)	

# analysis all .xml in sys.argv[1]
# judge JS confusion and urls order
def analysis_xml_csv():
	file=open('analysis_log.csv','w')
	file.write("sample-path,obfuscation,URL,rank\n")
	for f in os.listdir(folder_path):
		try:
			if f[-4:]=='.xml':
				log=''
				file_path=os.path.join(folder_path,f)
				print time.ctime(),'	running	',file_path
				tree=ET.parse(file_path)
				root = tree.getroot()
				log=log+root[0].text+','

				SALineup_decision=root[4].text
				#if decision is Undetermined,xml don't have <evidence>
				if root[-1].tag=='evidence':  
					evidence=root[-1]
					malicious_flag=0
					if evidence[-1].tag=='content':
						content=evidence[-1].text
						line_list=content.split('\n')
						#judge JS confusion
						eval_flag=0
						for line in line_list:
							if line[:15].find('window.eval')!=-1:
								eval_flag=1
								break
						if eval_flag==1:
							malicious_flag=1
							log=log+'yes,'
						else:
							log=log+'no,'
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
								no=analysis_url(url)
								file.write(log+url+','+str(no)+'\n')
						file.flush()
					else:
						return "the last one child isn't aimed element,script is uncorrect"
		except ET.ParseError as e:
			pass # encoding error
	file.close()


TP=[] #saline=m , people=m
FP=[] #saline=m , people=n
TN=[] #saline=n , people=n
FN=[] #saline=n , people=m

# analysis all .xml in sys.argv[1]
# judge JS confusion and urls order
def analysis_xml_log():
	file=open('analysis_log','w')
	for f in os.listdir(folder_path):
		try:
			if f[-4:]=='.xml':
				log=[]
				file_path=os.path.join(folder_path,f)
				print 'Start analysis %s' % f
				log.append('Start analysis %s\n' % f)
				tree=ET.parse(file_path)
				root = tree.getroot()
				print 'Sample is %s'%root[0].text
				log.append('Sample is %s\n'%root[0].text)

				SALineup_decision=root[4].text

				evidence=root[-1]
				malicious_flag=0

				#if evidence.attrib.has_key('matched') and evidence[-1].tag=='content':
				if evidence[-1].tag=='content':
					content=evidence[-1].text
					line_list=content.split('\n')
					#judge JS confusion
					eval_flag=0
					for line in line_list:
						if line[:15].find('window.eval')!=-1:
							eval_flag=1
							break
					if eval_flag==1:
						print 'JS confusion'
						malicious_flag=1
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
							flag,no=analysis_url_flag(url)
							if flag in [0,3]:
								malicious_flag=1
							print url,'\t',flag,'\t',no
							log.append(url+'\t'+str(flag)+'\t'+str(no)+'\n')
					print '\n'

					if SALineup_decision=='Malicious' and malicious_flag==1:
						log.append('TP'+'\n')
						TP.append(root[0].text)
					elif SALineup_decision=='Malicious' and malicious_flag==0:
						log.append('FP'+'\n')
						FP.append(root[0].text)
					elif SALineup_decision!='Malicious' and malicious_flag==1:
						log.append('FN'+'\n')
						FN.append(root[0].text)
					elif SALineup_decision!='Malicious' and malicious_flag==0:
						log.append('TN'+'\n')
						TN.append(root[0].text)

					log.append('\n')
					file.writelines(log)
				else:
					return "the last one child isn't aimed element,script is uncorrect"
		except ET.ParseError as e:
			pass
	log=[]
	log.append('\n')
	if len(TP)+len(FP)!=0:
		log.append("TPR = "+str( (len(TP)+0.0) /(len(TP)+len(FP)) )+"\n")
		log.append("FPR = "+str( (len(FP)+0.0) /(len(TP)+len(FP)) )+"\n")
	else:
		log.append("len(TP)+len(FP)=0"+"\n")
	if len(TN)+len(FN)!=0:
		log.append("TNR = "+str( (len(TN)+0.0) /(len(TN)+len(FN)) )+"\n")
		log.append("FNR = "+str( (len(FN)+0.0) /(len(TN)+len(FN)) )+"\n")
	else:
		log.append("len(TN)+len(FN)=0")
	file.writelines(log)
	file.close()



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

# >>> test.analysis_url('360.cn')
# (1, 20)
# 0 means not exists
# 1 means in [:10000]
# 2 means in [:100000]
# 3 means in [:1000000]
# db_folder_path='D:\\'
def analysis_url_flag(_url):
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
	analysis_xml_csv()

if __name__=='__main__':
	main()