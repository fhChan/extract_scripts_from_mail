# usage : python parse_behavior.py srcfolder_path
import os,sys,re

def parse_behavior(srcfolder_path):
	folder_path=srcfolder_path
	count=0
	if not os.path.exists(folder_path):
		print "srcfolder don't exist"
		exit(0)
	report=open('new_report.csv','w')
	report.write('name,decision,rules,wscript.shell,shell.application,scripting.filesystem,window.xxx,document.xxx,xmlhttp,\
adodb.stream,getElementsByTagName,getElementById,<div,console,parentNode,window[xxx],document[xxx],$.\n')
	js_tag='<evidence type="javascript"'
	set1=set()
	for f in os.listdir(folder_path):
		if f[-4:]=='.xml':
			count+=1
			print count

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
			log=js_name+','

			# extract decision
			i1=s.find('<decision>')+10
			i2=s.find('</decision>')
			dec=s[i1:i2]
			log+=dec+','

			# extract rules
			i1=s.find('<matched_rules>')
			i2=s.find('</matched_rules>')
			rules=s[i1:i2]
			i1=rules.find('<rule>')
			while i1 != -1:
				i2=rules.find('</rule>',i1)
				set1.add(rules[i1+6:i2])
				i1=rules.find('<rule>',i2)
		 	for i in set1:
		 		log+=i+';'
		 	set1.clear()
		 	if log[-1]==';':
		 		log=log[:-1]
			log+=','

			# xml stru error
			if s.count(js_tag)<3:
				print 'xml stru error:\t',f
				continue

			# step over the first two pairs js tag
			i1=s.find(js_tag)+20
			i2=s.find(js_tag,i1)+20
			index=s.find(js_tag,i2)
			s=s[index+20:].lower()

			if s.find('wscript.shell')>-1:
				log+='T'
			log+=','
			if s.find('shell.application')>-1:
				log+='T'
			log+=','
			if s.find('scripting.filesystemobject')>-1:
				log+='T'
			log+=','

			re_win=re.findall('\\bwindow\.[a-z0-9]+',s)
			if re_win:
			 	for item in re_win:
			 		set1.add(item)
			 	for i in set1:
			 		log+=i+';'
			 	set1.clear()
			 	if log[-1]==';':
			 		log=log[:-1]
			log+=','

			re_doc=re.findall('\\bdocument\.[a-z0-9]+',s)
			if re_doc:
			 	for item in re_doc:
			 		set1.add(item)
			 	for i in set1:
			 		log+=i+';'
			 	set1.clear()
			 	if log[-1]==';':
			 		log=log[:-1]
			log+=','

			if s.find('xmlhttp')>-1:
				log+='T'
			log+=',' 
			if s.find('adodb.stream')>-1:
			 	log+='T'
			log+=','  

			if s.find('getElementsByTagName')>-1:
				log+='T'
			log+=',' 
			if s.find('getElementById')>-1:
				log+='T'
			log+=',' 
			if s.find('<div')>-1:
				log+='T'
			log+=',' 
			if s.find('\\bconsole\.')>-1:
				log+='T'
			log+=',' 
			if s.find('parentNode')>-1:
				log+='T'
			log+=',' 
			
			re_win=re.findall('\\bwindow\[[a-z0-9]+\]',s)
			if re_win:
			 	for item in re_win:
			 		set1.add(item)
			 	for i in set1:
			 		log+=i+';'
			 	set1.clear()
			 	if log[-1]==';':
			 		log=log[:-1]
			log+=','

			re_doc=re.findall('\\bdocument\[[a-z0-9]+\]',s)
			if re_doc:
			 	for item in re_doc:
			 		set1.add(item)
			 	for i in set1:
			 		log+=i+';'
			 	set1.clear()
			 	if log[-1]==';':
			 		log=log[:-1]
			log+=',' 
			if re.search('\s\$\.',s)!=None:
				log+='T'

			file.close()
			report.write(log+'\n')
			report.flush()
	report.close()


def main():
	if len(sys.argv)!=2:
		print 'python parse_behavior.py srcfolder_path'
		exit(0)

	parse_behavior(sys.argv[1])

if __name__=='__main__':
	main()
