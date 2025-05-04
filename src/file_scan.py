import os
import sys
import hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from src.utils.config import ENABLE_DIRECT_RUN

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
        print(f"Error: Cannot open file {path}: {e}")
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
                print(f"❌ WARNING: {path} contains malware (hash matched)")
        else:
            with safe_lock:
                safe_files.append(str(path))
                print(f"✅ Safe: {path}")

    elif path.is_dir():
        for child in path.iterdir():
            scan_file(child, hash_type)
    else:
        print(f"Invalid path: {path}")

def scan_directory(root_path: str, hash_type="sha256"):
    path = Path(root_path)
    if not path.exists():
        print("Path does not exist.")
        return

    tasks = []
    with ThreadPoolExecutor() as executor:
        for entry in path.iterdir():
            tasks.append(executor.submit(scan_file, entry, hash_type))

        for task in as_completed(tasks):
            pass  # Wait for all tasks

def reset_results():
    with safe_lock, infected_lock:
        safe_files.clear()
        infected_files.clear()

def print_results():
    print("\n--- Scan Results ---")

    print("\n❌ Infected files:")
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

if __name__ == "__main__" and ENABLE_DIRECT_RUN:
    main()
else:
    if __name__ == "__main__":
        print("[ERROR] This script cannot be run directly. Use NO_ONX.exe instead.")
