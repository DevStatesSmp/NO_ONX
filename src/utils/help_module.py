def help():
    print("""
\033[94mUsage:\033[0m
  \033[92m1.\033[0m nnx [COMMAND] [...] ()
  \033[92m2.\033[0m python3 src/[FILE_MODULE_NAME].py (Only compare, readfile, file_info and file_scan command)
          
\033[94mOptions:\033[0m
  \033[93m--version\033[0m (-v)           - Show version information
  \033[93m--help\033[0m (-h)              - Show help
  \033[93m--system_info\033[0m (-si)      - Show system information

\033[94mCommands:\033[0m

  \033[96m--readfile\033[0m <file_type> <file_path>         - Read and display content of a file
      \033[93mArguments:\033[0m
          <file_type> - 'text' or 'binary'
          <file_path> - Path to the file

  \033[96m--file_info\033[0m <file_path>                   - Retrieve detailed file information
      \033[93mArguments:\033[0m
          <file_path> - Path to the file

  \033[96m--file_hash\033[0m <file_path> [algorithm]       - Retrieve file hash
      \033[93mArguments:\033[0m
          <file_path> - Path to the file
          <algorithm> (optional) - Hashing algorithm (default: sha256)

  \033[96m--dir_info\033[0m <directory_path>              - Retrieve directory information
      \033[93mArguments:\033[0m
          <directory_path> - Path to the directory

  \033[96m--symlink_info\033[0m <symlink_path>            - Retrieve symlink information
      \033[93mArguments:\033[0m
          <symlink_path> - Path to the symlink

  \033[96m--extended_info\033[0m <file_path>              - Retrieve extended file information
      \033[93mArguments:\033[0m
          <file_path> - Path to the file

  \033[96m--scan_dir\033[0m <directory_path> [algorithm]  - Scan directory for malware
      \033[93mArguments:\033[0m
          <directory_path> - Path to the directory
          <algorithm> (optional) - Hashing algorithm (default: sha256)

  \033[96m--check_permission\033[0m <file_path>           - Check file or directory permissions
      \033[93mArguments:\033[0m
          <file_path> - Path to the file or directory

  \033[96m--hidden_file_info\033[0m <file_path>           - Check hidden file or directory
      \033[93mArguments:\033[0m
          <file_path> - Path to the file or directory

  \033[96m--compare\033[0m --mode <option> <path1> <path2>    - Compare two files or directories
      \033[93mArguments:\033[0m
          <option> - 'simple' or 'deep'
          <path1> - Path to the first directory
          <path2> - Path to the second directory

\033[94mModification Commands:\033[0m

  \033[96m--modify_file_permission\033[0m <file_path> <permissions>         - Modify file permissions
      \033[93mArguments:\033[0m
          <file_path> - Path to the file
          <permissions> - New permission (e.g., 755)

  \033[96m--modify_file_content\033[0m <file_path> <operation> <target_text> [optional_text]
                                                      - Modify the content of a file
      \033[93mArguments:\033[0m
          <file_path> - Path to the file
          <operation> - 'replace', 'delete', or 'append'
          <target_text> - Target text for operation
          <optional_text> - Replacement text or text to append

  \033[96m--modify_file_name\033[0m <old_name> <new_name>                  - Rename a file
      \033[93mArguments:\033[0m
          <old_name> - Current file name
          <new_name> - New file name

  \033[96m--modify_file_metadata\033[0m <file_path> <metadata_type> <value>
                                                      - Modify file metadata
      \033[93mArguments:\033[0m
          <file_path> - Path to the file
          <metadata_type> - Metadata type (e.g., timestamp)
          <value> - New metadata value

  \033[96m--modify_file_line\033[0m <file_path> <line_number> <operation> [optional_new_line]
                                                      - Modify a specific line in the file
      \033[93mArguments:\033[0m
          <file_path> - Path to the file
          <line_number> - Line number
          <operation> - 'replace' or 'insert'
          <optional_new_line> - New content for the line

  \033[96m--modify_file_symlink\033[0m <target_path> <symlink_path> <operation>
                                                      - Modify symlink of a file
      \033[93mArguments:\033[0m
          <target_path> - Target file/directory path
          <symlink_path> - Path to symlink
          <operation> - 'create', 'remove', or 'update'

  \033[96m--modify_directory\033[0m <dir_path> <operation> <new_path>       - Modify directory (move/rename)
      \033[93mArguments:\033[0m
          <dir_path> - Path to the directory
          <operation> - 'move' or 'rename'
          <new_path> - New path

  \033[96m--modify_directory_permissions\033[0m <dir_path> <permissions>     - Change directory permissions
      \033[93mArguments:\033[0m
          <dir_path> - Path to the directory
          <permissions> - New permission (e.g., 755)

  \033[96m--modify_file_owner\033[0m <file_path> <new_owner>               - Change file owner
      \033[93mArguments:\033[0m
          <file_path> - Path to the file
          <new_owner> - New owner ID

\033[94mBackup commands:\033[0m
  \033[96m--backup\033[0m <option> <path1> (<path2>)                       - Backup restore files or directories
      \033[93mArguments:\033[0m
          <option> - -backup_file, -backup_restore_file,...
          <path1> - Path to the file or directory (Required)
          <path2> - Path to the backup file or directory (Optional if have)

       <option>:
           -backup_file <path1>
           -backup_restore_file <path1>
           -backup_dir <path1>
           -backup_restore_dir <path1>
           -backup_file_timestamp <path1>
           -backup_multiple_files <path1> <path2>
           -backup_multiple_files <path1> <path2>
           -clean_old_backups
""")