import os
import subprocess
import sys
import socket
import traceback
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils.config import INTERNAL_COMMANDS, NOONX_COMMANDS, FEATURE, SETTINGS, get_prompt

if getattr(sys, 'frozen', False):
    app_path = sys._MEIPASS
    noonx_candidate = os.path.join(app_path, "noonx.py")
    if not os.path.exists(noonx_candidate):
        app_path = os.path.abspath(os.path.dirname(__file__))
else:
    app_path = os.path.abspath(os.path.dirname(__file__))

noonx_path = os.path.join(app_path, "noonx.py")

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
                if base_cmd == "clear" or base_cmd == "ls" or base_cmd == "cd":
                    subprocess.run(INTERNAL_COMMANDS[base_cmd], shell=True)

                elif FEATURE["ENABLE_INTERNAL_COMMANDS"]:
                    subprocess.run(INTERNAL_COMMANDS[base_cmd], shell=True)
                else:
                    print("\033[91m[•]\033[0m INTERNAL_COMMANDS not supported anymore, use 'nnx' instead.\n")
                continue

            elif base_cmd == "nnx":
                cmd_args = cmd.split()
                if len(cmd_args) > 1:
                    arg_str = ' '.join(cmd_args[1:])
                    if any(cmd_arg in arg_str for cmd_arg in NOONX_COMMANDS):
                        try:
                            import noonx  # Import module noonx
                            # Gọi hàm từ noonx thay vì chạy file trực tiếp
                            sys.argv = ["noonx.py"] + arg_str.split()
                            result = noonx.main()
                            if result:
                                print(result)
                        except Exception as e:
                            print(f"\033[91m[!]\033[0m {e}")
                            traceback.print_exc()
                    else:
                        print(f"\033[91m[!]\033[0m Unsupported nnx command: {cmd}, use 'nnx --help' for more information.\n")
                else:
                    print("\033[91m[!]\033[0m Missing arguments for 'nnx'. Use 'nnx --help' for guidance.\n")

            else:
                print(f"\033[91m[!]\033[0m Unsupported nnx command: {cmd}, use 'nnx --help' for more information.\n")

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except Exception as e:
            print(f"\033[91m[!]\033[0m {e}")
            traceback.print_exc()

if __name__ == '__main__' and SETTINGS["NNX_SHELL"]:
    no_onx_shell()

else:
    if __name__ == '__main__':
        print("\033[91m[!]\033[0m The NO_ONX Shell have been disabled, To use it, set 'NNX_Shell' to 'True' in the configuration.\n", file=sys.stderr)