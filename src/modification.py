import os
import shutil
import time
import platform

class mod:
    class modify:

        @staticmethod
        def modify_file_permission(path, permission):
            try:
                if os.name == 'nt':
                    print("⚠️ File permission change is not fully supported on Windows.")
                    return
                os.chmod(path, int(permission, 8))  # Unix-based systems
                print(f"Permission of '{path}' changed to {permission}")
            except Exception as e:
                print(f"Error modifying permission: {e}")

        @staticmethod
        def modify_file_content(path, operation, text, target_text=None):
            try:
                with open(path, 'r+', encoding='utf-8') as file:
                    content = file.readlines()

                    if operation == 'append':
                        file.seek(0, os.SEEK_END)
                        file.write(text + "\n")
                    elif operation == 'replace' and target_text:
                        content = [line.replace(target_text, text) for line in content]
                        file.seek(0)
                        file.truncate()
                        file.writelines(content)
                    elif operation == 'delete' and target_text:
                        content = [line for line in content if target_text not in line]
                        file.seek(0)
                        file.truncate()
                        file.writelines(content)
                    else:
                        print("Invalid operation.")
                        return

                    print(f"File content modified in {operation} mode.")
            except Exception as e:
                print(f"Error modifying file content: {e}")

        @staticmethod
        def modify_file_name(old_name, new_name):
            try:
                os.rename(old_name, new_name)
                print(f"File renamed from {old_name} to {new_name}")
            except Exception as e:
                print(f"Error renaming file: {e}")

        @staticmethod
        def modify_file_metadata(path, metadata_type, value):
            try:
                if os.name == 'nt':
                    print("⚠️ File metadata modification is limited on Windows.")
                    return

                if metadata_type == 'owner':
                    print("⚠️ Changing file owner is not supported on Windows.")
                elif metadata_type == 'last_modified':
                    os.utime(path, (value, value))
                    print(f"Last modified time of '{path}' changed.")
                else:
                    print("Invalid metadata type.")
            except Exception as e:
                print(f"Error modifying file metadata: {e}")

        @staticmethod
        def modify_file_line(path, line_number, operation, new_line=None):
            try:
                with open(path, 'r+', encoding='utf-8') as file:
                    lines = file.readlines()

                    if operation == 'replace' and new_line:
                        lines[line_number - 1] = new_line + "\n"
                    elif operation == 'delete':
                        lines.pop(line_number - 1)
                    elif operation == 'insert' and new_line:
                        lines.insert(line_number - 1, new_line + "\n")
                    else:
                        print("Invalid operation.")
                        return

                    file.seek(0)
                    file.truncate()
                    file.writelines(lines)
                    print(f"File line {line_number} modified in {operation} mode.")
            except Exception as e:
                print(f"Error modifying file line: {e}")

        @staticmethod
        def modify_file_symlink(target_path, symlink_path, operation):
            try:
                if os.name == 'nt':
                    print("⚠️ Symlink creation requires admin rights or developer mode on Windows.")
                    return

                if operation == 'create':
                    if not os.path.exists(target_path):
                        print("⚠️ Target path does not exist.")
                        return
                    os.symlink(target_path, symlink_path)
                    print(f"Symlink created from {target_path} to {symlink_path}")
                elif operation == 'delete' and os.path.islink(symlink_path):
                    os.remove(symlink_path)
                    print(f"Symlink {symlink_path} deleted.")
                else:
                    print("Invalid operation.")
            except Exception as e:
                print(f"Error modifying symlink: {e}")

        @staticmethod
        def modify_directory(path, operation, new_path=None):
            try:
                if operation == 'rename' and new_path:
                    os.rename(path, new_path)
                    print(f"Directory renamed from {path} to {new_path}")
                elif operation == 'move' and new_path:
                    shutil.move(path, new_path)
                    print(f"Directory moved from {path} to {new_path}")
                else:
                    print("Invalid operation.")
            except Exception as e:
                print(f"Error modifying directory: {e}")

        @staticmethod
        def modify_directory_permissions(path, permission):
            try:
                if os.name == 'nt':
                    print("⚠️ Directory permission changes are limited on Windows.")
                    return
                os.chmod(path, int(permission, 8))  # Unix-based systems
                print(f"Permissions of directory '{path}' changed to {permission}")
            except Exception as e:
                print(f"Error modifying directory permissions: {e}")

        @staticmethod
        def modify_file_owner(path, new_owner):
            try:
                if os.name == 'nt':
                    print("⚠️ File owner modification is not supported on Windows.")
                    return
                # This functionality is generally not supported on Windows unless using Windows Subsystem for Linux (WSL)
                print("File owner modification is typically not supported on Windows.")
            except Exception as e:
                print(f"Error modifying file owner: {e}")
