

import json, urllib, urllib2,hashlib, re, sys, time,os

if len(sys.argv)!=2:
  print 'python vt_public.py sha1s.txt'
  exit(0)
else:
  if not os.path.exists(sys.argv[1]):
    print "file don't exists"
    exit(0)

class vtAPI():
    def __init__(self):
        self.api = '835e016eefcb38be48a7dcb2723b2da0f6fa8b59fc22a38c633f986888b44215'  #public api
        self.base = 'https://www.virustotal.com/vtapi/v2/'
    
#   File "vt_public.py", line 20, in getReport
#     jdata =  json.loads(result.read())
#   File "C:\Python27\lib\json\__init__.py", line 310, in loads
#     return _default_decoder.decode(s)
#   File "C:\Python27\lib\json\decoder.py", line 346, in decode
#     obj, end = self.raw_decode(s, idx=_w(s, 0).end())
#   File "C:\Python27\lib\json\decoder.py", line 364, in raw_decode
#     raise ValueError("No JSON object could be decoded")
#   ValueError: No JSON object could be decoded
    def getReport(self,md5):
        param = {'resource':md5,'apikey':self.api}
        url = self.base + "file/report"
        data = urllib.urlencode(param)
        result = urllib2.urlopen(url,data)
        jdata =  json.loads(result.read())##
        return jdata

# Md5 Function
def checkMD5(checkval):
  if re.match(r"([a-fA-F\d]{32})", checkval) == None:
    md5 = md5sum(checkval)
    return md5.upper()
  else: 
    return checkval.upper()

def md5sum(filename):
  fh = open(filename, 'rb')
  m = hashlib.md5()
  while True:
      data = fh.read(8192)
      if not data:
          break
      m.update(data)
  return m.hexdigest() 

def parse(it, md5):
  if it['response_code'] == 0:
    print md5 + " -- Not Found in VT"
    return ',,,,'
  log=str(it['positives'])+'/'+str(it['total'])+','
  if 'Sophos' in it['scans']:
    log+=str(it['scans']['Sophos']['result'])+','
  if 'Kaspersky' in it['scans']:
    log+=str(it['scans']['Kaspersky']['result'])+','
  if 'ESET-NOD32' in it['scans']:
    log+=str(it['scans']['ESET-NOD32']['result'])+','
  if 'Microsoft' in it['scans']:
    log+=str(it['scans']['Microsoft']['result'])
  return log
  

def main():

  sha1=open(sys.argv[1],'r')
  report=open('report.csv','w')
  report.write('SHA1,Detected by,Sophos,Kaspersky,ESET-NOD32,Microsoft\n')
  vt=vtAPI()
  for line in sha1:
    log=line[:-1]+','   # remove '\n'
    md5=checkMD5(line[:-1])   
    print 'start anaylsis %s'%line[:-1]
    try:
      log+=parse(vt.getReport(md5), md5)
    except ValueError as e:
      print 'more than 4r/min,20s later try to reparse'
      time.sleep(20)
      log+=parse(vt.getReport(md5), md5)
    report.write(log+'\n')
    report.flush()
    time.sleep(14)
  report.close()

if __name__ == '__main__':
    main()
