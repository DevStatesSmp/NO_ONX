# permissions.py

import os
import stat
import pwd
import grp
import argparse

def analyze_permissions(path):
    try:
        st = os.stat(path)
        mode = stat.filemode(st.st_mode)
        owner = pwd.getpwuid(st.st_uid).pw_name
        group = grp.getgrgid(st.st_gid).gr_name
        print(f"[+] {path}")
        print(f"    Mode  : {mode}")
        print(f"    Owner : {owner}")
        print(f"    Group : {group}")
        print(f"    SUID  : {'Yes' if st.st_mode & stat.S_ISUID else 'No'}")
        print(f"    SGID  : {'Yes' if st.st_mode & stat.S_ISGID else 'No'}")
        print(f"    Sticky: {'Yes' if st.st_mode & stat.S_ISVTX else 'No'}")
        print()

    except FileNotFoundError:
        print(f"[-] File not found: {path}")
    except Exception as e:
        print(f"[-] Error analyzing {path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Analyze file/folder permissions")
    parser.add_argument("target", nargs='+', help="Target file(s) or directory(ies)")
    args = parser.parse_args()

    for path in args.target:
        analyze_permissions(path)

if __name__ == "__main__":
    main()
