# THIS IS MODULE, DO NOT RUN THIS FILE DIRECTLY

import os
import sys
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.getError import *

# Known malware hashes
KNOWN_MALWARE_HASHES = {
    "d41d8cd98f00b204e9800998ecf8427e",  # Empty file
    "e99a18c428cb38d5f260853678922e03"   # "abc123" (MD5)
}

safe_files = []
infected_files = []
safe_lock = threading.Lock()
infected_lock = threading.Lock()

def get_file_hash(path: str, hash_type="sha256") -> str:
    BUF_SIZE = 8192
    hash_func = hashlib.sha256() if hash_type == "sha256" else hashlib.md5()

    try:
        with open(path, 'rb') as f:
            while chunk := f.read(BUF_SIZE):
                hash_func.update(chunk)
    except Exception as e:
        handle_error(
            error_type=ErrorContent.SCANNING_ERROR,
            details={"file_path": path, "exception": str(e)},
            reason=ErrorReason.FILE_NOT_FOUND
        )
        return ""

    return hash_func.hexdigest()

def scan_file(path: Path, hash_type="sha256"):
    if path.is_file():
        file_hash = get_file_hash(str(path), hash_type)
        if not file_hash:
            return

        if file_hash in KNOWN_MALWARE_HASHES:
            with infected_lock:
                infected_files.append(str(path))
                handle_error("WARNING", {path}, "contains malware (hash matched)")
        else:
            with safe_lock:
                safe_files.append(str(path))
                print(f"✅ Safe: {path}")

    elif path.is_dir():
        for child in path.iterdir():
            scan_file(child, hash_type)
    else:
        handle_error(ErrorContent.SCANNING_ERROR, {path}, ErrorReason.MISSING_PATH)

def scan_directory(root_path: str, hash_type="sha256"):
    path = Path(root_path)
    if not path.exists():
        handle_error(ErrorContent.READFILE_ERROR, {path}, ErrorReason.MISSING_FILE)
        return

    tasks = []
    with ThreadPoolExecutor() as executor:
        for entry in path.iterdir():
            tasks.append(executor.submit(scan_file, entry, hash_type))

        for task in as_completed(tasks):
            pass 

def reset_results():
    with safe_lock, infected_lock:
        safe_files.clear()
        infected_files.clear()

def print_results():
    print("\n--- Scan Results ---")

    print("\n\033[91m[!]\033[0m Infected files:")
    if not infected_files:
        print("  -> No malware found.")
    else:
        for f in infected_files:
            print(f"  -> {f}")

    print("\n✅ Safe files:")
    if not safe_files:
        print("  -> No safe files found.")
    else:
        for f in safe_files:
            print(f"  -> {f}")

    print("\n--- Scan complete ---")

def main():
    if len(sys.argv) >= 2:
        directory_to_scan = sys.argv[1]
    else:
        directory_to_scan = input("Enter directory to scan: ").strip()

    hash_type = sys.argv[2] if len(sys.argv) >= 3 else "sha256"

    print("\n--- Starting scan ---\n")
    reset_results()
    scan_directory(directory_to_scan, hash_type)
    print_results()