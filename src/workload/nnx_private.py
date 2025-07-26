import subprocess
import sys
import traceback
import os
import shutil
import tempfile
import shlex

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.config.NNX_PROMPT import get_prompt_private
from src.config.NNX_COMMAND import ALLOWED_PRIVATE_NOONX_COMMANDS, INTERNAL_COMMANDS
from src.utils.getError import *

def run_private_shell():
    print("Entering private shell sandbox.")
    print("Type 'exit' or 'quit' to quit private shell.\n")

    sandbox_dir = tempfile.mkdtemp(prefix="nnx_private_")
    os.chdir(sandbox_dir)

    try:
        while True:
            try:
                cmd = input(get_prompt_private()).strip()
                if not cmd:
                    continue

                if cmd.lower() in ["exit", "quit"]:
                    print("Exiting private shell.\n")
                    break

                tokens = shlex.split(cmd)
                base_cmd = tokens[0]

                if base_cmd in INTERNAL_COMMANDS:
                    if base_cmd == "clear":
                        os.system('cls' if os.name == 'nt' else 'clear')
                    elif base_cmd == "ls":
                        for item in os.listdir():
                            print(item)
                    else:
                        print(f"\033[91m[•] INTERNAL command '{base_cmd}' is not allowed in private shell.\033[0m\n")
                    continue

                elif base_cmd == "nnx":
                    if len(tokens) > 1:
                        arg_str = ' '.join(tokens[1:])
                        if any(arg in arg_str for arg in ALLOWED_PRIVATE_NOONX_COMMANDS):
                            try:
                                import noonx
                                sys.argv = ["noonx.py"] + tokens[1:]
                                result = noonx.main()
                                if result:
                                    print(result)
                            except Exception as e:
                                print(f"\033[91m[!]\033[0m Error while running nnx: {e}")
                                traceback.print_exc()
                                continue
                        else:
                            handle_error(ErrorContent.UNSUPPORTEDCOMMAND_ERROR, {cmd},
                                         "This nnx command is not allowed in private shell.", to_stderr=True)
                    else:
                        handle_error(ErrorContent.MISSING_ARGUMENTS_ERROR, {cmd},
                                     "Missing arguments for nnx command.", to_stderr=True)
                else:
                    handle_error(ErrorContent.UNSUPPORTEDCOMMAND_ERROR, {cmd},
                                 "This command is not allowed in private shell.", to_stderr=True)

            except KeyboardInterrupt:
                print("\n(Use 'exit' to quit private shell.)")
            except Exception as e:
                print(f"\033[91m[!]\033[0m Unexpected error: {e}")
                traceback.print_exc()

    finally:
        try:
            shutil.rmtree(sandbox_dir, ignore_errors=True)
            print("Sandbox environment cleaned up.")
        except Exception as cleanup_err:
            print(f"\033[91m[!]\033[0m Failed to clean sandbox: {cleanup_err}")
