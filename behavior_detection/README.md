vt_public.py
# python vt_public.py sha1s.txt
在VT中搜索.txt中所有文件名（一行一个），提取返回的部分检测数据（认为是Malicious的比例，Sophos、Kaspersky、ESET-NOD32、Microsoft四家厂商的判定结果），写入同路径下report.csv
* 受public API限制，一分钟只能发送4次请求，若需要处理大量文件，可考虑申请多个账户，使用多个public API轮流发送请求，或申请private API


anaylsis_xml.py
# python anaylsis_xml.py D:\xml_floder
分析SALineup生成的xml报告，输入参数为报告文件夹路径，脚本会分析文件夹下所有xml，生成一个包含sample路径、是否存在JS混淆以及所有访问URL及排名的csv


dir.py
# python dir.py floder_path  file_path
将指定文件夹下所有文件名 输出到 指定文件中


top-1m.csv  
100W条url及排名

