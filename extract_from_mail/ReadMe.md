extract_from_mail_autorun
===============

[extract_from_mail_autorun] is a automatic tool to extract malware files from emails.
A portion of files attached to emails may contain scripts such as js,wsf,vbs and so on.[extract_from_mail_autorun] 
can extract them into different directories by their typies.In addition,the analysis of .js and .wsf files is 
included.All the analysis can be found in the directoriy 'logs'.

In the directory:
-------------------------
- [salineup_for_script_malware]:to analyse .js and .wsf files extracted and generate a report.
- [oletools]:An open-sourced tool to analyze [Microsoft OLE2 files].See [http://www.decalage.info/python/oletools](http://www.decalage.info/python/oletools) for more info.
- [autorun.py]:The main function of this tool.
- [extract_from_mail.py]:to extract attachments in their original format.
- [unzip_classify.py]:to unzip the packages extracted.
- [extract_vbs_from_log.py]:to extract vbscripts from logs since oletools put them here.

News
----
- 2016-10-31:implement the antorun.py by gathering the codes and modifying from elder versions

Usage:
------
print "python autorun.py input_dir output_dir" in command window

Note:"input_dir" should contain emails in .eml format.
You need to assign an output_dir for saving results and logs.