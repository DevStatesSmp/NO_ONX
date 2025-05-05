# THIS IS MODULE, DO NOT RUN THIS FILE DIRECTLY

import os
import stat
import time
import hashlib
import getpass
import argparse
import platform
import logging
from datetime import datetime
import mimetypes
from tabulate import tabulate
from colorama import init, Fore, Style

init(autoreset=True)

# Optional: only import win32security if on Windows and available
try:
    if platform.system() == "Windows":
        import win32security
except ImportError:
    win32security = None

# set up logging
logging.basicConfig(filename='hidden_file_info.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Define info class with static methods for file operations
class info:
    @staticmethod
    def get_owner(path):
        if platform.system() == "Windows" and win32security:
            try:
                sd = win32security.GetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
                return f"{domain}\\{name}"
            except Exception:
                return getpass.getuser()
        elif platform.system() != "Windows":  # Check if not on Windows
            try:
                import pwd  # Import pwd only if not on Windows
                return pwd.getpwuid(os.stat(path).st_uid).pw_name
            except Exception:
                return getpass.getuser()
        else:
            return getpass.getuser()  # Default to current user on other systems

    @staticmethod
    def file_info(path):
        if not os.path.exists(path):
            print(f"❌ Path not found: {path}")
            return

        try:
            stat_info = os.lstat(path)
            file_type = "Directory" if stat.S_ISDIR(stat_info.st_mode) else \
                        "Symlink" if stat.S_ISLNK(stat_info.st_mode) else \
                        "File"

            print(f"📄 Path: {path}")
            print(f"🔍 Type: {file_type}")
            print(f"📦 Size: {stat_info.st_size} bytes")
            print(f"👤 Owner: {info.get_owner(path)}")
            print(f"🔒 Permissions: {oct(stat_info.st_mode)[-3:]}")
            print(f"🕓 Last modified: {time.ctime(stat_info.st_mtime)}")
            print(f"🕓 Last accessed: {time.ctime(stat_info.st_atime)}")
            print(f"🕓 Created (inode change): {time.ctime(stat_info.st_ctime)}")
        except Exception as e:
            print(f"❌ Error retrieving file info: {e}")

    @staticmethod
    def file_hash(path, algo="sha256"):
        if not os.path.isfile(path):
            print(f"❌ Not a valid file: {path}")
            return

        hash_func = getattr(hashlib, algo.lower(), None)
        if hash_func is None:
            print(f"❌ Unsupported hash algorithm: {algo}")
            return

        try:
            with open(path, "rb") as f:
                hasher = hash_func()
                while chunk := f.read(8192):
                    hasher.update(chunk)
                print(f"🔑 {algo.upper()} hash of {path}: {hasher.hexdigest()}")
        except Exception as e:
            print(f"❌ Error computing hash: {e}")

    @staticmethod
    def symlink_info(path):
        if not os.path.islink(path):
            print(f"❌ Not a symlink: {path}")
            return
        try:
            target = os.readlink(path)
            print(f"🔗 Symlink: {path} -> {target}")
        except Exception as e:
            print(f"❌ Error reading symlink: {e}")

    @staticmethod
    def dir_info(path):
        if not os.path.isdir(path):
            print(f"❌ Not a directory: {path}")
            return
        try:
            print(f"📁 Contents of directory {path}:")
            for item in os.listdir(path):
                full = os.path.join(path, item)
                print(f" - {item} ({'dir' if os.path.isdir(full) else 'file'})")
        except Exception as e:
            print(f"❌ Error listing directory: {e}")

    @staticmethod
    def extended_info(path):
        print("📌 Extended Information\n")
        info.file_info(path)
        if os.path.isfile(path):
            info.file_hash(path)
        if os.path.islink(path):
            info.symlink_info(path)

class check_permission:
    """Class to analyze and print file/directory permissions along with special flags."""

    @staticmethod
    def analyze(path):
        """Analyzes and prints file/directory permissions along with special flags."""
        try:
            # Check if path exists
            if not os.path.exists(path):
                print(f"[-] Path does not exist: {path}")
                return
            if platform.system() == "Windows" and win32security:
                try:
                    sd = win32security.GetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION)
                    dacl = sd.GetSecurityDescriptorDacl()

                    owner_sid = sd.GetSecurityDescriptorOwner()
                    owner_name, domain, _ = win32security.LookupAccountSid(None, owner_sid)

                    print(f"[+] {path} (Windows)")
                    print(f"    Owner : {domain}\\{owner_name}")
                    print(f"    Permissions:")

                    for i in range(dacl.GetAceCount()):
                        ace = dacl.GetAce(i)
                        print(f"      ACE {i}: {ace}")

                except Exception as e:
                    print(f"[-] Error reading security descriptor: {e}")

            info.file_info(path)

        except FileNotFoundError:
            print(f"[-] File not found: {path}")
        except PermissionError:
            print(f"[-] Permission denied: {path}")
        except Exception as e:
            print(f"[-] Error analyzing {path}: {e}")

# Hidden file info
class hidden_file_info:
    def __init__(self, path):
        self.path = path
        self.hidden_count = 0
    
    def is_hidden(self, filepath):
        """Check if the file is hidden based on its name or permissions."""
        name = os.path.basename(filepath)
        if name.startswith('.'):
            return True
        return not os.access(filepath, os.R_OK)

    def file_info(self, filepath):
        """Collect file information like size, hash, and modification time."""
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

    def scan_hidden(self):
        for root, dirs, files in os.walk(self.path):
            for name in files + dirs:
                fullpath = os.path.join(root, name)
                if self.is_hidden(fullpath):
                    self.hidden_count += 1
                    info = self.file_info(fullpath)
                    print(f"[Hidden] {fullpath}")
                    for k, v in info.items():
                        print(f"    {k}: {v}")
                    print("")
                    logging.info(f"[Hidden] {fullpath}")
                    for k, v in info.items():
                        logging.info(f"    {k}: {v}")
                    logging.info("")  # Add a blank line for readability

        if self.hidden_count == 0:
            print("No hidden files or directories found.")
        else:
            print(f"Total hidden files and directories found: {self.hidden_count}")


    def hidden_file_main():
        parser = argparse.ArgumentParser(description="Analyze file/folder permissions and retrieve additional information")
        parser.add_argument("target", nargs='+', help="Target file(s) or directory(ies) to check permissions")
        parser.add_argument("--scan-hidden", action="store_true", help="Scan for hidden files and directories")
        args = parser.parse_args()

        if args.scan_hidden:
            for path in args.target:
                hidden_scanner = hidden_file_info(path)
                hidden_scanner.scan_hidden()

        for path in args.target:
            check_permission.analyze(path)

class file_list:
    @staticmethod
    def get_path(path=''):
        file_list = []

        for entry in os.scandir(path):
            file_info = {}
            if entry.is_file():
                file_info['Name'] = entry.name
                file_info['Size (KB)'] = round(entry.stat().st_size / 1024, 2)
                file_info['Modified'] = time.ctime(entry.stat().st_mtime)
                file_info['Permissions'] = oct(entry.stat().st_mode)[-3:]
                file_info['IsHidden'] = False
                file_list.append(file_info)
            elif entry.is_dir():
                dir_name = entry.name
                if dir_name.startswith('.'):
                    file_list.append({
                        'Name': dir_name + '/',
                        'Size (KB)': '-',
                        'Modified': '-',
                        'Permissions': '-',
                        'IsHidden': True
                    })
                else:
                    file_list.append({
                        'Name': dir_name + '/',
                        'Size (KB)': '-',
                        'Modified': '-',
                        'Permissions': '-',
                        'IsHidden': False
                    })

        return file_list 

    @staticmethod
    def display_file_structure(path='.', level=0):
        files = file_list.get_path(path)

        if files:
            table = []

            for item in files:
                indent = '  ' * level
                if item['IsHidden']:
                    name = Fore.RED + item['Name']
                else:
                    name = item['Name']

                if item['Size (KB)'] == '-':
                    table.append([f"{indent}{name}", 'Directory', '-', '-'])
                else:
                    table.append([f"{indent}{name}", 'File', item['Size (KB)'], item['Modified']])

            print(tabulate(table, headers=["Name", "Type", "Size (KB)", "Modified"], tablefmt="pretty"))

            for item in files:
                if item['Size (KB)'] == '-' and not item['IsHidden']:
                    file_list.display_file_structure(os.path.join(path, item['Name']), level + 1)
        else:
            print(f"The directory '{path}' is empty or doesn't contain any files or subfolders.")