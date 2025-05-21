# Import libraries
import os
import socket

# For Shell prompt
username = os.getenv('USER') or os.getenv('USERNAME') # Get Username
hostname = socket.gethostname() # Get Host name

# === FEATURE TOGGLE (Modular options) ===
FEATURE = {
    # ENABLE
    "ENABLE_EXPERIMENTAL_COMMANDS": False, # Set to True to enable experimental commands
    "ENABLE_DIRECT_RUN": False, # Set to True to run the script directly
    "DISABLE_AUTO_UPDATE": False, # Set to True to disable auto update
    "ENABLE_INTERNAL_COMMANDS": False, # Set to True to enable internal commands
    "ENABLE_NNX_COMMANDS": True, # Set to False to disable NNX commands
    "TEST": False,

    # "ENABLE_FORCE_RUN": False, # Set to True to force run the script, not available yet

    # DISABLE
    "HIDDEN_BANNER": False, # Set to True to hide the banner
    "DISABLE_LOADING": False,
}


# DO NOT CHANGE THESE CONFIGURATION UNLESS YOU KNOW WHAT YOU ARE DOING

# === Settings === (Do not change even if you know what you are doing)
from typing import Dict, Any

SETTINGS: Dict[str, Any] = {
    "NNX_VERSION": "v0.3.1 Beta", # NNX version
    "NNX_SHELL": True, # NNX Shell, not recommended to diasble this, but you can if you want to.
}

def get_prompt():
    return f"┌──({username}㉿{hostname})-(NO_ONX {SETTINGS["NNX_VERSION"]})\n└─$ "

# === NNX COMMANDS ===
INTERNAL_COMMANDS = {
    # Only basic command is useable
    "clear": "cls" if os.name == "nt" else "clear", # Clear
    "ls": "dir" if os.name == "nt" else "ls", # ls

}

# NOONX command
NOONX_COMMANDS = [
    "--help", "-h", "--system_info", "-si", "--version", "-v", # main options
    "--readfile", "--file_info", "--file_hash", "--dir_info", "--file_list", "--symlink_info", "--extended_info", "--scan_dir", "--check_permission", "--hidden_file_info", # File_info options
    "--modify_file_permission", "--modify_file_content", "--modify_file_name", "--modify_file_metadata", "--modify_file_line", "--modify_file_symlink", "--modify_directory", "--modify_directory_permissions", "--modify_file_owner", # Modification options
    "--detective", # Monitoring System
    
    # Other option
    "--compare --mode",
    "--backup",

    # Plugin
    "--plugins", "--plugin", "list_plugins"
]