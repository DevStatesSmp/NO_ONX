# THIS IS MODULE, DO NOT RUN THIS FILE DIRECTLY

import sys

# Import source
## Workload
from .utils.help_module import help
from .utils.system_info_module import get_system_info, get_gpu_info
from .utils.banner_module import banner, version
from .utils.loading_effect import loading_effect
from .workload.compare_module import deep_compare_dirs, simple_compare_dirs
from .workload.modification_module import mod
from .workload.file_info_module import info, check_permission, hidden_file_info
from .workload.backup_module import *
# Other
from . import file_scan
from .readfile import *
    

# ==== Main ====
def main():
    banner()
    if len(sys.argv) >= 2:
        arg = sys.argv[1]

        # Main argument for noonx.py
        if arg in ('--help', '-h'):
            loading_effect("Loading help")
            help()
        elif arg in ('--system_info', '-si'):
            loading_effect("Fetching system info")
            get_system_info()

        elif arg in ('--version', '-v'):
            version()

        ## Class info
        elif arg == '--file_info' and len(sys.argv) >= 3:
            info.file_info(sys.argv[2])

        elif arg == '--file_hash' and len(sys.argv) >= 3:
            path = sys.argv[2]
            algo = sys.argv[3] if len(sys.argv) >= 4 else "sha256"
            info.file_hash(path, algo)

        elif arg == '--dir_info' and len(sys.argv) >= 3:
            info.dir_info(sys.argv[2])

        elif arg == '--symlink_info' and len(sys.argv) >= 3:
            info.symlink_info(sys.argv[2])

        elif arg == '--extended_info' and len(sys.argv) >= 3:
            info.extended_info(sys.argv[2])

        ## class check_permission
        elif arg == '--check_permission' and len(sys.argv) >= 3:
            path = sys.argv[2]
            check_permission.analyze(path)
        
        ## Class hidden_file_info
        elif arg == '--hidden_file_info' and len(sys.argv) >= 3:
            path = sys.argv[2]
            hidden_scanner = hidden_file_info(path)
            hidden_scanner.scan_hidden()

        # Read file

        elif arg == '--readfile' and len(sys.argv) >= 4:
            file_type = sys.argv[2]
            file_path = sys.argv[3]
            if not validate_file_path(file_path):
                return
            if file_type == 'text':
                read_text_file(file_path)
            elif file_type == 'binary':
                read_binary_file(file_path)
            else:
                print("Error: Invalid readfile type. Use 'text' or 'binary'.", file=sys.stderr)


        # Modification
        elif arg == '--modify_file_permission' and len(sys.argv) >= 4:
            path = sys.argv[2]
            permission = sys.argv[3]
            mod.modify.modify_file_permission(path, permission)

        elif arg == '--modify_file_content' and len(sys.argv) >= 5:
            path = sys.argv[2]
            operation = sys.argv[3]
            if operation == 'replace' or operation == 'delete':
                target_text = sys.argv[4]
                text = sys.argv[5] if operation == 'replace' and len(sys.argv) >= 6 else None
                mod.modify.modify_file_content(path, operation, text, target_text)
            elif operation == 'append':
                text = sys.argv[4]
                mod.modify.modify_file_content(path, operation, text)

        elif arg == '--modify_file_name' and len(sys.argv) >= 4:
            old_name = sys.argv[2]
            new_name = sys.argv[3]
            mod.modify.modify_file_name(old_name, new_name)

        elif arg == '--modify_file_metadata' and len(sys.argv) >= 5:
            path = sys.argv[2]
            metadata_type = sys.argv[3]
            value = float(sys.argv[4])
            mod.modify.modify_file_metadata(path, metadata_type, value)

        elif arg == '--modify_file_line' and len(sys.argv) >= 5:
            path = sys.argv[2]
            line_number = int(sys.argv[3])
            operation = sys.argv[4]
            new_line = sys.argv[5] if operation in ('replace', 'insert') and len(sys.argv) >= 6 else None
            mod.modify.modify_file_line(path, line_number, operation, new_line)

        elif arg == '--modify_file_symlink' and len(sys.argv) >= 5:
            target_path = sys.argv[2]
            symlink_path = sys.argv[3]
            operation = sys.argv[4]
            mod.modify.modify_file_symlink(target_path, symlink_path, operation)

        elif arg == '--modify_directory' and len(sys.argv) >= 5:
            path = sys.argv[2]
            operation = sys.argv[3]
            new_path = sys.argv[4]
            mod.modify.modify_directory(path, operation, new_path)

        elif arg == '--modify_directory_permissions' and len(sys.argv) >= 4:
            path = sys.argv[2]
            permission = sys.argv[3]
            mod.modify.modify_directory_permissions(path, permission)

        elif arg == '--modify_file_owner' and len(sys.argv) >= 4:
            path = sys.argv[2]
            new_owner = int(sys.argv[3])
            mod.modify.modify_file_owner(path, new_owner)

        # File Scan
        elif arg in ('--scan_dir') and len(sys.argv) >= 3:
            path = sys.argv[2]
            algo = sys.argv[3] if len(sys.argv) >= 4 else "sha256"
            loading_effect(f"Scanning directory ({path}) using {algo.upper()}")
            file_scan.reset_results()
            file_scan.scan_directory(path, algo)
            file_scan.print_results()

        # Compare
        elif arg == '--compare --mode' and len(sys.argv) >= 5:
            compare_type = sys.argv[2]
            path1 = sys.argv[3]
            path2 = sys.argv[4]
    
            if compare_type == 'deep':
                loading_effect(f"Deep comparing {path1} and {path2}")
                identical_files, different_files, only_in_dir1, only_in_dir2, diff_files, table_data = deep_compare_dirs(path1, path2)
                print(f"Identical files: {identical_files}")
                print(f"Different files: {different_files}")
                if only_in_dir1:
                    print(f"Only in {path1}: {only_in_dir1}")
                if only_in_dir2:
                    print(f"Only in {path2}: {only_in_dir2}")
                if diff_files:
                    print(f"Different files: {diff_files}")

                for row in table_data:
                    print(f"{row[0]}: {row[1]} - {row[2]}")
        
            elif compare_type == 'simple':
                loading_effect(f"Simple comparing {path1} and {path2}")

                result = simple_compare_dirs(path1, path2)
                if result:
                    for res in result:
                        print(res)
                else:
                    print("No differences found.")
            else:
                print("Error: Invalid compare type. Use 'deep' or 'simple'.", file=sys.stderr)

        # Backup
        elif arg == '--backup':
            backup_type = sys.argv[2]
            path1 = sys.argv[3] if len(sys.argv) > 3 else None # Default path
            path2 = sys.argv[4] if len(sys.argv) > 4 else None  # Second path (If have)

            if backup_type == '-backup_file':
                loading_effect(f"Backing up {path1}")
                backup_file(path1)
            elif backup_type == '-backup_restore_file':
                if not path1 or not path2:
                    print("Error: Both backup file path and restore location are required.")
                else:
                    loading_effect(f"Restoring {path1} to {path2}")
                    restore_backup(path1, path2)

            elif backup_type == '-backup_dir':
                loading_effect(f"Backing up {path1}")
                backup_directory(path1)
            elif backup_type == '-backup_restore_dir':
                loading_effect(f"Restoring {path1}")
                restore_directory(path1)

            elif backup_type == '-backup_file_timestamp':
                loading_effect(f"Backing up {path1} with timestamp")
                backup_file_with_timestamp(path1)

            elif backup_type == '-backup_multiple_files':
                loading_effect(f"Backing up multiple files: {path1} and {path2}")
                backup_multiple_files(path1, path2)

            elif backup_type == '-backup_multiple_directory':
                loading_effect(f"Restoring multiple files: {path1} and {path2}")
                backup_multiple_files(path1, path2)

            elif backup_type == '-clean_old_backups':
                loading_effect(f"Cleanup old backups older than 30 days...")
                clean_old_backups(days=30)

            else:
                print("Error: Invalid backup type. Use 'backup_file', 'backup_dir', 'backup_file_timestamp', 'backup_multiple_files', 'backup_multiple_directory', or 'clean_old_backups'.", file=sys.stderr)

        else:
            print(f"\033[91m[!] Unknown or incomplete command:\033[0m {' '.join(sys.argv[1:])}")
            print("Run with \033[93m--help\033[0m to see available modules.\n")
    else:
        print("\033[90mTip:\033[0m Use --help for more commands")