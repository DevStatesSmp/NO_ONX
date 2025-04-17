from file_info_module import info

def info_commands():
    print("📌 Available operations in file_info.py:\n")
    print("🔍 file_info(path)")
    print("🔑 file_hash(path, algo='sha256')")
    print("🔗 symlink_info(path)")
    print("📁 dir_info(path)")
    print("📦 extended_info(path)\n")

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

        else:
            print("❓ Unknown operation. Please choose from available commands.\n")
            info_commands()

if __name__ == "__main__":
    main()

