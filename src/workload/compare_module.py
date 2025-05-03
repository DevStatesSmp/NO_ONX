# THIS IS MODULE, DO NOT RUN THIS FILE DIRECTLY

import os
import hashlib
import filecmp
import stat

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
                print(f"[!] Error reading {fullpath}: {e}")
    return filemap

def deep_compare_dirs(dir1, dir2):
    files1 = walk_dir(dir1)
    files2 = walk_dir(dir2)

    all_keys = set(files1.keys()).union(files2.keys())

    identical_files = 0
    different_files = 0
    only_in_dir1 = []
    only_in_dir2 = []
    diff_files = []

    table_data = []

    for key in sorted(all_keys):
        f1 = files1.get(key)
        f2 = files2.get(key)
        row = [key]
        if not f1:
            only_in_dir2.append(key)
            different_files += 1  
            row.append(f"{dir2}: Only")
            row.append("-")
        elif not f2:
            only_in_dir1.append(key)
            different_files += 1 
            row.append(f"{dir1}: Only")
            row.append("-")
        elif f1["hash"] != f2["hash"]:
            different_files += 1
            diff_files.append(key)
            row.append("Different")
            row.append(f"{f1['hash'][:6]}... <=> {f2['hash'][:6]}...")  
        elif f1["mode"] != f2["mode"]:
            different_files += 1
            diff_files.append(key)
            row.append("Permissions differ")
            row.append(f"{f1['mode']} <=> {f2['mode']}")
        else:
            identical_files += 1
            row.append("Identical")
            row.append("-")
        table_data.append(row)

    headers = ["File", "Status", "Details"]
    return identical_files, different_files, only_in_dir1, only_in_dir2, diff_files, table_data

def deep_compare_files(f1, f2):
    h1 = hash_file(f1)
    h2 = hash_file(f2)
    if h1 == h2:
        return "Identical"
    else:
        return "Different"

def simple_compare_files(f1, f2):
    if not os.path.exists(f1) or not os.path.exists(f2):
        return "One or both files do not exist."
    result = filecmp.cmp(f1, f2, shallow=False)
    return "IDENTICAL" if result else "DIFFERENT"

def simple_compare_dirs(d1, d2):
    dcmp = filecmp.dircmp(d1, d2)
    result = []
    if dcmp.left_only:
        result.append(f"Left only : {dcmp.left_only}")
    if dcmp.right_only:
        result.append(f"Right only: {dcmp.right_only}")
    if dcmp.diff_files:
        result.append(f"Different : {dcmp.diff_files}")
    if dcmp.funny_files:
        result.append(f"Problematic: {dcmp.funny_files}")
    return result