import os
import sys
import json

from src.utils.getError import handle_error, ErrorContent, ErrorReason
from src.config.PATH import feature_path, settings_path

IMMUTABLE_SETTINGS = ['NNX_VERSION', 'NNX_RELEASE_VER']

def toggle_value(file_path: str, key: str, state: str, immutable_keys=None):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        if key not in config:
            handle_error(ErrorContent.INVALID_INPUT, f"'{key}' not found in {os.path.basename(file_path)}", ErrorReason.UNKNOWN_COMMAND)
            return

        if immutable_keys and key in immutable_keys:
            handle_error(ErrorContent.INVALID_INPUT, f"'{key}' is immutable and cannot be modified.", ErrorReason.PERMISSION_DENIED)
            return

        if state.lower() == 'true':
            config[key] = True
        elif state.lower() == 'false':
            config[key] = False
        else:
            handle_error(ErrorContent.INVALID_INPUT, "Value must be 'true' or 'false'", ErrorReason.UNKNOWN_COMMAND)
            return

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        print(f"[INFO] '{key}' has been set to {state.lower()} in {os.path.basename(file_path)}.\n")

    except Exception as e:
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, str(e), ErrorReason.UNKNOWN_ERROR)

def CONFIG_TOGGLE():
    args = sys.argv

    if len(args) != 4:
        print("Usage: nnx --config <FEATURE_NAME> true/false")
        return

    _, _, name, value = args

    try:
        with open(feature_path, 'r', encoding='utf-8') as f:
            feature_config = json.load(f)
    except Exception:
        feature_config = {}

    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings_config = json.load(f)
    except Exception:
        settings_config = {}

    if name in feature_config:
        toggle_value(feature_path, name, value)
    elif name in settings_config:
        toggle_value(settings_path, name, value, IMMUTABLE_SETTINGS)
    else:
        handle_error(ErrorContent.INVALID_INPUT, f"'{name}' not found in any config file", ErrorReason.UNKNOWN_COMMAND)
