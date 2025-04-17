# THIS IS NOT A MODULE, INSTEAD USE FILE_INFO_MODULE.PY, YOU SHOULD USE FILE_INFO.PY

import os
import stat
import pwd
import grp
import time
import hashlib

class info:
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
            print(f"👤 Owner: {pwd.getpwuid(stat_info.st_uid).pw_name} (UID: {stat_info.st_uid})")
            print(f"👥 Group: {grp.getgrgid(stat_info.st_gid).gr_name} (GID: {stat_info.st_gid})")
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
