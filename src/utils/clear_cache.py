import os
import shutil
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'config')))

from src.config.PATH import BASE_DIR, CACHE_DIRS, CACHE_EXTS
from src.utils.getError import handle_error, ErrorContent, ErrorReason
from src.utils.loading_effect import loading_effect
from src.utils.clear_line import clear_line

def find_project_root(start_path):
    current = os.path.abspath(start_path)
    while current != os.path.dirname(current):
        entries = os.listdir(current)
        if 'src' in entries and ('nnx.exe' in entries or 'nnx-terminal.exe' in entries):
            return current
        current = os.path.dirname(current)
    return None

def find_python_caches(root_dir='.'):
    targets = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for dirname in dirnames:
            if dirname in CACHE_DIRS:
                targets.append(os.path.join(dirpath, dirname))
        for filename in filenames:
            if any(filename.endswith(ext) for ext in CACHE_EXTS):
                targets.append(os.path.join(dirpath, filename))
    return targets

def prompt_delete(targets):
    print("\nThe following cache files/folders were found:")
    for path in targets:
        print(f" - {path}")

    choice = input("\nDo you want to delete ALL of them? (y/n): ").strip().lower()
    if choice == 'y':
        for path in targets:
            try:
                if not os.path.exists(path):
                    # print(f"→ Skipped (not found): {path}")
                    continue

                if os.path.isdir(path):
                    shutil.rmtree(path)
                    print(f"→ Deleted directory: {path}")
                else:
                    os.remove(path)
                    print(f"→ Deleted file: {path}")
            except Exception as e:
                handle_error(ErrorContent.WHEN_RUNNING_ERROR, f'{path}: {e}', ErrorReason.UNKNOWN_ERROR)
    else:
        handle_error("Deletion canceled by user.")


def clear_cache():
    loading_effect(f"Finding Python cache in {BASE_DIR}", duration=1)
    clear_line()
    cache_targets = find_python_caches(BASE_DIR)
    if not cache_targets:
        print("\nNo Python cache found.")
    else:
        print(f"Found {len(cache_targets)} targets to check.")
        prompt_delete(cache_targets)
