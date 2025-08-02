import json
import os
import sys
from src.config.PATH import settings_path, feature_path

SETTINGS = {}
FEATURE = {}


def load_settings():
    global SETTINGS
    # settings_path = os.path.join(os.path.dirname(__file__), 'SETTING.json')
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            SETTINGS = json.load(f)
    except Exception as e:
        print(f"[DEBUG] Failed to read {settings_path}: {e}")
        from src.utils.getError import handle_error, ErrorContent, ErrorReason
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, ErrorReason.CANNOT_READ_FILE, "Failed to read SETTING.json", to_stderr=True)
        return {}

def load_feature():
    global FEATURE
    # feature_path = os.path.join(os.path.dirname(__file__), 'FEATURE.json')
    try:
        with open(feature_path, 'r', encoding='utf-8') as f:
            FEATURE = json.load(f)
    except Exception as e:
        print(f"[DEBUG] Failed to read {feature_path}: {e}")
        from src.utils.getError import handle_error, ErrorContent, ErrorReason
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, ErrorReason.CANNOT_READ_FILE, "Failed to read FEATURE.json", to_stderr=True)
        return {}

load_settings()
load_feature()
