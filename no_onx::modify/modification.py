import os
import shutil
import time

class NO_ONX:
    class modify:

        @staticmethod
        def modify_file_permission(path, permission):
            try:
                os.chmod(path, int(permission, 8))
                print(f"Permission of '{path}' changed to {permission}")
            except Exception as e:
                print(f"Error modifying permission: {e}")

        @staticmethod
        def modify_file_content(path, operation, text, target_text=None):
            try:
                with open(path, 'r+') as file:
                    content = file.readlines()
                    
                    if operation == 'append':
                        file.write(text + "\n")
                    elif operation == 'replace' and target_text:
                        content = [line.replace(target_text, text) for line in content]
                        file.seek(0)
                        file.writelines(content)
                    elif operation == 'delete' and target_text:
                        content = [line for line in content if target_text not in line]
                        file.seek(0)
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
                if metadata_type == 'owner':
                    os.chown(path, value)  # `value` here would be user ID (uid)
                    print(f"Owner of '{path}' changed.")
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
                with open(path, 'r+') as file:
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
                    file.writelines(lines)
                    print(f"File line {line_number} modified in {operation} mode.")
            except Exception as e:
                print(f"Error modifying file line: {e}")

        @staticmethod
        def modify_file_symlink(target_path, symlink_path, operation):
            try:
                if operation == 'create':
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
                os.chmod(path, int(permission, 8))
                print(f"Permissions of directory '{path}' changed to {permission}")
            except Exception as e:
                print(f"Error modifying directory permissions: {e}")

        @staticmethod
        def modify_file_owner(path, new_owner):
            try:
                os.chown(path, new_owner, -1)  # new_owner should be the user ID
                print(f"Owner of '{path}' changed to {new_owner}")
            except Exception as e:
                print(f"Error modifying file owner: {e}")

# Main function to interact with user
def list_operations():
    print("Available operations (Not number, enter name):\n")
    icons = {
        "modify_file_permission": "🔐",
        "modify_file_content": "📝",
        "modify_file_name": "✏️",
        "modify_file_metadata": "📂",
        "modify_file_line": "📄",
        "modify_file_symlink": "🔗",
        "modify_directory": "📁",
        "modify_directory_permissions": "🛡️",
        "modify_file_owner": "👤"
    }

    ops = [func for func in dir(NO_ONX.modify) if callable(getattr(NO_ONX.modify, func)) and not func.startswith("__")]
    for op in ops:
        icon = icons.get(op, "⚙️")
        print(f" {icon} {op}")


def main():
    while True:
        list_operations()
        operation = input("\n 🛠 Enter the operation you want to perform (or 'exit' to quit): ").strip()
        
        if operation == "exit":
            print("The program is closing.")
            break

        if operation == "modify_file_permission":
            path = input("Enter the path of the file: ").strip()
            permission = input("Enter the new permission (e.g., '777'): ").strip()
            NO_ONX.modify.modify_file_permission(path, permission)

        elif operation == "modify_file_content":
            path = input("Enter the path of the file: ").strip()
            action = input("Enter the operation ('append', 'replace', 'delete'): ").strip()
            if action == "replace" or action == "delete":
                target_text = input("Enter the target text to replace/delete: ").strip()
                text = input("Enter the new text (for replace): ").strip() if action == "replace" else None
                NO_ONX.modify.modify_file_content(path, action, text, target_text)
            else:
                text = input("Enter the text to append: ").strip()
                NO_ONX.modify.modify_file_content(path, action, text)

        elif operation == "modify_file_name":
            old_name = input("Enter the old file name: ").strip()
            new_name = input("Enter the new file name: ").strip()
            NO_ONX.modify.modify_file_name(old_name, new_name)

        elif operation == "modify_file_metadata":
            path = input("Enter the path of the file: ").strip()
            metadata_type = input("Enter the metadata type ('owner' or 'last_modified'): ").strip()
            value = input("Enter the value to set (user ID for 'owner' or timestamp for 'last_modified'): ").strip()
            NO_ONX.modify.modify_file_metadata(path, metadata_type, float(value))

        elif operation == "modify_file_line":
            path = input("Enter the file path: ").strip()
            line_number = int(input("Enter the line number to modify: ").strip())
            action = input("Enter the operation ('replace', 'delete', 'insert'): ").strip()
            if action == "insert" or action == "replace":
                new_line = input("Enter the new line text: ").strip()
                NO_ONX.modify.modify_file_line(path, line_number, action, new_line)
            else:
                NO_ONX.modify.modify_file_line(path, line_number, action)

        elif operation == "modify_file_symlink":
            target_path = input("Enter the target path: ").strip()
            symlink_path = input("Enter the symlink path: ").strip()
            action = input("Enter the operation ('create' or 'delete'): ").strip()
            NO_ONX.modify.modify_file_symlink(target_path, symlink_path, action)

        elif operation == "modify_directory":
            path = input("Enter the directory path: ").strip()
            action = input("Enter the operation ('rename' or 'move'): ").strip()
            if action in ("rename", "move"):
                new_path = input("Enter the new path: ").strip()
                NO_ONX.modify.modify_directory(path, action, new_path)
            else:
                print("Invalid operation for directory.")
        
        elif operation == "modify_directory_permissions":
            path = input("Enter the directory path: ").strip()
            permission = input("Enter the new permission (e.g., '755'): ").strip()
            NO_ONX.modify.modify_directory_permissions(path, permission)

        elif operation == "modify_file_owner":
            path = input("Enter the file path: ").strip()
            new_owner = int(input("Enter the new owner UID: ").strip())
            NO_ONX.modify.modify_file_owner(path, new_owner)
        else:
            print("❌ Invalid operation. Please try again.")
            continue
        
        break
        

if __name__ == "__main__":
    main()
