import os
import subprocess
import sys
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config.CONFIG import SETTINGS, FEATURE
from src.config.NNX_COMMAND import NOONX_COMMANDS, INTERNAL_COMMANDS
from src.utils.getError import *
from src.workload.nnx_private import run_private_shell

if getattr(sys, 'frozen', False):
    app_path = sys._MEIPASS
    noonx_candidate = os.path.join(app_path, "noonx.py")
    if not os.path.exists(noonx_candidate):
        app_path = os.path.abspath(os.path.dirname(__file__))
else:
    app_path = os.path.abspath(os.path.dirname(__file__))

noonx_path = os.path.join(app_path, "noonx.py")

def process_command(cmd: str):
    if not cmd:
        return

    if cmd.lower() in ["exit", "quit"]:
        sys.exit(0)

    if cmd.lower() == "private":
        if SETTINGS.get("NNX_SHELL"):
            run_private_shell()
        else:
            handle_error(ErrorContent.WHEN_RUNNING_ERROR, "The NO_ONX Shell have been disabled. Set 'NNX_Shell' to 'True' in the configuration.\n", to_stderr=True)
        return

    cmd_args = cmd.strip().split()
    base_cmd = cmd.split()[0]
    args = cmd[len(base_cmd):].strip()

    if base_cmd in INTERNAL_COMMANDS:
        if base_cmd in ["clear", "ls"]:
            subprocess.run(INTERNAL_COMMANDS[base_cmd], shell=True)
        elif FEATURE["ENABLE_INTERNAL_COMMANDS"]:
            subprocess.run(INTERNAL_COMMANDS[base_cmd], shell=True)
        else:
            print("\033[91m[•] INTERNAL_COMMANDS not supported anymore, use 'nnx' instead.\033[0m\n")
        return

    if base_cmd in NOONX_COMMANDS or any(arg in NOONX_COMMANDS for arg in cmd_args):
        try:
            import noonx
            sys.argv = ["noonx.py"] + cmd_args
            result = noonx.main()
            if result:
                print(result)
        except Exception as e:
                print(f"\033[91m[!]\033[0m {e}")
                traceback.print_exc()
        return

    handle_error(ErrorContent.UNSUPPORTEDCOMMAND_ERROR, {cmd}, ErrorReason.UNSUPPORTED_COMMAND, to_stderr=True)

def no_onx_shell():
    print(f"NNX Shell v{SETTINGS.get('NNX_VERSION', 'unknown')}")
    print("Type 'exit' or 'quit' to quit.\n")
    while True:
        try:
            cmd = input("NNX > ").strip()
            process_command(cmd)
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"\033[91m[!]\033[0m {e}")
            traceback.print_exc()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd_line = ' '.join(sys.argv[1:])
        process_command(cmd_line)
    elif SETTINGS.get("NNX_SHELL", True):
        no_onx_shell()
    else:
        handle_error(ErrorContent.WHEN_RUNNING_ERROR, "The NO_ONX Shell have been disabled. To use it, set 'NNX_Shell' to 'True' in the configuration.\n", to_stderr=True)