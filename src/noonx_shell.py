import os
import subprocess
import sys
import socket
from src.utils.config import ENABLE_INTERNAL_COMMANDS

# Get user name
username = os.getenv('USER') or os.getenv('USERNAME')
hostname = socket.gethostname()

if getattr(sys, 'frozen', False):
    app_path = sys._MEIPASS
else:
    app_path = os.path.abspath(".")

noonx_path = os.path.join(app_path, "noonx.py")

INTERNAL_COMMANDS = {
    # The internal commands are not supported anymore, use 'nnx' instead. (Only clear is supported)

    "compare": "python src/compare.py",
    "info": "python src/file_info.py",
    "readfile": "python src/readfile.py",
    "file_scan": "python src/file_scan.py",


    "clear": "cls" if os.name == "nt" else "clear"
}

# NOONX command
NOONX_COMMANDS = [
    "--help", "-h", "--system_info", "-si",
    "--version", "-v","--readfile", "--file_info", "--file_hash", "--dir_info",
    "--symlink_info", "--extended_info", "--scan_dir",
    "--check_permission", "--hidden_file_info", "--compare",
    "--modify_file_permission", "--modify_file_content",
    "--modify_file_name", "--modify_file_metadata",
    "--modify_file_line", "--modify_file_symlink",
    "--modify_directory", "--modify_directory_permissions",
    "--modify_file_owner", "--compare --mode", "--backup"
]


def get_prompt():
    return f"┌──({username}㉿{hostname})-(NO_ONX v0.2.8 Beta)\n└─$ "

def no_onx_shell():
    subprocess.run("python noonx.py", shell=True)
    print("Type 'exit' or 'quit' to quit.\n")

    while True:
        try:
            cmd = input(get_prompt()).strip()

            if not cmd:
                continue

            if cmd.lower() in ["exit", "quit"]:
                break

            base_cmd = cmd.split()[0]
            args = cmd[len(base_cmd):].strip()

            if base_cmd in INTERNAL_COMMANDS:
                if base_cmd == "clear":
                    subprocess.run(INTERNAL_COMMANDS[base_cmd], shell=True)

                elif ENABLE_INTERNAL_COMMANDS:
                    subprocess.run(INTERNAL_COMMANDS[base_cmd], shell=True)
                else:
                    print("[NOTICE] INTERNAL_COMMANDS not supported anymore, use 'nnx' instead.\n")
                continue


            elif base_cmd == "nnx":
                cmd_args = cmd.split()
                if len(cmd_args) > 1 and cmd_args[1] in NOONX_COMMANDS:
                    final_cmd = f"python {noonx_path} {' '.join(cmd_args[1:])}"
                    subprocess.run(final_cmd, shell=True)

                else:
                    print(f"[ERROR] Unsupported nnx command: {cmd}, use 'nnx --help' for more information.")

            else:
                completed = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if completed.returncode != 0 and "' is not recognized as" in completed.stderr:
                    print(f"[ERROR] Unsupported nnx command: {cmd}, use 'nnx --help' for more information.\n")
                else:
                    print(completed.stdout, end="")
                    print(completed.stderr, end="")

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == '__main__':
    no_onx_shell()