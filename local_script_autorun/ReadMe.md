local_script_autorun
===============
Please empty the directory 'salineup_for_script_malware\\result' or drag it out each time you use this tool!!!

[local_script_autorun] is a automatic tool to detect whether a script file is based on local environment.

In the directory:
-------------------------
- [salineup_for_script_malware]:to analyse .js and .wsf files extracted and generate a report.
- [autorun.py]:The main function of this tool.
- [local_script_feature.py]:to form a CSV file to display the features.
- [local_list.py]:to list the sha1 of local scripts into local_list.txt.

News
----
- 2016-11-21:implement the local_script.py v1.0

Usage:
------
print "python autorun.py srcfolder_path" in command window

Note:"srcfolder_path" should contain script files.