import shutil
import os
import time

backup_dir = os.path.join("backup")

# Kiểm tra nếu thư mục backup không tồn tại, tạo mới
os.makedirs(backup_dir, exist_ok=True)

# Sao lưu tệp
def backup_file(source):
    try:
        backup_location = os.path.join(backup_dir, os.path.basename(source))
        shutil.copy(source, backup_location)
        print(f"Backup successful: {source} -> {backup_location}")
    except Exception as e:
        print(f"Error during backup: {e}")

# Khôi phục tệp từ sao lưu
def restore_backup(backup_location, restore_location):
    try:
        shutil.copy(backup_location, restore_location)
        print(f"Restore successful: {backup_location} -> {restore_location}")
    except Exception as e:
        print(f"Error during restore: {e}")

# Sao lưu thư mục
def backup_directory(source_dir):
    try:
        backup_location = os.path.join(backup_dir, os.path.basename(source_dir))
        if os.path.exists(backup_location):
            shutil.rmtree(backup_location)
        shutil.copytree(source_dir, backup_location)
        print(f"Backup successful: {source_dir} -> {backup_location}")
    except Exception as e:
        print(f"Error during backup: {e}")

# Khôi phục thư mục từ sao lưu
def restore_directory(backup_location, restore_location):
    try:
        if os.path.exists(restore_location):
            shutil.rmtree(restore_location)
        shutil.copytree(backup_location, restore_location)
        print(f"Restore successful: {backup_location} -> {restore_location}")
    except Exception as e:
        print(f"Error during restore: {e}")

# Sao lưu tệp với tên theo thời gian
def backup_file_with_timestamp(source):
    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        backup_location = os.path.join(backup_dir, f"{timestamp}_{os.path.basename(source)}")
        shutil.copy(source, backup_location)
        print(f"Backup successful: {source} -> {backup_location}")
    except Exception as e:
        print(f"Error during backup: {e}")

# Sao lưu và nén thư mục
def backup_and_compress_directory(source_dir):
    try:
        backup_archive = os.path.join(backup_dir, os.path.basename(source_dir) + "_backup")
        shutil.make_archive(backup_archive, 'zip', source_dir)
        print(f"Backup and compression successful: {source_dir} -> {backup_archive}.zip")
    except Exception as e:
        print(f"Error during backup and compression: {e}")

# Sao lưu và nén tệp
def backup_and_compress_file(source_file):
    try:
        backup_archive = os.path.join(backup_dir, os.path.basename(source_file) + "_backup")
        shutil.make_archive(backup_archive, 'zip', os.path.dirname(source_file), os.path.basename(source_file))
        print(f"File backup and compression successful: {source_file} -> {backup_archive}.zip")
    except Exception as e:
        print(f"Error during backup and compression: {e}")

# Main function to interact with the user
def main():

    print("Choose the backup operation:")
    print("1. 📄 Backup a file")
    print("2. ♻️ restore a file")
    print("3. 📁 Backup a directory")
    print("4. ♻️ Restore a directory")
    print("5. 🕒 Backup a file with timestamp")
    print("6. 🗜️ Backup and compress a directory")
    print("7. 🗜️ Backup and compress a file")

    choice = input("Enter your choice (From 1-7 or 'exit to quit'): ")
    
    if choice = "exit":
        print("The progam will close")
    
    if choice == '1':
        source_file = input("Enter the file path to backup: ")
        backup_file(source_file)

    elif choice == '2':
        backup_file_location = input("Enter the backup file path: ")
        restore_location = input("Enter the location to restore: ")
        restore_backup(backup_file_location, restore_location)

    elif choice == '3':
        source_directory = input("Enter the directory path to backup: ")
        backup_directory(source_directory)

    elif choice == '4':
        backup_directory_location = input("Enter the directory path to restore: ")
        restore_directory_location = input("Enter the location to restore the directory: ")
        restore_directory(backup_directory_location, restore_directory_location)

    elif choice == '5':
        source_file = input("Enter the file path to backup: ")
        backup_file_with_timestamp(source_file)

    elif choice == '6':
        source_directory = input("Enter the directory path to backup: ")
        backup_and_compress_directory(source_directory)

    elif choice == '7':
        source_file = input("Enter the file path to backup: ")
        backup_and_compress_file(source_file)

    else:
        print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
