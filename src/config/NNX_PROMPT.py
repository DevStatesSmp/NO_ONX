import os
import sys
import socket
import json

# For Shell prompt
username = os.getenv('USER') or os.getenv('USERNAME') # Get Username
hostname = socket.gethostname() # Get Host name
from src.utils.getError import handle_error, ErrorContent, ErrorReason
from src.config.CONFIG import SETTINGS

def get_prompt():
    version = "unknown"
    try:
        settings_path = os.path.join(os.path.dirname(__file__), 'SETTING.json')
        with open(settings_path, 'r') as f:
            settings_json = json.load(f)
            version = settings_json.get("NNX_VERSION", "unknown")
    except Exception:
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, ErrorReason.CANNOT_READ_FILE, "Failed to read SETTING.json", to_stderr=True, exit_code=None)
        pass

    cwd = os.getcwd()
    return f"\033[38;5;93m╭─[\033[38;5;51mNNX \033[38;5;93m:: \033[38;5;198mNO_ONX {version}\033[38;5;93m]──[\033[38;5;51m{SETTINGS["NNX_RELEASE_VER"]}\033[38;5;93m]\n╰─[\033[38;5;87m{username}\033[38;5;93m@\033[38;5;87m{hostname}\033[38;5;93m]⟶ $\033[0m "

def get_prompt_private():
    version = "unknown"
    try:
        settings_path = os.path.join(os.path.dirname(__file__), 'SETTING.json')
        with open(settings_path, 'r') as f:
            settings_json = json.load(f)
            version = settings_json.get("NNX_VERSION", "unknown")
    except Exception:
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, ErrorReason.CANNOT_READ_FILE, "Failed to read SETTING.json", to_stderr=True, exit_code=None)
        pass

    cwd = os.getcwd()
    return f"\033[38;5;46m[PRIVATE]──[\033[38;5;196mNNX \033[38;5;46m:: \033[38;5;196mNO_ONX {version}\033[38;5;46m]──[\033[38;5;51m{SETTINGS["NNX_RELEASE_VER"]}\033[38;5;46m]\n╰─[\033[38;5;87m{username}\033[38;5;46m@\033[38;5;87m{hostname}\033[38;5;46m]⟶ $\033[0m "





