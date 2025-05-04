# Usage:
1. NO_ONX.exe <argument> <...>
3. python src/[MODULE_NAME].py (<argument> <...>)

(Note: you can use python noonx.py <argument> <...> but not recommend to use because too complex and long)

# Command Usage Guide

## 1. **File Info Commands**

- **`file_info(path)`**: Displays detailed information about a specified file.
    - **Usage**:
      ```bash
      nnx --file_info /path/to/file
      ```

- **`file_hash(path, algo='sha256')`**: Computes the hash of a file using the specified algorithm (`md5`, `sha1`, or `sha256`).
    - **Usage**:
      ```bash
      nnx --file_hash /path/to/file sha256
      ```
      Default algorithm is `sha256` if not specified.

- **`dir_info(path)`**: Provides details about the contents of a directory.
    - **Usage**:
      ```bash
      nnx --dir_info /path/to/directory
      ```

- **`symlink_info(path)`**: Displays information about a symbolic link.
    - **Usage**:
      ```bash
      nnx --symlink_info /path/to/symlink
      ```

- **`extended_info(path)`**: Displays extended information about the specified path (file or directory).
    - **Usage**:
      ```bash
      nnx --extended_info /path/to/file_or_directory
      ```

---

## 2. **File Permission Commands**

- **`check_permission(path)`**: Analyzes and checks the permissions of the specified path.
    - **Usage**:
      ```bash
      nnx --check_permission /path/to/file_or_directory
      ```

- **`hidden_file_info(path)`**: Scans and provides details about hidden files in the specified path.
    - **Usage**:
      ```bash
      nnx --hidden_file_info /path/to/directory
      ```

---

## 3. **File Modification Commands**

- **`modify_file_permission(path, permission)`**: Changes the file permissions for the specified file.
    - **Usage**:
      ```bash
      nnx --modify_file_permission /path/to/file 755
      ```

- **`modify_file_content(path, operation, text, target_text=None)`**: Modifies the content of a file by appending, replacing, or deleting text.
    - **Usage**:
      ```bash
      nnx --modify_file_content /path/to/file append "New content to add"
      nnx --modify_file_content /path/to/file replace "Old text" "New text"
      nnx --modify_file_content /path/to/file delete "Text to delete"
      ```

- **`modify_file_name(old_name, new_name)`**: Renames a file.
    - **Usage**:
      ```bash
      nnx --modify_file_name old_file.txt new_file.txt
      ```

- **`modify_file_metadata(path, metadata_type, value)`**: Modifies file metadata, such as the last modified time.
    - **Usage**:
      ```bash
      nnx --modify_file_metadata /path/to/file last_modified 1672531200
      ```

- **`modify_file_line(path, line_number, operation, new_line=None)`**: Modifies a specific line in a file.
    - **Usage**:
      ```bash
      nnx --modify_file_line /path/to/file 2 replace "New line content"
      nnx --modify_file_line /path/to/file 3 delete
      nnx --modify_file_line /path/to/file 4 insert "Inserted line content"
      ```

- **`modify_file_symlink(target_path, symlink_path, operation)`**: Creates or deletes a symbolic link.
    - **Usage**:
      ```bash
      nnx --modify_file_symlink /path/to/target /path/to/symlink create
      nnx --modify_file_symlink None /path/to/symlink delete
      ```

- **`modify_directory(path, operation, new_path=None)`**: Renames or moves a directory.
    - **Usage**:
      ```bash
      nnx --modify_directory /path/to/dir rename /path/to/new_dir
      nnx --modify_directory /path/to/dir move /new/location/dir
      ```

- **`modify_directory_permissions(path, permission)`**: Changes the permissions of a directory.
    - **Usage**:
      ```bash
      nnx --modify_directory_permissions /path/to/dir 755
      ```

- **`modify_file_owner(path, new_owner)`**: Modifies the owner of a file (not supported on Windows).
    - **Usage**:
      ```bash
      nnx --modify_file_owner /path/to/file new_owner
      ```

---

## 4. **File Scanning Commands**

- **`scan_dir(path)`**: Scans a directory for files and computes their hash using the specified algorithm (`md5`, `sha1`, `sha256`).
    - **Usage**:
      ```bash
      nnx --scan_dir /path/to/directory sha256
      ```

---

## 5. **Read File Commands**

- **`readfile(file_type, file_path)`**: Reads a file, either as text or binary.
    - **Usage**:
      ```bash
      nnx --readfile text /path/to/textfile
      nnx --readfile binary /path/to/binaryfile
      ```

## 6. **Compare commands**
- **`--mode <option> (path1, path2)`**: Compare two directory
    - **Usage**:
      ```bash
      nnx --compare --mode  text /path/to/textfile
      nnx --readfile binary /path/to/binaryfile
      ```

## 7. **Backup commands**
- **--backup <option> (path1, <path2>)**: Backup file & directory
    - **Usage**:
      ```bash
      nnx --backup -backup_file /path/to/textfile1
      nnx --backup -backup_restore_file /path/to/textfile1
      nnx --backup -backup_dir /path/to/directory1
      nnx --backup -backup_restore_dir /path/to/directory1
      nnx --backup -backup_file_timestamp /path/to/file1
      nnx --backup -backup_multiple_files /path/to/file1 /path/to/file2
      nnx --backup -backup_multiple_files /path/to/directory1 /path/to/directory2
      nnx --backup -clean_old_backups
      ```
---

## Notes:

1. **Command Syntax:**
   - All commands are case-insensitive.
   - You can use `Tab` for auto-completion of file and folder names.
   - Be cautious with commands that modify or delete files (e.g., `modify_file_content`, `modify_file_name`, etc.).

2. **Examples:**
   - **Changing file permissions**:  
     ```bash
     nnx --modify_file_permission /path/to/file 755
     ```

   - **Renaming a file**:  
     ```bash
     nnx --modify_file_name file_old_name.txt new_name.txt
     ```

   - **Reading a file as binary**:  
     ```bash
     nnx --readfile binary /path/to/file
     ```

3. **Error Handling:**
   - Ensure that the file or directory paths provided are correct.
   - If using `--readfile`, specify the correct type: `text` or `binary`.
   - For commands like `modify_file_metadata`, use appropriate values for timestamps.
