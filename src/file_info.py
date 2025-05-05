import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.workload.file_info_module import info, check_permission, hidden_file_info
from src.utils.config import FEATURE

def info_commands():
    print("📌 Available operations in file_info.py:\n")
    print("🔍 file_info(path)")
    print("🔍 hidden_file_info(path)")
    print("🔑 file_hash(path, algo='sha256')")
    print("🔗 symlink_info(path)")
    print("📁 dir_info(path)")
    print("📦 extended_info(path)\n")
    print("🔒 check_permission(path)\n")
    print("🗂️ hidden_file_info(path)\n")
    print("")

def main():
    print("Available operations (Not number, enter name)")
    info_commands()

    while True:
        operation = input("🛠️ Enter operation (or 'exit' to quit): ").strip()

        if operation == "exit":
            print("👋 Exiting info module.")
            break

        elif operation == "file_info":
            path = input("📂 Enter path: ").strip()
            info.file_info(path)

        elif operation == "file_hash":
            path = input("📂 Enter file path: ").strip()
            algo = input("🔑 Enter hash algorithm (md5/sha1/sha256): ").strip().lower()
            info.file_hash(path, algo)

        elif operation == "symlink_info":
            path = input("🔗 Enter symlink path: ").strip()
            info.symlink_info(path)

        elif operation == "dir_info":
            path = input("📁 Enter directory path: ").strip()
            info.dir_info(path)

        elif operation == "extended_info":
            path = input("📦 Enter path: ").strip()
            info.extended_info(path)

        elif operation == "check_permission":
            path = input("🔒 Enter path to check permissions: ").strip()
            check_permission.analyze(path)

        elif operation == "hidden_file_info":
            path = input("📂 Enter path: ").strip()
            hidden_scanner = hidden_file_info(path)
            hidden_scanner.scan_hidden()

        else:
            print("❓ Unknown operation. Please choose from available commands.\n")
            info_commands()

if __name__ == "__main__" and FEATURE["ENABLE_DIRECT_RUN"]:
    main()
else:
    if __name__ == "__main__":
        print("[ERROR] This script cannot be run directly. Use NO_ONX.exe instead.")