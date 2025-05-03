import os
import subprocess
import sys
import socket

# Get user name
username = os.getenv('USER') or os.getenv('USERNAME')
hostname = socket.gethostname()

if getattr(sys, 'frozen', False):
    app_path = sys._MEIPASS
else:
    app_path = os.path.abspath(".")

noonx_path = os.path.join(app_path, "noonx.py")

INTERNAL_COMMANDS = {
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
    "--modify_file_owner"
]


def get_prompt():
    return f"┌──({username}㉿{hostname})-(NO_ONX v0.2.4 Beta)\n└─$ "

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
                final_cmd = INTERNAL_COMMANDS[base_cmd]
                if args:
                    final_cmd += " " + args
                subprocess.run(final_cmd, shell=True)

            elif base_cmd == "nnx":
                cmd_args = cmd.split()
                if len(cmd_args) > 1 and cmd_args[1] in NOONX_COMMANDS:
                    final_cmd = f"python noonx.py {' '.join(cmd_args[1:])}"
                    subprocess.run(final_cmd, shell=True)
                else:
                    print(f"[ERROR] Unsupported nnx command: {cmd}, use 'nnx --help' for more information.")

            else:
                subprocess.run(cmd, shell=True)

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == '__main__':
    no_onx_shell()