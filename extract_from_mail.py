import os, sys, re
import base64

dest_dir = './'
processd_file_count = 0
saved_file_count = 0


def process_section(info, dest_dir):
    global saved_file_count
    # print info
    re_matched_attachment_filename = re.compile(r'name=[\"\']?([^\"\'\r\n]*)[\"\']?')
    matched_attachment_filename_list = re.findall(re_matched_attachment_filename, info)
    if len(matched_attachment_filename_list) >= 1:

        filename = matched_attachment_filename_list[0]
        # print 'filename = ' + filename
        filename = filename.replace('?', '-')
    else:
        print '[ERROR] cannot find filename in content disposition info'
        return
    
    re_matched_encoding = re.compile(r'Content-Transfer-Encoding\s*:\s*(.*)')
    matched_encoding_list = re.findall(re_matched_encoding, info)
    if len(matched_encoding_list) == 1:
        encoding = matched_encoding_list[0]
        # print encoding
    else:
        print "[ERROR] cannot find encoding in content dispositon info"
        return
    
    re_matched_attachment = re.compile(r'(\r?\n){2}([\s\S]*)(\r?\n)')
    matched_attachment_list = re.findall(re_matched_attachment, info)
    # print len(matched_attachment_list)

    if len(matched_attachment_list) == 1:
        attachment_content = matched_attachment_list[0][1]
    else:
        print "[ERROR] cannot find attachment content in content dispositon info"
        return
    
    if encoding.lower() == 'base64':
        dest_file = os.path.join(dest_dir, filename)
        if os.path.exists(dest_file):
            print "[WARN] find exist file, name = " + dest_file
        with open(dest_file, 'wb') as output:
            output.write(base64.b64decode(attachment_content.replace('\n', '')))
            print "[INFO] save file into: " + dest_file
            saved_file_count+=1
    else:
        print "[ERROR] unsupported encoding type: " + encoding


def extract_from_mail(mail_path, dest_dir):
    if not os.path.exists(mail_path):
        print "[ERROR] Cannot find mail path, " + mail_path
        return
    print "Now process " + mail_path
    global processd_file_count
    processd_file_count+=1

    boundary = ''
    find_boundary = False
    with open(mail_path, 'r') as fh:
        content = fh.read()
        # print content

        if 'Content-Disposition' in content:
            re_boundary_sig = re.compile(r'(\r?\n|--)\r?\n--(.*)\r?\n[\s\S]{0,500}Content-Disposition')
        else:
            re_boundary_sig = re.compile(r'(\r?\n|--)\r?\n--(.*)\r?\n[\s\S]{0,500}Content-Transfer-Encoding')
        matched_boundary_sig_list = re.findall(re_boundary_sig, content)
        if len(matched_boundary_sig_list) >= 1:
            boundary_sig = matched_boundary_sig_list[0][1]
            print "[INFO] find boundary signature: " + boundary_sig
        else:
            print "[ERROR] cannot find boundary signature"
            return

        re_matched_boundary = re.compile(r'boundary=[\"\']?([^\'\"\r\n]*)[\"\']?', re.DOTALL)
        matched_boundary_list = re.findall(re_matched_boundary, content)
        if len(matched_boundary_list) >= 1:
            #print matched_boundary_list
            boundary = matched_boundary_list[0]

            if boundary_sig in matched_boundary_list:
                boundary = boundary_sig
            else:
                print "[WARN] cannot find boundary signature in matched boundary list"
            
            print "[INFO] find boundary: " + boundary
        else:
            print "[ERROR] cannot find boundary!"
            return

        re_section_info = re.compile(r'--'+boundary+r'\r?\n(.*)--'+boundary+r'\r?\n(.*)--'+boundary+r'--', re.DOTALL)
        matched_section_info = re.findall(re_section_info, content)
        if len(matched_section_info) == 0:
            print "[ERROR] cannot match section info"
            return

        print "matched_section_info:"
        print matched_section_info
        for info in matched_section_info[0]:
            print info
            if "Content-Disposition" in info and 'Content-Transfer-Encoding' in info:
                print "[INFO] find Content-Disposition and Content-Transfer-Encoding"
                process_section(info, dest_dir)
            elif len(info) > 10000:
                print "[INFO] length of info > 10000"
                process_section(info, dest_dir)
            else:
                print "[ERROR] cannot find target section in mail"

def process_single_mail(file_path, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    extract_from_mail(file_path, dest_dir)

def process_multiple_mail(folder_path, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            extract_from_mail(os.path.join(root,name), dest_dir)

def print_usage():
    print """
Usage:
    python extract_from_mail.py --[file|dir] input_path output_path
    """

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print_usage()
        exit(-1)
    if 'file' in sys.argv[1]:
        process_single_mail(sys.argv[2], sys.argv[3])
    elif 'dir' in sys.argv[1]:
        process_multiple_mail(sys.argv[2], sys.argv[3])
    else:
        print "Unsupported argument!"

    print "\n\n*************************************"
    print "Processd file count: " + str(processd_file_count)
    print "Saved file count: " + str(saved_file_count)
