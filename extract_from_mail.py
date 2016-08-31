import os, sys, re
import base64

dest_dir = './'

def extract_from_mail(mail_path, dest_dir):
    if not os.path.exists(mail_path):
        print "[ERROR] Cannot find mail path, " + mail_path
        return
    print "Now process " + mail_path

    boundary = ''
    find_boundary = False
    with open(mail_path) as fh:
        content = fh.read()
        re_matched_boundary = re.compile(r'boundary=[\"\']?(.*?)[\"\']?', re.DOTALL)
        matched_boundary_list = re.findall(re_matched_boundary, content)
        if len(matched_boundary_list) >= 1:
            boundary = matched_boundary_list[0]
            #print "[INFO] find boundary: " + boundary
        else:
            print "[ERROR] cannot find boundary!"
            return
        re_matched_attachment_info = re.compile(r'Content-Type: (.*?)\nContent-Transfer-Encoding: (.*?)\nContent-Disposition: (.*?)\n\n([\s\S]*)?\n--' + boundary)
        matched_attachment_info_list = re.findall(re_matched_attachment_info, content)
        if len(matched_attachment_info_list) == 1 and len(matched_attachment_info_list[0]) == 4:
            content_type = matched_attachment_info_list[0][0]
            content_transfer_encoding = matched_attachment_info_list[0][1]
            content_disposition = matched_attachment_info_list[0][2]
            attachment_content = matched_attachment_info_list[0][3]
            #print content_type
            #print content_transfer_encoding
            #print content_disposition
            #print attachment_content

            if content_type.find('application/x-zip-compressed'):
                pass

            re_matched_attachment_filename = re.compile(r'filename=\"(.*?)\"')
            matched_attachment_filename_list = re.findall(re_matched_attachment_filename, content_disposition)
            if len(matched_attachment_filename_list) == 1:
                filename = matched_attachment_filename_list[0]
            else:
                print '[ERROR] cannot find filename in content disposition'
                return
            
            if content_transfer_encoding == 'base64':
                with open(os.path.join(dest_dir, filename), 'wb') as output:
                    output.write(base64.b64decode(attachment_content.replace('\n', '')), )
            else:
                print "[ERROR] unsupported encoding type: " + content_transfer_encoding

def process_multiple_mail(folder_path, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for root, dirs, files in os.walk(folder_path):
        for name in files:
            extract_from_mail(os.path.join(root,name), dest_dir)

if __name__ == '__main__':
    process_multiple_mail(sys.argv[1], sys.argv[2])
