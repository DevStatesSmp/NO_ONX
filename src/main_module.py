# THIS IS MODULE, DO NOT RUN THIS FILE DIRECTLY

import sys

# Import source
## Utils
from .utils.help_module import *
from .utils.system_info_module import get_system_info, get_gpu_info
from .utils.banner_module import banner, version
from .utils.loading_effect import loading_effect
from .utils.config import FEATURE
from .utils.getError import *
# Workload
from .workload.compare_module import deep_compare_dirs, simple_compare_dirs
from .workload.modification_module import mod
from .workload import file_scan_module
from .workload.file_info_module import info, check_permission, hidden_file_info, file_list
from .workload.backup_module import *
from .workload.readfile_module import read_binary_file, read_text_file, validate_file_path
from .workload.detective_module import watch_detective, activity_detective, monitor_user_activity, network_detective, system_health, process_detective, process_watcher


# ==== Main ====
def main():
    # Plugin management
    from .plugins.init import load_plugins, get_plugin, list_plugins, ask_use_plugin
    load_plugins()


    # Sys args
    if len(sys.argv) >= 2:
        arg = sys.argv[1]

        # Plugins
        if arg == "--plugins" :
            print("[PLUGINS] Available Plugins:")
            for p in list_plugins():
                print(f" - {p}")
            return

        if arg == "--plugin":
            if len(sys.argv) < 3:
                print("Please specify plugin name")
                return
            plugin_name = sys.argv[2]
            plugin_args = sys.argv[3:]
            plugin = get_plugin(plugin_name)
            if not plugin:
                print(f"[!] Plugin '{plugin_name}' not found")
                return
            if hasattr(plugin, 'execute'):
                if ask_use_plugin(plugin_name):
                    plugin.execute(plugin_args)
                else:
                    return
            else:
                handle_error("Error when loading plugins", {plugin_name}, "Has no execute() function.")
            return

        if arg == '--list_plugins':
            plugins = list_plugins()
            print("[PLUGINS] Available Plugins:")
            for p in plugins:
                print(f" - {p}")
            return


        # Run NO_ONX Shell
        if arg in ('--shell', '-s'):
            loading_effect("preparing NO_ONX Shell...")
            from .noonx_shell import no_onx_shell
            no_onx_shell()
            return

        # Main argument for noonx.py
        if arg in ('--help', '-h'):
            if len(sys.argv) > 2:
                sub_arg = sys.argv[2]
                if sub_arg == 'compare':
                    help_compare()
                elif sub_arg == 'backup':
                    help_backup()
                elif sub_arg == 'monitoring':
                    help_monitoring()
                elif sub_arg == 'modify':
                    help_modify()
                elif sub_arg == 'fileinfo':
                    help_fileinfo()
                else:
                    loading_effect("Loading help...")
                    help()
            else:
                loading_effect("Loading help...")
                help()

        elif arg in ('--system_info', '-si'):
            loading_effect("Fetching system info")
            get_system_info()

        elif arg in ('--version', '-v'):
            if not FEATURE.get("HIDDEN_BANNER", False):
                banner()
            version()

        ## Class info
        elif arg == '--file_info' and len(sys.argv) >= 3:
            info.file_info(sys.argv[2])

        elif arg == '--file_hash' and len(sys.argv) >= 3:
            path = sys.argv[2]
            algo = sys.argv[3] if len(sys.argv) >= 4 else "sha256"
            loading_effect(f"Generating hash for {path} using {algo.upper()}")
            info.file_hash(path, algo)

        elif arg == '--dir_info' and len(sys.argv) >= 3:
            loading_effect(f"Loading directory info for {sys.argv[2]}")
            info.dir_info(sys.argv[2])

        elif arg == '--symlink_info' and len(sys.argv) >= 3:
            loading_effect(f"Loading symlink info for {sys.argv[2]}")
            info.symlink_info(sys.argv[2])

        elif arg == '--extended_info' and len(sys.argv) >= 3:
            loading_effect(f"Loading extended info for {sys.argv[2]}")
            info.extended_info(sys.argv[2])

        ## class check_permission
        elif arg == '--check_permission' and len(sys.argv) >= 3:
            path = sys.argv[2]
            loading_effect(f"Checking permissions for {path}")
            check_permission.analyze(path)
        
        ## Class hidden_file_info
        elif arg == '--hidden_file_info' and len(sys.argv) >= 3:
            path = sys.argv[2]
            loading_effect(f"Scanning hidden files in {path}")
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
                handle_error(ErrorContent.MISSING_TYPE_COMMAND, {file_type}, ErrorReason.INVALID_TYPE), print("Use 'text' or 'binary'")
                return


        # Modification
        elif arg == '--modify_file_permission' and len(sys.argv) >= 4:
            path = sys.argv[2]
            permission = sys.argv[3]
            loading_effect(f"Modifying file permissions for {path}")
            mod.modify.modify_file_permission(path, permission)

        elif arg == '--modify_file_content' and len(sys.argv) >= 5:
            path = sys.argv[2]
            operation = sys.argv[3]
            if operation == 'replace' or operation == 'delete':
                target_text = sys.argv[4]
                text = sys.argv[5] if operation == 'replace' and len(sys.argv) >= 6 else None
                loading_effect(f"Modifying content in file {path}")
                mod.modify.modify_file_content(path, operation, text, target_text)
            elif operation == 'append':
                text = sys.argv[4]
                loading_effect(f"Appending text to file {path}")
                mod.modify.modify_file_content(path, operation, text)

        elif arg == '--modify_file_name' and len(sys.argv) >= 4:
            old_name = sys.argv[2]
            new_name = sys.argv[3]
            mod.modify.modify_file_name(old_name, new_name)

        elif arg == '--modify_file_metadata' and len(sys.argv) >= 5:
            path = sys.argv[2]
            metadata_type = sys.argv[3]
            value = float(sys.argv[4])
            loading_effect(f"Modifying file metadata for {path}")
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
            loading_effect(f"Modifying directory {path}")
            mod.modify.modify_directory(path, operation, new_path)

        elif arg == '--modify_directory_permissions' and len(sys.argv) >= 4:
            path = sys.argv[2]
            permission = sys.argv[3]
            loading_effect(f"Modifying directory permissions for {path}")
            mod.modify.modify_directory_permissions(path, permission)

        elif arg == '--modify_file_owner' and len(sys.argv) >= 4:
            path = sys.argv[2]
            new_owner = int(sys.argv[3])
            loading_effect(f"Modifying file owner for {path}")
            mod.modify.modify_file_owner(path, new_owner)

        # File Scan
        elif arg in ('--scan_dir') and len(sys.argv) >= 3:
            path = sys.argv[2]
            algo = sys.argv[3] if len(sys.argv) >= 4 else "sha256"
            loading_effect(f"Scanning directory ({path}) using {algo.upper()}")
            file_scan_module.reset_results()
            file_scan_module.scan_directory(path, algo)
            file_scan_module.print_results()

        # Compare
        elif len(sys.argv) >= 5 and sys.argv[1] == '--compare' and sys.argv[2] == '--mode':
            compare_type = sys.argv[3]
            path1 = sys.argv[4]
            path2 = sys.argv[5]
    
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
                handle_error(ErrorContent.MISSING_TYPE_COMMAND, {compare_type}, ErrorReason.INVALID_TYPE), print("Use 'deep' or 'simple'.")
                return

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
                    print("\033[91m[!]\033[0m Both backup file path and restore location are required.")
                    return
                else:
                    loading_effect(f"Restoring {path1} to {path2}")
                    restore_backup(path1, path2)

            elif backup_type == '-backup_dir':
                loading_effect(f"Backing up {path1}")
                backup_directory(path1)
            elif backup_type == '-backup_restore_dir':
                loading_effect(f"Restoring {path1} to {path2}")
                restore_directory(path1, path2)

            elif backup_type == '-backup_file_timestamp':
                loading_effect(f"Backing up {path1} with timestamp")
                backup_file_with_timestamp(path1)

            elif backup_type == '-backup_multiple_files':
                loading_effect(f"Backing up multiple files: {path1} and {path2}")
                backup_multiple_files([path1, path2])

            elif backup_type == '-backup_multiple_directory':
                loading_effect(f"Restoring multiple files: {path1} and {path2}")
                backup_multiple_files(path1, path2)

            elif backup_type == '-clean_old_backups':
                loading_effect(f"Cleanup old backups older than 30 days...")
                clean_old_backups(days=30)

            else:
                handle_error(ErrorContent.MISSING_TYPE_COMMAND, {backup_type}, ErrorReason.INVALID_TYPE), print("\nUse 'backup_file', 'backup_dir', 'backup_file_timestamp', 'backup_multiple_files', 'backup_multiple_directory', or 'clean_old_backups'.")
                return
            
        elif arg == '--file_list' and len(sys.argv) >= 3:
            path = sys.argv[2]
            loading_effect(f"Loading file list for {path}")
            file_list_data = file_list.get_path(path)

            if file_list_data:
                file_list.display_file_structure(path)
            else:
                print(f"\033[91m[!]\033[0m No files found or error occurred in: {path}")
                return

        # Monitoring Security
        elif len(sys.argv) >= 2 and sys.argv[1] == '--detective':

            if len(sys.argv) < 4:
                handle_error(ErrorContent.MISSING_ARGUMENTS_ERROR, ErrorReason.MISSING_ARGUMENTS), print("\nUsage: --detective --type [watcher|activity|security|network|sys_health]", file=sys.stderr)
                return 
            if len(sys.argv) < 4 or sys.argv[2] != '--type':
                handle_error(ErrorContent.MISSING_TYPE_COMMAND, {detective_type}, ErrorReason.INVALID_TYPE), print("\nUse 'watcher', 'activity', 'security', 'network', or 'sys_health'.", file=sys.stderr)
                return
            else:
                detective_type = sys.argv[3]
    
            if detective_type == 'watcher':
                if len(sys.argv) >= 5:
                    path = sys.argv[4]
                    watch_detective(path)
                else:
                    handle_error(ErrorContent.MISSING_ARGUMENTS_ERROR, {"path": None}, ErrorReason.MISSING_PATH)
                    return
        
            elif detective_type == 'activity':
                activity_detective()

            elif detective_type == "security":
                monitor_user_activity()

            elif detective_type == "network":
                network_detective()

            elif detective_type in ["sys_health", "system_health"]:
                system_health()

            elif detective_type == "process":
                process_detective()

            elif detective_type == "process_watcher":
                process_watcher()
            else:
                handle_error(ErrorContent.MISSING_TYPE_COMMAND, {detective_type}, ErrorReason.MISSING_TYPE), print("Use 'watcher', 'activity', 'security', 'network', or 'sys_health'.")
        
        # Added you custom command here
        # Ex: elif len(sys.argv) >= 2 and sys.argv[1] == '--example':
        
        else:
            handle_error(ErrorContent.UNSUPPORTEDCOMMAND_ERROR, sys.argv[1] if len(sys.argv) > 1 else None, ErrorReason.UNSUPPORTED_COMMAND)
            print("Run with \033[93mnnx --help\033[0m to see available modules.\n")