import os

# === NNX COMMANDS ===
INTERNAL_COMMANDS = {
    # Only basic command is useable
    "clear": "cls" if os.name == "nt" else "clear", # Clear
    "ls": "dir" if os.name == "nt" else "ls", # ls

}

# NOONX command
NOONX_COMMANDS = [
    "--help", "-h", "--system_info", "-si", "--version", "-v", "--clear_cache", "-cc", "config", # main options
    "--readfile", "--file_info", "--file_hash", "--dir_info", "--file_list", "--symlink_info", "--extended_info", "--scan_dir", "--check_permission", "--hidden_file_info", # File_info options
    "--modify_file_permission", "--modify_file_content", "--modify_file_name", "--modify_file_metadata", "--modify_file_line", "--modify_file_symlink", "--modify_directory", "--modify_directory_permissions", "--modify_file_owner", # Modification options
    "--detective", # Monitoring System
    
    # Other option
    "--compare --mode",
    "--backup",

    # Plugin
    "--plugin", "-p"
]

ALLOWED_PRIVATE_NOONX_COMMANDS = {
    "--help", "-h", "--system_info", "-si", "--version", "-v",  "--clear_cache", "-cc", "config", # Main options
    "--sandbox" # Sandbox options
}

# This for suggestion "Do you mean...?" when typing an approximate command name
SUPPORTED_COMMANDS = {
    "--help", "-h", "--system_info", "-si", "--version", "-v", "--clear_cache", "-cc", "config", # main options
    "--readfile", "--file_info", "--file_hash", "--dir_info", "--file_list", "--symlink_info", "--extended_info", "--scan_dir", "--check_permission", "--hidden_file_info", # File_info options
    "--modify_file_permission", "--modify_file_content", "--modify_file_name", "--modify_file_metadata", "--modify_file_line", "--modify_file_symlink", "--modify_directory", "--modify_directory_permissions", "--modify_file_owner", # Modification options
    "--detective", # Monitoring System
    
    # Other option
    "--compare --mode",
    "--backup", "--sandbox",

    # Plugin
    "--plugin", "-p", "plugin_list", "-list", "--plugin_uninstall", "-uninstall"    
}