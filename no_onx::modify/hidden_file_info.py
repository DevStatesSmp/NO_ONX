import os
import stat
import mimetypes
import hashlib
import logging
from datetime import datetime

logging.basicConfig(filename='hidden_file_info.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def is_hidden(filepath):

    name = os.path.basename(filepath)
    if name.startswith('.'):
        return True
    return not os.access(filepath, os.R_OK)

def file_info(filepath):
    try:
        statinfo = os.lstat(filepath)
        if stat.S_ISDIR(statinfo.st_mode): 
            return {"error": f"'{filepath}' is a directory, not a file."}

        mime, _ = mimetypes.guess_type(filepath)
        with open(filepath, 'rb') as f:
            data = f.read(4096)
            hash_val = hashlib.sha256(data).hexdigest()
        
        file_info_dict = {
            "size": statinfo.st_size,
            "type": mime,
            "uid": statinfo.st_uid,
            "gid": statinfo.st_gid,
            "mode": stat.filemode(statinfo.st_mode),
            "hash": hash_val,
            "mtime": datetime.fromtimestamp(statinfo.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "atime": datetime.fromtimestamp(statinfo.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            "ctime": datetime.fromtimestamp(statinfo.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        }
        return file_info_dict
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def scan_hidden(path):
    hidden_count = 0
    for root, dirs, files in os.walk(path):
        for name in files + dirs:
            fullpath = os.path.join(root, name)
            if is_hidden(fullpath):
                hidden_count += 1
                info = file_info(fullpath)
                print(f"[Hidden] {fullpath}")
                for k, v in info.items():
                    print(f"    {k}: {v}")
                print("")
                logging.info(f"[Hidden] {fullpath}")
                for k, v in info.items():
                    logging.info(f"    {k}: {v}")
                logging.info("")  # Thêm một dòng trống để dễ đọc log

    if hidden_count == 0:
        print("No hidden files or directories found.")
    else:
        print(f"Total hidden files and directories found: {hidden_count}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 hidden_file_info.py <target_dir>")
    else:
        scan_hidden(sys.argv[1])


