import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.config import FEATURE

# Check error
def validate_file_path(file_path):
    trimmed_path = file_path.strip()

    if not trimmed_path:
        print("Error: The file path is empty.", file=sys.stderr)
        return False

    path_obj = Path(trimmed_path)

    if not path_obj.exists():
        print(f"Error: The file at {trimmed_path} does not exist.", file=sys.stderr)
        return False
    elif not path_obj.is_file():
        print(f"Error: The path at {trimmed_path} is not a valid file.", file=sys.stderr)
        return False

    return True

# Read text file
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            for line_number, line in enumerate(f, start=1):
                print(f"Line {line_number}: {line.rstrip()}")
    except Exception as e:
        print(f"Error: Could not open the file {file_path}\n{e}", file=sys.stderr)

# Read binary file (optional)
def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            content = f.read(16)  # Read first 16 bytes as a sample
            print(f"First 16 bytes of the file {file_path}: {content.hex()}")
    except Exception as e:
        print(f"Error: Could not open the binary file {file_path}\n{e}", file=sys.stderr)

# Main function
def main():
    try:
        file_path = input("Enter file path: ").strip()
    except EOFError:
        print("No input provided.", file=sys.stderr)
        return

    if not validate_file_path(file_path):
        return

    # Determine if it's a binary or text file
    if file_path.lower().endswith(('.txt', '.md', '.log', '.csv')):  # Example of common text file extensions
        read_text_file(file_path)
    else:
        print("The file is treated as binary.")
        read_binary_file(file_path)


if __name__ == "__main__" and FEATURE["ENABLE_DIRECT_RUN"]:
    main()
else:
    if __name__ == "__main__":
        print("[ERROR] This script cannot be run directly. Use NO_ONX.exe instead.")

