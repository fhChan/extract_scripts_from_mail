import os, sys, shutil, hashlib

def calc_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def unique_files(input_folder, output_folder):
    if not os.path.exists(input_folder):
        print "[ERROR] cannot find input folder, " + input_folder
        return
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    unique_map = {}
    for root, dirs, files in os.walk(input_folder):
        for name in files:
            md5_val = calc_md5(os.path.join(root, name))
            unique_map[md5_val] = os.path.join(root, name)

    for key in unique_map.keys():
        src_file = unique_map[key]
        target_file = os.path.join(output_folder, src_file.replace(input_folder, '').strip('\\'))
        target_dir, filename = os.path.split(target_file)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copy2(src_file, target_dir)


def print_usage():
    print """
Usage:
    python unique_files.py input_dir output_dir
    """

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        exit(-1)
    unique_files(sys.argv[1], sys.argv[2])