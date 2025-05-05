import os

# === FEATURE TOGGLE (Modular options) ===
FEATURE = {
    # ENABLE
    "ENABLE_EXPERIMENTAL_COMMANDS": False, # Set to True to enable experimental commands
    "ENABLE_DIRECT_RUN": False, # Set to True to run the script directly
    "DISABLE_AUTO_UPDATE": False, # Set to True to disable auto update
    "ENABLE_INTERNAL_COMMANDS": False, # Set to True to enable internal commands
    "ENABLE_NNX_COMMANDS": True, # Set to False to disable NNX commands

    # "ENABLE_FORCE_RUN": False, # Set to True to force run the script, not available yet

    # DISABLE
    "HIDDEN_BANNER": False, # Set to True to hide the banner
}


# DO NOT CHANGE THESE CONFIGURATION UNLESS YOU KNOW WHAT YOU ARE DOING

# === Settings === (Do not change even if you know what you are doing)
SETTINGS = {
    "NNX_VERSION": "v0.2.9 Beta", # NNX version
    "NNX_SHELL": True, # NNX Shell, not recommended to diasble this, but you can if you want to.
}

# === NNX COMMANDS ===
INTERNAL_COMMANDS = {
    # The internal commands are not supported anymore, use 'nnx' instead. (Only clear is supported)
    "compare": "python src/compare.py",
    "info": "python src/file_info.py",
    "readfile": "python src/readfile.py",
    "file_scan": "python src/file_scan.py",

    # Only clear is useable
    "clear": "cls" if os.name == "nt" else "clear"
}

# NOONX command
NOONX_COMMANDS = [
    "--help", "-h", "--system_info", "-si", "--version", "-v", # main options
    "--readfile", "--file_info", "--file_hash", "--dir_info", "--file_list", "--symlink_info", "--extended_info", "--scan_dir", "--check_permission", "--hidden_file_info", # File_info options
    "--modify_file_permission", "--modify_file_content", "--modify_file_name", "--modify_file_metadata", "--modify_file_line", "--modify_file_symlink", "--modify_directory", "--modify_directory_permissions", "--modify_file_owner", # Modification options

    # Other option
    "--compare --mode",
    "--backup"
]