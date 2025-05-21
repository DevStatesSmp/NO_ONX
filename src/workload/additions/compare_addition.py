import os
import hashlib
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "utils"))
from src.utils.getError import *

def hash_file(filepath):
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except Exception:
        return None

def walk_dir(path):
    filemap = {}
    for root, dirs, files in os.walk(path):
        for name in files:
            fullpath = os.path.join(root, name)
            relpath = os.path.relpath(fullpath, path)
            try:
                statinfo = os.stat(fullpath)
                filemap[relpath] = {
                    "size": statinfo.st_size,
                    "mtime": statinfo.st_mtime,
                    "mode": statinfo.st_mode,
                    "uid": statinfo.st_uid,
                    "gid": statinfo.st_gid,
                    "hash": hash_file(fullpath),
                }
            except Exception as e:
                handle_error(
                    ErrorContent.READFILE_ERROR,
                    {"filepath": fullpath, "error": str(e)},
                    ErrorReason
                )
    return filemap