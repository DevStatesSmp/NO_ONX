import os
import argparse
import hashlib
import filecmp
import stat
import sys
from tabulate import tabulate

### ==== MODE: DEEP ====

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
    print(f"\nSummary:")
    print(f"Total files: {len(all_keys)}")
    print(f"Identical files: {identical_files}")
    print(f"Different files: {different_files}")
    print(f"Only in {dir1}: {len(only_in_dir1)}")
    print(f"Only in {dir2}: {len(only_in_dir2)}")


    print("\nComparison Table:")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


    if diff_files:
        print("\nDifferent files (content or permissions):")
        for f in diff_files:
            print(f"  - {f}")
    else:
        print("")
        

    if only_in_dir1:
        print(f"\nFiles only in {dir1}:")
        for f in only_in_dir1:
            print(f"  - {f}")
            
    if only_in_dir2:
        print(f"\nFiles only in {dir2}:")
        for f in only_in_dir2:
            print(f"  - {f}")

def deep_compare_files(f1, f2):
    h1 = hash_file(f1)
    h2 = hash_file(f2)
    print(f"[+] Comparing (deep): {f1} <=> {f2}")
    if h1 == h2:
        print("    ✅ Identical")
    else:
        print("    ❗ Different")

### ==== MODE: SIMPLE ====

def simple_compare_files(f1, f2):
    print(f"[+] Comparing (simple): {f1} <=> {f2}")
    if not os.path.exists(f1) or not os.path.exists(f2):
        print("[-] One or both files do not exist.")
        return
    result = filecmp.cmp(f1, f2, shallow=False)
    print(f"    => {'IDENTICAL' if result else 'DIFFERENT'}\n")

def simple_compare_dirs(d1, d2):
    print(f"[+] Comparing directories: {d1} <=> {d2}")
    if not os.path.isdir(d1) or not os.path.isdir(d2):
        print("[-] One or both paths are not directories.")
        return
    dcmp = filecmp.dircmp(d1, d2)
    if dcmp.left_only:
        print("  Left only :", dcmp.left_only)
    if dcmp.right_only:
        print("  Right only:", dcmp.right_only)
    if dcmp.diff_files:
        print("  Different :", dcmp.diff_files)
    if dcmp.funny_files:
        print("  Problematic:", dcmp.funny_files)
    print()

### ==== MAIN CLI ====

def main():
    parser = argparse.ArgumentParser(description="Compare file or directory (simple or deep)")
    parser.add_argument("path1", help="first path")
    parser.add_argument("path2", help="second path")
    parser.add_argument("--mode", choices=["simple", "deep"], default="simple",
                        help="Compare mode (default: simple)")
    args = parser.parse_args()

    if not os.path.exists(args.path1):
        print(f"❌ The path is not exist: {args.path1}")
        sys.exit(1)
    if not os.path.exists(args.path2):
        print(f"❌ The path is not exist: {args.path2}")
        sys.exit(1)

    is_dir1 = os.path.isdir(args.path1)
    is_dir2 = os.path.isdir(args.path2)

    if is_dir1 != is_dir2:
        print("⚠️ Cannot compare between file and directory!")
        sys.exit(1)

    if args.mode == "simple":
        if is_dir1:
            simple_compare_dirs(args.path1, args.path2)
        else:
            simple_compare_files(args.path1, args.path2)
    else:  # deep
        if is_dir1:
            deep_compare_dirs(args.path1, args.path2)
        else:
            deep_compare_files(args.path1, args.path2)

if __name__ == "__main__":
    main()

